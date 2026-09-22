##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import abc
import logging
import uuid

from enum import Enum
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, parse_qs
from typing import Any, Dict, Optional, TYPE_CHECKING
from azure.storage.blob import BlobClient, BlobProperties

from azure.quantum.storage import upload_blob, download_blob, download_blob_properties, ContainerClient
from azure.quantum._client.models import JobDetails
from azure.quantum.job.workspace_item import WorkspaceItem


if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 300  # Default timeout for waiting for job to complete
_ATTACHMENT_CONTAINER_SAS_PERMISSIONS = frozenset({"r", "w", "l"})

class ContentType(str, Enum):
    json = "application/json"
    text_plain = "text/plain"

class BaseJob(WorkspaceItem):
    # Optionally override these to create a Provider-specific Job subclass
    """
    Base job class with methods to create a job from raw blob data,
    upload blob data and download results.

    :param workspace: Workspace instance of the job
    :type workspace: Workspace
    :param details: Item details model,
            contains item ID, name and other details
    :type details: ItemDetails
    """

    def __init__(self, workspace: "Workspace", details: JobDetails, **kwargs):
        self._attachment_container_uri_cache: Optional[str] = None
        self._attachment_container_uri_cache_identity: Optional[tuple[Optional[str], str]] = None
        super().__init__(workspace=workspace, details=details, **kwargs)

    @staticmethod
    def create_job_id() -> str:
        """Create a unique id for a new job."""
        return str(uuid.uuid1())

    @property
    def details(self) -> JobDetails:
        """Job details"""
        return self._details

    @details.setter
    def details(self, value: JobDetails):
        self._details = value
        self._attachment_container_uri_cache = None
        self._attachment_container_uri_cache_identity = None

    @property
    def container_name(self) -> str:
        """Job input/output data container name"""

        if self._details.container_uri is None:
            return  f"job-{self.id}"

        path = urlparse(self._details.container_uri).path
        container_name = path.lstrip("/").split("/", 1)[0]
        if not container_name:
            raise ValueError("Job container URI does not include a container name.")
        return container_name

    @classmethod
    def from_input_data(
        cls,
        workspace: "Workspace",
        name: str,
        target: str,
        input_data: bytes,
        content_type: ContentType = ContentType.json,
        blob_name: str = "inputData",
        encoding: str = "",
        job_id: str = None,
        container_name: str = None,
        provider_id: str = None,
        input_data_format: str = None,
        output_data_format: str = None,
        input_params: Dict[str, Any] = None,
        session_id: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[list[str]] = None,
        **kwargs
    ) -> "BaseJob":
        """Create a new Azure Quantum job based on a raw input_data payload.

        :param workspace: Azure Quantum workspace to submit the input_data to
        :type workspace: Workspace
        :param name: Name of the job
        :type name: str
        :param target: Azure Quantum target
        :type target: str
        :param input_data: Raw input data to submit
        :type input_data: bytes
        :param blob_name: Input data blob name, defaults to "inputData"
        :type blob_name: str
        :param content_type: Content type, e.g. "application/json"
        :type content_type: ContentType
        :param encoding: input_data encoding, e.g. "gzip", defaults to empty string
        :type encoding: str
        :param job_id: Job ID, defaults to None
        :type job_id: str
        :param container_name: Container name, defaults to None
        :type container_name: str
        :param provider_id: Provider ID, defaults to None
        :type provider_id: str
        :param input_data_format: Input data format, defaults to None
        :type input_data_format: str
        :param output_data_format: Output data format, defaults to None
        :type output_data_format: str
        :param input_params: Input parameters, defaults to None
        :type input_params: Dict[str, Any]
        :param input_params: Input params for job
        :type input_params: Dict[str, Any]
        :param priority: Priority of job.
        :type priority: str
        :param tags: Tags for the job.
        :type tags: list[str]
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
            encoding=encoding,
        )

        # Create and submit job
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
            input_params=input_params,
            session_id=session_id,
            priority=priority,
            tags=tags,
            **kwargs
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
        input_params: Dict[str, Any] = None,
        submit_job: bool = True,
        session_id: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[list[str]] = None,
        **kwargs
    ) -> "BaseJob":
        """Create new Job from URI if input data is already uploaded
        to blob storage

        :param workspace: Azure Quantum workspace to submit the blob to
        :type workspace: Workspace
        :param name: Job name
        :type name: str
        :param target: Azure Quantum target
        :type target: str
        :param input_data_uri: Input data URI
        :type input_data_uri: str
        :param provider_id: Provider ID
        :type provider_id: str
        :param input_data_format: Input data format
        :type input_data_format: str
        :param output_data_format: Output data format
        :type output_data_format: str
        :param container_uri: Container URI, defaults to None
        :type container_uri: str
        :param job_id: Pre-generated job ID, defaults to None
        :type job_id: str
        :param input_params: Input parameters, defaults to None
        :type input_params: Dict[str, Any]
        :param submit_job: If job should be submitted to the service, defaults to True
        :type submit_job: bool
        :param priority: Priority of job.
        :type priority: str
        :param tags: Tags for the job.
        :type tags: list[str]
        :return: Job instance
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
            input_params=input_params,
            session_id=session_id,
            priority=priority,
            tags=tags,
            **kwargs
        )
        job = cls(workspace, details, **kwargs)

        logger.info(
            f"Submitting job '{name}'. \
                Using payload from: '{job.details.input_data_uri}'"
        )

        if submit_job:
            logger.debug(f"==> submitting: {job.details}")
            job.submit()

        return job

    @staticmethod
    def upload_input_data(
        container_uri: str,
        input_data: bytes,
        content_type: Optional[ContentType] = ContentType.json,
        blob_name: str = "inputData",
        encoding: str = "",
        return_sas_token: bool = False
    ) -> str:
        """Upload input data file

        :param container_uri: Container URI
        :type container_uri: str
        :param input_data: Input data in binary format
        :type input_data: bytes
        :param content_type: Content type, e.g. "application/json"
        :type content_type: Optional, ContentType
        :param blob_name: Blob name, defaults to "inputData"
        :type blob_name: str
        :param encoding: Encoding, e.g. "gzip", defaults to ""
        :type encoding: str
        :param return_sas_token: Flag to return SAS token as part of URI, defaults to False
        :type return_sas_token: bool
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
        
        blob_uri_with_sas_token = self._get_blob_uri_with_sas_token(blob_uri)
        payload = download_blob(blob_uri_with_sas_token)

        return payload


    def download_blob_properties(self, blob_uri: str):
        """Download Blob properties

        :param blob_uri: Blob URI
        :type blob_uri: str
        :return: Blob properties
        :rtype: dict
        """

        blob_uri_with_sas_token = self._get_blob_uri_with_sas_token(blob_uri)
        return download_blob_properties(blob_uri_with_sas_token)


    def upload_attachment(
        self,
        name: str,
        data: bytes,
        container_uri: str = None,
        **kwargs
    ) -> str:
        """Uploads an attachment to the job's container file. Attachment's are identified by name.
        Uploading to an existing attachment overrides its previous content.

        :param name: Attachment name
        :type name: str
        :param data: Attachment data in binary format
        :type input_data: bytes
        :param container_uri: Container URI, defaults to the job's linked container.
        :type container_uri: str

        :return: Uploaded data URI
        :rtype: str
        """

        if container_uri is None:
            container_uri = self._get_attachment_container_uri()

        uploaded_blob_uri = self.upload_input_data(
            container_uri = container_uri,
            blob_name = name,
            input_data = data,
            **kwargs
        )
        return uploaded_blob_uri

    def download_attachment(
        self,
        name: str,
        container_uri: str = None
    ):
        """ Downloads an attachment from job's container in Azure Storage. Attachments are blobs of data
            created as part of the Job's execution, or they can be created by uploading directly from Python
            using the upload_attachment method.
            
        :param name: Attachment name
        :type name: str
        :param container_uri: Container URI, defaults to the job's linked container.
        :type container_uri: str

        :return: Attachment data
        :rtype: bytes
        """

        if container_uri is None:
            container_uri = self._get_attachment_container_uri()

        container_client = ContainerClient.from_container_url(container_uri)
        blob_client = container_client.get_blob_client(name)
        response = blob_client.download_blob().readall()
        return response


    def list_attachments(self) -> list[BlobProperties]:
        """ Lists the attachments in the job's linked storage container. Attachments are blobs of
            data created as part of the Job's execution, or they can be uploaded directly from Python
            using the upload_attachment method.

        :return: List of blobs in the job's linked storage container.
        :rtype: list[~azure.storage.blob.BlobProperties]
        """

        container_uri = self._get_attachment_container_uri()

        container_client = ContainerClient.from_container_url(container_uri)
        return list(container_client.list_blobs())


    def _get_attachment_container_uri(self) -> str:
        container_uri = self._details.container_uri
        container_identity = self._get_attachment_container_identity(container_uri)
        cached_container_uri = self._attachment_container_uri_cache
        if cached_container_uri:
            if self._attachment_container_uri_cache_identity != container_identity:
                self._attachment_container_uri_cache = None
                self._attachment_container_uri_cache_identity = None
            elif self._is_attachment_container_uri_usable(cached_container_uri):
                return cached_container_uri

        if container_uri is None:
            refreshed_container_uri = self.workspace.get_container_uri(job_id=self.id)
        else:
            refreshed_container_uri = self.workspace.get_container_uri(
                job_id=self.id,
                container_name=self.container_name,
            )
            stored_hostname = urlparse(container_uri).hostname
            refreshed_hostname = urlparse(refreshed_container_uri).hostname
            if stored_hostname != refreshed_hostname:
                raise ValueError(
                    "Refreshed attachment container hostname "
                    f"'{refreshed_hostname}' does not match job container hostname "
                    f"'{stored_hostname}'."
                )

        if not self._is_attachment_container_uri_usable(refreshed_container_uri):
            raise ValueError(
                "Refreshed attachment container URI does not contain a usable SAS token."
            )

        self._attachment_container_uri_cache = refreshed_container_uri
        self._attachment_container_uri_cache_identity = container_identity
        return refreshed_container_uri


    def _get_attachment_container_identity(
        self,
        container_uri: Optional[str],
    ) -> tuple[Optional[str], str]:
        if container_uri is None:
            return (None, f"/job-{self.id}")

        parsed_uri = urlparse(container_uri)
        return (parsed_uri.hostname, parsed_uri.path.rstrip("/"))


    def _is_attachment_container_uri_usable(
        self,
        container_uri: str,
    ) -> bool:

        parsed_uri = urlparse(container_uri)
        if (
            parsed_uri.scheme.lower() != "https"
            or parsed_uri.hostname is None
            or not parsed_uri.path.strip("/")
        ):
            return False

        query_params = parse_qs(parsed_uri.query)
        token_expire_query_param = query_params.get("se")
        token_start_query_param = query_params.get("st")
        token_permissions = set(query_params.get("sp", [""])[0])
        if (
            not query_params.get("sig")
            or not _ATTACHMENT_CONTAINER_SAS_PERMISSIONS.issubset(token_permissions)
            or not token_expire_query_param
        ):
            return False

        try:
            token_expire_time = datetime.fromisoformat(
                token_expire_query_param[0].replace("Z", "+00:00")
            )
            if token_expire_time.tzinfo is None:
                token_expire_time = token_expire_time.replace(tzinfo=timezone.utc)

            token_start_time = None
            if token_start_query_param:
                token_start_time = datetime.fromisoformat(
                    token_start_query_param[0].replace("Z", "+00:00")
                )
                if token_start_time.tzinfo is None:
                    token_start_time = token_start_time.replace(tzinfo=timezone.utc)

            current_utc_time = datetime.now(tz=timezone.utc)
            has_started = token_start_time is None or token_start_time <= current_utc_time
            return has_started and current_utc_time + timedelta(minutes=5) < token_expire_time
        except ValueError:
            logger.debug(
                "Unable to parse attachment SAS start or expiry time; requesting a fresh URI."
            )
            return False


    def _get_blob_uri_with_sas_token(self, blob_uri: str) -> str:
        """Get Blob URI with SAS-token if one was not specified in blob_uri parameter
        :param blob_uri: Blob URI
        :type blob_uri: str
        :return: Blob URI with SAS-token
        :rtype: str
        """
        url = urlparse(blob_uri)
        query_params = parse_qs(url.query)
        token_expire_query_param = query_params.get("se")

        token_expire_time = None

        if token_expire_query_param is not None:
            token_expire_time_str = token_expire_query_param[0]

            # Since python < 3.11 can not easily parse Z suffixed UTC timestamp and 
            # assuming that the timestamp is always UTC, we replace that suffix with UTC offset.
            token_expire_time = datetime.fromisoformat(
                token_expire_time_str.replace('Z', '+00:00')
            )
            
            # Make an expiration time a little earlier, so there's no case where token is
            # used a second or so before of its expiration.
            token_expire_time = token_expire_time - timedelta(minutes=5)

        current_utc_time = datetime.now(tz=timezone.utc)
        if token_expire_time is None or current_utc_time >= token_expire_time:
            # blob_uri does not contains SAS token or it is expired,
            # get sas url from service
            blob_client = BlobClient.from_blob_url(
                blob_uri
            )
            blob_uri = self.workspace._get_linked_storage_sas_uri(
                blob_client.container_name, blob_client.blob_name
            )

        return blob_uri