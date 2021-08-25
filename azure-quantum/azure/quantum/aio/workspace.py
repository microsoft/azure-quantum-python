##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from datetime import datetime
import logging
import re

from typing import Iterable, List, Optional, Dict, Any, TYPE_CHECKING, Tuple, Union

from azure.quantum.aio._authentication._default import _DefaultAzureCredential
from azure.quantum._client.aio import QuantumClient
from azure.quantum._client.models import BlobDetails, JobStatus
from azure.quantum.aio.job import Job
from azure.quantum.aio.storage import create_container_using_client, get_container_uri, ContainerClient

from azure.quantum.workspace import BASE_URL, ARM_BASE_URL

if TYPE_CHECKING:
    from azure.quantum.aio.target import Target
    from azure.quantum._client.models import TargetStatus

logger = logging.getLogger(__name__)

DEFAULT_CONTAINER_NAME_FORMAT = "job-{job_id}"

__all__ = ["Workspace"]


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
        Normally one of the credential types from Azure.Identity (https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#credential-classes).

        Defaults to \"DefaultAzureCredential\", which will attempt multiple 
        forms of authentication.
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
                                                 subscription_id=subscription_id,
                                                 arm_base_url=ARM_BASE_URL)

        self.credentials = credential
        self.name = name
        self.resource_group = resource_group
        self.subscription_id = subscription_id
        self.storage = storage

        # Convert user-provided location into names
        # recognized by Azure resource manager.
        # For example, a customer-provided value of
        # "West US" should be converted to "westus".
        self.location = "".join(location.split()).lower()

        base_url = BASE_URL(self.location)
        logger.debug(
            f"Creating client for: subs:{self.subscription_id},"
            + f"rg={self.resource_group}, ws={self.name}, frontdoor={base_url}"
        )

        self._client = QuantumClient(
            credential=self.credentials,
            subscription_id=self.subscription_id,
            resource_group_name=self.resource_group,
            workspace_name=self.name,
            base_url=base_url,
        )

    async def _get_linked_storage_sas_uri(
        self, container_name: str, blob_name: str = None
    ) -> str:
        """
        Calls the service and returns a container sas url
        """
        blob_details = BlobDetails(
            container_name=container_name, blob_name=blob_name
        )
        container_uri = await self._client.storage.sas_uri(blob_details=blob_details)
        logger.debug(f"Container URI from service: {container_uri}")
        return container_uri.sas_uri

    async def submit_job(self, job: Job) -> Job:
        details = await self._client.jobs.create(
            job.details.id, job.details
        )
        return Job(self, details)

    async def cancel_job(self, job: Job) -> Job:
        await self._client.jobs.cancel(job.details.id)
        details = await self._client.jobs.get(job.id)
        return Job(self, details)

    async def get_job(self, job_id: str) -> Job:
        """Returns the job corresponding to the given id."""
        details = await self._client.jobs.get(job_id)
        return Job(self, details)

    async def list_jobs(
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
        jobs = self._client.jobs.list()

        result = []
        async for j in jobs:
            deserialized_job = Job(self, j)
            if deserialized_job.matches_filter(name_match, status, created_after):
                result.append(deserialized_job)
        return result
    
    async def _get_target_status(self, name: str, provider_id: str) -> List[Tuple[str, "TargetStatus"]]:
        """Get provider ID and status for targets"""
        return [
            (provider.id, target)
            async for provider in self._client.providers.get_status()
            for target in provider.targets
            if (provider_id is None or provider.id.lower() == provider_id.lower())
                and (name is None or target.id.lower() == name.lower())
        ]

    async def get_targets(
        self, 
        name: str = None, 
        provider_id: str = None,
        **kwargs
    ) -> Union["Target", Iterable["Target"]]:
        """Returns all available targets for this workspace filtered by name and provider ID.
        
        :param name: Optional target name to filter by, defaults to None
        :type name: str, optional
        :param provider_id: Optional provider Id to filter by, defaults to None
        :type provider_id: str, optional
        :return: Targets
        :rtype: Iterable[Target]
        """
        from azure.quantum.aio.target.target_factory import TargetFactory
        target_factory = TargetFactory()
        return await target_factory.get_targets(
            workspace=self,
            name=name,
            provider_id=provider_id
        )

    async def get_quotas(self) -> List[Dict[str, Any]]:
        """Get a list of job quotas for the given workspace.

        :return: Job quotas
        :rtype: List[Dict[str, Any]]
        """
        return [q.as_dict() async for q in self._client.quotas.list()]

    async def get_container_uri(
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
            container_uri = await self._get_linked_storage_sas_uri(
                container_name
            )
            container_client = ContainerClient.from_container_url(
                container_uri
            )
            await create_container_using_client(container_client)
        else:
            # Use the storage acount specified to generate container URI,
            # create a new container if it does not yet exist
            container_uri = await get_container_uri(
                self.storage, container_name
            )
        return container_uri
