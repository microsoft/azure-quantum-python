#!/bin/env python
# -*- coding: utf-8 -*-
##
# common.py: Contain base class and helper functions for unit tests
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import os
import re

import six
import pytest
import asyncio

from azure.quantum import Workspace
from azure.identity import ClientSecretCredential
from azure.quantum.aio import Workspace as AsyncWorkspace
from azure.identity.aio import ClientSecretCredential as AsyncClientSecretCredential

from azure_devtools.scenario_tests.base import ReplayableTest
from azure_devtools.scenario_tests.recording_processors import (
    RecordingProcessor,
    is_text_payload,
    AccessTokenReplacer,
    SubscriptionRecordingProcessor,
    OAuthRequestResponsesFilter,
    RequestUrlNormalizer,
)
from azure_devtools.scenario_tests.utilities import _get_content_type
import json

ZERO_UID = "00000000-0000-0000-0000-000000000000"
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
PLACEHOLDER = "PLACEHOLDER"
RESOURCE_GROUP = "myresourcegroup"
WORKSPACE = "myworkspace"
LOCATION = "eastus"
STORAGE = "mystorage"

@pytest.mark.usefixtures("event_loop_instance")
class QuantumTestBase(ReplayableTest):
    """QuantumTestBase

    During init, gets Azure Credentials and
    Azure Quantum Workspace parameters from OS environment variables.
    """

    def __init__(self, method_name):
        self._client_id = os.environ.get("AZURE_CLIENT_ID", ZERO_UID)
        self._client_secret = os.environ.get("AZURE_CLIENT_SECRET", PLACEHOLDER)
        self._tenant_id = os.environ.get("AZURE_TENANT_ID", TENANT_ID)
        self._resource_group = os.environ.get("AZURE_QUANTUM_WORKSPACE_RG", os.environ.get("RESOURCE_GROUP", RESOURCE_GROUP))
        self._subscription_id = os.environ.get("AZURE_QUANTUM_SUBSCRIPTION_ID", os.environ.get("SUBSCRIPTION_ID", ZERO_UID))
        self._workspace_name = os.environ.get("AZURE_QUANTUM_WORKSPACE_NAME")
        self._location = os.environ.get("AZURE_QUANTUM_WORKSPACE_LOCATION", os.environ.get("LOCATION", LOCATION))
        self._user_agent = os.environ.get("AZURE_QUANTUM_PYTHON_APPID")

        self._pause_recording_processor = PauseRecordingProcessor()
        regex_replacer = CustomRecordingProcessor()
        recording_processors = [
            self._pause_recording_processor,
            regex_replacer,
            AccessTokenReplacer(),
            InteractiveAccessTokenReplacer(),
            SubscriptionRecordingProcessor(ZERO_UID),
            AuthenticationMetadataFilter(),
            OAuthRequestResponsesFilter(),
            RequestUrlNormalizer()
        ]

        replay_processors = [
            AuthenticationMetadataFilter(),
            OAuthRequestResponsesFilter(),
            RequestUrlNormalizer(),
            OAuthResponsesFilter(),
        ]

        super(QuantumTestBase, self).__init__(
            method_name,
            recording_processors=recording_processors,
            replay_processors=replay_processors,
        )

        if self.is_playback:
            self._client_id = ZERO_UID
            self._client_secret = PLACEHOLDER
            self._tenant_id = TENANT_ID
            self._resource_group = RESOURCE_GROUP
            self._subscription_id = ZERO_UID
            self._workspace_name = WORKSPACE
            self._location = LOCATION

        regex_replacer.register_regex(self.client_id, ZERO_UID)
        regex_replacer.register_regex(
            self.client_secret, PLACEHOLDER
        )
        regex_replacer.register_regex(self.tenant_id, ZERO_UID)
        regex_replacer.register_regex(self.subscription_id, ZERO_UID)
        regex_replacer.register_regex(self.workspace_name, WORKSPACE)
        regex_replacer.register_regex(self.location, LOCATION)
        regex_replacer.register_regex(self.resource_group, RESOURCE_GROUP)
        regex_replacer.register_regex(
            r"/subscriptions/([a-f0-9]+[-]){4}[a-f0-9]+",
            "/subscriptions/" + ZERO_UID,
        )
        regex_replacer.register_regex(
            r"job-([a-f0-9]+[-]){4}[a-f0-9]+", "job-" + ZERO_UID
        )
        regex_replacer.register_regex(
            r"jobs/([a-f0-9]+[-]){4}[a-f0-9]+", "jobs/" + ZERO_UID
        )
        regex_replacer.register_regex(
            r"job-([a-f0-9]+[-]){4}[a-f0-9]+", "job-" + ZERO_UID
        )
        regex_replacer.register_regex(
            r"\d{8}-\d{6}", "20210101-000000"
        )        
        regex_replacer.register_regex(
            r'"id":\s*"([a-f0-9]+[-]){4}[a-f0-9]+"',
            '"id": "{}"'.format(ZERO_UID),
        )
        regex_replacer.register_regex(
            r"/resourceGroups/[a-z0-9-]+/", f'/resourceGroups/{RESOURCE_GROUP}/'
        )
        regex_replacer.register_regex(
            r"/workspaces/[a-z0-9-]+/", f'/workspaces/{WORKSPACE}/'
        )
        regex_replacer.register_regex(
            r"https://[^\.]+.blob.core.windows.net/", f'https://{STORAGE}.blob.core.windows.net/'
        )
        regex_replacer.register_regex(
            r"https://[^\.]+.quantum.azure.com/", f'https://{LOCATION}.quantum.azure.com/'
        )
        regex_replacer.register_regex(
            r"/workspaces/[a-z0-9-]+/", f'/workspaces/{WORKSPACE}/'
        )

        regex_replacer.register_regex(r"sig=[^&]+\&", "sig=PLACEHOLDER&")
        regex_replacer.register_regex(r"sv=[^&]+\&", "sv=PLACEHOLDER&")
        regex_replacer.register_regex(r"se=[^&]+\&", "se=PLACEHOLDER&")
        regex_replacer.register_regex(r"client_id=[^&]+\&", "client_id=PLACEHOLDER&")
        regex_replacer.register_regex(r"claims=[^&]+\&", "claims=PLACEHOLDER&")
        regex_replacer.register_regex(r"code_verifier=[^&]+\&", "code_verifier=PLACEHOLDER&")
        regex_replacer.register_regex(r"code=[^&]+\&", "code_verifier=PLACEHOLDER&")
        regex_replacer.register_regex(r"code=[^&]+\&", "code_verifier=PLACEHOLDER&")

    def pause_recording(self):
        self._pause_recording_processor.pause_recording()

    def resume_recording(self):
        self._pause_recording_processor.resume_recording()

    def setUp(self):
        super(QuantumTestBase, self).setUp()
        # mitigation for issue https://github.com/kevin1024/vcrpy/issues/533
        self.cassette.allow_playback_repeats = True

    @property
    def is_playback(self):
        return self.subscription_id == ZERO_UID or \
               (not (self.in_recording or self.is_live))

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def tenant_id(self):
        return self._tenant_id

    @property
    def resource_group(self):
        return self._resource_group

    @property
    def location(self):
        return self._location

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def workspace_name(self):
        return self._workspace_name
    
    def create_workspace(self, **kwargs) -> Workspace:
        """Create workspace using credentials passed via OS Environment Variables
        described in the README.md documentation, or when in playback mode use
        a placeholder credential.

        :return: Workspace
        :rtype: Workspace
        """

        playback_credential = ClientSecretCredential(self.tenant_id,
                                                     self.client_id,
                                                     self.client_secret)
        default_credential = playback_credential if self.is_playback \
                             else None

        workspace = Workspace(
            credential=default_credential,
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            name=self.workspace_name,
            location=self.location,
            **kwargs
        )
        workspace.append_user_agent("testapp")

        return workspace

    def get_async_result(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)
    
    def create_async_workspace(self, **kwargs) -> AsyncWorkspace:
        """Create workspace using credentials passed via OS Environment Variables
        described in the README.md documentation, or when in playback mode use
        a placeholder credential.

        :return: AsyncWorkspace
        :rtype: AsyncWorkspace
        """

        playback_credential = AsyncClientSecretCredential(self.tenant_id,
                                                     self.client_id,
                                                     self.client_secret)
        default_credential = playback_credential if self.is_playback \
                             else None

        workspace = AsyncWorkspace(
            credential=default_credential,
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            name=self.workspace_name,
            location=self.location,
             **kwargs
        )
        workspace.append_user_agent("testapp")

        return workspace

