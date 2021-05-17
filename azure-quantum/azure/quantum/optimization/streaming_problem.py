##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import logging
import uuid
import io
import gzip
import json
import threading
import sys

from typing import List, Union, Dict, Optional
from azure.quantum import Workspace
from azure.quantum.optimization import Term, Problem, ProblemType
from azure.quantum.storage import (
    StreamedBlob,
    ContainerClient,
    BlobClient,
    download_blob,
)
from queue import Queue, Empty

logger = logging.getLogger(__name__)

__all__ = ["StreamingProblem"]


class StreamingProblem(object):
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

    def __init__(
        self,
        workspace: Workspace,
        name: str = "Optimization Problem",
        terms: Optional[List[Term]] = None,
        init_config: Optional[Dict[str, int]] = None,
        problem_type: ProblemType = ProblemType.ising,
        metadata: Dict[str, str] = {},
        **kw,
    ):
        super(StreamingProblem, self).__init__(**kw)
        self.name = name
        self.id = str(uuid.uuid1())
        self.workspace = workspace
        self.problem_type = problem_type
        self.init_config = init_config
        self.terms_queue = Queue()
        self.uploaded_uri = None
        self.upload_to_url = None
        self.uploader = None
        self.compress = True
        self.__n_couplers = 0
        self.stats = {
            "type": problem_type.name,
            "max_coupling": 0,
            "avg_coupling": 0,
            "min_coupling": sys.maxsize,
            "num_terms": 0,
        }
        self.upload_size_threshold = 10e6
        self.upload_terms_threshold = 1000
        self.metadata = metadata
        if terms is not None and len(terms) > 0:
            self.add_terms(terms.copy())

    def add_term(self, c: Union[int, float], indices: List[int]):
        """Adds a single term to the `Problem`
        representation and queues it to be uploaded

        :param c: The cost or weight of this term
        :type c: int, float
        :param indices: The variable indices that are in this term
        :type indices: List[int]
        """
        self.add_terms([Term(indices=indices, c=c)])

    def _get_upload_coords(self):
        blob_name = self.id
        if self.upload_to_url:
            blob_client = BlobClient.from_blob_url(self.upload_to_url)
            container_client = ContainerClient.from_container_url(
                self.workspace._get_linked_storage_sas_uri(
                    blob_client.container_name
                )
            )
            blob_name = blob_client.blob_name
        elif not self.workspace.storage:
            # No storage account is passed, use the linked one
            container_uri = self.workspace._get_linked_storage_sas_uri(self.id)
            container_client = ContainerClient.from_container_url(
                container_uri
            )
        else:
            # Use the specified storage account
            container_client = ContainerClient.from_connection_string(
                self.workspace.storage, self.id
            )

        return {"blob_name": blob_name, "container_client": container_client}

    def add_terms(self, terms: List[Term]):
        """Adds a list of terms to the `Problem`
         representation and queues them to be uploaded

        :param terms: The list of terms to add to the problem
        """
        if self.uploaded_uri is not None:
            raise Exception("Cannot add terms after problem has been uploaded")

        if terms is not None:
            if self.uploader is None:
                upload_coords = self._get_upload_coords()
                self.uploader = JsonStreamingProblemUploader(
                    problem=self,
                    container=upload_coords["container_client"],
                    name=upload_coords["blob_name"],
                    compress=self.compress,
                    upload_size_threshold=self.upload_size_threshold,
                    upload_term_threshold=self.upload_terms_threshold,
                )
                self.uploader.start()
            elif self.uploader.is_done():
                raise Exception(
                    "Cannot add terms after problem has been uploaded"
                )

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
            self.terms_queue.put(terms)

    def download(self):
        """Downloads the uploaded problem as an instance of `Problem`"""
        if not self.uploaded_uri:
            raise Exception(
                "StreamingProblem may not be downloaded before it is uploaded"
            )

        coords = self._get_upload_coords()
        blob = coords["container_client"].get_blob_client(coords["blob_name"])
        contents = download_blob(blob.url)
        return Problem.deserialize(contents, self.name)

    def upload(
        self,
        workspace,
        container_name: str = "qio-problems",
        blob_name: str = None,
        compress: bool = True,
    ):
        """Uploads an optimization problem instance
           to the cloud storage linked with the Workspace.

        :param workspace: interaction terms of the problem.
        :return: uri of the uploaded problem
        """
        if not self.uploaded_uri:
            self.uploader.blob_properties = {
                k: str(v) for k, v in {**self.stats, **self.metadata}.items()
            }
            self.terms_queue.put(None)
            blob = self.uploader.join()
            self.uploaded_uri = blob.getUri(not not self.workspace.storage)
            self.uploader = None
            self.terms_queue = None

        return self.uploaded_uri


