##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from datetime import datetime
import logging
import os
import re

from azure.core.pipeline import policies

from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING, Tuple, Union

# Temporarily replacing the DefaultAzureCredential with
# a custom _DefaultAzureCredential
#   from azure.identity import DefaultAzureCredential
from azure.quantum._authentication import _DefaultAzureCredential

from azure.quantum._client import QuantumClient
from azure.quantum._client.operations import (
    JobsOperations,
    StorageOperations,
    QuotasOperations,
    SessionsOperations,
    TopLevelItemsOperations
)
from azure.quantum._client.models import BlobDetails, JobStatus
from azure.quantum import Job, Session
from azure.quantum.storage import create_container_using_client, get_container_uri, ContainerClient

from .version import __version__

if TYPE_CHECKING:
    from azure.quantum._client.models import TargetStatus
    from azure.quantum.target import Target

logger = logging.getLogger(__name__)

__all__ = ["Workspace"]

DEFAULT_CONTAINER_NAME_FORMAT = "job-{job_id}"
USER_AGENT_APPID_ENV_VAR_NAME = "AZURE_QUANTUM_PYTHON_APPID"


def sdk_environment(name):
    return (
        "AZURE_QUANTUM_ENV" in os.environ
        and os.environ["AZURE_QUANTUM_ENV"] == name
    )


# Settings based on environment variables:
BASE_URL_FROM_ENV = (
    os.environ["AZURE_QUANTUM_BASEURL"]
    if "AZURE_QUANTUM_BASEURL" in os.environ
    else None
)
if sdk_environment("dogfood"):
    logger.info("Using DOGFOOD configuration.")
    BASE_URL = (
        lambda location: BASE_URL_FROM_ENV
        or f"https://{location}.quantum-test.azure.com/"
    )
    ARM_BASE_URL = "https://api-dogfood.resources.windows-int.net/"
else:
    if sdk_environment("canary"):
        logger.info("Using CANARY configuration.")
        BASE_URL = (
            lambda location: BASE_URL_FROM_ENV
            or f'{"https://eastus2euap.quantum.azure.com/"}'
        )
    else:
        logger.debug("Using production configuration.")
        BASE_URL = (
            lambda location: BASE_URL_FROM_ENV
            or f"https://{location}.quantum.azure.com/"
        )
    ARM_BASE_URL = "https://management.azure.com/"


