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
        expected = "startswith%28Name%2C%20%27name%27%29%20and%20%28%24ItemType%20eq%20%27Session%27%20or%20ItemType%20eq%20%27Job%27%29%20and%20%28JobType%20eq%20%27Regular%27%20or%20JobType%20eq%20%27Chemistry%27%29%20and%20%28ProviderId%20eq%20%27ionq%27%20or%20ProviderId%20eq%20%27quantinuum%27%29%20and%20%28Target%20eq%20%27ionq.sim%27%20or%20Target%20eq%20%27quantinuum%2Csim%27%29%20and%20%28State%20eq%20%27Completed%27%20or%20State%20eq%20%27Failed%27%29%20and%20CreationTime%20ge%202024-10-01%20and%20CreationTime%20le%202024-11-01"
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
            expected = var_name + "%20"+"asc"
            self.assertEqual(orderby, expected)

        for var_name in var_names:
            # pylint: disable=protected-access
            orderby = ws._create_orderby(var_name, False)
            # pylint: enable=protected-access
            expected = var_name + "%20"+"desc"
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
    
        test_date = date(2024, 8, 1)
        jobs = ws.list_jobs(created_after = test_date)
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_created_after = job.details.creation_time.date() >= test_date
            self.assertTrue( check_job_created_after, job.details.creation_time)

    @pytest.mark.live_test
    def test_list_jobs_filtered_by_created_before(self):
        ws = self.create_workspace()
    
        test_date = date(2024, 4, 1)
        jobs = ws.list_jobs(created_before = test_date)
        for job in jobs:
            self.assertEqual(job.item_type, "Job")

            check_job_created_before = job.details.creation_time.date() <= test_date
            self.assertTrue( check_job_created_before, job.details.creation_time)
    
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
    
    #: Optional[list[str]]= None,
    #    target: Optional[list[str]]= None,
    #    status: Optional[list[JobStatus]] = None,
    #    created_after: Optional[datetime] = None,
    #    created_before: Optional[datetime] = None
    
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
