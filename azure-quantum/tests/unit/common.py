##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import os
import re
from unittest.mock import patch

import six
import pytest
from vcr.request import Request as VcrRequest

from azure.quantum import Workspace
from azure.identity import ClientSecretCredential

from azure_devtools.scenario_tests.base import ReplayableTest
from azure_devtools.scenario_tests.recording_processors import (
    RecordingProcessor,
    is_text_payload,
    AccessTokenReplacer,
    SubscriptionRecordingProcessor,
    OAuthRequestResponsesFilter,
    RequestUrlNormalizer,
)
import json

from azure.quantum.job.job import Job

ZERO_UID = "00000000-0000-0000-0000-000000000000"
ONE_UID = "00000000-0000-0000-0000-000000000001"
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
PLACEHOLDER = "PLACEHOLDER"
RESOURCE_GROUP = "myresourcegroup"
WORKSPACE = "myworkspace"
LOCATION = "eastus"
STORAGE = "mystorage"
DEFAULT_TIMEOUT_SECS = 300

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

        # needed to make sure the Default Credential will work
        os.environ["LOCATION"] = self._location

        regex_replacer = CustomRecordingProcessor(self)
        recording_processors = [
            regex_replacer,
            AccessTokenReplacerWithListException(),
            InteractiveAccessTokenReplacer(),
            SubscriptionRecordingProcessor(ZERO_UID),
            AuthenticationMetadataFilter(),
            OAuthRequestResponsesFilter(),
            RequestUrlNormalizer()
        ]

        replay_processors = [
            regex_replacer,
            AuthenticationMetadataFilter(),
            OAuthRequestResponsesFilter(),
            RequestUrlNormalizer(),
            OAuthResponsesFilter(),
            CustomUrlPlaybackProcessor()
        ]

        super(QuantumTestBase, self).__init__(
            method_name,
            recording_processors=recording_processors,
            replay_processors=replay_processors,
        )
        # as we append a sequence id to every request,
        # we ensure that that a request can only be recorded once
        self.vcr.record_mode = 'once'
        self.vcr.register_matcher('query', self._custom_request_query_matcher)

        if self.is_playback:
            self._client_id = ZERO_UID
            self._client_secret = PLACEHOLDER
            self._tenant_id = TENANT_ID
            self._resource_group = RESOURCE_GROUP
            self._subscription_id = ZERO_UID
            self._workspace_name = WORKSPACE
            self._location = LOCATION

        regex_replacer.register_guid_regex(
            r"(?:job-|jobs/|session-|sessions/)((?:[a-f0-9]+[-]){4}[a-f0-9]+)")
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
            r"\d{8}-\d{6}", "20210101-000000"
        )
        regex_replacer.register_regex(
            r'blob.core.windows.net/([a-f0-9]+[-]){4}[a-f0-9]+',
            'blob.core.windows.net/{}'.format(ZERO_UID),
        )
        regex_replacer.register_regex(
            r"/resourceGroups/[a-z0-9-]+/", f'/resourceGroups/{RESOURCE_GROUP}/'
        )
        regex_replacer.register_regex(
            r"/workspaces/[a-z0-9-]+/", f'/workspaces/{WORKSPACE}/'
        )
        regex_replacer.register_regex(
            r"https://[^\.]+.blob.core.windows.net", f'https://{STORAGE}.blob.core.windows.net'
        )
        regex_replacer.register_regex(
            r"https://[^\.]+.quantum.azure.com", f'https://{LOCATION}.quantum.azure.com'
        )
        regex_replacer.register_regex(
            r"/workspaces/[a-z0-9-]+/", f'/workspaces/{WORKSPACE}/'
        )

        regex_replacer.register_regex(r"sig=[^&]+\&", "sig=PLACEHOLDER&")
        regex_replacer.register_regex(r"sv=[^&]+\&", "sv=PLACEHOLDER&")
        regex_replacer.register_regex(r"se=[^&]+\&", "se=PLACEHOLDER&")
        regex_replacer.register_regex(r"client_id=[^&]+\&", "client_id=PLACEHOLDER&")
        regex_replacer.register_regex(r"client_secret=[^&]+\&", "client_secret=PLACEHOLDER&")
        regex_replacer.register_regex(r"claims=[^&]+\&", "claims=PLACEHOLDER&")
        regex_replacer.register_regex(r"code_verifier=[^&]+\&", "code_verifier=PLACEHOLDER&")
        regex_replacer.register_regex(r"code=[^&]+\&", "code_verifier=PLACEHOLDER&")
        regex_replacer.register_regex(r"code=[^&]+\&", "code_verifier=PLACEHOLDER&")
        regex_replacer.register_regex(r"http://", "https://")  # Devskim: ignore DS137138

    @classmethod
    def _custom_request_query_matcher(cls, r1: VcrRequest, r2: VcrRequest):
        """ Ensure method, path, and query parameters match. """
        from six.moves.urllib_parse import urlparse, parse_qs  # pylint: disable=import-error, relative-import

        assert r1.method == r2.method, f"method: {r1.method} != {r2.method}"

        url1 = urlparse(r1.uri)
        url2 = urlparse(r2.uri)

        assert url1.hostname == url2.hostname, f"hostname: {url1.hostname} != {url2.hostname}"
        assert url1.path == url2.path, f"path: {url1.path} != {url2.path}"

        q1 = parse_qs(url1.query)
        q2 = parse_qs(url2.query)

        for key in q1.keys():
            assert key in q2, f"&{key} not found in {url2.query}"
            assert q1[key][0].lower() == q2[key][0].lower(), f"&{key}: {q1[key][0].lower()} != {q2[key][0].lower()}"

        for key in q2.keys():
            assert key in q1, f"&{key} not found in {url1.query}"
            assert q1[key][0].lower() == q2[key][0].lower(), f"&{key}: {q1[key][0].lower()} != {q2[key][0].lower()}"

        return True

    def setUp(self):
        self.in_test_setUp = True
        super(QuantumTestBase, self).setUp()
        # Since we are appending a sequence id to the requests
        # we don't allow playback repeats
        self.cassette.allow_playback_repeats = False

        # modify the _default_poll_wait time to zero
        # so that we don't artificially wait or delay
        # the tests when in playback mode
        self.patch_default_poll_wait = patch.object(
            Job,
            "_default_poll_wait",
            0.0
        )
        if self.is_playback:
            self.patch_default_poll_wait.start()

        self.in_test_setUp = False

    def tearDown(self):
        self.patch_default_poll_wait.stop()
        super().tearDown()

    def pause_recording(self):
        self.disable_recording = True

    def resume_recording(self):
        self.disable_recording = False

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


