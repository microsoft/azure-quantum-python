#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_workspace.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest
from azure.quantum.aio import Workspace
from ..common import QuantumTestBase


class TestWorkspace(QuantumTestBase):

    def test_create_async_workspace_instance_valid(self):
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
        assert ws.location.lower() == self.location.lower()

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

    def test_create_async_workspace_locations(self):
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

    def test_create_async_workspace_instance_invalid(self):
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

    def test_workspace_get_targets(self):
        ws = self.create_async_workspace()
        targets = self.get_async_result(ws.get_targets())
        assert sorted([t.name for t in targets]) == [
            '1qbit.pathrelinking',
            '1qbit.pticm',
            '1qbit.tabu',
            'honeywell.hqs-lt-s1',
            'honeywell.hqs-lt-s1-apival',
            'honeywell.hqs-lt-s1-sim',
            'ionq.qpu',
            'ionq.simulator',
            'microsoft.paralleltempering-parameterfree.cpu',
            'microsoft.populationannealing.cpu',
            'microsoft.qmc.cpu',
            'microsoft.simulatedannealing-parameterfree.cpu',
            'microsoft.substochasticmontecarlo.cpu',
            'microsoft.tabu-parameterfree.cpu',
            'toshiba.sbm.ising'
        ]

        target = self.get_async_result(ws.get_targets("ionq.qpu"))
        assert target.average_queue_time is not None
        assert target.current_availability is not None
        assert target.name == "ionq.qpu"
        self.get_async_result(target.refresh())
        assert target.average_queue_time is not None
        assert target.current_availability is not None

        with pytest.raises(ValueError):
            target.name = "foo"
            self.get_async_result(target.refresh())
    
    def test_workspace_job_quotas(self):
        ws = self.create_async_workspace()
        quotas = self.get_async_result(ws.get_quotas())
        assert len(quotas) > 0
        assert "dimension" in quotas[0]
        assert "scope" in quotas [0]
        assert "provider_id" in quotas [0]
        assert "utilization" in quotas [0]
        assert "holds" in quotas [0]
        assert "limit" in quotas [0]
        assert "period" in quotas [0]
