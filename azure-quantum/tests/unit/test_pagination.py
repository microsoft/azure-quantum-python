##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
from common import (
    QuantumTestBase
)

class TestWorkspacePagination(QuantumTestBase):    
    @pytest.mark.live_test
    def test_list_jobs(self):
        ws = self.create_workspace()
        
        jobs = ws.list_jobs()
        for job in jobs:
            self.assertEqual(job.item_type, "Job")
    
    @pytest.mark.live_test
    def test_list_sessions(self):
        ws = self.create_workspace()
        sessions = ws.list_sessions()
        for session in sessions:
            self.assertEqual(session.item_type, "Session")
    
    @pytest.mark.live_test
    def test_list_session_jobs(self):
        session_id = "aa9da17d-f786-11ee-a6f7-aa03815e5e6b"

        ws = self.create_workspace()
        jobs = ws.list_session_jobs(session_id=session_id)

        for job in jobs:
            self.assertEqual(job.item_type, "Job")
            self.assertEqual(job._details.session_id, session_id)
    
    @pytest.mark.live_test
    def test_list_top_level_items(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name
        
        items = ws.list_top_level_items()
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)
