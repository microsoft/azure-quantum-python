##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import os
from unittest import mock
import pytest
from common import (
    QuantumTestBase,
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
    LOCATION,
    STORAGE,
    ENDPOINT_URI,
    API_KEY,
    ZERO_UID,
    PLACEHOLDER,
)
from azure.quantum import Workspace
from azure.quantum._constants import (
    EnvironmentVariables,
    ConnectionConstants,
)
from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.policies import AzureKeyCredentialPolicy
from azure.identity import EnvironmentCredential


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
    quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(LOCATION)
)

SIMPLE_CONNECTION_STRING_V2 = ConnectionConstants.VALID_CONNECTION_STRING(
    subscription_id=SUBSCRIPTION_ID,
    resource_group=RESOURCE_GROUP,
    workspace_name=WORKSPACE,
    api_key=API_KEY,
    quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT_v2(LOCATION)
)


class TestWorkspace(QuantumTestBase):
    def test_create_workspace_instance_valid(self):
        def assert_all_required_params(ws: Workspace):
            self.assertEqual(ws.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(ws.resource_group, RESOURCE_GROUP)
            self.assertEqual(ws.name, WORKSPACE)
            self.assertEqual(ws.location, LOCATION)
            self.assertEqual(ws._connection_params.quantum_endpoint, ENDPOINT_URI)
        
        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
        )
        assert_all_required_params(ws)

        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            storage=STORAGE,
        )
        assert_all_required_params(ws)
        self.assertEqual(ws.storage, STORAGE)

        ws = Workspace(
            resource_id=SIMPLE_RESOURCE_ID,
        )
        assert_all_required_params(ws)

        ws = Workspace(
            resource_id=SIMPLE_RESOURCE_ID,
            storage=STORAGE,
        )
        assert_all_required_params(ws)
        self.assertEqual(ws.storage, STORAGE)

        ws = Workspace(
            name=WORKSPACE,
        )
        assert_all_required_params(ws)

        ws = Workspace(
            name=WORKSPACE,
            storage=STORAGE,
        )
        assert_all_required_params(ws)
        self.assertEqual(ws.storage, STORAGE)

        ws = Workspace(
            name=WORKSPACE,
            location=LOCATION,
        )
        assert_all_required_params(ws)

        ws = Workspace(
            name=WORKSPACE,
            subscription_id=SUBSCRIPTION_ID,
        )
        assert_all_required_params(ws)

        ws = Workspace(
            name=WORKSPACE,
            subscription_id=SUBSCRIPTION_ID,
            location=LOCATION,
        )
        assert_all_required_params(ws)

        ws = Workspace(
            name=WORKSPACE,
            resource_group=RESOURCE_GROUP,
        )
        assert_all_required_params(ws)

        ws = Workspace(
            name=WORKSPACE,
            resource_group=RESOURCE_GROUP,
            location=LOCATION,
        )
        assert_all_required_params(ws)

    def test_create_workspace_locations(self):
        # User-provided location name should be normalized
        location = "East US"
        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=location,
        )
        self.assertEqual(ws.location, "eastus")

    def test_env_connection_string(self):
        with mock.patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            os.environ[EnvironmentVariables.CONNECTION_STRING] = SIMPLE_CONNECTION_STRING

            workspace = Workspace()
            self.assertEqual(workspace.location, LOCATION)
            self.assertEqual(workspace.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(workspace.name, WORKSPACE)
            self.assertEqual(workspace.resource_group, RESOURCE_GROUP)
            self.assertIsInstance(workspace.credential, AzureKeyCredential)
            self.assertEqual(workspace.credential.key, API_KEY)
            # pylint: disable=protected-access
            self.assertIsInstance(
                workspace._client._config.authentication_policy,
                AzureKeyCredentialPolicy)
            auth_policy = workspace._client._config.authentication_policy
            self.assertEqual(auth_policy._name, ConnectionConstants.QUANTUM_API_KEY_HEADER)
            self.assertEqual(id(auth_policy._credential),
                             id(workspace.credential))

    def test_workspace_from_connection_string(self):
        with mock.patch.dict(
            os.environ,
            clear=True
        ):
            workspace = Workspace.from_connection_string(SIMPLE_CONNECTION_STRING)
            self.assertEqual(workspace.location, LOCATION)
            self.assertIsInstance(workspace.credential, AzureKeyCredential)
            self.assertEqual(workspace.credential.key, API_KEY)
            # pylint: disable=protected-access
            self.assertIsInstance(
                workspace._client._config.authentication_policy,
                AzureKeyCredentialPolicy)
            auth_policy = workspace._client._config.authentication_policy
            self.assertEqual(auth_policy._name, ConnectionConstants.QUANTUM_API_KEY_HEADER)
            self.assertEqual(id(auth_policy._credential),
                             id(workspace.credential))

        # assert that the connection string environment variable
        # does not overwrite values that were set
        # via the other environment variables
        with mock.patch.dict(os.environ):
            self.clear_env_vars(os.environ)

            wrong_subscription_id = "00000000-2BAD-2BAD-2BAD-000000000000"
            wrong_resource_group = "wrongrg"
            wrong_workspace = "wrong-workspace"
            wrong_location = "wrong-location"

            # make sure the values above are really different from the default values
            self.assertNotEqual(wrong_subscription_id, SUBSCRIPTION_ID)
            self.assertNotEqual(wrong_resource_group, RESOURCE_GROUP)
            self.assertNotEqual(wrong_workspace, WORKSPACE)
            self.assertNotEqual(wrong_location, LOCATION)

            wrong_connection_string = ConnectionConstants.VALID_CONNECTION_STRING(
                subscription_id=wrong_subscription_id,
                resource_group=wrong_resource_group,
                workspace_name=wrong_workspace,
                api_key=API_KEY,
                quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(wrong_location)
            )

            os.environ[EnvironmentVariables.CONNECTION_STRING] = wrong_connection_string
            os.environ[EnvironmentVariables.LOCATION] = LOCATION
            os.environ[EnvironmentVariables.SUBSCRIPTION_ID] = SUBSCRIPTION_ID
            os.environ[EnvironmentVariables.RESOURCE_GROUP] = RESOURCE_GROUP
            os.environ[EnvironmentVariables.WORKSPACE_NAME] = WORKSPACE

            workspace = Workspace()
            self.assertEqual(workspace.location, LOCATION)
            self.assertEqual(workspace.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(workspace.resource_group, RESOURCE_GROUP)
            self.assertEqual(workspace.name, WORKSPACE)
            # since no credential was passed, we will use the api-key
            # credential from the connection string
            self.assertIsInstance(workspace.credential, AzureKeyCredential)

            # if we pass a credential, then it should be used
            os.environ[EnvironmentVariables.AZURE_CLIENT_ID] = ZERO_UID
            os.environ[EnvironmentVariables.AZURE_TENANT_ID] = ZERO_UID
            os.environ[EnvironmentVariables.AZURE_CLIENT_SECRET] = PLACEHOLDER
            workspace = Workspace(credential=EnvironmentCredential())
            self.assertIsInstance(workspace.credential, EnvironmentCredential)

            # the connection string passed as a parameter should override the
            # connection string from the env var
            self.clear_env_vars(os.environ)
            os.environ[EnvironmentVariables.CONNECTION_STRING] = wrong_connection_string
            connection_string = ConnectionConstants.VALID_CONNECTION_STRING(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                workspace_name=WORKSPACE,
                api_key=API_KEY,
                quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(LOCATION)
            )
            workspace = Workspace.from_connection_string(connection_string=connection_string)
            self.assertEqual(workspace.location, LOCATION)
            self.assertEqual(workspace.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(workspace.resource_group, RESOURCE_GROUP)
            self.assertEqual(workspace.name, WORKSPACE)

            # the connection string in the env var should not be parsed if we
            # don't really need it
            self.clear_env_vars(os.environ)
            os.environ[EnvironmentVariables.CONNECTION_STRING] = "bad-connection-string"
            connection_string = ConnectionConstants.VALID_CONNECTION_STRING(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                workspace_name=WORKSPACE,
                api_key=API_KEY,
                quantum_endpoint=ConnectionConstants.GET_QUANTUM_PRODUCTION_ENDPOINT(LOCATION)
            )
            workspace = Workspace.from_connection_string(connection_string=connection_string)
            self.assertEqual(workspace.location, LOCATION)
            self.assertEqual(workspace.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(workspace.resource_group, RESOURCE_GROUP)
            self.assertEqual(workspace.name, WORKSPACE)
    
    def test_workspace_from_connection_string_v2(self):
        """Test that v2 QuantumEndpoint format is correctly parsed."""
        with mock.patch.dict(
            os.environ,
            clear=True
        ):
            workspace = Workspace.from_connection_string(SIMPLE_CONNECTION_STRING_V2)
            self.assertEqual(workspace.location, LOCATION)
            self.assertEqual(workspace.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(workspace.resource_group, RESOURCE_GROUP)
            self.assertEqual(workspace.name, WORKSPACE)
            self.assertIsInstance(workspace.credential, AzureKeyCredential)
            self.assertEqual(workspace.credential.key, API_KEY)
            # pylint: disable=protected-access
            self.assertIsInstance(
                workspace._client._config.authentication_policy,
                AzureKeyCredentialPolicy)
            auth_policy = workspace._client._config.authentication_policy
            self.assertEqual(auth_policy._name, ConnectionConstants.QUANTUM_API_KEY_HEADER)
            self.assertEqual(id(auth_policy._credential),
                             id(workspace.credential))
    
    def test_workspace_from_connection_string_v2_dogfood(self):
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
            workspace = Workspace.from_connection_string(dogfood_connection_string_v2)
            self.assertEqual(workspace.location, canary_location)
            self.assertEqual(workspace.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(workspace.resource_group, RESOURCE_GROUP)
            self.assertEqual(workspace.name, WORKSPACE)
            self.assertIsInstance(workspace.credential, AzureKeyCredential)
            self.assertEqual(workspace.credential.key, API_KEY)

    def test_env_connection_string_v2(self):
        """Test v2 QuantumEndpoint from environment variable."""
        with mock.patch.dict(os.environ):
            self.clear_env_vars(os.environ)
            os.environ[EnvironmentVariables.CONNECTION_STRING] = SIMPLE_CONNECTION_STRING_V2

            workspace = Workspace()
            self.assertEqual(workspace.location, LOCATION)
            self.assertEqual(workspace.subscription_id, SUBSCRIPTION_ID)
            self.assertEqual(workspace.name, WORKSPACE)
            self.assertEqual(workspace.resource_group, RESOURCE_GROUP)
            self.assertIsInstance(workspace.credential, AzureKeyCredential)
            self.assertEqual(workspace.credential.key, API_KEY)
            # pylint: disable=protected-access
            self.assertIsInstance(
                workspace._client._config.authentication_policy,
                AzureKeyCredentialPolicy)
            auth_policy = workspace._client._config.authentication_policy
            self.assertEqual(auth_policy._name, ConnectionConstants.QUANTUM_API_KEY_HEADER)
            self.assertEqual(id(auth_policy._credential),
                             id(workspace.credential))

    def test_create_workspace_instance_invalid(self):
        def assert_value_error(exception):
            self.assertIn("Azure Quantum workspace not fully specified.",
                          exception.args[0])

        with mock.patch.dict(os.environ):
            self.clear_env_vars(os.environ)

            # missing workspace name
            with self.assertRaises(ValueError) as context:
                Workspace(
                    location=LOCATION,
                    subscription_id=SUBSCRIPTION_ID,
                    resource_group=RESOURCE_GROUP,
                    name=None
                )
            assert_value_error(context.exception)

            # provide only subscription id and resource group
            with self.assertRaises(ValueError) as context:
                Workspace(
                    subscription_id=SUBSCRIPTION_ID,
                    resource_group=RESOURCE_GROUP,
                )
            assert_value_error(context.exception)

            # missing everything
            with self.assertRaises(ValueError) as context:
                Workspace()
            assert_value_error(context.exception)

            # invalid resource id
            with self.assertRaises(ValueError) as context:
                Workspace(
                    location=LOCATION,
                    resource_id="invalid/resource/id")
            self.assertIn("Invalid resource id",
                          context.exception.args[0])

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_workspace_get_targets_ionq(self):
        ws = self.create_workspace()
        targets = ws.get_targets()
        self.assertNotIn(None, targets)
        test_targets = set([
            'ionq.simulator'
        ])
        self.assertTrue(test_targets.issubset(set([t.name for t in targets])))

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_workspace_get_targets_quantinuum(self):
        ws = self.create_workspace()
        targets = ws.get_targets()
        self.assertNotIn(None, targets)
        test_targets = set([
            'quantinuum.sim.h2-1sc',
            'quantinuum.sim.h2-1e',
            'quantinuum.qpu.h2-1'
        ])
        self.assertTrue(test_targets.issubset(set([t.name for t in targets])))


    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_workspace_get_target_ionq(self):
        ws = self.create_workspace()
        target = ws.get_targets("ionq.qpu.aria-1")
        self.assertIsNotNone(target.average_queue_time)
        self.assertIsNotNone(target.current_availability)
        self.assertEqual(target.name, "ionq.qpu.aria-1")
        target.refresh()
        self.assertIsNotNone(target.average_queue_time)
        self.assertIsNotNone(target.current_availability)
        # target lookup is case insensitive
        target1 = ws.get_targets("IonQ.QPU.Aria-1")
        self.assertEqual(target.name, target1.name)

        with pytest.raises(ValueError):
            target.name = "foo"
            target.refresh()

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_workspace_get_targets_result_type(self):
        ws = self.create_workspace()
        targets = ws.get_targets()
        assert isinstance(targets, list)
        # For now, we keep a single result as instance instead of list, 
        # but it has to be changed in the next major release.
        target = ws.get_targets(name="ionq.qpu.aria-1")
        assert not isinstance(target, list)

    @pytest.mark.live_test
    def test_workspace_job_quotas(self):
        ws = self.create_workspace()
        quotas = ws.get_quotas()
        self.assertGreater(len(quotas), 0)
        self.assertIn("dimension", quotas[0])
        self.assertIn("scope", quotas[0])
        self.assertIn("providerId", quotas[0])
        self.assertIn("utilization", quotas[0])
        self.assertIn("holds", quotas[0])
        self.assertIn("limit", quotas[0])
        self.assertIn("period", quotas[0])

    @pytest.mark.live_test
    def test_workspace_list_jobs(self):
        ws = self.create_workspace()
        jobs = ws.list_jobs()
        self.assertIsInstance(jobs, list)

    def test_workspace_user_agent_appid(self):
        app_id = "MyEnvVarAppId"
        user_agent = "MyUserAgent"
        with mock.patch.dict(os.environ):
            self.clear_env_vars(os.environ)

            # no UserAgent parameter and no EnvVar AppId
            os.environ[EnvironmentVariables.USER_AGENT_APPID] = ""
            ws = Workspace(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
                location=LOCATION
            )
            self.assertIsNone(ws.user_agent)

            # no UserAgent parameter and with EnvVar AppId
            os.environ[EnvironmentVariables.USER_AGENT_APPID] = app_id
            ws = Workspace(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
                location=LOCATION
            )
            self.assertEqual(ws.user_agent, app_id)

            # with UserAgent parameter and no EnvVar AppId
            os.environ[EnvironmentVariables.USER_AGENT_APPID] = ""
            ws = Workspace(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
                location=LOCATION,
                user_agent=user_agent
            )
            self.assertEqual(ws.user_agent, user_agent)

            # with UserAgent parameter and EnvVar AppId
            os.environ[EnvironmentVariables.USER_AGENT_APPID] = app_id
            ws = Workspace(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
                location=LOCATION,
                user_agent=user_agent
            )
            self.assertEqual(ws.user_agent,
                             f"{app_id} {user_agent}")

            # Append with UserAgent parameter and with EnvVar AppId
            os.environ[EnvironmentVariables.USER_AGENT_APPID] = app_id
            ws = Workspace(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
                location=LOCATION,
                user_agent=user_agent
            )
            ws.append_user_agent("featurex")
            self.assertEqual(ws.user_agent,
                             f"{app_id} {user_agent}-featurex")

            ws.append_user_agent(None)
            self.assertEqual(ws.user_agent, app_id)

            # Append with no UserAgent parameter and no EnvVar AppId
            os.environ[EnvironmentVariables.USER_AGENT_APPID] = ""
            ws = Workspace(
                subscription_id=SUBSCRIPTION_ID,
                resource_group=RESOURCE_GROUP,
                name=WORKSPACE,
                location=LOCATION
            )
            ws.append_user_agent("featurex")
            self.assertEqual(ws.user_agent, "featurex")
