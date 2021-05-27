# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import logging

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import InteractiveBrowserCredential

_LOGGER = logging.getLogger(__name__)

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    # pylint:disable=unused-import
    from typing import Any


class _InteractiveBrowserCredential(InteractiveBrowserCredential):
    """
    Based on InteractiveBrowserCredential from:
    https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/identity/azure-identity/azure/identity/_credentials/browser.py

    We inherit from InteractiveBrowserCredential and display a warning if the 
    user has not specified a tenant_id and an authentication attempt is made.
    """

    def __init__(self, **kwargs):
        super(_InteractiveBrowserCredential, self).__init__(**kwargs)

    def get_token(self, *scopes, **kwargs):  # pylint:disable=unused-argument
        if not self._tenant_id:
              _LOGGER.warning("If you are using a personal (non-work/school) account to sign-in \
                               with the Interactive Browser login, you need to pass your tenant id. \
                               To learn more, please visit http://aka.ms/TODO")
        super().get_token(*scopes, **kwargs)
