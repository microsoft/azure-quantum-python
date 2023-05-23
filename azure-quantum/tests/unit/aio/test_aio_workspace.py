##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest
from azure.quantum.aio import Workspace
from common import QuantumTestBase


class TestWorkspace(QuantumTestBase):

    def test_create_async_workspace_instance_valid(self):
        storage = "strg"

        ws = Workspace(
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            name=self.workspace_name,
            location=self.location
        )
        self.assertEqual(ws.subscription_id, self.subscription_id)
        self.assertEqual(ws.resource_group, self.resource_group)
        self.assertEqual(ws.name, self.workspace_name)
        self.assertEqual(ws.location.lower().replace(" ", ""), self.location.lower().replace(" ", ""))

        ws = Workspace(
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            name=self.workspace_name,
            location=self.location,
            storage=storage
        )
        self.assertEqual(ws.storage, storage)

        resource_id = f"/subscriptions/{self.subscription_id}/ResourceGroups/{self.resource_group}/providers/Microsoft.Quantum/Workspaces/{self.workspace_name}"
        ws = Workspace(resource_id=resource_id, location=self.location)
        self.assertEqual(ws.subscription_id, self.subscription_id)
        self.assertEqual(ws.resource_group, self.resource_group)
        self.assertEqual(ws.name, self.workspace_name)

        ws = Workspace(resource_id=resource_id, storage=storage, location=self.location)
        self.assertEqual(ws.storage, storage)

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
        self.assertEqual(ws.location, "eastus")

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
        test_targets = set([
            'microsoft.paralleltempering-parameterfree.cpu',
            'microsoft.populationannealing.cpu',
            'microsoft.qmc.cpu',
            'microsoft.simulatedannealing-parameterfree.cpu',
            'microsoft.substochasticmontecarlo.cpu',
            'microsoft.tabu-parameterfree.cpu',
        ])
        self.assertTrue(test_targets.issubset(set([t.name for t in targets])))

    def test_workspace_job_quotas(self):
        ws = self.create_async_workspace()
        quotas = self.get_async_result(ws.get_quotas())
        self.assertGreater(len(quotas), 0)
        self.assertIn("dimension", quotas[0])
        self.assertIn("scope", quotas[0])
        self.assertIn("provider_id", quotas[0])
        self.assertIn("utilization", quotas[0])
        self.assertIn("holds", quotas[0])
        self.assertIn("limit", quotas[0])
        self.assertIn("period", quotas[0])
