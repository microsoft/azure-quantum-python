# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import logging
import os

from azure.identity._constants import EnvironmentVariables
from azure.identity._internal import get_default_authority, normalize_authority
from azure.identity import (
    AzurePowerShellCredential,
    EnvironmentCredential,
    ManagedIdentityCredential,
    SharedTokenCacheCredential,
    AzureCliCredential,
    VisualStudioCodeCredential
)
from ._chained import _ChainedTokenCredential
from ._browser import _InteractiveBrowserCredential

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Any, List
    from azure.core.credentials import AccessToken, TokenCredential

_LOGGER = logging.getLogger(__name__)


class _DefaultAzureCredential(_ChainedTokenCredential):
    """
    Based on Azure.Identity.DefaultAzureCredential from:
    https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/identity/azure-identity/azure/identity/_credentials/default.py

    The two key differences are:
    1) Inherit from _ChainedTokenCredential, which has 
       more aggressive error handling than ChainedTokenCredential
    2) Use of the _InteractiveBrowserCredential which prints a warning message
       if tenant_id is not passed
    """

    def __init__(self, **kwargs):
        # type: (**Any) -> None
        authority = kwargs.pop("authority", None)
        authority = normalize_authority(authority) if authority else get_default_authority()

        interactive_browser_tenant_id = kwargs.pop(
            "interactive_browser_tenant_id", os.environ.get(EnvironmentVariables.AZURE_TENANT_ID)
        )

        managed_identity_client_id = kwargs.pop(
            "managed_identity_client_id", os.environ.get(EnvironmentVariables.AZURE_CLIENT_ID)
        )

        shared_cache_username = kwargs.pop("shared_cache_username", os.environ.get(EnvironmentVariables.AZURE_USERNAME))
        shared_cache_tenant_id = kwargs.pop(
            "shared_cache_tenant_id", os.environ.get(EnvironmentVariables.AZURE_TENANT_ID)
        )

        vscode_tenant_id = kwargs.pop(
            "visual_studio_code_tenant_id", os.environ.get(EnvironmentVariables.AZURE_TENANT_ID)
        )

        exclude_environment_credential = kwargs.pop("exclude_environment_credential", False)
        exclude_managed_identity_credential = kwargs.pop("exclude_managed_identity_credential", False)
        exclude_shared_token_cache_credential = kwargs.pop("exclude_shared_token_cache_credential", False)
        exclude_visual_studio_code_credential = kwargs.pop("exclude_visual_studio_code_credential", False)
        exclude_cli_credential = kwargs.pop("exclude_cli_credential", False)
        exclude_interactive_browser_credential = kwargs.pop("exclude_interactive_browser_credential", True)
        exclude_powershell_credential = kwargs.pop("exclude_powershell_credential", False)

        credentials = []  # type: List[TokenCredential]
        if not exclude_environment_credential:
            credentials.append(EnvironmentCredential(authority=authority, **kwargs))
        if not exclude_managed_identity_credential:
            credentials.append(ManagedIdentityCredential(client_id=managed_identity_client_id, **kwargs))
        if not exclude_shared_token_cache_credential and SharedTokenCacheCredential.supported():
            try:
                # username and/or tenant_id are only required when the cache contains tokens for multiple identities
                shared_cache = SharedTokenCacheCredential(
                    username=shared_cache_username, tenant_id=shared_cache_tenant_id, authority=authority, **kwargs
                )
                credentials.append(shared_cache)
            except Exception as ex:  # pylint:disable=broad-except
                _LOGGER.info("Shared token cache is unavailable: '%s'", ex)
        if not exclude_visual_studio_code_credential:
            credentials.append(VisualStudioCodeCredential(tenant_id=vscode_tenant_id))
        if not exclude_cli_credential:
            credentials.append(AzureCliCredential())
        if not exclude_powershell_credential:
            credentials.append(AzurePowerShellCredential())
        if not exclude_interactive_browser_credential:
            credentials.append(_InteractiveBrowserCredential(tenant_id=interactive_browser_tenant_id))

        super(_DefaultAzureCredential, self).__init__(*credentials)

    def get_token(self, *scopes, **kwargs):
        # type: (*str, **Any) -> AccessToken
        """Request an access token for `scopes`.
        This method is called automatically by Azure SDK clients.
        :param str scopes: desired scopes for the access token. This method requires at least one scope.
        :raises ~azure.core.exceptions.ClientAuthenticationError: authentication failed. The exception has a
          `message` attribute listing each authentication attempt and its error message.
        """
        if self._successful_credential:
            token = self._successful_credential.get_token(*scopes, **kwargs)
            _LOGGER.info(
                "%s acquired a token from %s", self.__class__.__name__, self._successful_credential.__class__.__name__
            )
            return token

        return super(_DefaultAzureCredential, self).get_token(*scopes, **kwargs)