#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_workspace.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest
import os
from azure.quantum import Workspace
from azure.quantum.workspace import USER_AGENT_APPID_ENV_VAR_NAME
from common import QuantumTestBase

class TestWorkspace(QuantumTestBase):

    def test_create_workspace_instance_valid(self):
        storage = "strg"

        ws = Workspace(
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            name=self.workspace_name,
            location=self.location
        )
        assert ws.subscription_id == self.subscription_id
        assert ws.resource_group == self.resource_group
        assert ws.name == self.workspace_name
        assert ws.location.lower().replace(" ", "") == self.location.lower().replace(" ", "")

        ws = Workspace(
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            name=self.workspace_name,
            location=self.location,
            storage=storage
        )
        assert ws.storage == storage

        resource_id = f"/subscriptions/{self.subscription_id}/ResourceGroups/{self.resource_group}/providers/Microsoft.Quantum/Workspaces/{self.workspace_name}"
        ws = Workspace(resource_id=resource_id, location=self.location)
        assert ws.subscription_id == self.subscription_id
        assert ws.resource_group == self.resource_group
        assert ws.name == self.workspace_name

        ws = Workspace(resource_id=resource_id, storage=storage, location=self.location)
        assert ws.storage == storage

    def test_create_workspace_locations(self):
        # location is mandatory
        with self.assertRaises(Exception) as context:
            Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
            )
            self.assertTrue("Azure Quantum workspace does not have an associated location." in context.exception)

        # User-provided location name should be normalized
        location = "East US"
        ws = Workspace(
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            name=self.workspace_name,
            location=location,
        )
        assert ws.location == "eastus"

    def test_create_workspace_instance_invalid(self):
        storage = "invalid_storage"

        with pytest.raises(ValueError):
            Workspace()

        with pytest.raises(ValueError):
            Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name="",
            )

        with pytest.raises(ValueError):
            Workspace(resource_id="invalid/resource/id")

        with pytest.raises(ValueError):
            Workspace(storage=storage)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_workspace_get_targets_ionq(self):
        ws = self.create_workspace()
        targets = ws.get_targets()
        assert None not in targets
        test_targets = set([
            'ionq.simulator'
        ])
        assert test_targets.issubset(set([t.name for t in targets]))
    
    @pytest.mark.honeywell
    @pytest.mark.live_test
    def test_workspace_get_targets_honeywell(self):
        ws = self.create_workspace()
        targets = ws.get_targets()
        assert None not in targets
        test_targets = set([
            'honeywell.hqs-lt-s1-apival'
        ])
        assert test_targets.issubset(set([t.name for t in targets]))

    @pytest.mark.honeywell
    @pytest.mark.live_test
    def test_workspace_get_targets_quantinuum(self):
        if self.get_test_quantinuum_enabled():
            ws = self.create_workspace()
            targets = ws.get_targets()
            assert None not in targets
            test_targets = set([
                'quantinuum.hqs-lt-s1-apival'
            ])
            assert test_targets.issubset(set([t.name for t in targets]))
            test_targets = set([
                'quantinuum.sim.h1-1sc'
            ])
            assert test_targets.issubset(set([t.name for t in targets]))
            test_targets = set([
                'quantinuum.sim.h1-2sc'
            ])
            assert test_targets.issubset(set([t.name for t in targets]))

    @pytest.mark.qio
    @pytest.mark.live_test
    def test_workspace_get_targets_qio(self):
        ws = self.create_workspace()
        targets = ws.get_targets()
        assert None not in targets
        test_targets = set([
            'microsoft.paralleltempering-parameterfree.cpu',
            'microsoft.populationannealing.cpu',
            'microsoft.qmc.cpu',
            'microsoft.simulatedannealing-parameterfree.cpu',
            'microsoft.substochasticmontecarlo.cpu',
            'microsoft.tabu-parameterfree.cpu',
        ])
        assert test_targets.issubset(set([t.name for t in targets]))

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_workspace_get_target_ionq(self):
        ws = self.create_workspace()
        target = ws.get_targets("ionq.qpu")
        assert target.average_queue_time is not None
        assert target.current_availability is not None
        assert target.name == "ionq.qpu"
        target.refresh()
        assert target.average_queue_time is not None
        assert target.current_availability is not None
        # target lookup is case insensitive
        target1 = ws.get_targets("IonQ.QPU")
        assert target.name == target1.name

        with pytest.raises(ValueError):
            target.name = "foo"
            target.refresh()

    @pytest.mark.live_test
    def test_workspace_job_quotas(self):
        ws = self.create_workspace()
        quotas = ws.get_quotas()
        assert len(quotas) > 0
        assert "dimension" in quotas[0]
        assert "scope" in quotas[0]
        assert "provider_id" in quotas[0]
        assert "utilization" in quotas[0]
        assert "holds" in quotas[0]
        assert "limit" in quotas[0]
        assert "period" in quotas[0]

    def test_workspace_user_agent_appid(self):
        env_var_app_id = "MyEnvVarAppId"
        user_agent = "MyUserAgentAppId"
        very_long_user_agent = "MyVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongUserAgentAppId"
        original_env_app_id = os.environ.get(USER_AGENT_APPID_ENV_VAR_NAME, "")
        try:
            # no UserAgent parameter and no EnvVar AppId
            os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = ""
            ws = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location
            )
            assert ws.user_agent is None

            # no UserAgent parameter and with EnvVar AppId
            os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = env_var_app_id
            ws = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location
            )
            assert ws.user_agent == env_var_app_id

            # with UserAgent parameter and no EnvVar AppId
            os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = ""
            ws = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location,
                user_agent=user_agent
            )
            assert ws.user_agent == user_agent

            # with very long UserAgent parameter and no EnvVar AppId
            os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = ""
            ws = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location,
                user_agent=very_long_user_agent
            )
            assert ws.user_agent == very_long_user_agent

            # with UserAgent parameter and with EnvVar AppId
            os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = env_var_app_id
            ws = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location,
                user_agent=user_agent
            )
            assert ws.user_agent == f"{user_agent}-{env_var_app_id}"

            # Append with UserAgent parameter and with EnvVar AppId 
            os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = env_var_app_id
            ws = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location,
                user_agent=user_agent
            )
            ws.append_user_agent("featurex")
            assert ws.user_agent == f"{user_agent}-featurex-{env_var_app_id}"

            # Append with no UserAgent parameter and no EnvVar AppId 
            os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = ""
            ws = Workspace(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location
            )
            ws.append_user_agent("featurex")
            assert ws.user_agent == "featurex"
        finally:
            if original_env_app_id:
                os.environ[USER_AGENT_APPID_ENV_VAR_NAME] = original_env_app_id
            else:
                os.environ.pop(USER_AGENT_APPID_ENV_VAR_NAME)
