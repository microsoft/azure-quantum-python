##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import os
from unittest import mock
from azure.quantum.job.job import Job
from azure.quantum._client.models import JobDetails
from azure.quantum._constants import EnvironmentVariables, ConnectionConstants
from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.policies import AzureKeyCredentialPolicy
from azure.identity import EnvironmentCredential

from mock_client import WorkspaceMock, MockWorkspaceMgmtClient
from common import (
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
    LOCATION,
    STORAGE,
    API_KEY,
    ENDPOINT_URI,
)

SIMPLE_RESOURCE_ID = ConnectionConstants.VALID_RESOURCE_ID(
    subscription_id=SUBSCRIPTION_ID,
    resource_group=RESOURCE_GROUP,
    workspace_name=WORKSPACE,
)

SIMPLE_CONNECTION_STRING = ConnectionConstants.VALID_CONNECTION_STRING(
    subscription_id=SUBSCRIPTION_ID,
    resource_group=RESOURCE_GROUP,
    workspace_name=WORKSPACE,
    api_key=API_KEY,
    quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(LOCATION),
)

SIMPLE_CONNECTION_STRING_V2 = ConnectionConstants.VALID_CONNECTION_STRING(
    subscription_id=SUBSCRIPTION_ID,
    resource_group=RESOURCE_GROUP,
    workspace_name=WORKSPACE,
    api_key=API_KEY,
    quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT_v2(LOCATION)
)


def test_create_workspace_instance_valid():
    def assert_all_required_params(ws: WorkspaceMock):
        assert ws.subscription_id == SUBSCRIPTION_ID
        assert ws.resource_group == RESOURCE_GROUP
        assert ws.name == WORKSPACE
        assert ws.location == LOCATION
        assert ws._connection_params.quantum_endpoint == ENDPOINT_URI
    
    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
    )
    assert_all_required_params(ws)

    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
        storage=STORAGE,
    )
    assert_all_required_params(ws)
    assert ws.storage == STORAGE

    ws = WorkspaceMock(
        resource_id=SIMPLE_RESOURCE_ID,
    )
    assert_all_required_params(ws)

    ws = WorkspaceMock(
        resource_id=SIMPLE_RESOURCE_ID,
        storage=STORAGE,
    )
    assert_all_required_params(ws)
    assert ws.storage == STORAGE

    ws = WorkspaceMock(
        name=WORKSPACE,
    )
    assert_all_required_params(ws)

    ws = WorkspaceMock(
        name=WORKSPACE,
        storage=STORAGE,
    )
    assert_all_required_params(ws)
    assert ws.storage == STORAGE

    ws = WorkspaceMock(
        name=WORKSPACE,
        location=LOCATION,
    )
    assert_all_required_params(ws)

    ws = WorkspaceMock(
        name=WORKSPACE,
        subscription_id=SUBSCRIPTION_ID,
    )
    assert_all_required_params(ws)

    ws = WorkspaceMock(
        name=WORKSPACE,
        subscription_id=SUBSCRIPTION_ID,
        location=LOCATION,
    )
    assert_all_required_params(ws)

    ws = WorkspaceMock(
        name=WORKSPACE,
        resource_group=RESOURCE_GROUP,
    )
    assert_all_required_params(ws)

    ws = WorkspaceMock(
        name=WORKSPACE,
        resource_group=RESOURCE_GROUP,
        location=LOCATION,
    )
    assert_all_required_params(ws)


def test_create_workspace_locations():
    # Location name should be normalized
    _mgmt_client = MockWorkspaceMgmtClient()
    def mock_load_workspace_from_arm(connection_params):
        connection_params.location = "East US"
        connection_params.quantum_endpoint = ENDPOINT_URI
    _mgmt_client.load_workspace_from_arm = mock_load_workspace_from_arm
    
    ws = WorkspaceMock(
        name=WORKSPACE,
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        location="East US",
        _mgmt_client=_mgmt_client,
    )
    assert ws.location == "eastus"


