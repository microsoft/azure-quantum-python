##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import re
import os
import json
import time
from unittest.mock import patch
from vcr.request import Request as VcrRequest

from azure_devtools.scenario_tests.base import ReplayableTest
from azure_devtools.scenario_tests.recording_processors import (
    RecordingProcessor,
    is_text_payload,
)
from azure.quantum import Workspace
from azure.quantum._workspace_connection_params import (
    WorkspaceConnectionParams,
)
from azure.quantum._constants import (
    EnvironmentVariables,
    ConnectionConstants,
    GUID_REGEX_PATTERN,
)
from azure.quantum import Job
from azure.quantum.target import Target
from azure.identity import ClientSecretCredential


ZERO_UID = "00000000-0000-0000-0000-000000000000"
ONE_UID = "00000000-0000-0000-0000-000000000001"
TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47"
PLACEHOLDER = "PLACEHOLDER"
TRUE = "True"
FALSE = "False"
SUBSCRIPTION_ID = "11111111-2222-3333-4444-555555555555"
RESOURCE_GROUP = "myresourcegroup"
WORKSPACE = "myworkspace"
LOCATION = "eastus"
STORAGE = "mystorage"
API_KEY = "myapikey"
APP_ID = "testapp"
DEFAULT_TIMEOUT_SECS = 300
AUTH_URL = "https://login.microsoftonline.com/"
GUID_REGEX_CAPTURE = f"(?P<guid>{GUID_REGEX_PATTERN})"

class RegexScrubbingPatterns:
    URL_PATH_SUBSCRIPTION_ID = f"/subscriptions/{GUID_REGEX_CAPTURE}"
    DATE_TIME = r"\d{8}-\d{6}"
    URL_PATH_BLOB_GUID = f'blob.core.windows.net/{GUID_REGEX_CAPTURE}'
    URL_PATH_RESOURCE_GROUP = r"/resourceGroups/[a-z0-9-]+/"
    URL_PATH_WORKSPACE_NAME = r"/workspaces/[a-z0-9-]+/"
    URL_STORAGE_ACCOUNT = r"https://[^\.]+.blob.core.windows.net"
    URL_QUANTUM_ENDPOINT = r"https://[^\.]+.quantum(-test)?.azure.com/"
    URL_OAUTH_ENDPOINT = \
        f"https://login.(microsoftonline.com|windows-ppe.net)/{GUID_REGEX_CAPTURE}/oauth2/.*"
    URL_QUERY_SAS_KEY_SIGNATURE = r"sig=[^&]+\&"
    URL_QUERY_SAS_KEY_VALUE = r"sv=[^&]+\&"
    URL_QUERY_SAS_KEY_EXPIRATION = r"se=[^&]+\&"
    URL_QUERY_AUTH_CLIENT_ID = r"client_id=[^&]+\&"
    URL_QUERY_AUTH_CLIENT_SECRET = r"client_secret=[^&]+\&"
    URL_QUERY_AUTH_CLIENT_ASSERTION = r"client_assertion=[^&]+\&"
    URL_QUERY_AUTH_CLIENT_ASSERTION_TYPE = r"client_assertion_type=[^&]+\&"
    URL_QUERY_AUTH_CLAIMS = r"claims=[^&]+\&"
    URL_QUERY_AUTH_CODE_VERIFIER = r"code_verifier=[^&]+\&"
    URL_QUERY_AUTH_CODE = r"code=[^&]+\&"
    URL_HTTP = r"http://" # Devskim: ignore DS137138

