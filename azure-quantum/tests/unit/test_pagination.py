##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from unittest import mock
import pytest
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
#    def test_filter_valid(self):
#        return True
    
#    def test_filter_invalid(self):
#        return False

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