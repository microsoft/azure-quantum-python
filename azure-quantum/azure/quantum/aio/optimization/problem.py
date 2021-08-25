##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from azure.quantum.aio.storage import (
    ContainerClient,
    download_blob,
    BlobClient
)
from azure.quantum.aio.job.job import Job
from azure.quantum.optimization import Problem as SyncProblem
from azure.quantum.optimization import ProblemType

logger = logging.getLogger(__name__)

__all__ = ["Problem", "ProblemType"]

if TYPE_CHECKING:
    from azure.quantum.aio.workspace import Workspace


class Problem(SyncProblem):
    """Problem to submit to the service.

    :param name: Problem name
    :type name: str
    :param terms: Problem terms, depending on solver.
        Defaults to None
    :type terms: Optional[List[Term]], optional
    :param init_config: Optional configuration details, depending on solver.
        Defaults to None
    :type init_config: Optional[Dict[str,int]], optional
    :param problem_type: Problem type (ProblemType.pubo or
        ProblemType.ising), defaults to ProblemType.ising
    :type problem_type: ProblemType, optional
    """
    async def upload(
        self,
        workspace: "Workspace",
        container_name: str = "qio-problems",
        blob_name: str = "inputData",
        compress: bool = True,
        container_uri: str = None
    ):
        """Uploads an optimization problem instance to
        the cloud storage linked with the Workspace.

        :param workspace: interaction terms of the problem.
        :type workspace: Workspace
        :param container_name: Container name, defaults to "qio-problems"
        :type container_name: str, optional
        :param blob_name: Blob name, defaults to None
        :type blob_name: str, optional
        :param compress: Flag to compress the payload, defaults to True
        :type compress: bool, optional
        :param container_uri: Optional container URI
        :type container_uri: str
        :return: uri of the uploaded problem
        :rtype: str
        """
        blob_params = [workspace, container_name, blob_name, compress]
        if self.uploaded_blob_uri and self.uploaded_blob_params == blob_params:
            return self.uploaded_blob_uri

        if blob_name is None:
            blob_name = self._blob_name()

        encoding = "gzip" if compress else ""
        blob = self.to_blob(compress=compress)
        if container_uri is None:
            container_uri = await workspace.get_container_uri(
                container_name=container_name
            )
        input_data_uri = await Job.upload_input_data(
            input_data=blob,
            blob_name=blob_name,
            container_uri=container_uri,
            encoding=encoding,
            content_type="application/json"
        )
        self.uploaded_blob_params = blob_params
        self.uploaded_blob_uri = input_data_uri
        return input_data_uri

    async def download(self, workspace:"Workspace"):
        """Downloads the uploaded problem as an instance of `Problem`"""
        if not self.uploaded_blob_uri:
            raise Exception(
                "Problem may not be downloaded before it is uploaded"
            )
        blob_client = BlobClient.from_blob_url(self.uploaded_blob_uri)
        container_client = ContainerClient.from_container_url(
            await workspace._get_linked_storage_sas_uri(
                blob_client.container_name
            )
        )
        blob_name = blob_client.blob_name
        blob = container_client.get_blob_client(blob_name)
        contents = await download_blob(blob.url)
        return Problem.deserialize(contents, self.name)