class QuantumTestBase(ReplayableTest):
    """QuantumTestBase

    During init, gets Azure Credentials and
    Azure Quantum Workspace parameters from OS environment variables.
    """
    def __init__(self, method_name):
        connection_params = WorkspaceConnectionParams.from_env_vars()
        connection_params.apply_defaults(
            client_id=ZERO_UID,
            tenant_id=TENANT_ID,
            resource_group=RESOURCE_GROUP,
            subscription_id=SUBSCRIPTION_ID,
            workspace_name=WORKSPACE,
            location=LOCATION,
            user_agent_app_id=APP_ID,
        )
        self.connection_params = connection_params
        self._client_secret = os.environ.get(EnvironmentVariables.AZURE_CLIENT_SECRET, PLACEHOLDER)
        self._client_certificate_path = os.environ.get(EnvironmentVariables.AZURE_CLIENT_CERTIFICATE_PATH, PLACEHOLDER)
        self._client_send_certificate_chain = os.environ.get(EnvironmentVariables.AZURE_CLIENT_SEND_CERTIFICATE_CHAIN, TRUE)
        
        self._regex_replacer = CustomRecordingProcessor(self)
        recording_processors = [
            AuthenticationMetadataFilter(),
            self._regex_replacer,
            CustomAccessTokenReplacer(),
        ]

        replay_processors = [
            AuthenticationMetadataFilter(),
            self._regex_replacer,
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

        self._regex_replacer.register_guid_regex(
            f"(?:job-|jobs/|session-|sessions/){GUID_REGEX_CAPTURE}")
        self._regex_replacer.register_scrubbing(connection_params.client_id, ZERO_UID)
        self._regex_replacer.register_scrubbing(
            self._client_secret, PLACEHOLDER
        )
        self._regex_replacer.register_scrubbing(connection_params.tenant_id, ZERO_UID)
        self._regex_replacer.register_scrubbing(connection_params.subscription_id, ZERO_UID)
        self._regex_replacer.register_scrubbing(connection_params.workspace_name, WORKSPACE)
        self._regex_replacer.register_scrubbing(connection_params.location, LOCATION)
        self._regex_replacer.register_scrubbing(connection_params.resource_group, RESOURCE_GROUP)
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_PATH_SUBSCRIPTION_ID,
            f"/subscriptions/{ZERO_UID}",
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.DATE_TIME,
            "20210101-000000"
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_PATH_BLOB_GUID,
            f'blob.core.windows.net/{ZERO_UID}',
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_PATH_RESOURCE_GROUP,
            f'/resourceGroups/{RESOURCE_GROUP}/'
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_PATH_WORKSPACE_NAME,
            f'/workspaces/{WORKSPACE}/'
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_STORAGE_ACCOUNT,
            f'https://{STORAGE}.blob.core.windows.net'
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_QUANTUM_ENDPOINT,
            ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(LOCATION)
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_OAUTH_ENDPOINT,
            f'https://login.microsoftonline.com/{ZERO_UID}/oauth2/v2.0/token'
        )
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_SAS_KEY_SIGNATURE,
                                      "sig=PLACEHOLDER&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_SAS_KEY_VALUE,
                                      "sv=PLACEHOLDER&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_SAS_KEY_EXPIRATION,
                                      "se=2050-01-01T00%3A00%3A00Z&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_AUTH_CLIENT_ID,
                                      "client_id=PLACEHOLDER&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_AUTH_CLIENT_SECRET,
                                      "client_secret=PLACEHOLDER&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_AUTH_CLAIMS,
                                      "claims=PLACEHOLDER&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_AUTH_CODE_VERIFIER,
                                      "code_verifier=PLACEHOLDER&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_QUERY_AUTH_CODE,
                                      "code=PLACEHOLDER&")
        self._regex_replacer.register_scrubbing(RegexScrubbingPatterns.URL_HTTP, "https://")

        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_QUERY_AUTH_CLIENT_ASSERTION,
            "client_assertion=PLACEHOLDER&"
        )
        self._regex_replacer.register_scrubbing(
            RegexScrubbingPatterns.URL_QUERY_AUTH_CLIENT_ASSERTION_TYPE,
            "client_assertion_type=PLACEHOLDER&"
        )

    def disable_scrubbing(self, pattern: str) -> None:
        """
        Disable scrubbing of a pattern.
        This is useful when you need to have a value in the recording
        that would otherwise be scrubbed by default.
        Use it carefully not to leak any secrets in the recording.
        To be used in conjunction with `enable_scrubbing()` method.

        :param pattern:
            Pattern to disable scrubbing.
        """
        self._regex_replacer.disable_scrubbing(pattern)

    def enable_scrubbing(self, pattern: str) -> None:
        """
        Enable scrubbing of a pattern.
        This is useful when you need to have a value in the recording
        that would otherwise be scrubbed by default.
        You disable the scrubbing with `disable_scrubbing()` method
        and then re-enable the scrubbing with this method.
        :param pattern:
            Pattern to enable scrubbing.
        """
        self._regex_replacer.enable_scrubbing(pattern)

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
        return (self.connection_params.subscription_id == SUBSCRIPTION_ID
                and not self.in_recording 
                and not self.is_live)

    def clear_env_vars(self, os_environ):
        for env_var in EnvironmentVariables.ALL:
            if env_var in os_environ:
                del os_environ[env_var]

    def create_workspace(
            self,
            credential = None,
            **kwargs) -> Workspace:
        """
        Create workspace using credentials passed via OS Environment Variables
        described in the README.md documentation, or when in playback mode use
        a placeholder credential.
        """

        connection_params = self.connection_params

        if not credential and self.is_playback:
            credential = ClientSecretCredential(
                tenant_id=TENANT_ID,
                client_id=ZERO_UID,
                client_secret=PLACEHOLDER)

        workspace = Workspace(
            credential=credential,
            subscription_id=connection_params.subscription_id,
            resource_group=connection_params.resource_group,
            name=connection_params.workspace_name,
            location=connection_params.location,
            user_agent=connection_params.user_agent_app_id,
            **kwargs
        )

        return workspace

    def create_echo_target(
        self,
        credential = None,
        **kwargs
    ) -> Target:
        """
        Create a `Microsoft.Test.echo-target` Target for simple job submission tests.
        Uses the Workspace returned from `create_workspace()` method. 
        """
        workspace = self.create_workspace(credential=credential, **kwargs)
        target = Target(
            workspace=workspace,
            name="echo-output",
            provider_id="Microsoft.Test",
            input_data_format = "microsoft.quantum-log.v1",
            output_data_format = "microsoft.quantum-log.v1"
        )
        return target

