from common import QuantumTestBase
from azure.quantum.workspace import Workspace
import os
from unittest import mock

class TestConnectionString(QuantumTestBase):
    def test_parse_connection_string(self):
        workspace = Workspace.from_connection_string("SubscriptionId=17a12c5a-df19-48c6-9ceb-b476d0265a01;ResourceGroupName=someRG;WorkspaceName=csWS;ApiKey=FakeKey;QuantumEndpoint=https://westus.quantum.azure.com/;")
        authentication_policy = workspace.kwargs.get("authentication_policy")
        key_credential_name = authentication_policy._name
        key_credential = authentication_policy._credential
        assert workspace.credentials == "FakeKey"
        assert workspace.location == "westus"
        assert authentication_policy != None
        assert "x-ms-quantum-api-key" == key_credential_name
        assert "FakeKey" == key_credential.key

    def test_env_connection_string(self):
        with mock.patch.dict(os.environ, {"AZURE_QUANTUM_CONNECTION_STRING": "SubscriptionId=17a12c5a-df19-48c6-9ceb-b476d0265a01;ResourceGroupName=someRG;WorkspaceName=csWS;ApiKey=FakeKey;QuantumEndpoint=https://westus.quantum.azure.com/;"}):
            workspace = Workspace()
            authentication_policy = workspace.kwargs.get("authentication_policy")
            key_credential_name = authentication_policy._name
            key_credential = authentication_policy._credential
            assert workspace.credentials == "FakeKey"
            assert workspace.location == "westus"
            assert authentication_policy != None
            assert "x-ms-quantum-api-key" == key_credential_name
            assert "FakeKey" == key_credential.key
