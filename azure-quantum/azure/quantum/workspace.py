##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import json
import logging
import msal
import os
import re
import sys
import time
import requests

from azure.storage.blob import ContainerClient
from pathlib import Path
from typing import List, Optional

from msrest.authentication import Authentication, BasicTokenAuthentication
from azure.quantum._client import QuantumClient
from azure.quantum._client.operations import JobsOperations, StorageOperations
from azure.quantum._client.models import BlobDetails
from azure.quantum import Job
try:
    from .version import __version__
except:
    __version__ = "<unknown>"

logger = logging.getLogger(__name__)

__all__ = ['Workspace']

def sdk_environment(name):
    return 'AZURE_QUANTUM_ENV' in os.environ and os.environ['AZURE_QUANTUM_ENV'] == name

## Settings based on environment variables:
BASE_URL_FROM_ENV = os.environ['AZURE_QUANTUM_BASEURL'] if 'AZURE_QUANTUM_BASEURL' in os.environ else None
if  sdk_environment('dogfood'):
    logger.info("Using DOGFOOD configuration.")
    BASE_URL                = lambda location: BASE_URL_FROM_ENV or f"https://{location}.quantum-test.azure.com/"
    ARM_BASE_URL            = "https://api-dogfood.resources.windows-int.net/"
    AAD_CLIENT_ID           = "46a998aa-43d0-4281-9cbb-5709a507ac36" # Microsoft Quantum Development Kit
    AAD_SCOPES              = [ "api://dogfood.azure-quantum/Jobs.ReadWrite" ]

else:
    if sdk_environment('canary'):
        logger.info("Using CANARY configuration.")
        BASE_URL                = lambda location: BASE_URL_FROM_ENV or f"https://eastus2euap.quantum.azure.com/"
    else:
        logger.debug("Using production configuration.")
        BASE_URL                = lambda location: BASE_URL_FROM_ENV or f"https://{location}.quantum.azure.com/"
    ARM_BASE_URL            = "https://management.azure.com/"
    AAD_CLIENT_ID           = "84ba0947-6c53-4dd2-9ca9-b3694761521b" # Microsoft Quantum Development Kit
    AAD_SCOPES              = [ "https://quantum.microsoft.com/Jobs.ReadWrite" ]

TOKEN_CACHE = os.environ['AZURE_QUANTUM_TOKEN_CACHE'] if 'AZURE_QUANTUM_TOKEN_CACHE' in os.environ else os.path.join(Path.home(), ".azure-quantum", "aad.bin")

# Keeps track of the account name the current token is associated, so we only show
# a log message about acquiring a new token if the account changes.
_last_account = None

# Caches the MSAL Apps based on the subscription id
_msal_apps = {}

class TokenCacheWrapper:
    def __init__(self):
        self.cache_path  = TOKEN_CACHE
        self.initialize_cache()

    def initialize_cache(self):
        logger.debug(f"Using path '{self.cache_path}' for AAD token cache")

        self.token_cache = msal.SerializableTokenCache()
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as cache:
                self.token_cache.deserialize(cache.read())

    def write_out_cache(self):
        logger.debug(f"Updating AAD token cache at '{self.cache_path}'")

        cache_folder = os.path.dirname(self.cache_path)
        if not os.path.isdir(cache_folder):
            os.makedirs(cache_folder)

        with open(self.cache_path, "w") as afile:
            afile.write(self.token_cache.serialize())