class CustomUrlPlaybackProcessor(RecordingProcessor):
    def process_request(self, request):
        request.uri = re.sub('https://[^.]+.quantum.azure.com/',
                        f'https://{LOCATION}.quantum.azure.com/',
                        request.uri,
                        flags=re.IGNORECASE)
        return request


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

    def __init__(self, quantumTest: QuantumTestBase):
        self._regexes = []
        self._auto_guid_regexes = []
        self._guids = dict[str, int]()
        self._sequence_ids = dict[str, float]()
        self._quantumTest = quantumTest

    def register_regex(self, regex, replacement_text):
        """
        Registers a regular expression that should be used to replace the
        HTTP requests' uri, headers and body with a replacement_text
        """
        self._regexes.append((re.compile(pattern=regex,
                                         flags=re.IGNORECASE | re.MULTILINE),
                             replacement_text))

    def register_guid_regex(self, guid_regex):
        """
        Registers a regular expression that should detect guids from
        HTTP requests' uri, headers and body and automatically
        register replacements with an auto-incremented deterministic guid
        to be included in the recordings
        """
        self._auto_guid_regexes.append(re.compile(pattern=guid_regex,
                                                  flags=re.IGNORECASE | re.MULTILINE))

    def _search_for_guids(self, value: str):
        """
        Looks for a registered guid pattern and, if found,
        automatically adds it to be replaced in future
        requests/responses.
        """
        if value:
            for regex in self._auto_guid_regexes:
                match = regex.search(value)
                if match:
                    guid = match.groups(1)[0]
                    if (guid not in self._guids
                        and not guid.startswith("00000000-")):
                        i = len(self._guids) + 1
                        new_guid = "00000000-0000-0000-0000-%0.12X" % i
                        self._guids[guid] = new_guid
                        self.register_regex(guid, new_guid)

    def _append_sequence_id(self, request: VcrRequest):
        """
        Appends a sequential `&test-sequence-id=` in the querystring
        of the recordings, such that multiple calls to the same
        URL will be recorded multiple times with potentially different
        responses.

        For example, when a job is submitted and we want to fetch
        the job status, the HTTP request to get the job status is the same,
        but the response can be different, initially returning
        Status="In-Progress" and later returning Status="Completed".

        The sequence is only for `quantum.azure.com` API requests
        and is on a per Method+Uri basis.
        """
        if "quantum.azure.com" not in request.uri:
            return request

        import math
        SEQUENCE_ID_KEY = "&test-sequence-id="
        if SEQUENCE_ID_KEY not in request.uri:
            key = f"{request.method}:{request.uri}"
            sequence_id = self._sequence_ids.pop(key, 0.0)
            # if we are in playback
            # or we are recording and the recording is not suspended
            # we increment the sequence id
            if (self._quantumTest.is_playback or
                not self._quantumTest.disable_recording):
                # VCR calls this method twice per request
                # so we need to increment the sequence by 0.5
                # and use the ceiling
                sequence_id += 0.5
            self._sequence_ids[key] = sequence_id
            if "?" not in request.uri:
                request.uri += "?"
            request.uri += SEQUENCE_ID_KEY + "%0.f" % math.ceil(sequence_id)
        return request

    def _regex_replace_all(self, value: str):
        for regex, replacement_text in self._regexes:
            value = regex.sub(replacement_text, value)
        return value

    def process_request(self, request):
        # when loading the VCR cassete during
        # the test playback, just return the request
        # that is recorded in the cassete
        if self._quantumTest.in_test_setUp:
            return request

        content_type = self._get_content_type(request)
        body = request.body
        encode_body = False
        if body:
            if ((content_type == "application/x-www-form-urlencoded") and
                (isinstance(body, bytes) or isinstance(body, bytearray))):
                body = body.decode("utf-8")
                encode_body = True
            else:
                body = str(body)

        for key in request.headers:
            self._search_for_guids(request.headers[key])
        self._search_for_guids(request.uri)
        self._search_for_guids(body)

        headers = {}
        for key in request.headers:
            if key.lower() in self.ALLOW_HEADERS:
                headers[key] = self._regex_replace_all(request.headers[key])
        request.headers = headers

        request.uri = self._regex_replace_all(request.uri)
        self._append_sequence_id(request)

        if body is not None:
            body = self._regex_replace_all(body)
            if encode_body:
                body = body.encode("utf-8")
            request.body = body
            request.headers["content-length"] = ["%s" % len(body)]

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
        # when loading the VCR cassete during
        # the test playback, just return the response
        # that is recorded in the cassete
        if self._quantumTest.in_test_setUp:
            return response

        headers = {}
        for key in response["headers"]:
            if key.lower() in self.ALLOW_HEADERS:
                new_header_values = []
                for old_header_value in response["headers"][key]:
                    new_header_value = self._regex_replace_all(old_header_value)
                    new_header_values.append(new_header_value)
                headers[key] = new_header_values
        response["headers"] = headers

        if "url" in response:
            response["url"] = self._regex_replace_all(response["url"])

        content_type = self._get_content_type(response)
        if is_text_payload(response) or "application/octet-stream" == content_type:
            body = response["body"]["string"]
            if body is not None:
                encode_body = False
                if not isinstance(body, six.string_types):
                    body = body.decode("utf-8")
                    encode_body = True
                if body:
                    body = self._regex_replace_all(body)
                    if encode_body:
                        body = body.encode("utf-8")
                    response["body"]["string"] = body
                    response["headers"]["content-length"] = ["%s" % len(body)]

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


class AccessTokenReplacerWithListException(AccessTokenReplacer):
    """
    Replace the access token for service principal authentication in a response body.

    This is customized for responses that return lists.
    """

    def __init__(self, replacement='fake_token'):
        self._replacement = replacement

    def process_response(self, response):
        import json
        try:
            body = json.loads(response['body']['string'])
            if not isinstance(body, list):
                body['access_token'] = self._replacement
        except (KeyError, ValueError):
            return response
        response['body']['string'] = json.dumps(body)
        return response


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
        body = json.dumps(body)
        response['body']['string'] = body
        response['headers']['content-length'] = ["%s" % len(body)]
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
