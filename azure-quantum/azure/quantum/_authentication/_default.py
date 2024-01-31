# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import logging
import re
from typing import Optional
import urllib3
from azure.identity._internal import get_default_authority, normalize_authority
from azure.identity import (
    AzurePowerShellCredential,
    EnvironmentCredential,
    ManagedIdentityCredential,
    AzureCliCredential,
    VisualStudioCodeCredential,
    InteractiveBrowserCredential,
    DeviceCodeCredential,
)
from ._chained import _ChainedTokenCredential
from ._token import _TokenFileCredential

_LOGGER = logging.getLogger(__name__)
MSA_TENANT_ID = "9188040d-6c67-4c5b-b112-36a304b66dad"
WWW_AUTHENTICATE_REGEX = re.compile(
    r"""
        ^
        Bearer\sauthorization_uri="
            https://(?P<authority>[^/]*)/
            (?P<tenant_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})
        "
    """,
    re.VERBOSE | re.IGNORECASE)
WWW_AUTHENTICATE_HEADER_NAME = "WWW-Authenticate"


class _DefaultAzureCredential(_ChainedTokenCredential):
    """
    Based on Azure.Identity.DefaultAzureCredential from:
    https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/identity/azure-identity/azure/identity/_credentials/default.py

    The three key differences are:
    1) Inherit from _ChainedTokenCredential, which has 
       more aggressive error handling than ChainedTokenCredential
    2) Instantiate the internal credentials the first time the get_token gets called
       such that we can get the tenant_id if it was not passed by the user (but we don't
       want to do that in the constructor).
       We automatically identify the user's tenant_id for a given subscription 
       so that users with MSA accounts don't need to pass it.
       This is a mitigation for bug https://github.com/Azure/azure-sdk-for-python/issues/18975
       We need the following parameters to enable auto-detection of tenant_id
       - subscription_id
       - arm_base_url (defaults to the production url "https://management.azure.com/")
    3) Add custom TokenFileCredential as first method to attempt, which will look for a local access token.
    """
    def __init__(
        self,
        arm_base_url: str,
        subscription_id: str,
        client_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        authority: Optional[str] = None,
    ):
        if arm_base_url is None:
            raise ValueError("arm_base_url is mandatory parameter")
        if subscription_id is None:
            raise ValueError("subscription_id is mandatory parameter")
        self.authority = normalize_authority(authority) if authority else authority
        self.tenant_id = tenant_id
        self.subscription_id = subscription_id
        self.arm_base_url = arm_base_url
        self.client_id = client_id
        # credentials will be created lazy on the first call to get_token
        super(_DefaultAzureCredential, self).__init__()

    def _initialize_credentials(self):
        self._update_authority_and_tenant_id_(
            arm_base_url=self.arm_base_url,
            subscription_id=self.subscription_id)
        credentials = []
        credentials.append(_TokenFileCredential())
        credentials.append(EnvironmentCredential())
        if self.client_id:
            credentials.append(ManagedIdentityCredential(client_id=self.client_id))
        if self.authority and self.tenant_id:
            credentials.append(VisualStudioCodeCredential(authority=self.authority, tenant_id=self.tenant_id))
            credentials.append(AzureCliCredential(tenant_id=self.tenant_id))
            credentials.append(AzurePowerShellCredential(tenant_id=self.tenant_id))
            credentials.append(InteractiveBrowserCredential(authority=self.authority, tenant_id=self.tenant_id))
            if self.client_id:
                credentials.append(DeviceCodeCredential(authority=self.authority, client_id=self.client_id, tenant_id=self.tenant_id))
        self.credentials = credentials

    def get_token(self, *scopes, **kwargs):
        """Request an access token for `scopes`.
        This method is called automatically by Azure SDK clients.
        :param str scopes: desired scopes for the access token. This method requires at least one scope.
        :raises ~azure.core.exceptions.ClientAuthenticationError: authentication failed. The exception has a
          `message` attribute listing each authentication attempt and its error message.
        """
        # lazy-initialize the credentials
        if self.credentials is None or len(self.credentials) == 0:
            self._initialize_credentials()

        return super(_DefaultAzureCredential, self).get_token(*scopes, **kwargs)

    def _update_authority_and_tenant_id_(self, arm_base_url:str, subscription_id:str):
        """
        If the authority or tenant_id were not given, try to obtain them
        by calling the management endpoint for the subscription_id,
        or by applying default values.
        """
        if self.tenant_id and self.authority:
            return

        try:
            url = (
                f"{arm_base_url.rstrip('/')}/subscriptions/"
                + f"{subscription_id}?api-version=2018-01-01"
            )
            http = urllib3.PoolManager()
            response = http.request(
                method="GET",
                url=url,
            )
            if WWW_AUTHENTICATE_HEADER_NAME in response.headers:
                www_authenticate = response.headers[WWW_AUTHENTICATE_HEADER_NAME]
                match = re.search(WWW_AUTHENTICATE_REGEX, www_authenticate)
                if match:
                    self.tenant_id = match.group("tenant_id")
                    self.authority = match.group("authority")
        # pylint: disable=broad-exception-caught
        except Exception as ex:
            _LOGGER.error(ex)

        # apply default values
        self.tenant_id = self.tenant_id or MSA_TENANT_ID
        self.authority = self.authority or get_default_authority()
