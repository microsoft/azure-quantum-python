# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import logging
import requests
import re

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

    We inherit from InteractiveBrowserCredential and we automatically identify
    the user's tenant_id for a given subscription so that users with MSA accounts
    don't need to pass it.
    This is a mitigation for bug https://github.com/Azure/azure-sdk-for-python/issues/18975

    We need the following parameters to enable auto-detection of tenant_id
    - subscription_id
    - arm_base_url (defaults to the production url "https://management.azure.com/")

    """

    def __init__(self, **kwargs):
        self.subscription_id = kwargs.pop("subscription_id")
        self.arm_base_url = kwargs.pop("arm_base_url", "https://management.azure.com/")

        # we need to keep track if the tenant_id was passed
        # because the base class constructor will default it to 
        # the generic "_organizations" value, that only works for work/school accounts
        tenant_id = kwargs.pop("tenant_id")
        self.has_tenant_id = tenant_id is not None

        super(_InteractiveBrowserCredential, self).__init__(**kwargs)


    def get_token(self, *scopes, **kwargs):  # pylint:disable=unused-argument
        if self.subscription_id is not None \
           and not self.has_tenant_id:
                self._tenant_id = self._get_tenant_id(arm_base_url=self.arm_base_url,
                                                      subscription_id=self.subscription_id)
                self.has_tenant_id = self._tenant_id is not None

        super().get_token(*scopes, **kwargs)


    def _get_tenant_id(self, arm_base_url:str, subscription_id:str):
        try:
            uri = (
                f"{arm_base_url}/subscriptions/"
                + f"{subscription_id}?api-version=2018-01-01"
            )
            response = requests.get(uri)

            # This gnarly piece of code is how we get the guest tenant
            # authority associated with the subscription.
            # We make a unauthenticated request to ARM and extract the tenant
            # authority from the WWW-Authenticate header in the response.
            # The header is of the form:
            # Bearer authorization_uri=
            # https://login.microsoftonline.com/tenantId, key1=value1s
            auth_header = response.headers["WWW-Authenticate"]
            _LOGGER.debug(
                f'{"got the following auth header from"}'
                f"the management endpoint: {auth_header}"
            )

            trimmed_auth_header = auth_header[
                len("Bearer "):
            ]  # trim the leading 'Bearer '
            trimmed_auth_header_parts = trimmed_auth_header.split(
                ","
            )  # get the various k=v parts
            key_value_pairs = dict(
                map(lambda s: tuple(s.split("=")), trimmed_auth_header_parts)
            )  # make the parts into a dictionary
            quoted_tenant_uri = key_value_pairs[
                "authorization_uri"
            ]  # get the value of the 'authorization_uri' key
            tenant_uri = quoted_tenant_uri[
                1:-1
            ]  # strip it of surrounding quotes

            _LOGGER.debug(
                f'{"got the following tenant uri from"}'
                + f"the authentication header: {tenant_uri}"
            )

            regex = re.compile(pattern=r"([a-f0-9]+[-]){4}[a-f0-9]+", flags=re.IGNORECASE)
            tenant_id = regex.search(tenant_uri).group()
            return tenant_id

        except Exception as e:
            _LOGGER.debug(
                f"Failed to get tenant authority for subscription: {e}"
            )
            return None