#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_session.py: Tests for Sessions
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest

from common import QuantumTestBase, ZERO_UID
from azure.quantum import Job, Session, JobDetails

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

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_list_session_jobs(self):
        workspace = self.create_workspace()

        import uuid
        session_id = None
        from common import ZERO_UID
        if self.is_playback:
            session_id = ZERO_UID

        job_id = str(uuid.uuid1())
        from common import ZERO_UID
        if self.is_playback:
            job_id = ZERO_UID

        session = workspace.create_session(session_id=session_id)
        self.assertIsInstance(session, Session)
        job = workspace.submit_job(
            Job(workspace=workspace,
                job_details=JobDetails(id=job_id,
                                       name=f"job-{job_id}",
                                       provider_id="ionq",
                                       target="ionq.simulator",
                                       container_uri="https://mystorage.blob.core.windows.net/job-00000000-0000-0000-0000-000000000000/inputData",
                                       input_data_format="mydataformat",
                                       output_data_format="mydataformat",
                                       session_id=session.id)
                                 ))

        jobs = workspace.list_session_jobs(session_id=session.id)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(job.id, jobs[0].id)
        self.assertEqual(job.details.id, jobs[0].details.id)
        self.assertEqual(job.details.name, jobs[0].details.name)
        self.assertEqual(job.details.provider_id, jobs[0].details.provider_id)
        self.assertEqual(job.details.target, jobs[0].details.target)
        self.assertEqual(job.details.container_uri, jobs[0].details.container_uri)
        self.assertEqual(job.details.input_data_format, jobs[0].details.input_data_format)
        self.assertEqual(job.details.output_data_format, jobs[0].details.output_data_format)
        self.assertEqual(job.details.session_id, jobs[0].details.session_id)

        result = workspace.end_session(session_id=session.id)
        self.assertIsInstance(result, Session)
