##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from __future__ import annotations
from datetime import datetime
import logging
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    TYPE_CHECKING,
    Tuple,
    Union)

from azure.quantum._client import QuantumClient
from azure.quantum._client.operations import (
    JobsOperations,
    StorageOperations,
    QuotasOperations,
    SessionsOperations,
    TopLevelItemsOperations
)
from azure.quantum._client.models import BlobDetails, JobStatus
from azure.quantum import  Job, Session
from azure.quantum._workspace_connection_params import (
    WorkspaceConnectionParams
)
from azure.quantum._constants import (
    DATA_PLANE_CREDENTIAL_SCOPE,
)
from azure.quantum.storage import (
    create_container_using_client,
    get_container_uri,
    ContainerClient
)

if TYPE_CHECKING:
    from azure.quantum._client.models import TargetStatus
    from azure.quantum.target import Target

logger = logging.getLogger(__name__)

__all__ = ["Workspace"]


class Workspace:
    DEFAULT_CONTAINER_NAME_FORMAT = "job-{job_id}"

    """Represents an Azure Quantum workspace.

    When creating a Workspace object, callers have three options for
    identifying the Azure Quantum workspace (in order of precedence):
    1. specify a valid connection string; or
    2. specify a valid location and resource ID; or
    3. specify a valid location, subscription ID,
       resource group, and workspace name.

    If the Azure Quantum workspace does not have linked storage, the caller
    must also pass a valid Azure storage account connection string.

    :param subscription_id:
        The Azure subscription ID.
        Ignored if resource_id or connection_string is specified.

    :param resource_group:
        The Azure resource group name.
        Ignored if resource_id or connection_string is specified.

    :param name:
        The Azure Quantum workspace name.
        Ignored if resource_id or connection_string is specified.

    :param storage:
        The Azure storage account connection string.
        Required only if the specified Azure Quantum
        workspace does not have linked storage.

    :param resource_id:
        The resource ID of the Azure Quantum workspace.
        Ignored if connection_string is specified.

    :param location:
        The Azure region where the Azure Quantum workspace is provisioned.
        This may be specified as a region name such as
        \"East US\" or a location name such as \"eastus\".
        Ignored if connection_string is specified.

    :param credential:
        The credential to use to connect to Azure services.
        Normally one of the credential types from `Azure.Identity` (https://docs.microsoft.com/python/api/overview/azure/identity-readme?view=azure-python#credential-classes).

        Defaults to \"DefaultAzureCredential\", which will attempt multiple
        forms of authentication.

        Ignored if connection_string is specified.

    :param user_agent:
        Add the specified value as a prefix to the
        HTTP User-Agent header when communicating to the Azure Quantum service.

    :param connection_string:
        A connection string to the Azure Quantum workspace.
    """
    def __init__(
        self,
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        name: Optional[str] = None,
        storage: Optional[str] = None,
        resource_id: Optional[str] = None,
        location: Optional[str] = None,
        credential: Optional[object] = None,
        connection_string: Optional[str] = None,
        **kwargs: Any,
    ):
        connection_params = WorkspaceConnectionParams(
            location=location,
            subscription_id=subscription_id,
            resource_group=resource_group,
            workspace_name=name,
            credential=credential,
            resource_id=resource_id,
            connection_string=connection_string,
            **kwargs
        ).default_from_env_vars()
        logger.info("Using %s environment.", connection_params.environment)

        connection_params.assert_complete()

        connection_params.on_new_client_request = self.on_new_client_request

        self._connection_params = connection_params
        self._storage = storage

        # Create QuantumClient
        self._client = self._create_client()

    def on_new_client_request(self):
        self._client = self._create_client()

    @property
    def location(self):
        return self._connection_params.location

    @property
    def subscription_id(self):
        return self._connection_params.subscription_id

    @property
    def resource_group(self):
        return self._connection_params.resource_group

    @property
    def name(self):
        return self._connection_params.workspace_name

    @property
    def credential(self):
        return self._connection_params.credential

    @property
    def storage(self):
        return self._storage

    def _create_client(self) -> QuantumClient:
        connection_params = self._connection_params
        kwargs = {}
        if connection_params.api_version:
            kwargs["api_version"] = connection_params.api_version
        client = QuantumClient(
            credential=connection_params.get_credential_or_default(),
            subscription_id=connection_params.subscription_id,
            resource_group_name=connection_params.resource_group,
            workspace_name=connection_params.workspace_name,
            azure_region=connection_params.location,
            user_agent=connection_params.get_full_user_agent(),
            authentication_policy=connection_params.get_auth_policy(),
            credential_scopes = [DATA_PLANE_CREDENTIAL_SCOPE],
            endpoint=connection_params.base_url,
            **kwargs
        )
        return client

    @property
    def user_agent(self):
        """
        Get the Workspace's UserAgent that is sent to
        the service via the header.
        """
        return self._connection_params.get_full_user_agent()

    def append_user_agent(self, value: str):
        """
        Append a new value to the Workspace's UserAgent and re-initialize the
        QuantumClient. The values are appended using a dash.

        :param value: UserAgent value to add, e.g. "azure-quantum-<plugin>"
        """
        self._connection_params.append_user_agent(value=value)

    @classmethod
    def from_connection_string(cls, connection_string, **kwargs):
        return cls(connection_string=connection_string, **kwargs)

    def _get_top_level_items_client(self) -> TopLevelItemsOperations:
        return self._client.top_level_items

    def _get_sessions_client(self) -> SessionsOperations:
        return self._client.sessions

    def _get_jobs_client(self) -> JobsOperations:
        return self._client.jobs

    def _get_workspace_storage_client(self) -> StorageOperations:
        return self._client.storage

    def _get_quotas_client(self) -> QuotasOperations:
        return self._client.quotas

    def _get_linked_storage_sas_uri(
        self, container_name: str, blob_name: str = None
    ) -> str:
        """
        Calls the service and returns a container sas url
        """
        client = self._get_workspace_storage_client()
        blob_details = BlobDetails(
            container_name=container_name, blob_name=blob_name
        )
        container_uri = client.sas_uri(blob_details=blob_details)

        logger.debug(f"Container URI from service: {container_uri}")
        return container_uri.sas_uri

    def submit_job(self, job: Job) -> Job:
        """
        Submit job.

        :param job: Job to submit
        :type job: Job
        """
        client = self._get_jobs_client()
        details = client.create(
            job.details.id, job.details
        )
        return Job(self, details)

    def cancel_job(self, job: Job) -> Job:
        """
        Job to cancel.

        :param job: Job to cancel
        :type job: Job
        """
        client = self._get_jobs_client()
        client.cancel(job.details.id)
        details = client.get(job.id)
        return Job(self, details)

    def get_job(self, job_id: str) -> Job:
        """
        Returns the job corresponding to the given id.
        
        :param job_id: Id of a job to fetch.
        :type job_id: str
        :return: Job
        :rtype: Job
        """
        from azure.quantum.target.target_factory import TargetFactory
        from azure.quantum.target import Target

        client = self._get_jobs_client()
        details = client.get(job_id)
        target_factory = TargetFactory(base_cls=Target, workspace=self)
        target_cls = target_factory._target_cls(
            details.provider_id,
            details.target)
        job_cls = target_cls._get_job_class()
        return job_cls(self, details)

    def list_jobs(
        self,
        name_match: str = None,
        status: Optional[JobStatus] = None,
        created_after: Optional[datetime] = None
    ) -> List[Job]:
        """
        Returns list of jobs that meet optional (limited) filter criteria.

        :param name_match: regex expression for job name matching
        :param status: filter by job status
        :param created_after: filter jobs after time of job creation
        :return: Jobs that matched the search criteria
        :rtype: typing.List[Job]
        """
        client = self._get_jobs_client()
        jobs = client.list()

        result = []
        for j in jobs:
            deserialized_job = Job(self, j)
            if deserialized_job.matches_filter(name_match, status, created_after):
                result.append(deserialized_job)

        return result

    def _get_target_status(self, name: str, provider_id: str) -> List[Tuple[str, "TargetStatus"]]:
        """Get provider ID and status for targets"""
        return [
            (provider.id, target)
            for provider in self._client.providers.get_status()
            for target in provider.targets
            if (provider_id is None or provider.id.lower() == provider_id.lower())
                and (name is None or target.id.lower() == name.lower())
        ]

    def get_targets(
        self, 
        name: str = None, 
        provider_id: str = None,
        **kwargs
    ) -> Union["Target", Iterable["Target"]]:
        """Returns all available targets for this workspace filtered by name and provider ID.

        :param name: Optional target name to filter by, defaults to None
        :type name: str
        :param provider_id: Optional provider Id to filter by, defaults to None
        :type provider_id: str

        :return: Targets
        :rtype: typing.Iterable[Target]
        """
        from azure.quantum.target.target_factory import TargetFactory
        from azure.quantum.target import Target

        target_factory = TargetFactory(
            base_cls=Target,
            workspace=self
        )

        return target_factory.get_targets(
            name=name,
            provider_id=provider_id
        )

    def get_quotas(self) -> List[Dict[str, Any]]:
        """Get a list of job quotas for the given workspace.

        :return: Job quotas
        :rtype: typing.List[typing.Dict[str, typing.Any]]
        """
        client = self._get_quotas_client()
        return [q.as_dict() for q in client.list()]

    def list_top_level_items(
        self
    ) -> List[Union[Job, Session]]:
        """Get a list of top level items for the given workspace.

        :return: Workspace items
        :rtype: typing.List[Job] or typing.List[Session]
        """
        from azure.quantum.job.workspace_item_factory import WorkspaceItemFactory
        client = self._get_top_level_items_client()
        item_details_list = client.list()
        result = [WorkspaceItemFactory.__new__(workspace=self, item_details=item_details) 
                  for item_details in item_details_list]
        return result

    def list_sessions(
        self
    ) -> List[Session]:
        """Get the list of sessions in the given workspace.

        :return: Session items
        :rtype: typing.List[Session]
        """
        client = self._get_sessions_client()
        session_details_list = client.list()
        result = [Session(workspace=self,details=session_details) 
                  for session_details in session_details_list]
        return result

    def open_session(
        self,
        session: Session,
        **kwargs
    ):
        """Opens/creates a session in the given workspace.

        :param session: The session to be opened/created.
        :type session: Session
        """
        client = self._get_sessions_client()
        session.details = client.open(
            session_id=session.id,
            session=session.details)

    def close_session(
        self,
        session: Session
    ):
        """Closes a session in the given workspace if the
           session is not in a terminal state.
           Otherwise, just refreshes the session details.

        :param session: The session to be closed.
        :type session: Session
        """
        client = self._get_sessions_client()
        if not session.is_in_terminal_state():
            session.details = client.close(session_id=session.id)
        else:
            session.details = client.get(session_id=session.id)

        if session.target:
            if (session.target.latest_session
                and session.target.latest_session.id == session.id):
                session.target.latest_session.details = session.details

    def refresh_session(
        self,
        session: Session
    ):
        """Updates the session details with the latest information
           from the workspace.

        :param session: The session to be refreshed.
        :type session: Session
        """
        session.details = self.get_session(session_id=session.id).details

    def get_session(
        self,
        session_id: str
    ) -> Session:
        """Gets a session from the workspace.

        :param session_id: The id of session to be retrieved.
        :type session_id: str

        :return: Session
        :rtype: Session
        """
        client = self._get_sessions_client()
        session_details = client.get(session_id=session_id)
        result = Session(workspace=self, details=session_details)
        return result

    def list_session_jobs(
        self,
        session_id: str
    ) -> List[Job]:
        """Gets all jobs associated with a session.

        :param session_id: The id of session.
        :type session_id: str

        :return: List of all jobs associated with a session.
        :rtype: typing.List[Job]
        """
        client = self._get_sessions_client()
        job_details_list = client.jobs_list(session_id=session_id)
        result = [Job(workspace=self, job_details=job_details)
                  for job_details in job_details_list]
        return result

    def get_container_uri(
        self,
        job_id: str = None,
        container_name: str = None,
        container_name_format: str = DEFAULT_CONTAINER_NAME_FORMAT
    ) -> str:
        """Get container URI based on job ID or container name.
        Creates a new container if it does not yet exist.

        :param job_id: Job ID, defaults to None
        :type job_id: str
        :param container_name: Container name, defaults to None
        :type container_name: str
        :param container_name_format: Container name format, defaults to "job-{job_id}"
        :type container_name_format: str
        :return: Container URI
        :rtype: str
        """
        if container_name is None:
            if job_id is not None:
                container_name = container_name_format.format(job_id=job_id)
            elif job_id is None:
                container_name = f"{self.name}-data"
        # Create container URI and get container client
        if self.storage is None:
            # Get linked storage account from the service, create
            # a new container if it does not yet exist
            container_uri = self._get_linked_storage_sas_uri(
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
                self.storage, container_name
            )
        return container_uri
