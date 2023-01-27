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

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_list_sessions(self):
        workspace = self.create_workspace()
        result = workspace.list_sessions()
        result_types = map(type, result)
        self.assertIn(Session, result_types)

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_create_session(self):
        workspace = self.create_workspace()
        session_id = None
        from common import ZERO_UID
        if self.is_playback:
            session_id = ZERO_UID
        result = workspace.create_session(session_id=session_id)
        self.assertIsInstance(result, Session)

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_get_session(self):
        workspace = self.create_workspace()
        session_id = None
        from common import ZERO_UID
        if self.is_playback:
            session_id = ZERO_UID
        result = workspace.create_session(session_id=session_id)
        self.assertIsInstance(result, Session)
        result = workspace.get_session(session_id=result.id)
        self.assertIsInstance(result, Session)

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_end_session(self):
        workspace = self.create_workspace()
        session_id = None
        from common import ZERO_UID
        if self.is_playback:
            session_id = ZERO_UID
        result = workspace.create_session(session_id=session_id)
        self.assertIsInstance(result, Session)
        result = workspace.end_session(session_id=result.id)
        self.assertIsInstance(result, Session)
