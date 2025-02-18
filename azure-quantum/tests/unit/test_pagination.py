##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
import os
from datetime import date
from unittest import mock
from datetime import datetime
from azure.quantum import  Workspace
from common import (
    QuantumTestBase,
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
    LOCATION,
)

class TestWorkspacePagination(QuantumTestBase):
    def test_filter_valid(self):
        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
        )

        # pylint: disable=protected-access
        filter_string = ws._create_filter(job_name="name",
                                          item_type=["Session", "Job"],
                                          job_type=["Regular", "Chemistry"],
                                          provider_ids=["ionq", "quantinuum"],
                                          target=["ionq.sim", "quantinuum,sim"],
                                          status=["Completed", "Failed"],
                                          created_after=datetime(2024, 10, 1),
                                          created_before=datetime(2024, 11, 1))
        # pylint: enable=protected-access
        expected = "startswith(Name, 'name') and (ItemType eq 'Session' or ItemType eq 'Job') and (JobType eq 'Regular' or JobType eq 'Chemistry') and (ProviderId eq 'ionq' or ProviderId eq 'quantinuum') and (Target eq 'ionq.sim' or Target eq 'quantinuum,sim') and (State eq 'Completed' or State eq 'Failed') and CreationTime ge 2024-10-01 and CreationTime le 2024-11-01"
        self.assertEqual(filter_string, expected)

    def test_orderby_valid(self):
        var_names = ["Name", "ItemType", "JobType", "ProviderId", "Target", "State", "CreationTime"]

        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
        )

        for var_name in var_names:
            # pylint: disable=protected-access
            orderby = ws._create_orderby(var_name, True)
            # pylint: enable=protected-access
            expected = var_name + " "+"asc"
            self.assertEqual(orderby, expected)

        for var_name in var_names:
            # pylint: disable=protected-access
            orderby = ws._create_orderby(var_name, False)
            # pylint: enable=protected-access
            expected = var_name + " "+"desc"
            self.assertEqual(orderby, expected)

    def test_orderby_invalid(self):
        ws = Workspace(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            name=WORKSPACE,
            location=LOCATION,
        )
        # pylint: disable=protected-access
        self.assertRaises(ValueError, ws._create_orderby, "test", True)
        self.assertRaises(ValueError, ws._create_orderby, "test", False)
        # pylint: enable=protected-access

    @pytest.mark.live_test
    def test_list_jobs(self):
        ws = self.create_workspace()
        
        jobs = ws.list_jobs()
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_name(self):
        ws = self.create_workspace()
        
        jobs = ws.list_jobs(name_match = "ionq")
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_name = job.details.name.startswith("ionq")
            self.assertTrue( check_job_name, job.details.name)

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_job_type(self):
        ws = self.create_workspace()
        
        jobs = ws.list_jobs(job_type = ["QuantumComputing", "QuantumChemistry"])
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_type = job.details.job_type == "QuantumComputing" or job.details.job_type == "QuantumChemistry"
            self.assertTrue( check_job_type, job.details.job_type)

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_provider(self):
        ws = self.create_workspace()
        
        jobs = ws.list_jobs(provider = ["microsoft-qc", "ionq"])
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_provider = job.details.provider_id == "microsoft-qc" or job.details.provider_id == "ionq"
            self.assertTrue( check_job_provider, job.details.provider_id)

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_target(self):
        ws = self.create_workspace()
        
        jobs = ws.list_jobs(target = ["microsoft.estimator", "microsoft.dft"])
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_target = job.details.target == "microsoft.estimator" or job.details.target == "microsoft.dft"
            self.assertTrue( check_job_target, job.details.target)

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_status(self):
        ws = self.create_workspace()
        
        jobs = ws.list_jobs(status = ["Failed", "Cancelled"])
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_status = job.details.status == "Failed" or job.details.status == "Cancelled"
            self.assertTrue( check_job_status, job.details.status)

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_created_after(self):
        ws = self.create_workspace()
    
        test_date = datetime(2024, 8, 1, 12, 30)
        jobs = ws.list_jobs(created_after = test_date)
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_created_after = job.details.creation_time.date() >= test_date.date()
            self.assertTrue( check_job_created_after, job.details.creation_time)

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_created_before(self):
        ws = self.create_workspace()
    
        test_date = datetime(2024, 4, 1, 12, 30)
        jobs = ws.list_jobs(created_before = test_date)
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_created_before = job.details.creation_time.date() <= test_date.date()
            self.assertTrue( check_job_created_before, job.details.creation_time)

    @pytest.mark.live_test
    def test_list_jobs_orderby_asc(self):
        ws = self.create_workspace()
    
        test_date = datetime(2024, 4, 1)
        jobs = ws.list_jobs(created_before = test_date, orderby_property="CreationTime", is_asc=True)

        creation_time = None
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_created_before = job.details.creation_time.date() <= test_date.date()
            self.assertTrue( check_job_created_before, job.details.creation_time)

            if creation_time is None:
                creation_time = job.details.creation_time
            else:
                check_item_created_before_order = job.details.creation_time >= creation_time
                self.assertTrue( check_item_created_before_order, job.details.creation_time)
                creation_time = job.details.creation_time
        
    @pytest.mark.live_test
    def test_list_jobs_orderby_desc(self):
        ws = self.create_workspace()
    
        test_date = datetime(2024, 4, 1)
        jobs = ws.list_jobs(created_before = test_date,  orderby_property="CreationTime", is_asc=False)

        creation_time = None
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_created_before = job.details.creation_time.date() <= test_date.date()
            self.assertTrue( check_job_created_before, job.details.creation_time)

            if creation_time is None:
                creation_time = job.details.creation_time
            else:
                check_item_created_before_order = job.details.creation_time <= creation_time
                self.assertTrue( check_item_created_before_order, job.details.creation_time)
                creation_time = job.details.creation_time
    
    @pytest.mark.live_test
    def test_list_sessions(self):
        ws = self.create_workspace()
        sessions = ws.list_sessions()
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

    @pytest.mark.live_test
    def test_list_sessions_filtered_by_provider(self):
        ws = self.create_workspace()

        sessions = ws.list_sessions(provider = ["microsoft-qc", "ionq"])
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

            check_session_provider = session._details.provider_id == "microsoft-qc" or session._details.provider_id == "ionq"
            self.assertTrue( check_session_provider, session._details.provider_id)

    @pytest.mark.live_test
    def test_list_sessions_filtered_by_target(self):
        ws = self.create_workspace()

        sessions = ws.list_sessions(target = ["ionq.test", "ionq.simulator"])
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

            check_session_target = session._details.target == "ionq.test" or session._details.target == "ionq.simulator"
            self.assertTrue( check_session_target, session._details.target)

    @pytest.mark.live_test
    def test_list_sessions_filtered_by_state(self):
        ws = self.create_workspace()

        sessions = ws.list_sessions(status = ["Succeeded"])
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

            check_session_status = session._details.status == "Succeeded"
            self.assertTrue( check_session_status, session._details.status)

    @pytest.mark.live_test
    def test_list_sessions_filtered_by_created_after(self):
        ws = self.create_workspace()

        test_date = datetime(2024, 4, 1, 12, 30)
        sessions = ws.list_sessions(created_after = test_date)
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

            check_session_created_after = session._details.creation_time.date() >= test_date.date()
            self.assertTrue(check_session_created_after, session._details.creation_time)

    @pytest.mark.live_test
    def test_list_sessions_filtered_by_created_before(self):
        ws = self.create_workspace()

        test_date = datetime(2024, 5, 1, 12, 30)
        sessions = ws.list_sessions(created_before = test_date)
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

            check_session_created_after = session._details.creation_time.date() <= test_date.date()
            self.assertTrue( check_session_created_after, session._details.creation_time)

    @pytest.mark.live_test
    def test_list_sessions_orderby_asc(self):
        ws = self.create_workspace()

        test_date = datetime(2024, 5, 1)

        creation_time = None
        sessions = ws.list_sessions(created_before = test_date, orderby_property="CreationTime", is_asc=True)
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

            check_session_created_after = session._details.creation_time.date() <= test_date.date()
            self.assertTrue( check_session_created_after, session._details.creation_time)

            if creation_time is None:
                creation_time = session.details.creation_time
            else:
                check_item_created_before_order = session.details.creation_time >= creation_time
                self.assertTrue( check_item_created_before_order, session.details.creation_time)
                creation_time = session.details.creation_time

    @pytest.mark.live_test
    def test_list_sessions_orderby_desc_filtered_by_created_before(self):
        ws = self.create_workspace()

        test_date = datetime(2024, 5, 1, 12, 30)

        creation_time = None
        sessions = ws.list_sessions(created_before = test_date, orderby_property="CreationTime", is_asc=False)
        for session in sessions:
            self.assertEqual(session.item_type, "Session")

            check_session_created_after = session._details.creation_time.date() <= test_date.date()
            self.assertTrue( check_session_created_after, session._details.creation_time)

            if creation_time is None:
                creation_time = session.details.creation_time
            else:
                check_item_created_before_order = session.details.creation_time <= creation_time
                self.assertTrue( check_item_created_before_order, session.details.creation_time)
                creation_time = session.details.creation_time
    
    @pytest.mark.live_test
    def test_list_session_jobs(self):
        # please change to valid session id for recording
        session_id = "cd61afdb-eb34-11ef-a0c7-5414f37777d8"
        #session_id = "00000000-0000-0000-0000-000000000001"

        ws = self.create_workspace()
        jobs = ws.list_session_jobs(session_id=session_id)

        for job in jobs:
            self.assertEqual(job.item_type, "Job")
            self.assertEqual(job._details.session_id, session_id)

    @pytest.mark.live_test
    def test_list_session_jobs_filtered_by_name(self):
        # please change to valid session id for recording
        session_id = "cd61afdb-eb34-11ef-a0c7-5414f37777d8"
        #session_id = "00000000-0000-0000-0000-000000000001"

        ws = self.create_workspace()
        jobs = ws.list_session_jobs(session_id=session_id, name_match="Job")

        for job in jobs:
            self.assertEqual(job.item_type, "Job")
            self.assertEqual(job._details.session_id, session_id)
            
            check_job_name = job.details.name.startswith("Job")
            self.assertTrue( check_job_name, job.details.name)

    @pytest.mark.live_test
    def test_list_session_jobs_filtered_by_status(self):
        # please change to valid session id for recording
        session_id = "cd61afdb-eb34-11ef-a0c7-5414f37777d8"
        #session_id = "00000000-0000-0000-0000-000000000001"

        ws = self.create_workspace()
        jobs = ws.list_session_jobs(session_id=session_id, status=["Succeeded"])

        for job in jobs:
            self.assertEqual(job.item_type, "Job")
            self.assertEqual(job._details.session_id, session_id)

            check_job_status = job.details.status == "Succeeded"
            self.assertTrue( check_job_status, job.details.status)

    @pytest.mark.live_test
    def test_list_session_jobs_orderby_asc(self):
        # please change to valid session id for recording
        session_id = "cd61afdb-eb34-11ef-a0c7-5414f37777d8"
        #session_id = "00000000-0000-0000-0000-000000000001"

        ws = self.create_workspace()
        jobs = ws.list_session_jobs(session_id=session_id, status=["Succeeded"], orderby_property="CreationTime", is_asc=True)

        creation_time = None
        for job in jobs:
            self.assertEqual(job.item_type, "Job")
            self.assertEqual(job._details.session_id, session_id)

            check_job_status = job.details.status == "Succeeded"
            self.assertTrue( check_job_status, job.details.status)

            if creation_time is None:
                creation_time = job.details.creation_time
            else:
                check_item_created_before_order = job.details.creation_time >= creation_time
                self.assertTrue( check_item_created_before_order, job.details.creation_time)
                creation_time = job.details.creation_time

    @pytest.mark.live_test
    def test_list_session_jobs_orderby_desc(self):
        # please change to valid session id for recording
        session_id = "cd61afdb-eb34-11ef-a0c7-5414f37777d8"
        #session_id = "00000000-0000-0000-0000-000000000001"

        ws = self.create_workspace()
        jobs = ws.list_session_jobs(session_id=session_id, status=["Succeeded"], orderby_property="CreationTime", is_asc=False)

        creation_time = None
        for job in jobs:
            self.assertEqual(job.item_type, "Job")
            self.assertEqual(job._details.session_id, session_id)

            check_job_status = job.details.status == "Succeeded"
            self.assertTrue( check_job_status, job.details.status)

            if creation_time is None:
                creation_time = job.details.creation_time
            else:
                check_item_created_before_order = job.details.creation_time <= creation_time
                self.assertTrue( check_item_created_before_order, job.details.creation_time)
                creation_time = job.details.creation_time
    
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

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_name(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name
        
        items = ws.list_top_level_items(name_match = "ionq")
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_name = item.details.name.startswith("ionq")
            self.assertTrue( check_item_name, item.details.name)

        items = ws.list_top_level_items(name_match = "session")
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_name = item.details.name.startswith("session")
            self.assertTrue( check_item_name, item.details.name)

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_item_type(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name
        
        items = ws.list_top_level_items(item_type = ["job"])
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            self.assertEqual(item.item_type, "Job")

        items = ws.list_top_level_items(item_type = ["session"])
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            self.assertEqual(item.item_type, "Session")

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_job_type(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name
        
        items = ws.list_top_level_items(job_type = ["QuantumComputing", "QuantumChemistry"])
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_type = item.details.job_type == "QuantumComputing" or item.details.job_type == "QuantumChemistry"
            self.assertTrue( check_item_type, item.details.job_type)

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_provider(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name
        
        items = ws.list_top_level_items(provider = ["microsoft-qc", "ionq"])
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_provider = item.details.provider_id == "microsoft-qc" or item.details.provider_id == "ionq"
            self.assertTrue( check_item_provider, item.details.provider_id)

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_target(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name
        
        items = ws.list_top_level_items(target = ["microsoft.estimator", "microsoft.dft"])
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_target = item.details.target == "microsoft.estimator" or item.details.target == "microsoft.dft"
            self.assertTrue( check_item_target, item.details.target)

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_status(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name
        
        items = ws.list_top_level_items(status = ["Failed", "Cancelled"])
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_status = item.details.status == "Failed" or item.details.status == "Cancelled"
            self.assertTrue( check_item_status, item.details.status)

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_created_after(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name

        test_date = datetime(2024, 12, 1, 12, 30)

        items = ws.list_top_level_items(created_after = test_date)
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_created_after = item.details.creation_time.date() >= test_date.date()
            self.assertTrue( check_item_created_after, item.details.creation_time)

    @pytest.mark.live_test
    def test_list_top_level_items_filtered_by_created_before(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name

        test_date = datetime(2024, 3, 1, 12, 30)

        items = ws.list_top_level_items(created_before = test_date)
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_created_before = item.details.creation_time.date() <= test_date.date()
            self.assertTrue( check_item_created_before, item.details.creation_time)

    @pytest.mark.live_test
    def test_list_top_level_items_orderby_asc(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name

        test_date = datetime(2024, 12, 1)

        items = ws.list_top_level_items(created_after = test_date, orderby_property="CreationTime", is_asc=True)

        creation_time = None
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_created_after = item.details.creation_time.date() >= test_date.date()
            self.assertTrue( check_item_created_after, item.details.creation_time)

            if creation_time is None:
                creation_time = item.details.creation_time
            else:
                check_item_created_before_order = item.details.creation_time >= creation_time
                self.assertTrue( check_item_created_before_order, item.details.creation_time)
                creation_time = item.details.creation_time

    @pytest.mark.live_test
    def test_list_top_level_items_orderby_desc(self):
        ws = self.create_workspace()
        subscription_id = ws.subscription_id
        resource_group = ws.resource_group
        workspace_name = ws.name

        test_date = datetime(2024, 12, 1)

        items = ws.list_top_level_items(created_after = test_date, orderby_property="CreationTime", is_asc=False)

        creation_time = None
        for item in items:
            self.assertEqual(item.workspace.subscription_id, subscription_id)
            self.assertEqual(item.workspace.resource_group, resource_group)
            self.assertEqual(item.workspace.name, workspace_name)

            check_item_created_after = item.details.creation_time.date() >= test_date.date()
            self.assertTrue( check_item_created_after, item.details.creation_time)

            if creation_time is None:
                creation_time = item.details.creation_time
            else:
                check_item_created_before_order = item.details.creation_time <= creation_time
                self.assertTrue( check_item_created_before_order, item.details.creation_time)
                creation_time = item.details.creation_time
