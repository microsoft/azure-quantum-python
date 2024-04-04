# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import logging
import re
import os
from typing import (
    Optional,
    List,
    Any,
)
import urllib3
from azure.core.credentials import (
    AccessToken,
    TokenCredential,
)
from azure.identity import (
    AzurePowerShellCredential,
    EnvironmentCredential,
    ManagedIdentityCredential,
    AzureCliCredential,
    VisualStudioCodeCredential,
    InteractiveBrowserCredential,
    DeviceCodeCredential,
    AzureDeveloperCliCredential,
    _internal as AzureIdentityInternals,
)
from azure.identity._constants import (
    EnvironmentVariables as SdkEnvironmentVariables,
    DEVELOPER_SIGN_ON_CLIENT_ID,
)
from azure.quantum._constants import (
    ConnectionConstants,
    EnvironmentVariables,
)
from ._chained import _ChainedTokenCredential
from ._token import _TokenFileCredential

_LOGGER = logging.getLogger(__name__)
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
       more graceful error handling than ChainedTokenCredential.
    2) Instantiate the internal credentials the first time the get_token gets called
       such that we can get the tenant_id if it was not passed by the user (but we don't
       want to do that in the constructor).
       We automatically identify the user's tenant_id for a given subscription 
       so that users with MSA accounts don't need to pass it.
       This is a mitigation for bug https://github.com/Azure/azure-sdk-for-python/issues/18975
       We need the following parameters to enable auto-detection of tenant_id
       - subscription_id
       - arm_endpoint (defaults to the production url "https://management.azure.com/")
    3) Add custom TokenFileCredential as first method to attempt,
       which will look for a local access token.
    """
    def __init__(
        self,
        arm_endpoint: str,
        subscription_id: str,
        client_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        authority: Optional[str] = None,
    ) -> None:
        if arm_endpoint is None:
            raise ValueError("arm_endpoint is mandatory parameter")
        if subscription_id is None:
            raise ValueError("subscription_id is mandatory parameter")

        self.authority = self._authority_or_default(
            authority=authority,
            arm_endpoint=arm_endpoint)
        self.tenant_id = tenant_id or os.environ.get(EnvironmentVariables.AZURE_TENANT_ID)
        self.subscription_id = subscription_id
        self.arm_endpoint = arm_endpoint
        self.client_id = client_id or os.environ.get(EnvironmentVariables.AZURE_CLIENT_ID)
        # credentials will be created lazy on the first call to get_token
        super().__init__()

    def _authority_or_default(self, authority: str, arm_endpoint: str) -> str:
        if authority:
            return AzureIdentityInternals.normalize_authority(authority)
        if arm_endpoint == ConnectionConstants.ARM_DOGFOOD_ENDPOINT:
            return ConnectionConstants.DOGFOOD_AUTHORITY
        return ConnectionConstants.AUTHORITY

    def _initialize_credentials(self) -> None:
        self._discover_tenant_id_(
            arm_endpoint=self.arm_endpoint,
            subscription_id=self.subscription_id)

        credentials: List[TokenCredential] = []

        common_args = {
            "_within_dac": True
        }

        credentials.append(_TokenFileCredential())

        env_cred_args = dict(common_args)
        if not SdkEnvironmentVariables.AZURE_AUTHORITY_HOST in os.environ:
            env_cred_args["authority"] = self.authority
        credentials.append(EnvironmentCredential(**env_cred_args))

        managed_identity_args = dict(common_args)
        if self.client_id:
            managed_identity_args["client_id"] = self.client_id
        credentials.append(ManagedIdentityCredential(**managed_identity_args))

        vscode_args = dict(common_args)
        if self.authority:
            vscode_args["authority"] = self.authority
        if self.tenant_id:
            vscode_args["tenant_id"] = self.tenant_id
        credentials.append(VisualStudioCodeCredential(**vscode_args))

        cli_args = {}
        if self.tenant_id:
            cli_args["tenant_id"] = self.tenant_id
        credentials.append(AzureCliCredential(**cli_args))
        credentials.append(AzurePowerShellCredential(**cli_args))
        credentials.append(AzureDeveloperCliCredential(**cli_args))

        browser_args = dict(common_args)
        if self.tenant_id:
            browser_args["tenant_id"] = self.tenant_id
        if self.client_id:
            browser_args["client_id"] = self.client_id
        credentials.append(InteractiveBrowserCredential(**browser_args))

        device_code_args = dict(common_args)
        device_code_args["client_id"] = self.client_id or DEVELOPER_SIGN_ON_CLIENT_ID
        if self.tenant_id:
            device_code_args["tenant_id"] = self.tenant_id
        credentials.append(DeviceCodeCredential(**device_code_args))

        self.credentials = credentials

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        **kwargs: Any
    ) -> AccessToken:
        """Request an access token for `scopes`.

        This method is called automatically by Azure SDK clients.

        :param str scopes: desired scopes for the access token.
            This method requires at least one scope.
            For more information about scopes, see
            https://learn.microsoft.com/azure/active-directory/develop/scopes-oidc.
        :keyword str claims: additional claims required in the token,
            such as those returned in a resource provider's
            claims challenge following an authorization failure.
        :keyword str tenant_id: optional tenant to include in the token request.

        :return: An access token with the desired scopes.
        :rtype: ~azure.core.credentials.AccessToken

        :raises ~azure.core.exceptions.ClientAuthenticationError: 
            authentication failed. The exception has a `message` attribute
            listing each authentication attempt and its error message.
        """
        # lazy-initialize the credentials
        if self.credentials is None or len(self.credentials) == 0:
            self._initialize_credentials()

        if self._successful_credential:
            token = self._successful_credential.get_token(
                *scopes,
                claims=claims,
                tenant_id=tenant_id,
                **kwargs
            )
            _LOGGER.info(
                "%s acquired a token from %s",
                self.__class__.__name__,
                self._successful_credential.__class__.__name__
            )
            return token
        AzureIdentityInternals.within_dac.set(True)
        token = super().get_token(
            *scopes,
            claims=claims,
            tenant_id=tenant_id,
            **kwargs
        )
        AzureIdentityInternals.within_dac.set(False)
        return token

    def _discover_tenant_id_(self, arm_endpoint:str, subscription_id:str):
        """
        If the tenant_id was not given, try to obtain it
        by calling the management endpoint for the subscription_id,
        or by applying default values.
        """
        if self.tenant_id:
            return

        try:
            url = (
                f"{arm_endpoint.rstrip('/')}/subscriptions/"
                + f"{subscription_id}?api-version=2018-01-01"
                + "&discover-tenant-id"  # used by the test recording infrastructure
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
        # pylint: disable=broad-exception-caught
        except Exception as ex:
            _LOGGER.error(ex)

        # apply default values
        self.tenant_id = self.tenant_id or ConnectionConstants.MSA_TENANT_ID