class PauseRecordingProcessor(RecordingProcessor):
    def __init__(self):
        self.is_paused = False

    def pause_recording(self):
        self.is_paused = True

    def resume_recording(self):
        self.is_paused = False

    def process_request(self, request):
        if self.is_paused:
            return None
        return request

    def process_response(self, response):
        if self.is_paused:
            return None
        return response


class CustomRecordingProcessor(RecordingProcessor):

    ALLOW_HEADERS = [
        "connection",
        "content-length",
        "content-range",
        "content-type",
        "accept",
        "accept-encoding",
        "accept-charset",
        "accept-ranges",
        "transfer-encoding",
        "x-ms-blob-content-md5",
        "x-ms-blob-type",
        "x-ms-creation-time",
        "x-ms-date",
        "x-ms-encryption-algorithm",
        "x-ms-lease-state",
        "x-ms-lease-status",
        "x-ms-meta-avg_coupling",
        "x-ms-meta-max_coupling",
        "x-ms-meta-min_coupling",
        "x-ms-meta-num_terms",
        "x-ms-meta-type",
        "x-ms-range",
        "x-ms-server-encrypted",
        "x-ms-version",
        "x-client-cpu",
        "x-client-current-telemetry",
        "x-client-os",
        "x-client-sku",
        "x-client-ver",
        "user-agent",
    ]

    def __init__(self):
        self._regexes = []

    def register_regex(self, old_regex, new):
        self._regexes.append((re.compile(pattern=old_regex, 
                                         flags=re.IGNORECASE | re.MULTILINE),
                             new))

    def regex_replace_all(self, value: str):
        for oldRegex, new in self._regexes:
            value = oldRegex.sub(new, value)
        return value

    def process_request(self, request):
        headers = {}
        for key in request.headers:
            if key.lower() in self.ALLOW_HEADERS:
                headers[key] = self.regex_replace_all(request.headers[key])
        request.headers = headers

        request.uri = self.regex_replace_all(request.uri)
        content_type = self._get_content_type(request)

        body = request.body
        if body is not None:
            if ((content_type == "application/x-www-form-urlencoded") and
                (isinstance(body, bytes) or isinstance(body, bytearray))):
                body = body.decode("utf-8")
                body = self.regex_replace_all(body)
                request.body = body.encode("utf-8")
            else:
                body = str(body)
                body = self.regex_replace_all(body)
                request.body = body

        return request

    def _get_content_type(self, entity):
        # 'headers' is a field of 'request', but it is a dict-key in 'response'
        if hasattr(entity, "headers"):
            headers = getattr(entity, "headers")
        else:
            headers = entity.get('headers')

        content_type = None
        if headers is not None:
            content_type = headers.get('content-type')
            if content_type is not None:
                # content-type could be an array from response, let us extract it out
                if isinstance(content_type, list):
                    content_type = content_type[0]
                content_type = content_type.split(";")[0].lower()
        return content_type

    def process_response(self, response):
        headers = {}
        for key in response["headers"]:
            if key.lower() in self.ALLOW_HEADERS:
                new_header_values = []
                for old_header_value in response["headers"][key]:
                    new_header_value = self.regex_replace_all(old_header_value)
                    new_header_values.append(new_header_value)
                headers[key] = new_header_values
        response["headers"] = headers

        if "url" in response:
            response["url"] = self.regex_replace_all(response["url"])

        content_type = self._get_content_type(response)
        if is_text_payload(response) or "application/octet-stream" == content_type:
            body = response["body"]["string"]
            if body is not None:
                if not isinstance(body, six.string_types):
                    body = body.decode("utf-8")
                if body:
                    body = self.regex_replace_all(body)
                    response["body"]["string"] = body

        return response


