#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_session.py: Tests for Sessions
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import unittest
import os
import functools
import pytest
from datetime import date, datetime, timedelta

from common import QuantumTestBase, ZERO_UID
from azure.quantum.job.base_job import ContentType
from azure.quantum import Job, Session

class TestSession(QuantumTestBase):
    """TestSession

    Tests for Session
    """

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_list_top_level_items(self):
        workspace = self.create_workspace()
        result = workspace.list_top_level_items()
        result_types = map(type, result)
        self.assertIn(Job, result_types)
        self.assertIn(Session, result_types)
