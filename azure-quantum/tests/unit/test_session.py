##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest

from common import QuantumTestBase, ZERO_UID
from test_job_payload_factory import JobPayloadFactory
from azure.quantum import Job, Session, JobDetails, SessionStatus


class TestSession(QuantumTestBase):
    def _get_session_id(self):
        return ZERO_UID if self.is_playback else None

    def _get_job_id(self):
        return ZERO_UID if self.is_playback else Job.create_job_id()

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
    def test_session_get_session(self):
        workspace = self.create_workspace()
        session_id = self._get_session_id()
        session = Session(workspace=workspace,
                          id=session_id,
                          name="My Session",
                          target="ionq.simulator")
        self.assertIsNone(session.details.status)

        session.open()
        session_id = session_id if self.is_playback else session.id
        self.assertEqual(session.details.status, SessionStatus.WAITING)

        obtained_session = workspace.get_session(session_id=session_id)
        self.assertIsInstance(obtained_session, Session)
        self.assertEqual(obtained_session.id, session.id)
        self.assertEqual(obtained_session.details.id, session.details.id)
        self.assertEqual(obtained_session.details.target, session.details.target)
        self.assertEqual(obtained_session.details.provider_id, session.details.provider_id)
        self.assertEqual(obtained_session.details.name, session.details.name)
        self.assertEqual(obtained_session.details.status, session.details.status)

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_open_close(self):
        workspace = self.create_workspace()
        session_id = self._get_session_id()
        session = Session(workspace=workspace,
                          id=session_id,
                          target="ionq.simulator")
        self.assertIsNone(session.details.status)

        session.open()
        self.assertEqual(session.details.status, SessionStatus.WAITING)

        session.close()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)


    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_target_open_session(self):
        workspace = self.create_workspace()
        target = workspace.get_targets("ionq.simulator")
        self.assertIsNone(target.latest_session)
        session_id = self._get_session_id()
        session = target.open_session(id=session_id)
        session_id = session_id if self.is_playback else session.id
        self.assertIsNotNone(target.latest_session)
        self.assertEqual(target.latest_session.id, session_id)
        self.assertEqual(target.get_latest_session_id(), session_id)
        self.assertEqual(session.details.status, SessionStatus.WAITING)
        session.close()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)


    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_with_target_open_session(self):
        workspace = self.create_workspace()
        target = workspace.get_targets("ionq.simulator")
        self.assertIsNone(target.latest_session)
        session_id = self._get_session_id()
        with target.open_session(id=session_id) as session:
            session_id = session_id if self.is_playback else session.id
            self.assertIsNotNone(target.latest_session)
            self.assertEqual(target.latest_session.id, session_id)
            self.assertEqual(target.get_latest_session_id(), session_id)
            self.assertEqual(session.details.status, SessionStatus.WAITING)
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)
