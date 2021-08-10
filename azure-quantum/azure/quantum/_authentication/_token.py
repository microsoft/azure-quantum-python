##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import json
from json.decoder import JSONDecodeError
import logging
import os
import time

from azure.identity import CredentialUnavailableError
from azure.core.credentials import AccessToken

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    # pylint:disable=unused-import,ungrouped-imports
    from typing import Any, Optional
    from azure.core.credentials import AccessToken

_LOGGER = logging.getLogger(__name__)

_TOKEN_FILE_ENV_VARIABLE="AZUREQUANTUM_TOKEN_FILE"
_AZURE_QUANTUM_SCOPE = "https://quantum.microsoft.com/.default"


class _AzureQuantumTokenCredential(object):
    """
    Implements a custom TokenCredential to use a local file as the source for an AzureQuantum token.

    It will only use the local file if the AZUREQUANTUM_TOKEN_FILE environment variable is set, and references
    an existing json file that contains the access_token and expires_on timestamp in milliseconds.

    If the environment variable is not set, the file does not exist, or the token is invalid in any way (expired, for example),
    then the credential will throw CredentialUnavailableError, so that _ChainedTokenCredential can fallback to other methods.
    """
    def __init__(self, **kwargs):
        # type: (**Any) -> None
        self.token_file = os.environ.get(_TOKEN_FILE_ENV_VARIABLE)
        if self.token_file:
            _LOGGER.debug("Using provided token file location: {}".format(self.token_file))
        else:
            _LOGGER.debug("No token file location provided for {} environment variable.".format(_TOKEN_FILE_ENV_VARIABLE))

    def get_token(self, *scopes, **kwargs):  # pylint:disable=unused-argument
        # type: (*str, **Any) -> AccessToken
        """Request an access token for `scopes`.
        This method is called automatically by Azure SDK clients.
        :param str scopes: desired scopes for the access token. This method only returns tokens for the https://quantum.microsoft.com/.default scope.
        :raises ~azure.identity.CredentialUnavailableError: when failing to get token. The exception has a
          `message` attribute with the error message.
        """
        if scopes != (_AZURE_QUANTUM_SCOPE,):
            raise CredentialUnavailableError(message="AzureQuantumTokenCredential only supports {} scope.".format(_AZURE_QUANTUM_SCOPE))

        if not self.token_file:
            raise CredentialUnavailableError(message="Token file location not set.")

        if not os.path.isfile(self.token_file):
            raise CredentialUnavailableError(message="Token file at {} does not exist.".format(self.token_file))

        try:
            token = self._parse_token_file(self.token_file)
        except JSONDecodeError:
            raise CredentialUnavailableError(message="Failed to parse token file: Invalid JSON.")
        except KeyError as e:
            raise CredentialUnavailableError(message="Failed to parse token file: Missing expected value: " + str(e))
        except Exception as e:
            raise CredentialUnavailableError(message="Failed to parse token file: " + str(e))

        if token.expires_on <= time.time():
            raise CredentialUnavailableError(message="Token already expired at {}".format(time.asctime(time.localtime(token.expires_on))))

        return token
    
    def _parse_token_file(self, path):
        # type: (*str) -> AccessToken
                
        with open(path, "r") as file:
            data = json.load(file)
            expires_on = int(data["expires_on"]) / 1000 # Convert ms to seconds, since python time.time only handles epoch time in seconds
            token = AccessToken(data["access_token"],  expires_on)

        return token