# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from __future__ import annotations
import logging
import sys
from typing import Any, Optional
from azure.core.exceptions import ClientAuthenticationError
from azure.core.credentials import AccessToken, TokenCredential
from azure.identity import (
    CredentialUnavailableError,
    _internal as AzureIdentityInternals,
)

_LOGGER = logging.getLogger(__name__)


def filter_credential_warnings(record) -> bool:
    """Suppress warnings from credentials other than DefaultAzureCredential"""
    if record.levelno == logging.WARNING:
        message = record.getMessage()
        return "DefaultAzureCredential" in message
    return True


def _get_error_message(history) -> str:
    attempts = []
    for credential, error in history:
        if error:
            attempts.append(f"{credential.__class__.__name__}: {error}")
        else:
            attempts.append(credential.__class__.__name__)
    return """
Attempted credentials:\n\t{}""".format(
        "\n\t".join(attempts)
    )


class _ChainedTokenCredential():
    """
    Based on Azure.Identity.ChainedTokenCredential from:
    https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/identity/azure-identity/azure/identity/_credentials/chained.py

    The key difference is that we don't stop attempting all credentials
    if some of then failed or raised an exception.
    We also don't log a warning unless all credential attempts have failed.
    """

    def __init__(self, *credentials: TokenCredential) -> None:
        self._successful_credential: TokenCredential = None
        self.credentials = credentials

    def __enter__(self) -> _ChainedTokenCredential:
        for credential in self.credentials:
            credential.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        for credential in self.credentials:
            credential.__exit__(*args)

    def close(self) -> None:
        """Close the transport session of each credential in the chain."""
        self.__exit__()

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        **kwargs: Any
    ) -> AccessToken:
        """
        Request a token from each chained credential, in order,
        returning the first token received.

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
            no credential in the chain provided a token
        """
        history = []
        AzureIdentityInternals.within_credential_chain.set(True)
        # Suppress warnings from credentials in Azure.Identity
        azure_identity_logger = logging.getLogger("azure.identity")
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.addFilter(filter_credential_warnings)
        azure_identity_logger.addHandler(handler)
        try:
            for credential in self.credentials:
                try:
                    token = credential.get_token(
                        *scopes,
                        claims=claims,
                        tenant_id=tenant_id,
                        **kwargs)
                    _LOGGER.info(
                        "%s acquired a token from %s",
                        self.__class__.__name__,
                        credential.__class__.__name__
                    )
                    self._successful_credential = credential
                    AzureIdentityInternals.within_credential_chain.set(False)
                    return token
                except CredentialUnavailableError as ex:
                    # credential didn't attempt authentication
                    # because it lacks required data or state -> continue
                    history.append((credential, ex.message))
                    _LOGGER.info(
                        "%s - %s is unavailable",
                        self.__class__.__name__,
                        credential.__class__.__name__,
                    )
                except Exception as ex:  # pylint: disable=broad-except
                    # instead of logging a warning, we just want to log an info
                    # since other credentials might succeed
                    history.append((credential, str(ex)))
                    _LOGGER.info(
                        '%s.get_token failed: %s raised unexpected error "%s"',
                        self.__class__.__name__,
                        credential.__class__.__name__,
                        ex,
                        exc_info=_LOGGER.isEnabledFor(logging.DEBUG),
                    )
                    # here we do NOT want break and
                    # will continue to try other credentials
        finally:
            AzureIdentityInternals.within_credential_chain.set(False)
            # Re-enable warnings from credentials in Azure.Identity
            azure_identity_logger.removeHandler(handler)

        # if all attempts failed, only then we log a warning and raise an error
        attempts = _get_error_message(history)
        message = (
            self.__class__.__name__
            + " failed to retrieve a token from the included credentials."
            + attempts
            + "\nTo mitigate this issue, please refer to the troubleshooting guidelines here at "
            "https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot."
        )
        _LOGGER.warning(message)
        raise ClientAuthenticationError(message=message)
