#!/bin/env python
# -*- coding: utf-8 -*-
##
# recording_updater.py: Updates test recordings with dummy values
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

## IMPORTS ##

import os
import io
import glob
import re
import unittest.mock
from azure.quantum import Workspace
from azure.quantum.workspace import MsalWrapper
from azure.common.credentials import ServicePrincipalCredentials
from azure_devtools.scenario_tests.base import ReplayableTest
from azure_devtools.scenario_tests.recording_processors import RecordingProcessor, GeneralNameReplacer, is_text_payload, AccessTokenReplacer, OAuthRequestResponsesFilter
from azure_devtools.scenario_tests.utilities import _get_content_type

class QuantumTestBase(ReplayableTest):
    """QuantumTestBase
    
    During init, gets Azure Credentials and Azure Quantum Workspace parameters from OS environment variables.
    """

    dummy_uid = "00000000-0000-0000-0000-000000000000"
    dummy_rg = "dummy-rg"
    dummy_ws = "dummy-ws"
    dummy_clientsecret = "sanitized"

    def __init__(self, method_name):
        self._client_id = os.environ.get("AZURE_CLIENT_ID","")
        self._client_secret = os.environ.get("AZURE_CLIENT_SECRET","")
        self._tenant_id = os.environ.get("AZURE_TENANT_ID","")
        self._resource_group = os.environ.get("RESOURCE_GROUP","")
        self._subscription_id = os.environ.get("SUBSCRIPTION_ID","")
        self._workspace_name = os.environ.get("WORKSPACE_NAME","")
        
        regex_replacer = RegexReplacerProcessor()
        recording_processors = []
        recording_processors.append(regex_replacer)
        recording_processors.append(AccessTokenReplacer())
        replay_processors = recording_processors
        
        super(QuantumTestBase, self).__init__(method_name, recording_processors=recording_processors, replay_processors=replay_processors)

        if self.in_recording or self.is_live:
            assert len(self.client_id)>0, "AZURE_CLIENT_ID not found in environment variables."
            assert len(self.client_secret)>0, "AZURE_CLIENT_SECRET not found in environment variables."
            assert len(self.tenant_id)>0, "AZURE_TENANT_ID not found in environment variables."
            assert len(self.resource_group)>0, "RESOURCE_GROUP not found in environment variables."
            assert len(self.subscription_id)>0, "SUBSCRIPTION_ID not found in environment variables."
            assert len(self.workspace_name)>0, "WORKSPACE_NAME not found in environment variables."
        else:
            self._client_id = self.dummy_uid
            self._client_secret = self.dummy_clientsecret
            self._tenant_id = self.dummy_uid
            self._resource_group = self.dummy_rg
            self._subscription_id = self.dummy_uid
            self._workspace_name = self.dummy_ws

        regex_replacer.register_name_pair(self.client_id, self.dummy_uid)
        regex_replacer.register_name_pair(self.client_secret, self.dummy_clientsecret)
        regex_replacer.register_name_pair(self.tenant_id, self.dummy_uid)
        regex_replacer.register_name_pair(self.subscription_id, self.dummy_uid)
        regex_replacer.register_name_pair(self.workspace_name, self.dummy_ws)
        regex_replacer.register_name_pair(self.resource_group, self.dummy_rg)
        regex_replacer.register_name_pair(r'/subscriptions/([a-f0-9]+[-]){4}[a-f0-9]+', "/subscriptions/" + self.dummy_uid)
        regex_replacer.register_name_pair(r'job-([a-f0-9]+[-]){4}[a-f0-9]+', "job-" + self.dummy_uid)
        regex_replacer.register_name_pair(r'jobs/([a-f0-9]+[-]){4}[a-f0-9]+', "jobs/" + self.dummy_uid)
        regex_replacer.register_name_pair(r'"id":\s*"([a-f0-9]+[-]){4}[a-f0-9]+"', '"id": "{}"'. format(self.dummy_uid))
        regex_replacer.register_name_pair(r'/resourceGroups/[a-z0-9-]+/', "/resourceGroups/dummy-rg/")
        regex_replacer.register_name_pair(r'/workspaces/[a-z0-9-]+/', "/workspaces/dummy-ws/")
        regex_replacer.register_name_pair(r'sig=[0-9a-zA-Z%]+\&', "sig=sanitized&")

    def setUp(self):
        super(QuantumTestBase, self).setUp()
        # mitigation for issue https://github.com/kevin1024/vcrpy/issues/533
        self.cassette.allow_playback_repeats = True

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
    def subscription_id(self):
        return self._subscription_id

    @property
    def workspace_name(self):
        return self._workspace_name


    def create_workspace_mock_login(self, **kwds) -> Workspace:
        """Create a mock Workspace object by patching the Azure authentication and uses a dummy authentication token."""
        workspace = Workspace(**kwds)

        dummy_auth_token = {'access_token': 'eyJ1eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJidWQiOiJodHRwczovL3F1YW50dW0ubWljcm9zb2Z0LmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJpYXQiOjE2MTE2ODMwNjAsIm5iZiI6MTYxMTY4MzA2MCwiZXhwIjoxNjExNjg2OTYwLCJfY2xhaW1fbmFtZXMiOnsiZ3JvdXBzIjoic3JjMSJ9LCJfY2xhaW1fc291cmNlcyI6eyJzcmMxIjp7ImVuZHBvaW50IjoiaHR0cHM6Ly9ncmFwaC53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvdXNlcnMvZTlhNGE5ZTEtODcxNS00Yjc1LTk2NWQtYzBkZDQxMTIzODY4L2dldE1lbWJlck9iamVjdHMifX0sImFjciI6IjEiLCJhaW8iOiJBVlFBcS84U0FBQUFXMnNsMlRORXd5eXA2OGdvejM2RnRoSXFZSlJDdmRibDF0WVJPanUrUzNCZDV5MGsyeWMyOFdKUk9IQ283a0VuNGRpaDh1dkpLQm00TFNoTHRUQ3FsMHMwNkp6N3NYclNpNTFJOEljZThZcz0iLCJhbXIiOlsid2lhIiwibWZhIl0sImFwcGlkIjoiODRiYTA5NDctNmM1My00ZGQyLTljYTktYjM2OTQ3NjE1MjFiIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJCcm93biIsImdpdmVuX25hbWUiOiJUb20iLCJpbl9jb3JwIjoidHJ1ZSIsImlwYWRkciI6IjczLjgzLjM5LjEwIiwibmFtZSI6IlRvbSBCcm93biIsIm9pZCI6ImU5YTRhOWUxLTg3MTUtNGI3NS05NjVkLWMwZGQ0MTEyMzg2OCIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0yMTI3NTIxMTg0LTE2MDQwMTI5MjAtMTg4NzkyNzUyNy0xNzc1MDU1MSIsInB1aWQiOiIxMDAzN0ZGRTkyREI4MzEyIiwicmgiOiIwLkFSb0F2NGo1Y3ZHR3IwR1JxeTE4MEJIYlIwY0p1b1JUYk5KTm5LbXphVWRoVWhzYUFPOC4iLCJzY3AiOiJKb2JzLlJlYWRXcml0ZSIsInN1YiI6IjNxVk1XZ3cxRWozYVRlTEdTenE0bmVsMms1UHFVS1BBY2ZVNDBSUl9JZ3MiLCJ0aWQiOiI3MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDciLCJ1bmlxdWVfbmFtZSI6InRoYnJvQG1pY3Jvc29mdC5jb20iLCJ1cG4iOiJ0aGJyb0BtaWNyb3NvZnQuY29tIiwidXRpIjoiUzMxNVVqbk9JVWUzeDdRR3ZaVWFBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il19.PCWEtCdso3_jehm3Ppg9lCSy_VgwY96IG0_Lqji5tN3yEmBmsP4Du-6MA2IHlz7pbKfQ8Qdw4aeobWZkuDW71Zo9PCkBSLQewng5EMbDvZO3jPJfCOd0IepaPVdtvtaCL2KnPEZicEM4kIO_9f8hCC4Ik8MAem788HuutNhN_YExJDWtM-aNoXIBLtDm39u3bCr2WFk4he3xpISLD3ZqAk2UPKagMwuwO-tArtcoQvA1_n_owv-I5P8vEk1wOmUh6LTB6pUAIS4wFIMgINUE1dBSuQmyimEfc7rRuWl-YJrMH0WRdbgFutwbBv_5dKs6VcYGgrvA3nIGU_Xz5vuJMA', 'token_type': 'Bearer', 'expires_in': 485}
        with unittest.mock.patch.object(MsalWrapper, 'acquire_auth_token', return_value=dummy_auth_token):
            workspace.login(True)

        return workspace


    def create_workspace(self) -> Workspace:
        """Create workspace using credentials stored in config file

        :return: Workspace
        :rtype: Workspace
        """

        if self.is_live or self.in_recording:
            workspace = Workspace(
            
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
            )
            workspace.credentials = ServicePrincipalCredentials(
                tenant=self.tenant_id,
                client_id=self.client_id,
                secret=self.client_secret,
                resource  = "https://quantum.microsoft.com"
            )
            workspace.login(False)
        else:
            workspace = self.create_workspace_mock_login(
                subscription_id=self.dummy_uid,
                resource_group=self.dummy_rg,
                name=self.dummy_ws,
            )
            workspace.credentials = ServicePrincipalCredentials(
                tenant=self.tenant_id,
                client_id=self.client_id,
                secret=self.client_secret,
                resource  = "https://quantum.microsoft.com"
            )

        return workspace

