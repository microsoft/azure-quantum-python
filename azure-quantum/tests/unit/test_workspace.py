#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_workspace.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest

from azure.quantum import Workspace
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
        assert ws.location == self.location

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
