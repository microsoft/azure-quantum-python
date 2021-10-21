##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import logging

from typing import List, Union
from azure.quantum.optimization import Term
from azure.quantum.aio.optimization import Problem
from azure.quantum.aio.storage import (
    ContainerClient,
    BlobClient,
    download_blob,
)
from azure.quantum.optimization.streaming_problem import StreamingProblem as SyncStreamingProblem
from azure.quantum.optimization.streaming_problem import JsonStreamingProblemUploader as SyncJsonStreamingProblemUploader
from asyncio import create_task
from queue import Empty

logger = logging.getLogger(__name__)

__all__ = ["StreamingProblem"]


class StreamingProblem(SyncStreamingProblem):
    """Problem to be streamed to the service.

    Streaming problems are uploaded on the fly as terms are added,
    meaning that the whole problem representation is not kept in memory. This
    is very useful when constructing large  problems.

    :param workspace: Workspace to upload problem to
    :type workspace: Workspace
    :param name: Problem name
    :type name: str
    :param terms: Problem terms, depending on solver. Defaults to None
    :type terms: Optional[List[Term]], optional
    :param init_config: Optional configuration details,
     depending on solver. Defaults to None
    :type init_config: Optional[Dict[str,int]], optional
    :param problem_type: Problem type (ProblemType.pubo or
     ProblemType.ising), defaults to ProblemType.ising
    :type problem_type: ProblemType, optional
    """
    async def add_term(self, c: Union[int, float], indices: List[int]):
        """Adds a single term to the `Problem`
        representation and queues it to be uploaded

        :param c: The cost or weight of this term
        :type c: int, float
        :param indices: The variable indices that are in this term
        :type indices: List[int]
        """
        await self.add_terms([Term(indices=indices, c=c)])

    async def _get_upload_coords(self):
        blob_name = self.id
        if self.upload_to_url:
            blob_client = BlobClient.from_blob_url(self.upload_to_url)
            container_client = ContainerClient.from_container_url(
                await self.workspace._get_linked_storage_sas_uri(
                    blob_client.container_name
                )
            )
            blob_name = blob_client.blob_name
        elif not self.workspace.storage:
            # No storage account is passed, use the linked one
            container_uri = await self.workspace._get_linked_storage_sas_uri(self.id)
            container_client = ContainerClient.from_container_url(
                container_uri
            )
        else:
            # Use the specified storage account
            container_client = ContainerClient.from_connection_string(
                self.workspace.storage, self.id
            )

        return {"blob_name": blob_name, "container_client": container_client}

    async def add_terms(self, terms: List[Term]):
        """Adds a list of terms to the `Problem`
         representation and queues them to be uploaded

        :param terms: The list of terms to add to the problem
        """
        if self.uploaded_uri is not None:
            raise Exception("Cannot add terms after problem has been uploaded")

        if terms is not None:
            if self.uploader is None:
                upload_coords = await self._get_upload_coords()
                self.uploader = JsonStreamingProblemUploader(
                    problem=self,
                    container=upload_coords["container_client"],
                    name=upload_coords["blob_name"],
                    compress=self.compress,
                    upload_size_threshold=self.upload_size_threshold,
                    upload_term_threshold=self.upload_terms_threshold,
                )
                uploader_task = create_task(self.uploader.start())

            term_couplings = [len(term.ids) for term in terms]
            max_coupling = max(term_couplings)
            min_coupling = min(term_couplings)
            self.__n_couplers += sum(term_couplings)
            self.stats["num_terms"] += len(terms)
            self.stats["avg_coupling"] = (
                self.__n_couplers / self.stats["num_terms"]
            )
            if self.stats["max_coupling"] < max_coupling:
                self.stats["max_coupling"] = max_coupling
            if self.stats["min_coupling"] > min_coupling:
                self.stats["min_coupling"] = min_coupling
            self.terms_queue.put_nowait(terms)
            await uploader_task

    async def download(self):
        """Downloads the uploaded problem as an instance of `Problem`"""
        if not self.uploaded_uri:
            raise Exception(
                "StreamingProblem may not be downloaded before it is uploaded"
            )

        coords = await self._get_upload_coords()
        blob = coords["container_client"].get_blob_client(coords["blob_name"])
        contents = await download_blob(blob.url)
        return Problem.deserialize(contents, self.name)


class JsonStreamingProblemUploader(SyncJsonStreamingProblemUploader):
    """Helper class for uploading json problem files in chunks.

    :param problem: Back-ref to the problem being uploaded
    :param container: Reference to the container
     client in which to store the problem
    :param name: Name of the problem (added to blob metadata)
    :param compress: Whether the problem should be compressed on the fly
    :param upload_size_threshold: Chunking threshold (in bytes).
     Once the internal buffer reaches this size, the chunk will be uploaded.
    :param upload_term_threshold: Chunking threshold (in terms).
     Once this many terms are ready to be uploaded, the chunk will be uploaded.
    :param blob_properties: Properties to set on the blob.
    """
    async def start(self):
        await self._run_queue()

    async def _run_queue(self):
        continue_processing = True
        terms = []
        while continue_processing:
            try:
                new_terms = await self.problem.terms_queue.get()
                if new_terms is None:
                    continue_processing = False
                else:
                    terms = terms + new_terms
                    if len(terms) < self.__upload_terms_threshold:
                        continue
            except Empty:
                pass
            except Exception as e:
                raise e

            if len(terms) > 0:
                await self._upload_next(terms)
                terms = []

        await self._finish_upload()

    async def _upload_start(self, terms):
        self.started_upload = True
        await self._upload_chunk(
            f'{{"cost_function":{{"version":"{self._get_version()}",'
            + f'"type":"{self._scrub(self.problem.problem_type.name)}",'
            + self._get_initial_config_string()
            + '"terms":['
            + self._get_terms_string(terms)
        )

    async def _upload_next(self, terms):
        if not self.started_upload:
            await self._upload_start(terms)
        else:
            await self._upload_chunk(self._get_terms_string(terms))

    async def _upload_chunk(self, chunk: str, is_final: bool = False):
        compressed = self._maybe_compress_bits(chunk.encode(), is_final)
        if compressed is None:
            return
        if len(compressed) > 0:
            await self.blob.upload_data(compressed)

    async def _finish_upload(self):
        if not self.started_upload:
            await self._upload_start([])

        await self._upload_chunk(f'{"]}}"}', True)
        await self.blob.commit(metadata=self.blob_properties)