def test_env_connection_string():
    with mock.patch.dict(os.environ):
        # Clear env vars then set connection string
        os.environ.clear()
        os.environ[EnvironmentVariables.CONNECTION_STRING] = SIMPLE_CONNECTION_STRING

        workspace = WorkspaceMock()
        assert workspace.location == LOCATION
        assert workspace.subscription_id == SUBSCRIPTION_ID
        assert workspace.name == WORKSPACE
        assert workspace.resource_group == RESOURCE_GROUP
        assert isinstance(workspace.credential, AzureKeyCredential)
        assert workspace.credential.key == API_KEY
        # pylint: disable=protected-access
        assert isinstance(
            workspace._client._config.authentication_policy, AzureKeyCredentialPolicy
        )
        auth_policy = workspace._client._config.authentication_policy
        assert auth_policy._name == ConnectionConstants.QUANTUM_API_KEY_HEADER
        assert id(auth_policy._credential) == id(workspace.credential)


def test_workspace_from_connection_string():
    with mock.patch.dict(os.environ):
        os.environ.clear()
        workspace = WorkspaceMock.from_connection_string(SIMPLE_CONNECTION_STRING)
        assert workspace.location == LOCATION
        assert isinstance(workspace.credential, AzureKeyCredential)
        assert workspace.credential.key == API_KEY
        # pylint: disable=protected-access
        assert isinstance(
            workspace._client._config.authentication_policy, AzureKeyCredentialPolicy
        )
        auth_policy = workspace._client._config.authentication_policy
        assert auth_policy._name == ConnectionConstants.QUANTUM_API_KEY_HEADER
        assert id(auth_policy._credential) == id(workspace.credential)

    # Ensure env var overrides behave as original tests expect
    with mock.patch.dict(os.environ):
        os.environ.clear()

        wrong_subscription_id = "00000000-2BAD-2BAD-2BAD-000000000000"
        wrong_resource_group = "wrongrg"
        wrong_workspace = "wrong-workspace"
        wrong_location = "westus"

        wrong_connection_string = ConnectionConstants.VALID_CONNECTION_STRING(
            subscription_id=wrong_subscription_id,
            resource_group=wrong_resource_group,
            workspace_name=wrong_workspace,
            api_key=API_KEY,
            quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(
                wrong_location
            ),
        )

        os.environ[EnvironmentVariables.CONNECTION_STRING] = wrong_connection_string
        os.environ[EnvironmentVariables.LOCATION] = LOCATION
        os.environ[EnvironmentVariables.SUBSCRIPTION_ID] = SUBSCRIPTION_ID
        os.environ[EnvironmentVariables.RESOURCE_GROUP] = RESOURCE_GROUP
        os.environ[EnvironmentVariables.WORKSPACE_NAME] = WORKSPACE

        workspace = WorkspaceMock()
        assert workspace.location == LOCATION
        assert workspace.subscription_id == SUBSCRIPTION_ID
        assert workspace.resource_group == RESOURCE_GROUP
        assert workspace.name == WORKSPACE
        assert isinstance(workspace.credential, AzureKeyCredential)

        # If a credential is passed, it should be used
        workspace = WorkspaceMock(credential=EnvironmentCredential())
        assert isinstance(workspace.credential, EnvironmentCredential)

        # Parameter connection string should override env var
        os.environ.clear()
        os.environ[EnvironmentVariables.CONNECTION_STRING] = wrong_connection_string
        connection_string = ConnectionConstants.VALID_CONNECTION_STRING(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            workspace_name=WORKSPACE,
            api_key=API_KEY,
            quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(
                LOCATION
            ),
        )
        workspace = WorkspaceMock.from_connection_string(connection_string)
        assert workspace.location == LOCATION
        assert workspace.subscription_id == SUBSCRIPTION_ID
        assert workspace.resource_group == RESOURCE_GROUP
        assert workspace.name == WORKSPACE

        # Bad env var connection string should not be parsed if not needed
        os.environ.clear()
        os.environ[EnvironmentVariables.CONNECTION_STRING] = "bad-connection-string"
        connection_string = ConnectionConstants.VALID_CONNECTION_STRING(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            workspace_name=WORKSPACE,
            api_key=API_KEY,
            quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(
                LOCATION
            ),
        )
        workspace = WorkspaceMock.from_connection_string(connection_string)
        assert workspace.location == LOCATION
        assert workspace.subscription_id == SUBSCRIPTION_ID
        assert workspace.resource_group == RESOURCE_GROUP
        assert workspace.name == WORKSPACE

