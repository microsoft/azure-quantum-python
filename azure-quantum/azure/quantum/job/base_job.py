##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import abc
import logging
import uuid

from urllib.parse import urlparse
from typing import Tuple
from urllib.parse import urlparse
from azure.storage.blob import BlobClient

from azure.quantum.job import Job
from azure.quantum.workspace import Workspace
from azure.quantum.storage import upload_blob, download_blob, ContainerClient
from azure.quantum._client.models import JobDetails

DEFAULT_TIMEOUT = 100

_log = logging.getLogger(__name__)


class _BaseJob(abc.ABC):
    """
    Base job class with methods to create a job from raw blob data,
    upload blob data and download results.
    """
    @staticmethod
    def create_job_id() -> str:
        """Create a unique id for a new job."""
        return str(uuid.uuid1())

    @classmethod
    def from_blob(
        cls,
        workspace: Workspace,
        target: str,
        blob: bytes,
        name: str,
        timeout: int
    ) -> "Job":
        """Create a new Azure Quantum job based on a raw blob payload.

        :param workspace: Azure Quantum workspace to submit the blob to
        :type workspace: Workspace
        :param target: Azure Quantum target
        :type target: str
        :param blob: Raw blob data to submit
        :type blob: bytes
        :param name: Name of the job
        :type name: str
        :param timeout: Optional timeout, defaults to 100
        :type timeout: int
        :return: Azure Quantum Job
        :rtype: Job
        """
        job_id = cls.create_job_id()
        container_uri, input_data_uri = cls._upload_blob(
            workspace=workspace,
            job_id=job_id,
            blob=blob,
            blob_name=name
        )
        details = JobDetails(
            id=job_id,
            name=name,
            container_uri=container_uri,
            input_data_format=cls.input_data_format,
            output_data_format=cls.output_data_format,
            input_data_uri=input_data_uri,
            provider_id=cls.provider_id,
            target=target,
            input_params={'params': {'timeout': timeout}}
        )
        return cls(workspace, details)

    @staticmethod
    def _upload_blob(
        workspace: Workspace,
        job_id: str,
        blob: bytes,
        blob_name = "inputData",
        content_type = "application/json",
        encoding = ""
    ) -> Tuple[str, str]:
        """Upload blob file"""
        if blob is None:
            raise ValueError("Please provide blob data.")
        container_name = f"job-{job_id}"
        container_uri = workspace._get_linked_storage_sas_uri(
            container_name
        )
        container_client = ContainerClient.from_container_url(
            container_uri
        )
        uploaded_blob_uri = upload_blob(
            container_client,
            blob_name,
            content_type,
            encoding,
            blob,
            return_sas_token=False
        )
        return container_uri, uploaded_blob_uri
    
    @staticmethod
    def _download_blob(self, blob_uri: str) -> dict:
        """Download blob file"""
        url = urlparse(blob_uri)
        if url.query.find("se=") == -1:
            # output_data_uri does not contains SAS token,
            # get sas url from service
            blob_client = BlobClient.from_blob_url(
                blob_uri
            )
            blob_uri = self.workspace._get_linked_storage_sas_uri(
                blob_client.container_name, blob_client.blob_name
            )
            payload = download_blob(blob_uri)
        else:
            # output_data_uri contains SAS token, use it
            payload = download_blob(blob_uri)

        return payload