class OAuthResponsesFilter(RecordingProcessor):
    def process_request(self, request):
        request.uri = re.sub('https://login.microsoftonline.com/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
                        f'https://login.microsoftonline.com/{ZERO_UID}',
                        request.uri,
                        flags=re.IGNORECASE)
        return request


class AuthenticationMetadataFilter(RecordingProcessor):
    """Remove authority and tenant discovery requests and responses from recordings.
    MSAL sends these requests to obtain non-secret metadata about the token authority. Recording them is unnecessary
    because tests use fake credentials during playback that don't invoke MSAL.
    """

    def process_request(self, request):
        if "/.well-known/openid-configuration" in request.uri or "/common/discovery/instance" in request.uri:
            return None
        return request


class InteractiveAccessTokenReplacer(RecordingProcessor):
    """Replace the access token for interactive authentication in a response body."""

    def __init__(self, replacement='fake_token'):
        self._replacement = replacement

    def process_response(self, response):
        import json
        try:
            body = json.loads(response['body']['string'])
            if 'access_token' in body:
                body['access_token'] = self._replacement
                for property in ('scope', 'refresh_token',
                                'foci', 'client_info',
                                'id_token'):
                    if property in body:
                        del body[property]
        except (KeyError, ValueError):
            return response
        response['body']['string'] = json.dumps(body)
        return response


def expected_terms():
    expected = json.dumps(
        {
            "cost_function": {
                "version": "1.1",
                "type": "ising",
                "terms": [{"c": 3, "ids": [1, 0]}, {"c": 5, "ids": [2, 0]}],
                "initial_configuration": {"0": -1, "1": 1, "2": -1},
            }
        }
    )
    return expected
