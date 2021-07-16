##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import abc
import logging
import uuid

from urllib.parse import urlparse
from typing import Any, Dict, TYPE_CHECKING
from urllib.parse import urlparse
from azure.storage.blob import BlobClient

from azure.quantum.storage import upload_blob, download_blob, ContainerClient
from azure.quantum._client.models import JobDetails


if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 100


class BaseJob(abc.ABC):
    # Optionally override these to create a Provider-specific Job subclass
    """
    Base job class with methods to create a job from raw blob data,
    upload blob data and download results.
    """
    @staticmethod
    def create_job_id() -> str:
        """Create a unique id for a new job."""
        return str(uuid.uuid1())

    @property
    def container_name(self):
        return f"job-{self.id}"

    @classmethod
    def from_input_data(
        cls,
        workspace: "Workspace",
        name: str,
        target: str,
        input_data: bytes,
        blob_name: str,
        content_type: str,
        encoding: str = "",
        job_id: str = None,
        container_name: str = None,
        provider_id: str = None,
        input_data_format: str = None,
        output_data_format: str = None,
        input_params: Dict[str, Any] = None
    ) -> "BaseJob":
        """Create a new Azure Quantum job based on a raw input_data payload.

        :param workspace: Azure Quantum workspace to submit the input_data to
        :type workspace: "Workspace"
        :param name: Name of the job
        :type name: str
        :param target: Azure Quantum target
        :type target: str
        :param input_data: Raw input data to submit
        :type input_data: bytes
        :param blob_name: Input data blob name
        :type blob_name: str
        :param content_type: Content type, e.g. "application/json"
        :type content_type: str
        :param encoding: input_data encoding, e.g. "gzip", defaults to empty string
        :type encoding: str
        :param job_id: Job ID, defaults to None
        :type job_id: str, optional
        :param container_name: Container name, defaults to None
        :type container_name: str
        :param provider_id: Provider ID, defaults to None
        :type provider_id: str, optional
        :param input_data_format: Input data format, defaults to None
        :type input_data_format: str, optional
        :param output_data_format: Output data format, defaults to None
        :type output_data_format: str, optional
        :param input_params: Input parameters, defaults to None
        :type input_params: Dict[str, Any], optional
        :param input_params: Input params for job
        :type input_params: Dict[str, Any]
        :return: Azure Quantum Job
        :rtype: Job
        """
        # Generate job ID if not specified
        if job_id is None:
            job_id = cls.create_job_id()

        # Create container if it does not yet exist
        container_uri = workspace.get_container_uri(
            job_id=job_id,
            container_name=container_name
        )
        logger.debug(f"Container URI: {container_uri}")

        # Upload data to container
        input_data_uri = cls.upload_input_data(
            container_uri=container_uri,
            input_data=input_data,
            content_type=content_type,
            blob_name=blob_name,
            encoding=encoding
        )

        # Create job
        return cls.from_storage_uri(
            workspace=workspace,
            job_id=job_id,
            target=target,
            input_data_uri=input_data_uri,
            container_uri=container_uri,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            input_params=input_params
        )

    @classmethod
    def from_storage_uri(
        cls,
        workspace: "Workspace",
        name: str,
        target: str,
        input_data_uri: str,
        provider_id: str,
        input_data_format: str,
        output_data_format: str,
        container_uri: str = None,
        job_id: str = None,
        input_params: Dict[str, Any] = None
    ) -> "BaseJob":
        """Create new Job from URI if input data is already uploaded
        to blob storage

        :param workspace: Azure Quantum workspace to submit the blob to
        :type workspace: "Workspace"
        :param name: Job name
        :type name: str
        :param target: Azure Quantum target
        :type target: str
        :param input_data_uri: Input data URI
        :type input_data_uri: str
        :param provider_id: Provider ID
        :type provider_id: str, optional
        :param input_data_format: Input data format
        :type input_data_format: str, optional
        :param output_data_format: Output data format
        :type output_data_format: str, optional
        :param container_uri: Container URI, defaults to None
        :type container_uri: str
        :param job_id: Pre-generated job ID, defaults to None
        :type job_id: str
        :param input_params: Input parameters, defaults to None
        :type input_params: Dict[str, Any], optional
        :return: Job instsance
        :rtype: Job
        """
        # Generate job_id, input_params, data formats and provider ID if not specified
        if job_id is None:
            job_id = cls.create_job_id()
        if input_params is None:
            input_params = {}

        # Create container for output data if not specified
        if container_uri is None:
            container_uri = workspace.get_container_uri(job_id=job_id)

        # Create job details and return Job
        details = JobDetails(
            id=job_id,
            name=name,
            container_uri=container_uri,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            input_data_uri=input_data_uri,
            provider_id=provider_id,
            target=target,
            input_params=input_params
        )
        return cls(workspace, details)

    @staticmethod
    def upload_input_data(
        container_uri: str,
        input_data: bytes,
        content_type: str,
        blob_name: str = "inputData",
        encoding = "",
        return_sas_token: bool = False
    ) -> str:
        """Upload input data file

        :param container_uri: Container URI
        :type container_uri: str
        :param input_data: Input data in binary format
        :type input_data: bytes
        :param content_type: Content type, e.g. "application/json"
        :type content_type: str
        :param blob_name: Blob name, defaults to "inputData"
        :type blob_name: str, optional
        :param encoding: Encoding, e.g. "gzip", defaults to ""
        :type encoding: str, optional
        :param return_sas_token: Flag to return SAS token as part of URI, defaults to False
        :type return_sas_token: bool, optional
        :return: Uploaded data URI
        :rtype: str
        """
        container_client = ContainerClient.from_container_url(
            container_uri
        )

        uploaded_blob_uri = upload_blob(
            container_client,
            blob_name,
            content_type,
            encoding,
            input_data,
            return_sas_token=return_sas_token
        )
        return uploaded_blob_uri

    def download_data(self, blob_uri: str) -> dict:
        """Download file from blob uri

        :param blob_uri: Blob URI
        :type blob_uri: str
        :return: Payload from blob
        :rtype: dict
        """
        url = urlparse(blob_uri)
        if url.query.find("se=") == -1:
            # blob_uri does not contains SAS token,
            # get sas url from service
            blob_client = BlobClient.from_blob_url(
                blob_uri
            )
            blob_uri = self.workspace._get_linked_storage_sas_uri(
                blob_client.container_name, blob_client.blob_name
            )
            payload = download_blob(blob_uri)
        else:
            # blob_uri contains SAS token, use it
            payload = download_blob(blob_uri)

        return payload