class JsonStreamingProblemUploader:
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

    def __init__(
        self,
        problem: StreamingProblem,
        container: ContainerClient,
        name: str,
        compress: bool,
        upload_size_threshold: int,
        upload_term_threshold: int,
        blob_properties: Dict[str, str] = None,
    ):
        self.problem = problem
        self.started_upload = False
        self.blob = StreamedBlob(
            container,
            name,
            "application/json",
            self._get_content_type(compress),
        )
        self.compressedStream = io.BytesIO() if compress else None
        self.compressor = (
            gzip.GzipFile(mode="wb", fileobj=self.compressedStream)
            if compress
            else None
        )
        self.uploaded_terms = 0
        self.blob_properties = blob_properties
        self.__thread = None
        self.__queue_wait_timeout = 1
        self.__upload_terms_threshold = upload_term_threshold
        self.__upload_size_threshold = upload_size_threshold
        self.__read_pos = 0

    def _get_content_type(self, compress: bool):
        if compress:
            return "gzip"

        return "identity"

    def start(self):
        """Starts the problem uploader in another thread"""
        if self.__thread is not None:
            raise Exception(
                "JsonStreamingProblemUploader thread already started"
            )

        self.__thread = threading.Thread(target=self._run_queue)
        self.__thread.start()

    def join(self, timeout: float = None) -> StreamedBlob:
        """Joins the problem uploader thread -
        returning when it completes or when `timeout` is hit

        :param timeout: The the time to wait for the thread to complete.
        If omitted, the method will wait until the thread completes
        """
        if self.__thread is None:
            raise Exception("JsonStreamingProblemUploader has not started")

        self.__thread.join(timeout=timeout)
        return self.blob

    def is_done(self):
        """True if the thread uploader has completed"""
        return not self.__thread.isAlive()

    def _run_queue(self):
        continue_processing = True
        terms = []
        while continue_processing:
            try:
                new_terms = self.problem.terms_queue.get(
                    block=True, timeout=self.__queue_wait_timeout
                )
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
                self._upload_next(terms)
                terms = []

        self._finish_upload()

    def _upload_start(self, terms):
        self.started_upload = True
        self._upload_chunk(
            f'{{"cost_function":{{"version":"{self._get_version()}",'
            + f'"type":"{self._scrub(self.problem.problem_type.name)}",'
            + self._get_initial_config_string()
            + '"terms":['
            + self._get_terms_string(terms)
        )

    def _get_initial_config_string(self):
        if self.problem.init_config:
            return (
                f'{"initial_configuration":}'
                + json.dumps(self.problem.init_config)
                + ","
            )
        return ""

    def _get_version(self):
        return "1.1" if self.problem.init_config else "1.0"

    def _get_terms_string(self, terms):
        result = ("," if self.uploaded_terms > 0 else "") + ",".join(
            [json.dumps(term.to_dict()) for term in terms]
        )
        self.uploaded_terms += len(terms)
        return result

    def _scrub(self, s):
        if '"' in s:
            raise "string should not contain a literal double quote '\"'"

        return s

    def _upload_next(self, terms):
        if not self.started_upload:
            self._upload_start(terms)
        else:
            self._upload_chunk(self._get_terms_string(terms))

    def _maybe_compress_bits(self, chunk: bytes, is_final: bool):
        if self.compressor is None:
            return chunk

        if self.__read_pos > 0:
            self.compressedStream.truncate(0)
            self.compressedStream.seek(0)

        self.compressor.write(chunk)
        if is_final:
            self.compressor.flush()
            self.compressor.close()
        elif (
            self.compressedStream.getbuffer().nbytes
            < self.__upload_size_threshold
        ):
            self.__read_pos = 0
            return

        self.compressedStream.seek(0)
        compressed = self.compressedStream.read(-1)
        self.__read_pos = 0 if compressed is None else len(compressed)
        return compressed

    def _upload_chunk(self, chunk: str, is_final: bool = False):
        compressed = self._maybe_compress_bits(chunk.encode(), is_final)
        if compressed is None:
            return
        if len(compressed) > 0:
            self.blob.upload_data(compressed)

    def _finish_upload(self):
        if not self.started_upload:
            self._upload_start([])

        self._upload_chunk(f'{"]}}}}"}', True)
        self.blob.commit(metadata=self.blob_properties)
