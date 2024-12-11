##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
import os
from azure.quantum import Workspace

class TestWorkspacePagination():    
    @pytest.mark.live_test
    def test_list_jobs(self):
        subscription_id = os.getenv("SUBSCRIPTION_ID")
        resource_group = os.getenv("AZURE_QUANTUM_WORKSPACE_RG")
        name = os.getenv("AZURE_QUANTUM_WORKSPACE_NAME") 
        location = os.getenv("AZURE_QUANTUM_WORKSPACE_LOCATION")

        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location=location,
        )
        jobs = ws.list_jobs()
        jobs is not None
    
    @pytest.mark.live_test
    def test_list_sessions(self):
        subscription_id = os.getenv("SUBSCRIPTION_ID")
        resource_group = os.getenv("AZURE_QUANTUM_WORKSPACE_RG")
        name = os.getenv("AZURE_QUANTUM_WORKSPACE_NAME") 
        location = os.getenv("AZURE_QUANTUM_WORKSPACE_LOCATION")

        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location=location,
        )
        sessions = ws.list_sessions()
        sessions is not None
    
    @pytest.mark.live_test
    def test_list_session_jobs(self):
        subscription_id = os.getenv("SUBSCRIPTION_ID")
        resource_group = os.getenv("AZURE_QUANTUM_WORKSPACE_RG")
        name = os.getenv("AZURE_QUANTUM_WORKSPACE_NAME") 
        location = os.getenv("AZURE_QUANTUM_WORKSPACE_LOCATION")

        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location=location,
        )
        jobs = ws.list_session_jobs(session_id="aa9da17d-f786-11ee-a6f7-aa03815e5e6b")
        jobs is not None
    
    @pytest.mark.live_test
    def test_list_top_level_items(self):
        subscription_id = os.getenv("SUBSCRIPTION_ID")
        resource_group = os.getenv("AZURE_QUANTUM_WORKSPACE_RG")
        name = os.getenv("AZURE_QUANTUM_WORKSPACE_NAME")
        location = os.getenv("AZURE_QUANTUM_WORKSPACE_LOCATION")

        ws = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=name,
            location=location,
        )
        items = ws.list_top_level_items()
        items is not None
