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
    API_KEY,
)
from azure.quantum import Workspace
from azure.quantum._constants import (
    EnvironmentVariables,
    ConnectionConstants,
)
from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.policies import AzureKeyCredentialPolicy


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
    quantum_endpoint=ConnectionConstants.QUANTUM_BASE_URL(LOCATION)
)


class TestWorkspace(QuantumTestBase):
    def test_create_workspace_instance_valid(self):
        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
        )
        self.assertEqual(ws.subscription_id, SUBSCRIPTION_ID)
        self.assertEqual(ws.resource_group, RESOURCE_GROUP)
        self.assertEqual(ws.name, WORKSPACE)
        self.assertEqual(ws.location, LOCATION)

        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
            storage=STORAGE,
        )
        self.assertEqual(ws.storage, STORAGE)

        ws = Workspace(
            resource_id=SIMPLE_RESOURCE_ID,
            location=LOCATION,
        )
        self.assertEqual(ws.subscription_id, SUBSCRIPTION_ID)
        self.assertEqual(ws.resource_group, RESOURCE_GROUP)
        self.assertEqual(ws.name, WORKSPACE)
        self.assertEqual(ws.location, LOCATION)

        ws = Workspace(
            resource_id=SIMPLE_RESOURCE_ID,
            storage=STORAGE,
            location=LOCATION,
        )
        self.assertEqual(ws.storage, STORAGE)

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

    def test_parse_connection_string(self):
        workspace = Workspace.from_connection_string(SIMPLE_CONNECTION_STRING)
        self.assertEqual(workspace.location, LOCATION)
        self.assertIsInstance(workspace.credential, AzureKeyCredential)
        self.assertEqual(workspace.credential.key, API_KEY)
        # pylint: disable=protected-access
        self.assertIsInstance(workspace._client._config.authentication_policy,
                              AzureKeyCredentialPolicy)
        auth_policy = workspace._client._config.authentication_policy
        self.assertEqual(auth_policy._name, ConnectionConstants.QUANTUM_API_KEY_HEADER)
        self.assertEqual(id(auth_policy._credential), id(workspace.credential))

    def test_env_connection_string(self):
        with mock.patch.dict(
            os.environ,
            {EnvironmentVariables.CONNECTION_STRING: SIMPLE_CONNECTION_STRING},
            clear=True
        ):
            workspace = Workspace()
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

    def test_create_workspace_instance_invalid(self):
        def assert_value_error(exception):
            self.assertIn("Azure Quantum workspace not fully specified.",
                          exception.args[0])

        with mock.patch.dict(os.environ):
            self.clear_env_vars(os.environ)

            # missing location
            with self.assertRaises(ValueError) as context:
                Workspace(
                    location=None,
                    subscription_id=SUBSCRIPTION_ID,
                    resource_group=RESOURCE_GROUP,
                    name=WORKSPACE,
                )
            assert_value_error(context.exception)

            # missing location
            with self.assertRaises(ValueError) as context:
                Workspace(resource_id=SIMPLE_RESOURCE_ID)
            assert_value_error(context.exception)

            # missing subscription id
            with self.assertRaises(ValueError) as context:
                Workspace(
                    location=LOCATION,
                    subscription_id=None,
                    resource_group=RESOURCE_GROUP,
                    name=WORKSPACE
                )
            assert_value_error(context.exception)

            # missing resource group
            with self.assertRaises(ValueError) as context:
                Workspace(
                    location=LOCATION,
                    subscription_id=SUBSCRIPTION_ID,
                    resource_group=None,
                    name=WORKSPACE
                )
            assert_value_error(context.exception)

            # missing workspace name
            with self.assertRaises(ValueError) as context:
                Workspace(
                    location=LOCATION,
                    subscription_id=SUBSCRIPTION_ID,
                    resource_group=RESOURCE_GROUP,
                    name=None
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

            # invalid connection string
            with self.assertRaises(ValueError) as context:
                Workspace(
                    connection_string="invalid;connection=string")
            self.assertIn("Invalid connection string",
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
            'quantinuum.sim.h1-1sc',
            'quantinuum.sim.h1-2sc',
            'quantinuum.sim.h1-1e',
            'quantinuum.sim.h1-2e',
            'quantinuum.qpu.h1-1',
            'quantinuum.qpu.h1-2',
            'quantinuum.sim.h2-1sc',
            'quantinuum.sim.h2-1e',
            'quantinuum.qpu.h2-1'
        ])
        self.assertTrue(test_targets.issubset(set([t.name for t in targets])))


    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_workspace_get_target_ionq(self):
        ws = self.create_workspace()
        target = ws.get_targets("ionq.qpu")
        self.assertIsNotNone(target.average_queue_time)
        self.assertIsNotNone(target.current_availability)
        self.assertEqual(target.name, "ionq.qpu")
        target.refresh()
        self.assertIsNotNone(target.average_queue_time)
        self.assertIsNotNone(target.current_availability)
        # target lookup is case insensitive
        target1 = ws.get_targets("IonQ.QPU")
        self.assertEqual(target.name, target1.name)

        with pytest.raises(ValueError):
            target.name = "foo"
            target.refresh()

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_workspace_get_target_microsoft_qc(self):
        from azure.quantum.target.microsoft import MicrosoftEstimator

        ws = self.create_workspace()
        target = ws.get_targets("microsoft.estimator")

        self.assertEqual(type(target), MicrosoftEstimator)

    @pytest.mark.live_test
    def test_workspace_job_quotas(self):
        ws = self.create_workspace()
        quotas = ws.get_quotas()
        self.assertGreater(len(quotas), 0)
        self.assertIn("dimension", quotas[0])
        self.assertIn("scope", quotas[0])
        self.assertIn("provider_id", quotas[0])
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
