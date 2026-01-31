##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from mock_client import create_default_workspace


def test_list_top_level_items_includes_jobs_and_sessions():
    ws = create_default_workspace()
    items = list(ws.list_top_level_items())
    assert items
    item_types = {type(it).__name__ for it in items}
    assert "Job" in item_types
    assert "Session" in item_types


def test_list_sessions_basic():
    ws = create_default_workspace()
    sessions = list(ws.list_sessions())
    assert sessions
    assert all(type(s).__name__ == "Session" for s in sessions)


def test_get_session_returns_matching_details_and_jobs():
    ws = create_default_workspace()
    # Choose a known session from the seeded data
    sessions = list(ws.list_sessions())
    assert sessions
    sid = sessions[0].id

    s = ws.get_session(session_id=sid)
    assert s
    assert s.id == sid
    assert s.details.id == sid

    # Verify session-scoped jobs are returned and have matching session_id
    jobs = list(s.list_jobs())
    assert jobs
    assert all(j.item_type == "Job" for j in jobs)
    assert all(getattr(j._details, "session_id", None) == sid for j in jobs)