def test_workspace_from_connection_string_v2():
    """Test that v2 QuantumEndpoint format is correctly parsed."""
    with mock.patch.dict(
        os.environ,
        clear=True
    ):
        workspace = WorkspaceMock.from_connection_string(SIMPLE_CONNECTION_STRING_V2)
        assert workspace.location == LOCATION
        assert workspace.subscription_id == SUBSCRIPTION_ID
        assert workspace.resource_group == RESOURCE_GROUP
        assert workspace.name == WORKSPACE
        assert isinstance(workspace.credential, AzureKeyCredential)
        assert workspace.credential.key == API_KEY
        # pylint: disable=protected-access
        assert isinstance(
            workspace._client._config.authentication_policy,
            AzureKeyCredentialPolicy)
        auth_policy = workspace._client._config.authentication_policy
        assert auth_policy._name == ConnectionConstants.QUANTUM_API_KEY_HEADER
        assert id(auth_policy._credential) == id(workspace.credential)

def test_workspace_from_connection_string_v2_dogfood():
    """Test v2 QuantumEndpoint with dogfood environment."""
    canary_location = "eastus2euap"
    dogfood_connection_string_v2 = ConnectionConstants.VALID_CONNECTION_STRING(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
        api_key=API_KEY,
        quantum_endpoint=ConnectionConstants.GET_QUANTUM_DOGFOOD_ENDPOINT_v2(canary_location)
    )
    
    with mock.patch.dict(os.environ, clear=True):
        workspace = WorkspaceMock.from_connection_string(dogfood_connection_string_v2)
        assert workspace.location == canary_location
        assert workspace.subscription_id == SUBSCRIPTION_ID
        assert workspace.resource_group == RESOURCE_GROUP
        assert workspace.name == WORKSPACE
        assert isinstance(workspace.credential, AzureKeyCredential)
        assert workspace.credential.key == API_KEY

def test_env_connection_string_v2():
    """Test v2 QuantumEndpoint from environment variable."""
    with mock.patch.dict(os.environ):
        os.environ.clear()
        os.environ[EnvironmentVariables.CONNECTION_STRING] = SIMPLE_CONNECTION_STRING_V2

        workspace = WorkspaceMock()
        assert workspace.location == LOCATION
        assert workspace.subscription_id == SUBSCRIPTION_ID
        assert workspace.name == WORKSPACE
        assert workspace.resource_group == RESOURCE_GROUP
        assert isinstance(workspace.credential, AzureKeyCredential)
        assert workspace.credential.key == API_KEY
        # pylint: disable=protected-access
        assert isinstance(
            workspace._client._config.authentication_policy,
            AzureKeyCredentialPolicy)
        auth_policy = workspace._client._config.authentication_policy
        assert auth_policy._name == ConnectionConstants.QUANTUM_API_KEY_HEADER
        assert id(auth_policy._credential) == id(workspace.credential)

def test_create_workspace_instance_invalid():
    def assert_value_error(exception: Exception):
        assert "Azure Quantum workspace not fully specified." in exception.args[0]

    with mock.patch.dict(os.environ):
        os.environ.clear()

        # missing workspace name
        try:
            WorkspaceMock(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=None
            )
            assert False, "Expected ValueError"
        except ValueError as e:
            assert_value_error(e)

        # provide only subscription id and resource group
        try:
            WorkspaceMock(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
            )
            assert False, "Expected ValueError"
        except ValueError as e:
            assert_value_error(e)

        # missing everything
        try:
            WorkspaceMock()
            assert False, "Expected ValueError"
        except ValueError as e:
            assert_value_error(e)

        # invalid resource id
        try:
            WorkspaceMock(location=LOCATION, resource_id="invalid/resource/id")
            assert False, "Expected ValueError"
        except ValueError as e:
            assert "Invalid resource id" in e.args[0]