class RegexReplacerProcessor(RecordingProcessor):
    def __init__(self):
        self._regexes = []

    def register_name_pair(self, oldRegex, new):
        self._regexes.append((re.compile(oldRegex), new))

    def process_request(self, request):
        for oldRegex, new in self._regexes:
            request.uri = oldRegex.sub(new, request.uri)            

        if _get_content_type(request) == "application/x-www-form-urlencoded":
            body = request.body.decode("utf-8")
            for oldRegex, new in self._regexes:
                body = oldRegex.sub(new, body)
            request.body = body.encode("utf-8")

            # splits = [p.partition(b"=") for p in request.body.split(b"&")]
            # new_splits = []
            # for key, separator, value in splits:
            #     if separator is None:
            #         new_splits.append((key, separator, value))
            #     else:
            #         str_value = value.decode("utf-8")
            #         for oldRegex, new in self._regexes:
            #             str_value = oldRegex.sub(new, str_value)
            #         value = str_value.encode("utf-8")
            #         new_splits.append((key, separator, value))
            # request.body = b"&".join(k if sep is None else b"".join([k, sep, v]) for k, sep, v in new_splits)
        else:
            body = str(request.body)
            for oldRegex, new in self._regexes:
                body = oldRegex.sub(new, body)
            request.body = body

        return request

    def process_response(self, response):
        import six

        if is_text_payload(response):
            body = response['body']['string']
            if not isinstance(body, six.string_types):
                body = body.decode("utf-8")
            if is_text_payload(response) and body:
                for oldRegex, new in self._regexes:
                    body = oldRegex.sub(new, body)            
                response['body']['string'] = body

        if isinstance(response['body']['string'], six.string_types):
            #response['body']['string'] = io.BytesIO(response['body']['string'].encode("utf-8"))
            response['body']['string'] = response['body']['string'].encode("utf-8")

        return response