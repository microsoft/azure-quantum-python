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
from common import QuantumTestBase
from azure.identity import (
    CredentialUnavailableError,
    ClientSecretCredential,
    InteractiveBrowserCredential,
)
from azure.quantum._authentication import (
    _TokenFileCredential,
    _DefaultAzureCredential,
)
from azure.quantum import Workspace
from azure.quantum._constants import (
    EnvironmentVariables,
    DATA_PLANE_CREDENTIAL_SCOPE,
    VALID_CONNECTION_STRING,
)


class TestWorkspace(QuantumTestBase):
    def test_azure_quantum_token_credential_file_not_set(self):
        credential = _TokenFileCredential()
        with pytest.raises(CredentialUnavailableError) as exception:
            credential.get_token(DATA_PLANE_CREDENTIAL_SCOPE)
        self.assertIn("Token file location not set.", str(exception.value))

    def test_azure_quantum_token_credential_file_not_exists(self):
        with patch.dict(os.environ,
                        {EnvironmentVariables.QUANTUM_TOKEN_FILE: "fake_file_path"},
                        clear=True):
            with patch('os.path.isfile') as mock_isfile:
                mock_isfile.return_value = False
                credential = _TokenFileCredential()
                with pytest.raises(CredentialUnavailableError) as exception:
                    credential.get_token(DATA_PLANE_CREDENTIAL_SCOPE)
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
                credential.get_token(DATA_PLANE_CREDENTIAL_SCOPE)
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
                credential.get_token(DATA_PLANE_CREDENTIAL_SCOPE)
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
                credential.get_token(DATA_PLANE_CREDENTIAL_SCOPE)
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
            token = credential.get_token(DATA_PLANE_CREDENTIAL_SCOPE)
        self.assertEqual(token.token, "fake_token")
        self.assertEqual(token.expires_on, pytest.approx(one_hour_ahead))


    def test_workspace_auth_token_credential(self):
        with patch.dict(os.environ):
            self.clear_env_var(os.environ)
            connection_params = self.connection_params
            credential = ClientSecretCredential(connection_params.tenant_id,
                                                connection_params.client_id,
                                                connection_params.client_secret)
            token = credential.get_token(DATA_PLANE_CREDENTIAL_SCOPE)
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

    def test_workspace_auth_client_secret_credential(self):
        with patch.dict(os.environ):
            self.clear_env_var(os.environ)
            connection_params = self.connection_params
            credential = ClientSecretCredential(
                tenant_id=connection_params.tenant_id,
                client_id=connection_params.client_id,
                client_secret=connection_params.client_secret,
                validate_authority=False)
            workspace = self.create_workspace(credential=credential)
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)

    def test_workspace_auth_default_credential(self):
        with patch.dict(os.environ):
            self.clear_env_var(os.environ)
            connection_params = self.connection_params
            os.environ[EnvironmentVariables.AZURE_CLIENT_ID] = \
                connection_params.client_id
            os.environ[EnvironmentVariables.AZURE_CLIENT_SECRET] = \
                connection_params.client_secret
            os.environ[EnvironmentVariables.AZURE_TENANT_ID] = \
                connection_params.tenant_id
            credential = _DefaultAzureCredential(
                subscription_id=connection_params.subscription_id,
                arm_base_url=connection_params.arm_base_url)
            workspace = self.create_workspace(credential=credential)
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)

    @pytest.mark.skip(reason="Only to be used in manual testing")
    def test_workspace_auth_interactive_credential(self):
        with patch.dict(os.environ):
            self.clear_env_var(os.environ)
            connection_params = self.connection_params
            credential = InteractiveBrowserCredential(
                tenant_id=connection_params.tenant_id)
            workspace = self.create_workspace(credential=credential)
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)

    def _get_current_primary_api_key(self):
        # self.pause_recording()
        http = urllib3.PoolManager()
        connection_params = self.connection_params
        url = ("https://api-dogfood.resources.windows-int.net" +
               f"/subscriptions/{connection_params.subscription_id}" + 
               f"/resourceGroups/{connection_params.resource_group}" +
               "/providers/microsoft.quantum" +
               f"/Workspaces/{connection_params.workspace_name}" +
               "/listKeys?api-version=2023-11-13-preview")
        url = "https://api-dogfood.resources.windows-int.net/subscriptions/653caf24-0fdb-4486-8ab1-75314330bb8f/resourceGroups/dogfoodRG/providers/microsoft.quantum/Workspaces/DogfoodConnectionString?api-version=2022-01-10-preview"
        credential = self.connection_params.get_credential_or_default()
        scope = "https://management.azure.com/.default"
        token = credential.get_token(scope).token
        response = http.request(
            method="GET",
            url=url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        self.resume_recording()
        return ""

    @pytest.mark.skip()
    def test_workspace_auth_api_key_credential(self):
        api_key = self._get_current_primary_api_key()
        with patch.dict(os.environ):
            self.clear_env_var(os.environ)
            connection_params = self.connection_params
            connection_string =  VALID_CONNECTION_STRING(
                subscription_id=connection_params.subscription_id,
                resource_group=connection_params.resource_group,
                workspace_name=connection_params.workspace_name,
                api_key=api_key,
                quantum_endpoint=connection_params.base_url
            )
            workspace = Workspace.from_connection_string(
                connection_string=connection_string,
                api_version="2023-11-13-preview",
            )
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)

    @pytest.mark.skip()
    def test_workspace_auth_invalid_api_key_credential(self):
        api_key = "invalid_key"
        with patch.dict(os.environ):
            self.clear_env_var(os.environ)
            connection_params = self.connection_params
            connection_string =  VALID_CONNECTION_STRING(
                subscription_id=connection_params.subscription_id,
                resource_group=connection_params.resource_group,
                workspace_name=connection_params.workspace_name,
                api_key=api_key,
                quantum_endpoint=connection_params.base_url
            )
            workspace = Workspace.from_connection_string(
                connection_string=connection_string,
                api_version="2023-11-13-preview",
            )
            targets = workspace.get_targets()
            self.assertGreater(len(targets), 1)
