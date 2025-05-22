##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from pathlib import Path
from unittest.mock import patch
import json
import os
import time
import urllib3
import pytest
from common import (
    QuantumTestBase,
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
    LOCATION,
    API_KEY,
)
from azure.identity import (
    CredentialUnavailableError,
    ClientSecretCredential,
    InteractiveBrowserCredential,
)
from azure.quantum import Workspace
from azure.quantum._authentication import (
    _TokenFileCredential,
    _DefaultAzureCredential,
)
from azure.quantum._constants import (
    EnvironmentVariables,
    ConnectionConstants,
)


class TestWorkspace(QuantumTestBase):
    def test_azure_quantum_token_credential_file_not_set(self):
        credential = _TokenFileCredential()
        with pytest.raises(CredentialUnavailableError) as exception:
            credential.get_token(ConnectionConstants.DATA_PLANE_CREDENTIAL_SCOPE)
        self.assertIn("Token file location not set.", str(exception.value))

    def test_azure_quantum_token_credential_file_not_exists(self):
        with patch.dict(os.environ,
                        {EnvironmentVariables.QUANTUM_TOKEN_FILE: "fake_file_path"},
                        clear=True):
            with patch('os.path.isfile') as mock_isfile:
                mock_isfile.return_value = False
                credential = _TokenFileCredential()
                with pytest.raises(CredentialUnavailableError) as exception:
                    credential.get_token(ConnectionConstants.DATA_PLANE_CREDENTIAL_SCOPE)
                self.assertIn("Token file at fake_file_path does not exist.",
                              str(exception.value))

    def test_azure_quantum_token_credential_file_invalid_json(self):
        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text("not a json")
        with patch.dict(os.environ,
                        {EnvironmentVariables.QUANTUM_TOKEN_FILE: str(file.resolve())},
                        clear=True):
            credential = _TokenFileCredential()
            with pytest.raises(CredentialUnavailableError) as exception:
                credential.get_token(ConnectionConstants.DATA_PLANE_CREDENTIAL_SCOPE)
            self.assertIn("Failed to parse token file: Invalid JSON.",
                          str(exception.value))

    def test_azure_quantum_token_credential_file_missing_expires_on(self):
        content = {
            "access_token": "fake_token",
        }
        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text(json.dumps(content))
        with patch.dict(os.environ,
                        {EnvironmentVariables.QUANTUM_TOKEN_FILE: str(file.resolve())},
                        clear=True):
            credential = _TokenFileCredential()
            with pytest.raises(CredentialUnavailableError) as exception:
                credential.get_token(ConnectionConstants.DATA_PLANE_CREDENTIAL_SCOPE)
            self.assertIn("Failed to parse token file: " +
                          "Missing expected value: 'expires_on'""",
                          str(exception.value))

    def test_azure_quantum_token_credential_file_token_expired(self):
        content = {
            "access_token": "fake_token",
            # Matches timestamp in error message below
            "expires_on": 1628543125086
        }
        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text(json.dumps(content))
        with patch.dict(os.environ,
                        {EnvironmentVariables.QUANTUM_TOKEN_FILE: str(file.resolve())},
                        clear=True):
            credential = _TokenFileCredential()
            with pytest.raises(CredentialUnavailableError) as exception:
                credential.get_token(ConnectionConstants.DATA_PLANE_CREDENTIAL_SCOPE)
            self.assertIn("Token already expired at Mon Aug  9 21:05:25 2021",
                          str(exception.value))

    def test_azure_quantum_token_credential_file_valid_token(self):
        one_hour_ahead = time.time() + 60*60
        content = {
            "access_token": "fake_token",
            "expires_on": one_hour_ahead * 1000  # Convert to milliseconds
        }

        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text(json.dumps(content))
        with patch.dict(os.environ,
                        {EnvironmentVariables.QUANTUM_TOKEN_FILE: str(file.resolve())},
                        clear=True):
            credential = _TokenFileCredential()
            token = credential.get_token(ConnectionConstants.DATA_PLANE_CREDENTIAL_SCOPE)
        self.assertEqual(token.token, "fake_token")
        self.assertEqual(token.expires_on, pytest.approx(one_hour_ahead))

    @pytest.mark.live_test
    def test_workspace_auth_token_credential(self):
        with patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            connection_params = self.connection_params

            os.environ[EnvironmentVariables.AZURE_CLIENT_ID] = \
                connection_params.client_id
            os.environ[EnvironmentVariables.AZURE_TENANT_ID] = \
                connection_params.tenant_id

            if self.in_recording and os.path.exists(self._client_certificate_path):
                os.environ[EnvironmentVariables.AZURE_CLIENT_CERTIFICATE_PATH] = \
                    self._client_certificate_path
                os.environ[EnvironmentVariables.AZURE_CLIENT_SEND_CERTIFICATE_CHAIN] = \
                    self._client_send_certificate_chain
            else:
                os.environ[EnvironmentVariables.AZURE_CLIENT_SECRET] = \
                    self._client_secret
            
            credential = _DefaultAzureCredential(
                subscription_id=connection_params.subscription_id,
                arm_endpoint=connection_params.arm_endpoint,
                tenant_id=connection_params.tenant_id)
            
            token = credential.get_token(ConnectionConstants.DATA_PLANE_CREDENTIAL_SCOPE)
            content = {
                "access_token": token.token,
                "expires_on": token.expires_on * 1000
            }
            tmpdir = self.create_temp_dir()
            file = Path(tmpdir) / "token.json"
            try:
                file.write_text(json.dumps(content))
                with patch.dict(os.environ,
                                {EnvironmentVariables.QUANTUM_TOKEN_FILE: str(file.resolve())},
                                clear=True):
                    credential = _TokenFileCredential()
                    workspace = self.create_workspace(credential=credential)
                    targets = workspace.get_targets()
                    self.assertGreater(len(targets), 1)
            finally:
                os.remove(file)

    @pytest.mark.live_test
    def test_workspace_auth_client_secret_credential(self):
        client_secret = os.environ.get(EnvironmentVariables.AZURE_CLIENT_SECRET)
        if not client_secret:
            pytest.skip("Skipping the test as no Client Secret was provided")

        with patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            connection_params = self.connection_params
            credential = ClientSecretCredential(
                tenant_id=connection_params.tenant_id,
                client_id=connection_params.client_id,
                client_secret=client_secret)
            workspace = self.create_workspace(credential=credential)
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)

    @pytest.mark.live_test
    def test_workspace_auth_default_credential(self):
        with patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            connection_params = self.connection_params
            
            os.environ[EnvironmentVariables.AZURE_CLIENT_ID] = \
                connection_params.client_id
            os.environ[EnvironmentVariables.AZURE_TENANT_ID] = \
                connection_params.tenant_id

            if self.in_recording and os.path.exists(self._client_certificate_path):
                os.environ[EnvironmentVariables.AZURE_CLIENT_CERTIFICATE_PATH] = \
                    self._client_certificate_path
                os.environ[EnvironmentVariables.AZURE_CLIENT_SEND_CERTIFICATE_CHAIN] = \
                    self._client_send_certificate_chain
            else:
                os.environ[EnvironmentVariables.AZURE_CLIENT_SECRET] = \
                    self._client_secret

            credential = _DefaultAzureCredential(
                subscription_id=connection_params.subscription_id,
                arm_endpoint=connection_params.arm_endpoint,
                tenant_id=connection_params.tenant_id)
                
            workspace = self.create_workspace(credential=credential)
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)

    @pytest.mark.skip(reason="Only to be used in manual testing")
    @pytest.mark.live_test
    def test_workspace_auth_interactive_credential(self):
        with patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            connection_params = self.connection_params
            credential = InteractiveBrowserCredential(
                tenant_id=connection_params.tenant_id)
            workspace = self.create_workspace(credential=credential)
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)

    def _get_rp_credential(self):
        connection_params = self.connection_params
        # We have to use DefaultAzureCredential to avoid using ApiKeyCredential
        credential = _DefaultAzureCredential(
                    subscription_id=connection_params.subscription_id,
                    arm_endpoint=connection_params.arm_endpoint,
                    tenant_id=connection_params.tenant_id)
        scope = ConnectionConstants.ARM_CREDENTIAL_SCOPE
        token = credential.get_token(scope).token
        return token
    
    def _get_workspace(self, token: str):
        http = urllib3.PoolManager()
        connection_params = self.connection_params
        resource_id = ConnectionConstants.VALID_RESOURCE_ID(
            subscription_id=connection_params.subscription_id,
            resource_group=connection_params.resource_group,
            workspace_name=connection_params.workspace_name,
        )
        url = (connection_params.arm_endpoint.rstrip('/') +
               f"{resource_id}?api-version=2023-11-13-preview")
        
        # Get workspace object
        response = http.request(
            method="GET",
            url=url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        self.assertEqual(response.status, 200,
                         f"""
                         {url} failed with error code {response.status}.
                         Make sure the environment variables are correctly
                         set with the workspace connection parameters.
                         """)
        workspace = json.loads(response.data.decode("utf-8"))
        return workspace
    
    def _enable_workspace_api_keys(self, token: str, workspace: dict, enable_api_keys: bool):
        http = urllib3.PoolManager()
        # enable api key
        workspace["properties"]["apiKeyEnabled"] = enable_api_keys
        workspace_json = json.dumps(workspace)

        connection_params = self.connection_params
        resource_id = ConnectionConstants.VALID_RESOURCE_ID(
            subscription_id=connection_params.subscription_id,
            resource_group=connection_params.resource_group,
            workspace_name=connection_params.workspace_name,
        )
        url = (connection_params.arm_endpoint.rstrip('/') +
               f"{resource_id}?api-version=2023-11-13-preview")
        response = http.request(
            method="PUT",
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  # Assuming workspace is JSON data
            },
            body=workspace_json
        )
        self.assertEqual(response.status, 201,
                         f"""
                         {url} failed with error code {response.status}.
                         Failed to enable/disable api key.
                         """)
        
    def _get_current_primary_connection_string(self, token: str):
        # list keys
        http = urllib3.PoolManager()
        connection_params = self.connection_params
        resource_id = ConnectionConstants.VALID_RESOURCE_ID(
            subscription_id=connection_params.subscription_id,
            resource_group=connection_params.resource_group,
            workspace_name=connection_params.workspace_name,
        )
        url = (connection_params.arm_endpoint.rstrip('/') +
               f"{resource_id}/listKeys?api-version=2023-11-13-preview")
        response = http.request(
            method="POST",
            url=url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        self.assertEqual(response.status, 200,
                         f"""
                         {url} failed with error code {response.status}.
                         Make sure the environment variables are correctly
                         set with the workspace connection parameters.
                         """)
        connection_strings = json.loads(response.data.decode("utf-8"))
        self.assertTrue(connection_strings['apiKeyEnabled'],
                        f"""
                        API-Key is not enabled in workspace {resource_id}
                        """)
        connection_string = connection_strings['primaryConnectionString']
        self.assertIsNotNone(connection_string,
                             f"""
                             primaryConnectionString is empty or does not exist
                             in workspace {resource_id}
                             """)
        return connection_string

    @pytest.mark.live_test
    def test_workspace_auth_connection_string_api_key(self):
        connection_string = ""

        if self.is_playback:
            connection_string = ConnectionConstants.VALID_CONNECTION_STRING(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                workspace_name=WORKSPACE,
                api_key=API_KEY,
                quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(LOCATION))
        else:
            self.pause_recording()
            token = self._get_rp_credential()
            workspace = self._get_workspace(token)
            self._enable_workspace_api_keys(token, workspace, True)
            time.sleep(10)
            connection_string = self._get_current_primary_connection_string(token)
            self.resume_recording()
            # Sleep 1 min for cache to be cleared
            time.sleep(60)

        with patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            workspace = Workspace.from_connection_string(
                connection_string=connection_string,
            )
            jobs_paged = workspace.list_jobs_paginated()
            assert jobs_paged.next() is not None

        if not self.is_playback:
            self.pause_recording()
            token = self._get_rp_credential()
            workspace = self._get_workspace(token)
            self._enable_workspace_api_keys(token, workspace, False)
            self.resume_recording()
            # Sleep 1 min for cache to be cleared
            time.sleep(60)

        with patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            workspace = Workspace.from_connection_string(
                connection_string=connection_string,
            )
            with self.assertRaises(Exception) as context:
                workspace.list_jobs_paginated().next()

            self.assertIn("Unauthorized", context.exception.message)