class MsalWrapper:
    def __init__(self, subscription_id: str, refresh: bool):
        self.subscription_id     = subscription_id
        self.refresh             = refresh
        self.client_id           = AAD_CLIENT_ID
        self.scopes              = AAD_SCOPES
        self.token_cache_wrapper = TokenCacheWrapper()

    def get_tenant_authorization_uri(self):
        try:
            uri = f"{ARM_BASE_URL}/subscriptions/{self.subscription_id}?api-version=2018-01-01"
            response = requests.get(uri)

            # This gnarly piece of code is how we get the guest tenant authority associated with the subscription.
            # We make a unauthenticated request to ARM and extract the tenant authority from the WWW-Authenticate header in the response.
            # The header is of the form - Bearer authoritization_uri=https://login.microsoftonline.com/tenantId, key1=value1 
            auth_header = response.headers["WWW-Authenticate"]
            logger.debug (f"got the following auth header from the management endpoint: {auth_header}")

            trimmed_auth_header = auth_header[len("Bearer "):]                                  # trim the leading 'Bearer '
            trimmed_auth_header_parts = trimmed_auth_header.split(",")                            # get the various k=v parts
            key_value_pairs = dict(map(lambda s: tuple(s.split("=")), trimmed_auth_header_parts)) # make the parts into a dictionary
            quoted_tenant_uri = key_value_pairs["authorization_uri"]                             # get the value of the 'authorization_uri' key
            tenant_uri = quoted_tenant_uri[1:-1]                                                # strip it of surrounding quotes

            logger.debug (f"got the following tenant uri from the authentication header: {tenant_uri}")

            return tenant_uri

        except Exception as e:
            logger.debug(f"Failed to get tenant authority for subscription: {e}")
            return None

    def get_app(self):
        if not self.subscription_id in _msal_apps:
            authority = self.get_tenant_authorization_uri()
            if(authority == None):
                raise ValueError(f"Failed to get tenant authority for subscription '{self.subscription_id}'. Make sure the subscription id is correct.")

            try:
                _msal_apps[self.subscription_id] = msal.PublicClientApplication(
                    self.client_id,
                    authority   = authority,
                    token_cache = self.token_cache_wrapper.token_cache)
                logger.debug (f"Created a new app with the authority: {authority}")
            except Exception as e:
                 raise ValueError(f"Failed to create PublicClientApplication with tenant authority: {e}")
        return _msal_apps[self.subscription_id]

    def clear_accounts(self):
        accounts = self.get_app().get_accounts()
        for account in accounts:
            self.get_app().remove_account(account)

    def get_token_from_device_flow(self):
        # Clear accounts before doing device flow to make sure that we are left with a single account after the user completes the device flow.
        # We use that account is subsequent silent token acquisitions.
        self.clear_accounts()

        flow = self.get_app().initiate_device_flow(scopes=self.scopes)
        if "user_code" not in flow:
            raise ValueError("Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

        # Print a message for users to login via browser
        print(flow["message"])
        sys.stdout.flush()  # Some terminal needs this to ensure the message is shown

        result = self.get_app().acquire_token_by_device_flow(flow)  # Block until user has logged in and we're ready to continue:

        return result

    def try_get_token_silently(self):
        def try_get_account_from_app(app):
            accounts = app.get_accounts()
            if len(accounts) > 0:
                return accounts[0]
            else:
                return None

        account = try_get_account_from_app(self.get_app())

        if not account:
            return None

        # extract the tenant id from the home_account_id. The home_account_id is of the form "<oid>.<tenantId>"
        if "home_account_id" not in account:
            logger.debug("No home_account_id in account")
        
        tid = None
        account_parts = account["home_account_id"].split(".")
        if len(account_parts) < 2:
            logger.debug("No tenantId in account")
        else:
            tid = account_parts[1]

        global _last_account
        if _last_account != account['username']:
            _last_account = account['username']
            logger.info(f"Account(s) exists in aad token cache. Getting token for (userName: {account['username']}, tenantId: {tid})")

        return self.get_app().acquire_token_silent(self.scopes, account)

    def acquire_auth_token(self):
        """Returns an AAD token, either from a local cache or from AAD.

        It will first try to retrieve the token from a local cache
        (the location of the cache can be specified via the AZURE_QUANTUM_TOKEN_CACHE environent variable).
        If it the cache is empty or expired, then it uses the device token flow from MSAL (https://github.com/AzureAD/microsoft-authentication-library-for-python)
        to acquire the token from AAD.

        Once a token is received, it is inspected to see if it is a token for an MSA account.
        If so, the guest tenant id for that account is acquired, and a token is reaquired with that authority.

        If successful, it stores the acquired token in the cache for future calls.

        :param refresh:
            if true, by-passes the cache and fetches a fresh token from AAD.
        """
        result = None

        if self.refresh:
            logger.debug("Refresh forced. Skipping getting token from cache...")
            self.clear_accounts()
        else:
            logger.debug("Trying to get token from cache...")
            result = self.try_get_token_silently()

        if not result:
            logger.debug("...and trying to get a token from the device flow...")
            result = self.get_token_from_device_flow()
            logger.debug(f"...device flow returned: {result}")

        # At this point, there should be an access token; raise otherwise:
        if result and ("access_token" in result):
            logger.debug(f"Token:\n{result['access_token']}")

            # Store token back in cache:
            self.token_cache_wrapper.write_out_cache()
            return result
        else:
            raise ValueError("Failed to acquire AAD token.")

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
        The Azure storage account connection string. Required only if the specified Azure Quantum
        workspace does not have linked storage.
        
    :param resource_id:
        The resource ID of the Azure Quantum workspace.
        
    :param location:
        The Azure region where the Azure Quantum workspace is provisioned.
        This may be specified as a region name such as \"East US\" or a location name such as \"eastus\".
        If no valid value is specified, defaults to \"westus\".
    """
    credentials = None

    def __init__(
        self,
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        name: Optional[str] = None,
        storage: Optional[str] = None,
        resource_id: Optional[str] = None,
        location: Optional[str] = None
    ):

        if resource_id is not None:
            # A valid resource ID looks like:
            # /subscriptions/f846b2bd-d0e2-4a1d-8141-4c6944a9d387/resourceGroups/RESOURCE_GROUP_NAME/providers/Microsoft.Quantum/Workspaces/WORKSPACE_NAME
            regex = r'^/subscriptions/([a-fA-F0-9-]*)/resourceGroups/([^\s/]*)/providers/Microsoft\.Quantum/Workspaces/([^\s/]*)$'
            match = re.search(regex, resource_id, re.IGNORECASE)
            if match:
                # match should contain four groups:
                # -> match.group(0): The full resource ID for the Azure Quantum workspace
                # -> match.group(1): The Azure subscription ID
                # -> match.group(2): The Azure resource group name
                # -> match.group(3): The Azure Quantum workspace name
                subscription_id = match.group(1)
                resource_group = match.group(2)
                name = match.group(3)

        if not subscription_id or not resource_group or not name:
            raise ValueError(
                "Azure Quantum workspace not fully specified. Please specify either a valid resource ID " +
                "or a valid combination of subscription ID, resource group name, and workspace name.")

        self.name = name
        self.resource_group = resource_group
        self.subscription_id = subscription_id
        self.storage = storage

        # Convert user-provided location into names recognized by Azure resource manager.
        # For example, a customer-provided value of "West US" should be converted to "westus".
        self.location = "".join(location.split()).lower() if location and location.split() else "westus"

    def _create_client(self) -> QuantumClient:
        auth = self.login()
        base_url = BASE_URL(self.location)
        logger.debug(f"Creating client for: subs:{self.subscription_id}, rg={self.resource_group}, ws={self.name}, frontdoor={base_url}")
        client = QuantumClient(auth, self.subscription_id, self.resource_group, self.name, base_url)
        return client

    def _create_jobs_client(self) -> JobsOperations:
        client = self._create_client().jobs
        return client

    def _create_workspace_storage_client(self) -> StorageOperations:
        client = self._create_client().storage
        return client

    def _custom_headers(self):
        return {
            'x-ms-azurequantum-sdk-version': __version__
        }

    def _get_linked_storage_sas_uri(self, container_name: str, blob_name: str=None) -> str:
        """
        Calls the service and returns a container sas url
        """
        client = self._create_workspace_storage_client()
        blob_details = BlobDetails(container_name=container_name, blob_name=blob_name)
        container_uri = client.sas_uri(blob_details=blob_details)

        logger.debug(f"Container URI from service: {container_uri}")
        return container_uri.sas_uri

    def submit_job(self, job: Job) -> Job:
        client = self._create_jobs_client()
        details = client.create(job.details.id, job.details, custom_headers=self._custom_headers())
        return Job(self, details)

    def cancel_job(self, job: Job) -> Job:
        client = self._create_jobs_client()
        client.cancel(job.details.id, custom_headers=self._custom_headers())
        details = client.get(job.id, custom_headers=self._custom_headers())
        return Job(self, details)

    def get_job(self, job_id: str) -> Job:
        """Returns the job corresponding to the given id."""
        client = self._create_jobs_client()
        details = client.get(job_id, custom_headers=self._custom_headers())
        return Job(self, details)

    def list_jobs(self) -> List[Job]:
        client = self._create_jobs_client()
        jobs = client.list(custom_headers=self._custom_headers())

        result = []
        for j in jobs:
            result.append(Job(self, j))

        return result

    def login(self, refresh:bool=False) -> Authentication:
        """Creates user credentials to authenticate with Azure Quantum

        It will first try to read the credentials from a secure local cache
        (the location of the cache can be specified via the AZURE_QUANTUM_TOKEN_CACHE environent variable).
        If it the cache is empty or expired, then it uses the device token flow from MSAL (https://github.com/AzureAD/microsoft-authentication-library-for-python)
        to acquire a token from AAD.

        If successful, it stores the acquired token in the cache for future calls.

        :param refresh:
            if true, by-passes the cache and fetches a fresh token from AAD.

        :returns:
            the user credentials to authenticate with Azure Quantum
        """

        # We only clear the credentials if they are of type BasicTokenAuthentication
        if refresh and isinstance(self.credentials, BasicTokenAuthentication):
            self.credentials = None

        if self.credentials is None:
            msal_wrapper = MsalWrapper(subscription_id=self.subscription_id, refresh=refresh)

            auth_token = msal_wrapper.acquire_auth_token()
            return BasicTokenAuthentication(token=auth_token)

        # When we already have an object of type Authentication, like
        # the ServicePrincipalCredentials, we should NOT wrap it in a BasicTokenAuthentication
        if not isinstance(self.credentials, Authentication):
            return BasicTokenAuthentication(token=self.credentials)


        return self.credentials
