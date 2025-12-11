import os
from unittest import mock
from azure.quantum._constants import EnvironmentVariables, ConnectionConstants
from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.policies import AzureKeyCredentialPolicy
from azure.identity import EnvironmentCredential

from mock_client import WorkspaceMock
from common import (
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
    LOCATION,
    STORAGE,
    API_KEY,
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


def test_create_workspace_instance_valid():
    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
        location=LOCATION,
    )
    assert ws.subscription_id == SUBSCRIPTION_ID
    assert ws.resource_group == RESOURCE_GROUP
    assert ws.name == WORKSPACE
    assert ws.location == LOCATION

    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
        location=LOCATION,
        storage=STORAGE,
    )
    assert ws.storage == STORAGE

    ws = WorkspaceMock(resource_id=SIMPLE_RESOURCE_ID, location=LOCATION)
    assert ws.subscription_id == SUBSCRIPTION_ID
    assert ws.resource_group == RESOURCE_GROUP
    assert ws.name == WORKSPACE
    assert ws.location == LOCATION

    ws = WorkspaceMock(
        resource_id=SIMPLE_RESOURCE_ID, storage=STORAGE, location=LOCATION
    )
    assert ws.storage == STORAGE


def test_create_workspace_locations():
    # User-provided location name should be normalized
    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
        location="East US",
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
        wrong_location = "wrong-location"

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


def test_create_workspace_instance_invalid():
    def assert_value_error(exception: Exception):
        assert "Azure Quantum workspace not fully specified." in exception.args[0]

    with mock.patch.dict(os.environ):
        os.environ.clear()

        # missing location
        try:
            WorkspaceMock(
                location=None,  # type: ignore[arg-type]
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
            )
            assert False, "Expected ValueError"
        except ValueError as e:
            assert_value_error(e)

        # missing location with resource id
        try:
            WorkspaceMock(resource_id=SIMPLE_RESOURCE_ID)
            assert False, "Expected ValueError"
        except ValueError as e:
            assert_value_error(e)

        # missing subscription id
        try:
            WorkspaceMock(
                location=LOCATION,
                subscription_id=None,  # type: ignore[arg-type]
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
            )
            assert False, "Expected ValueError"
        except ValueError as e:
            assert_value_error(e)

        # missing resource group
        try:
            WorkspaceMock(
                location=LOCATION,
                subscription_id=SUBSCRIPTION_ID,
                resource_group=None,  # type: ignore[arg-type]
                name=WORKSPACE,
            )
            assert False, "Expected ValueError"
        except ValueError as e:
            assert_value_error(e)

        # missing workspace name
        try:
            WorkspaceMock(
                location=LOCATION,
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=None,  # type: ignore[arg-type]
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
            location=LOCATION,
        )
        assert ws.user_agent is None

        # with UserAgent parameter and no EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
            user_agent=user_agent,
        )
        assert ws.user_agent == user_agent

        # append with no UserAgent parameter and no EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
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
            location=LOCATION,
        )
        assert ws.user_agent == app_id

        # with UserAgent parameter and EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
            user_agent=user_agent,
        )
        assert ws.user_agent == f"{app_id} {user_agent}"

        # append with UserAgent parameter and with EnvVar AppId
        ws = WorkspaceMock(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
            user_agent=user_agent,
        )
        ws.append_user_agent("featurex")
        assert ws.user_agent == f"{app_id} {user_agent}-featurex"

        ws.append_user_agent(None)
        assert ws.user_agent == app_id
