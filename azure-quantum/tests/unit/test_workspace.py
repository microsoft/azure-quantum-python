#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_workspace.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import json
import pytest

from azure.quantum import Workspace
from common import QuantumTestBase


class TestWorkspace(QuantumTestBase):
    def test_workspace_login(self):
        subscription_id = "44ef49ad-64e4-44e5-a3ba-1ee87e19d3f4"
        resource_group = "rg"
        name = "n"

        ws = self.create_workspace()
        ws.login()

    def test_create_workspace_instance_valid(self):
        subscription_id = "44ef49ad-64e4-44e5-a3ba-1ee87e19d3f4"
        resource_group = "rg"
        name = "n"
        storage = "strg"

        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
        )
        assert ws.subscription_id == subscription_id
        assert ws.resource_group == resource_group
        assert ws.name == name

        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            storage=storage,
        )
        assert ws.storage == storage

        resource_id = f"/subscriptions/{subscription_id}/RESOurceGroups/{resource_group}/providers/Microsoft.Quantum/Workspaces/{name}"
        ws = Workspace(resource_id=resource_id)
        assert ws.subscription_id == subscription_id
        assert ws.resource_group == resource_group
        assert ws.name == name

        ws = Workspace(resource_id=resource_id, storage=storage)
        assert ws.storage == storage

    def test_create_workspace_locations(self):
        subscription_id = "44ef49ad-64e4-44e5-a3ba-1ee87e19d3f4"
        resource_group = "rg"
        name = "n"

        # Default should be westus
        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
        )
        assert ws.location == "westus"

        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location="   ",
        )
        assert ws.location == "westus"

        # User-provided location name should be normalized
        location = "East US"
        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location=location,
        )
        assert ws.location == "eastus"

    def test_create_workspace_instance_invalid(self):
        subscription_id = "44ef49ad-64e4-44e5-a3ba-1ee87e19d3f4"
        resource_group = "rg"
        name = "n"
        storage = "strg"

        with pytest.raises(ValueError):
            ws = Workspace()

        with pytest.raises(ValueError):
            ws = Workspace(
                subscription_id=subscription_id,
                resource_group=resource_group,
                name="",
            )

        with pytest.raises(ValueError):
            ws = Workspace(resource_id="invalid/resource/id")

        with pytest.raises(ValueError):
            ws = Workspace(storage=storage)
