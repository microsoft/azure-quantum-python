##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
from unittest import mock
from datetime import datetime
from azure.quantum import  Workspace

from common import (
    QuantumTestBase,
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
    LOCATION,
    STORAGE,
    API_KEY,
)

class TestWorkspace(QuantumTestBase):
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
        expected = """\startswith%28Name%2C%20%27name%27%29%20and%20%28%24\
            ItemType%20eq%20%27Session%27%20or%20ItemType%20eq%20%27\
            Job%27%29%20and%20%28%24JobType%20eq%20%27Regular%27%20or%20JobType%20eq%20%27Chemistry%27%29%20and%20%28%24\
            ProviderId%20eq%20%27ionq%27%20or%20ProviderId%20eq%20%27quantinuum%27%29%20and%20%28%24Target%20eq%20%27ionq.sim%27%20or%20\
            Target%20eq%20%27quantinuum%2Csim%27%29%20and%20%28%24State%20eq%20%27Completed%27%20or%20State%20eq%20%27Failed%27%29%20and%20\
            CreationTime%20ge%202024-10-01%20and%20CreationTime%20le%202024-11-01"""
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
    
 #   @pytest.mark.live_test
 #   def test_list_jobs(self):
 #       jobs = ws.list_jobs()
 #       return True
    
 #   @pytest.mark.live_test
 #   def test_list_jobs_paginated(self):
 #       jobs = ws.list_jobs()
 #       return True
    
 #   @pytest.mark.live_test
 #   def test_list_sessions(self):
 #       list_sessions
 #       return True
    
 #   @pytest.mark.live_test
 #   def test_list_sessions(self):
 #       list_sessions_paginated
 #       return True
    
 #   @pytest.mark.live_test
 #   def test_list_session_jobs(self):
 #       list_session_jobs
 #       return True
    
 #   @pytest.mark.live_test
 #   def test_list_session_jobs(self):
 #       list_session_jobs_paginated
 #       return True
    
 #   @pytest.mark.live_test
 #   def test_list_top_level_items(self):
 #       list_top_level_items
 #       return True
    
 #   @pytest.mark.live_test
 #   def test_list_top_level_items_paginated(self):
 #       list_top_level_items_paginated
 #       return True