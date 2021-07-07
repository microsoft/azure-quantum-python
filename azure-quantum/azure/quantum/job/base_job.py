##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import abc
import logging
import uuid

from urllib.parse import urlparse
from typing import Any, Dict, TYPE_CHECKING, Tuple
from urllib.parse import urlparse
from azure.storage.blob import BlobClient

from azure.quantum.storage import create_container_using_client, get_container_uri, upload_blob, download_blob, ContainerClient
from azure.quantum._client.models import JobDetails


if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 100


class BaseJob(abc.ABC):
    # Optionally override these to create a Provider-specific Job subclass
    input_data_format = None
    output_data_format = None
    provider_id = None

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
    def from_blob(
        cls,
        workspace: "Workspace",
        name: str,
        target: str,
        blob: bytes,
        blob_name: str,
        encoding: str = "",
        input_data_format: str = None,
        output_data_format: str = None,
        provider_id: str = None,
        input_params: Dict[str, Any] = None
    ) -> "BaseJob":
        """Create a new Azure Quantum job based on a raw blob payload.

        :param workspace: Azure Quantum workspace to submit the blob to
        :type workspace: "Workspace"
        :param name: Name of the job
        :type name: str
        :param target: Azure Quantum target
        :type target: str
        :param blob: Raw blob data to submit
        :type blob: bytes
        :param blob_name: Blob name
        :type blob_name: str
        :param encoding: Blob encoding, e.g. "gzip", defaults to empty string
        :type encoding: str
        :param input_data_format: Input data format, defaults to None
        :type input_data_format: str, optional
        :param output_data_format: Output data format, defaults to None
        :type output_data_format: str, optional
        :param provider_id: Provider ID, defaults to None
        :type provider_id: str, optional
        :param input_params: Input parameters, defaults to None
        :type input_params: Dict[str, Any], optional
        :param input_params: Input params for job
        :type input_params: Dict[str, Any]
        :return: Azure Quantum Job
        :rtype: Job
        """
        job_id = cls.create_job_id()
        container_name = f"job-{job_id}"
        container_uri = cls.create_container(
            workspace=workspace,
            container_name=container_name
        )
        logger.debug(f"Container URI: {container_uri}")
        input_data_uri = cls.upload_blob(
            blob=blob,
            blob_name=blob_name,
            encoding=encoding
        )

        return cls.from_uri(
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
    def from_uri(
        cls,
        name: str,
        workspace: "Workspace",
        job_id: str,
        target: str,
        input_data_uri: str,
        container_uri: str,
        input_data_format: str = None,
        output_data_format: str = None,
        provider_id: str = None,
        input_params: Dict[str, Any] = None
    ) -> "BaseJob":
        """Create new Job from URI if input data is already uploaded
        to blob storage

        :param name: Job name
        :type name: str
        :param workspace: Azure Quantum workspace to submit the blob to
        :type workspace: "Workspace"
        :param job_id: Pre-generated job ID
        :type job_id: str
        :param target: Azure Quantum target
        :type target: str
        :param input_data_uri: Input data URI
        :type input_data_uri: str
        :param container_uri: Container URI
        :type container_uri: str
        :param input_data_format: Input data format, defaults to None
        :type input_data_format: str, optional
        :param output_data_format: Output data format, defaults to None
        :type output_data_format: str, optional
        :param provider_id: Provider ID, defaults to None
        :type provider_id: str, optional
        :param input_params: Input parameters, defaults to None
        :type input_params: Dict[str, Any], optional
        :return: Job instsance
        :rtype: Job
        """
        if input_params is None:
            input_params = {"params": {"timeout": DEFAULT_TIMEOUT}}
        if input_data_format is None:
            input_data_format = cls.input_data_format
        if output_data_format is None:
            output_data_format = cls.output_data_format
        if provider_id is None:
            provider_id = cls.provider_id

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
    def create_container(
        workspace: "Workspace",
        container_name: str
    ):
        # Create container URI and get container client
        if workspace.storage is None:
            # Get linked storage account from the service, create
            # a new container if it does not yet exist
            container_uri = workspace._get_linked_storage_sas_uri(
                container_name
            )
            container_client = ContainerClient.from_container_url(
                container_uri
            )
            create_container_using_client(container_client)
        else:
            # Use the storage acount specified to generate container URI,
            # create a new container if it does not yet exist
            container_uri = get_container_uri(
                workspace.storage, container_name
            )
        return container_uri

    @staticmethod
    def upload_blob(
        container_uri: str,
        blob: bytes,
        blob_name = "inputData",
        content_type = "application/json",
        encoding = "",
        return_sas_token: bool = False
    ) -> str:
        """Upload blob file"""
        container_client = ContainerClient.from_container_url(
            container_uri
        )

        uploaded_blob_uri = upload_blob(
            container_client,
            blob_name,
            content_type,
            encoding,
            blob,
            return_sas_token=return_sas_token
        )
        return uploaded_blob_uri

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
