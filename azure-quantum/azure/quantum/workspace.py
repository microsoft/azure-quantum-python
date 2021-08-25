##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from datetime import datetime
import logging
import os
import re

from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING, Tuple, Union
from functools import reduce
from deprecated import deprecated

# Temporarily replacing the DefaultAzureCredential with
# a custom _DefaultAzureCredential
#   from azure.identity import DefaultAzureCredential
from azure.quantum._authentication import _DefaultAzureCredential

from azure.quantum._client import QuantumClient
from azure.quantum._client.operations import (
    JobsOperations,
    StorageOperations,
    QuotasOperations
)
from azure.quantum._client.models import BlobDetails, JobStatus
from azure.quantum import Job
from azure.quantum.storage import create_container_using_client, get_container_uri, ContainerClient

from .version import __version__

if TYPE_CHECKING:
    from azure.quantum._client.models import TargetStatus
    from azure.quantum.target import Target

logger = logging.getLogger(__name__)

__all__ = ["Workspace"]

DEFAULT_CONTAINER_NAME_FORMAT = "job-{job_id}"


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
        Normally one of the credential types from Azure.Identity (https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#credential-classes).

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
        self.user_agent = user_agent

        if self.user_agent == None:
            self.user_agent = os.environ.get("AZURE_QUANTUM_PYTHON_APPID")

        # Convert user-provided location into names
        # recognized by Azure resource manager.
        # For example, a customer-provided value of
        # "West US" should be converted to "westus".
        self.location = "".join(location.split()).lower()

        # Create QuantumClient
        self._client = self._create_client()

    def _create_client(self) -> QuantumClient:
        base_url = BASE_URL(self.location)
        logger.debug(
            f"Creating client for: subs:{self.subscription_id},"
            + f"rg={self.resource_group}, ws={self.name}, frontdoor={base_url}"
        )

        client = QuantumClient(
            credential=self.credentials,
            subscription_id=self.subscription_id,
            resource_group_name=self.resource_group,
            workspace_name=self.name,
            base_url=base_url,
            user_agent=self.user_agent
        )
        return client

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
        client = self._get_jobs_client()
        details = client.get(job_id)
        return Job(self, details)

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
        
        :param name: Optional target name to filter by, defaults to None
        :type name: str, optional
        :param provider_id: Optional provider Id to filter by, defaults to None
        :type provider_id: str, optional
        :return: Targets
        :rtype: Iterable[Target]
        """
        from azure.quantum.target.target_factory import TargetFactory
        target_factory = TargetFactory()
        return target_factory.get_targets(
            workspace=self,
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

    @deprecated(version='0.17.2105', reason="This method is deprecated and no longer necessary to be called")
    def login(self, refresh: bool = False) -> object:
        """DEPRECATED. 
        This method is deprecated and no longer necessary to be called.
        It will simply return self.credentials.

        :param refresh:
            the refresh parameter has no effect and is ignored

        :returns:
            the self.credentials
        """
        return self.credentials
    
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