def test_workspace_cancel_job_success():
    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
    )

    job_id = "test-cancel-success"
    details = JobDetails(
        id=job_id,
        name=f"job-{job_id}",
        container_uri="https://example.com/container",
        input_data_format="microsoft.resource-estimate.v2",
        provider_id="ionq",
        target="ionq.simulator",
        status="Executing",
    )
    ws._client.services.jobs._store.append(details)

    job = Job(ws, details)
    result = ws.cancel_job(job)

    assert result.details.status == "Cancelled"
    assert result.id == job_id


def test_workspace_user_agent_appid():
    app_id = "MyEnvVarAppId"
    user_agent = "MyUserAgent"
    with mock.patch.dict(os.environ):
        os.environ.clear()

        # no UserAgent parameter and no EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
        )
        assert ws.user_agent is None

        # with UserAgent parameter and no EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            user_agent=user_agent,
        )
        assert ws.user_agent == user_agent

        # append with no UserAgent parameter and no EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
        )
        ws.append_user_agent("featurex")
        assert ws.user_agent == "featurex"

        # set EnvVar AppId for remaining cases
        os.environ[EnvironmentVariables.USER_AGENT_APPID] = app_id

        # no UserAgent parameter and with EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
        )
        assert ws.user_agent == app_id

        # with UserAgent parameter and EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            user_agent=user_agent,
        )
        assert ws.user_agent == f"{app_id} {user_agent}"

        # append with UserAgent parameter and with EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            user_agent=user_agent,
        )
        ws.append_user_agent("featurex")
        assert ws.user_agent == f"{app_id} {user_agent}-featurex"

        ws.append_user_agent(None)
        assert ws.user_agent == app_id

def test_workspace_context_manager():
    """Test that Workspace can be used as a context manager"""
    with WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
    ) as ws:
        # Verify workspace is properly initialized
        assert ws.subscription_id == SUBSCRIPTION_ID
        assert ws.resource_group == RESOURCE_GROUP
        assert ws.name == WORKSPACE
        assert ws.location == LOCATION
        
        # Verify internal clients are accessible
        assert ws._client is not None
        assert ws._mgmt_client is not None

def test_workspace_context_manager_calls_enter_exit():
    """Test that __enter__ and __exit__ are called on internal clients"""
    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
    )
    
    # Mock the internal clients' __enter__ and __exit__ methods
    ws._client.__enter__ = mock.MagicMock(return_value=ws._client)
    ws._client.__exit__ = mock.MagicMock(return_value=None)
    ws._mgmt_client.__enter__ = mock.MagicMock(return_value=ws._mgmt_client)
    ws._mgmt_client.__exit__ = mock.MagicMock(return_value=None)
    
    # Use workspace as context manager
    with ws as context_ws:
        # Verify __enter__ was called on both clients
        ws._client.__enter__.assert_called_once()
        ws._mgmt_client.__enter__.assert_called_once()
        
        # Verify context manager returns the workspace instance
        assert context_ws is ws
    
    # Verify __exit__ was called on both clients after exiting context
    ws._client.__exit__.assert_called_once()
    ws._mgmt_client.__exit__.assert_called_once()


def test_get_container_uri_uses_linked_storage_sas_when_storage_none():
    """When storage is None, get_container_uri should use linked storage via service SAS."""
    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
    )
    assert ws.storage is None

    with mock.patch(
        "azure.quantum.storage.ContainerClient.from_container_url",
        return_value=mock.MagicMock(),
    ):
        with mock.patch(
            "azure.quantum.storage.create_container_using_client",
            return_value=None,
        ):
            uri = ws.get_container_uri(job_id="job-123")
            assert isinstance(uri, str)
            assert "https://example.com/" in uri
            assert "sas-token" in uri