class RegexScrubbingRule:
    """ A Regex Scrubbing Rule to be applied during test recordings and playbacks."""

    def __init__(
            self,
            pattern: str,
            replacement_text: str,
    ) -> None:
        self.pattern = pattern
        self.replacement_text = replacement_text
        self._regex = re.compile(pattern=pattern,
                                    flags=re.IGNORECASE | re.MULTILINE)
        self.enabled = True

    def replace(self, original_text) -> str:
        """
        If enabled, returns the `original_text` with the regex replacement applied to it.
        Otherwise, returns the unmodified `original_text`.
        """
        if self.enabled:
            return self._regex.sub(self.replacement_text, original_text)
        return original_text


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
        "www-authenticate",
    ]
    ALLOW_SANITIZED_HEADERS = [
        ConnectionConstants.QUANTUM_API_KEY_HEADER,
    ]

    def __init__(self, quantumTest: QuantumTestBase):
        self._scrubbingRules = dict[str, RegexScrubbingRule]()
        self._auto_guid_regexes = []
        self._guids = dict[str, int]()
        self._sequence_ids = dict[str, float]()
        self._quantumTest = quantumTest

    def disable_scrubbing(self, pattern: str) -> None:
        """
        Disable scrubbing of a pattern.
        This is useful when you need to have a value in the recording
        that would otherwise be scrubbed by default.
        Use it carefully not to leak any secrets in the recording.
        To be used in conjunction with `enable_scrubbing()` method.

        :param pattern:
            Pattern to disable scrubbing.
        """
        if pattern in self._scrubbingRules:
            self._scrubbingRules[pattern].enabled = False

    def enable_scrubbing(self, pattern: str) -> None:
        """
        Enable scrubbing of a pattern.
        This is useful when you need to have a value in the recording
        that would otherwise be scrubbed by default.
        You disable the scrubbing with `disable_scrubbing()` method
        and then re-enable the scrubbing with this method.

        Example:
            ```python
            self.disable_scrubbing(RegexScrubbingPatterns.URL_QUERY_SAS_KEY_EXPIRATION)
            try:
                # your testing logic here that relies on the un-scrubbed value
            finally:
                self.enable_scrubbing(RegexScrubbingPatterns.URL_QUERY_SAS_KEY_EXPIRATION)
            ```

        :param pattern:
            Pattern to enable scrubbing.
        """
        if pattern in self._scrubbingRules:
            self._scrubbingRules[pattern].enabled = True

    def register_scrubbing(self, regex_pattern, replacement_text):
        """
        Registers a regular expression that should be used to replace the
        HTTP requests' uri, headers and body with a `replacement_text`.
        """
        self._scrubbingRules[regex_pattern] = RegexScrubbingRule(
            pattern=regex_pattern,
            replacement_text=replacement_text
        )

    def register_guid_regex(self, guid_regex):
        """
        Registers a regular expression that should detect guids from
        HTTP requests' uri, headers and body and automatically
        register replacements with an auto-incremented deterministic guid
        to be included in the recordings
        """
        self._auto_guid_regexes.append(
            re.compile(pattern=guid_regex,
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
                    guid = match.groups("guid")[0]
                    if (
                        guid not in self._guids
                        and not guid.startswith("00000000-")
                    ):
                        i = len(self._guids) + 1
                        new_guid = "00000000-0000-0000-0000-%0.12X" % i
                        self._guids[guid] = new_guid
                        self.register_scrubbing(guid, new_guid)

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
            if (
                self._quantumTest.is_playback or
                not self._quantumTest.disable_recording
            ):
                # VCR calls this method twice per request
                # so we need to increment the sequence by 0.5
                # and use the ceiling
                sequence_id += 0.5
            self._sequence_ids[key] = sequence_id
            if "?" not in request.uri:
                request.uri += "?"
            request.uri += SEQUENCE_ID_KEY + "%0.f" % math.ceil(sequence_id)
        return request

    def _apply_scrubbings(self, value: str):
        for scrubbing_rule in self._scrubbingRules.values():
            value = scrubbing_rule.replace(value)
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
            if (
                (content_type == "application/x-www-form-urlencoded") and
                (isinstance(body, bytes) or isinstance(body, bytearray))
            ):
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
                headers[key] = self._apply_scrubbings(request.headers[key])
            if key.lower() in self.ALLOW_SANITIZED_HEADERS:
                headers[key] = PLACEHOLDER
        request.headers = headers

        request.uri = self._apply_scrubbings(request.uri)
        self._append_sequence_id(request)

        if body is not None:
            body = self._apply_scrubbings(body)
            if encode_body:
                body = body.encode("utf-8")
            request.body = body
            request.headers["content-length"] = ["%s" % len(body)]

        return request

    def _get_content_type(self, entity):
        # 'headers' is a field of 'request',
        # but it is a dict-key in 'response'
        if hasattr(entity, "headers"):
            headers = getattr(entity, "headers")
        else:
            headers = entity.get('headers')

        content_type = None
        if headers is not None:
            content_type = headers.get('content-type')
            if content_type is not None:
                # content-type could be an array from response
                # so we extract it out if needed
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
                    new_header_value = (
                        self._apply_scrubbings(old_header_value))
                    new_header_values.append(new_header_value)
                headers[key] = new_header_values
        response["headers"] = headers

        if "url" in response:
            response["url"] = self._apply_scrubbings(response["url"])

        content_type = self._get_content_type(response)
        if (
            is_text_payload(response)
            or "application/octet-stream" == content_type
        ):
            body = response["body"]["string"]
            if body is not None:
                encode_body = False
                if not isinstance(body, str):
                    body = body.decode("utf-8")
                    encode_body = True
                if body:
                    body = self._apply_scrubbings(body)
                    if encode_body:
                        body = body.encode("utf-8")
                    response["body"]["string"] = body
                    response["headers"]["content-length"] = ["%s" % len(body)]

        return response


class AuthenticationMetadataFilter(RecordingProcessor):
    """
    Remove authority and tenant discovery requests
    and responses from recordings.
    MSAL sends these requests to obtain non-secret
    metadata about the token authority.
    Recording them is unnecessary because tests use
    fake credentials during playback that don't invoke MSAL.
    """

    def process_request(self, request):
        if (
            "/.well-known/openid-configuration" in request.uri
            or "/common/discovery/instance" in request.uri
            or "&discover-tenant-id-and-authority" in request.uri
        ):
            return None
        return request


class CustomAccessTokenReplacer(RecordingProcessor):
    """
    Sanitize the access token in the response body.
    """
    def process_response(self, response):
        try:
            body = json.loads(response['body']['string'])
            if not isinstance(body, list) and 'access_token' in body:
                refresh_in =  365*24*60*60
                expires_in =  int(time.time()) + refresh_in
                body['access_token'] = PLACEHOLDER
                body['expires_in'] = expires_in
                body['ext_expires_in'] = expires_in
                body['refresh_in'] = refresh_in
                for prop in (
                    'scope', 'refresh_token',
                    'foci', 'client_info',
                    'id_token'
                ):
                    if prop in body:
                        del body[prop]
            body_bytes = json.dumps(body).encode()
            response['body']['string'] = body_bytes
            response['headers']['content-length'] = [str(len(body_bytes))]
        except (KeyError, ValueError):
            return response
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
        body_bytes = json.dumps(body).encode()
        response['body']['string'] = body_bytes
        response['headers']['content-length'] = [str(len(body_bytes))]
        return response