class Workspace:
    """Represents an Azure Quantum workspace.

    When creating a Workspace object, callers have two options for identifying
    the Azure Quantum workspace:
    1. specify a valid resource ID, or
    2. specify a valid subscription ID, resource group, and workspace name.

    If the Azure Quantum workspace does not have linked storage, the caller
    must also pass a valid Azure storage account connection string.

    :param subscription_id:
        The Azure subscription ID. Ignored if resource_id is specified.

    :param resource_group:
        The Azure resource group name. Ignored if resource_id is specified.

    :param name:
        The Azure Quantum workspace name. Ignored if resource_id is specified.

    :param storage:
        The Azure storage account connection string.
        Required only if the specified Azure Quantum
        workspace does not have linked storage.

    :param resource_id:
        The resource ID of the Azure Quantum workspace.

    :param location:
        The Azure region where the Azure Quantum workspace is provisioned.
        This may be specified as a region name such as
        \"East US\" or a location name such as \"eastus\".

    :param credential:
        The credential to use to connect to Azure services.
        Normally one of the credential types from Azure.Identity (https://docs.microsoft.com/python/api/overview/azure/identity-readme?view=azure-python#credential-classes).

        Defaults to \"DefaultAzureCredential\", which will attempt multiple 
        forms of authentication.

    :param user_agent:
        Add the specified value as a prefix to the HTTP User-Agent header when communicating to the Azure Quantum service.
    """

    credentials = None

    def __init__(
        self,
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        name: Optional[str] = None,
        storage: Optional[str] = None,
        resource_id: Optional[str] = None,
        location: Optional[str] = None,
        credential: Optional[object] = None,
        user_agent: Optional[str] = None,
        **kwargs: Any,
    ):
        if resource_id is not None:
            # A valid resource ID looks like:
            # /subscriptions/f846b2bd-d0e2-4a1d-8141-4c6944a9d387/resourceGroups/
            # RESOURCE_GROUP_NAME/providers/Microsoft.Quantum/Workspaces/WORKSPACE_NAME
            regex = r"^/subscriptions/([a-fA-F0-9-]*)/resourceGroups/([^\s/]*)/providers/Microsoft\.Quantum/Workspaces/([^\s/]*)$"
            match = re.search(regex, resource_id, re.IGNORECASE)
            if match:
                # match should contain four groups:
                # -> match.group(0):
                # The full resource ID for the Azure Quantum workspace
                # -> match.group(1): The Azure subscription ID
                # -> match.group(2): The Azure resource group name
                # -> match.group(3): The Azure Quantum workspace name
                subscription_id = match.group(1)
                resource_group = match.group(2)
                name = match.group(3)

        if not subscription_id or not resource_group or not name:
            raise ValueError(
                "Azure Quantum workspace not fully specified."
                + "Please specify either a valid resource ID "
                + "or a valid combination of subscription ID,"
                + "resource group name, and workspace name."
            )

        if not location:
            raise ValueError(
                "Azure Quantum workspace does not have an associated location. " +
                "Please specify the location associated with your workspace.")

        # Temporarily using a custom _DefaultAzureCredential
        # instead of Azure.Identity.DefaultAzureCredential
        # See _DefaultAzureCredential documentation for more info.
        if credential is None:
            credential = _DefaultAzureCredential(exclude_interactive_browser_credential=False,
                                                 exclude_shared_token_cache_credential=True,
                                                 subscription_id=subscription_id,
                                                 arm_base_url=ARM_BASE_URL)

        self.credentials = credential
        self.name = name
        self.resource_group = resource_group
        self.subscription_id = subscription_id
        self.storage = storage
        self._user_agent = user_agent
        self.kwargs = kwargs

        # Convert user-provided location into names
        # recognized by Azure resource manager.
        # For example, a customer-provided value of
        # "West US" should be converted to "westus".
        self.location = "".join(location.split()).lower()

        # Create QuantumClient
        self._client = self._create_client()

    def _create_client(self) -> QuantumClient:
        client = QuantumClient(
            credential=self.credentials,
            subscription_id=self.subscription_id,
            resource_group_name=self.resource_group,
            workspace_name=self.name,
            azure_region=self.location,
            user_agent=self.user_agent,
            kwargs=self.kwargs
        )
        return client

    @property
    def user_agent(self):
        """
        Get the Workspace's UserAgent that is sent to the service via the header.
        Uses the value specified during initialization and appends the environment
        variable AZURE_QUANTUM_PYTHON_APPID if specified.
        """
        full_user_agent = self._user_agent
        env_app_id = os.environ.get(USER_AGENT_APPID_ENV_VAR_NAME)
        if env_app_id:
            full_user_agent = f"{full_user_agent}-{env_app_id}" if full_user_agent else env_app_id
        return full_user_agent

    @classmethod
    def _parse_connection_string(cls, connection_string: str):
        # The connection string looks like:
        #SubscriptionId=<subId>;ResourceGroupName=<resourceGroupName>;WorkspaceName=<workspaceName>;
        #WorkspaceKey=<workspacekey>;QuantumEndpoint=https://<location>.quantum.azure.com; 
        regex = r"^SubscriptionId=([a-fA-F0-9-]*);ResourceGroupName=([^\s/]*);WorkspaceName=([^\s/]*);WorkspaceKey=([^\s/]*);QuantumEndpoint=https://([^\s/]*).quantum.azure.com;$"
        match = re.search(regex, connection_string, re.IGNORECASE)
        if match:
            # match should contain four groups:
            # -> match.group(0):
            # The full resource ID for the Azure Quantum workspace
            # -> match.group(1): The Azure subscription ID
            # -> match.group(2): The Azure resource group name
            # -> match.group(3): The Azure Quantum workspace name
            subscription_id = match.group(1)
            resource_group = match.group(2)
            workspace_name = match.group(3)
            workspace_key = match.group(4)
            location = match.group(5)

            return subscription_id, resource_group, workspace_name, location, workspace_key

        raise Exception("Invalid connection string")

    @classmethod
    def from_connection_string(cls, connection_string, **kwargs):
        subscription_id, resource_group, workspace_name, location, credential = cls._parse_connection_string(connection_string)

        authentication_policy = policies.AzureKeyCredentialPolicy(credential, "x-ms-quantum-api-key")
        
        return cls(subscription_id, resource_group, workspace_name, None, None, location, credential, None, authentication_policy, **kwargs)

    def append_user_agent(self, value: Union[str, None]):
        """
        Append a new value to the Workspace's UserAgent and re-initialize the
        QuantumClient. The values are appended using a dash.

        :param value: UserAgent value to add, e.g. "azure-quantum-<plugin>"
        """
        new_user_agent = None

        if value is not None and value not in (self._user_agent or ""):
            new_user_agent = f"{self._user_agent}-{value}" if self._user_agent else value

        if new_user_agent != self._user_agent:
            self._user_agent = new_user_agent
            # We need to recreate the client for it to
            # pick the new UserAgent
            if self._client is not None:
                self._client = self._create_client()

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

    def _custom_headers(self):
        return {"x-ms-azurequantum-sdk-version": __version__}

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
        client = self._get_jobs_client()
        details = client.create(
            job.details.id, job.details
        )
        return Job(self, details)

    def cancel_job(self, job: Job) -> Job:
        client = self._get_jobs_client()
        client.cancel(job.details.id)
        details = client.get(job.id)
        return Job(self, details)

    def get_job(self, job_id: str) -> Job:
        """Returns the job corresponding to the given id."""
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
        """Returns list of jobs that meet optional (limited) filter criteria. 
            :param name_match: regex expression for job name matching
            :param status: filter by job status
            :param created_after: filter jobs after time of job creation
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

        :param provider_id: Optional provider Id to filter by, defaults to None
        :type provider_id: str, optional

        :return: Targets
        :rtype: Iterable[Target]
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
        :rtype: List[Dict[str, Any]]
        """
        client = self._get_quotas_client()
        return [q.as_dict() for q in client.list()]

    def list_top_level_items(
        self
    ) -> List[Union[Job, Session]]:
        """Get a list of top level items for the given workspace.

        :return: Workspace items
        :rtype: List[WorkspaceItem]
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
        :rtype: List[Session]
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
        :rtype: List[Job]
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
        :type job_id: str, optional
        :param container_name: Container name, defaults to None
        :type container_name: str, optional
        :param container_name_format: Container name format, defaults to "job-{job_id}"
        :type container_name_format: str, optional
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
