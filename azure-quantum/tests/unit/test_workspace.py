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
from azure.identity import DefaultAzureCredential

class TestWorkspace(QuantumTestBase):

    def test_create_workspace_instance_valid(self):
        subscription_id = "44ef49ad-64e4-44e5-a3ba-1ee87e19d3f4"
        resource_group = "rg"
        name = "n"
        storage = "strg"
        location = "eastus"

        credential = DefaultAzureCredential()

        ws = Workspace(
            credential=credential,
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location=location
        )
        assert ws.subscription_id == subscription_id
        assert ws.resource_group == resource_group
        assert ws.name == name
        assert ws.location == location

        ws = Workspace(
            credential=credential,
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            storage=storage,
            location=location
        )
        assert ws.storage == storage

        resource_id = f"/subscriptions/{subscription_id}/ResourceGroups/{resource_group}/providers/Microsoft.Quantum/Workspaces/{name}"
        ws = Workspace(
            credential=credential,
            resource_id=resource_id, 
            location=location
        )
        assert ws.subscription_id == subscription_id
        assert ws.resource_group == resource_group
        assert ws.name == name

        ws = Workspace(
            credential=credential,
            resource_id=resource_id, 
            storage=storage, 
            location=location
        )
        assert ws.storage == storage

    def test_create_workspace_locations(self):
        subscription_id = "44ef49ad-64e4-44e5-a3ba-1ee87e19d3f4"
        resource_group = "rg"
        name = "n"

        credential = DefaultAzureCredential()

        # location is mandatory
        with self.assertRaises(Exception) as context:
            ws = Workspace(
                credential=credential,
                subscription_id=subscription_id,
                resource_group=resource_group,
                name=name,
            )
            self.assertTrue("Azure Quantum workspace does not have an associated location." in context.exception)

        # User-provided location name should be normalized
        location = "East US"
        ws = Workspace(
            credential=credential,
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location=location,
        )
        assert ws.location == "eastus"

    def test_create_workspace_instance_invalid(self):
        subscription_id = "44ef49ad-64e4-44e5-a3ba-1ee87e19d3f4"
        resource_group = "rg"
        storage = "strg"

        credential = DefaultAzureCredential()

        with pytest.raises(ValueError):
            Workspace(credential=credential)

        with pytest.raises(ValueError):
            Workspace(
                credential=credential,
                subscription_id=subscription_id,
                resource_group=resource_group,
                name="",
            )

        with pytest.raises(ValueError):
            Workspace(
                credential=credential,
                resource_id="invalid/resource/id"
            )

        with pytest.raises(ValueError):
            Workspace(
                credential=credential,
                storage=storage
            )
