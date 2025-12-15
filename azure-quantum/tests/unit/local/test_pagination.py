from datetime import datetime, UTC, timedelta

from mock_client import create_default_workspace


def test_list_jobs_basic():
    ws = create_default_workspace()
    jobs = list(ws.list_jobs())
    assert all(j.item_type == "Job" for j in jobs)
    assert len(jobs) >= 4


def test_list_jobs_filters():
    ws = create_default_workspace()
    # name prefix
    jobs = list(ws.list_jobs(name_match="ionq"))
    assert jobs and all(j.details.name.startswith("ionq") for j in jobs)
    # provider
    jobs = list(ws.list_jobs(provider=["ionq"]))
    assert jobs and all(j.details.provider_id == "ionq" for j in jobs)
    # target
    jobs = list(ws.list_jobs(target=["microsoft.estimator", "microsoft.dft"]))
    assert all(
        j.details.target in {"microsoft.estimator", "microsoft.dft"} for j in jobs
    )
    # status
    jobs = list(ws.list_jobs(status=["Failed", "Cancelled"]))
    assert all(j.details.status in {"Failed", "Cancelled"} for j in jobs)


def test_list_jobs_created_window_and_ordering():
    ws = create_default_workspace()
    after = datetime.now(UTC) - timedelta(days=9)
    before = datetime.now(UTC) + timedelta(days=1)
    # asc
    asc = list(
        ws.list_jobs(
            created_after=after,
            created_before=before,
            orderby_property="CreationTime",
            is_asc=True,
        )
    )
    assert all(
        j.details.creation_time.date() >= after.date()
        and j.details.creation_time.date() <= before.date()
        for j in asc
    )
    for a, b in zip(asc, asc[1:]):
        assert a.details.creation_time <= b.details.creation_time
    # desc
    desc = list(
        ws.list_jobs(
            created_after=after,
            created_before=before,
            orderby_property="CreationTime",
            is_asc=False,
        )
    )
    for a, b in zip(desc, desc[1:]):
        assert a.details.creation_time >= b.details.creation_time
    # missing creation_time default handling ensures item is included and sortable
    all_jobs = list(ws.list_jobs(orderby_property="CreationTime", is_asc=True))
    assert any(j.details.id == "j-rig-1" for j in all_jobs)


def test_list_jobs_paging_basic():
    ws = create_default_workspace()
    jobs = ws.list_jobs(orderby_property="CreationTime", is_asc=True)
    # Ensure iterable and ordered
    jobs_list = list(jobs)
    assert len(jobs_list) >= 1
    for a, b in zip(jobs_list, jobs_list[1:]):
        assert a.details.creation_time <= b.details.creation_time


def test_list_sessions_basic_and_filters():
    ws = create_default_workspace()
    sessions = list(ws.list_sessions())
    assert all(s.item_type == "Session" for s in sessions)
    # provider filter
    f = list(ws.list_sessions(provider=["ionq"]))
    assert f and all(s._details.provider_id == "ionq" for s in f)
    # target filter
    t = list(ws.list_sessions(target=["ionq.test", "ionq.simulator"]))
    assert t and all(s._details.target in {"ionq.test", "ionq.simulator"} for s in t)
    # status filter
    st = list(ws.list_sessions(status=["Succeeded"]))
    assert st and all(s._details.status == "Succeeded" for s in st)
    # multi-value ORs
    prov_or = ws.list_sessions(provider=["ionq", "quantinuum"])
    assert prov_or and all(
        s._details.provider_id in {"ionq", "quantinuum"} for s in prov_or
    )
    st_or = ws.list_sessions(status=["Succeeded", "WAITING"])
    assert st_or and all(s._details.status in {"Succeeded", "WAITING"} for s in st_or)


def test_list_sessions_created_ordering():
    ws = create_default_workspace()
    before = datetime.now(UTC) + timedelta(days=1)
    asc = list(
        ws.list_sessions(
            created_before=before, orderby_property="CreationTime", is_asc=True
        )
    )
    for a, b in zip(asc, asc[1:]):
        assert a.details.creation_time <= b.details.creation_time
    desc = list(
        ws.list_sessions(
            created_before=before, orderby_property="CreationTime", is_asc=False
        )
    )
    for a, b in zip(desc, desc[1:]):
        assert a.details.creation_time >= b.details.creation_time


def test_list_session_jobs_filters_and_order():
    ws = create_default_workspace()
    sessions = list(ws.list_sessions())
    assert sessions
    sid = sessions[0].id
    jobs = list(ws.list_session_jobs(session_id=sid))
    assert jobs and all(
        j.item_type == "Job" and j._details.session_id == sid for j in jobs
    )
    jn = list(ws.list_session_jobs(session_id=sid, name_match="ionqJob"))
    assert all(j.details.name.startswith("ionqJob") for j in jn)
    js = list(ws.list_session_jobs(session_id=sid, status=["Succeeded"]))
    assert all(j.details.status == "Succeeded" for j in js)
    asc = list(
        ws.list_session_jobs(
            session_id=sid, orderby_property="CreationTime", is_asc=True
        )
    )
    for a, b in zip(asc, asc[1:]):
        assert a.details.creation_time <= b.details.creation_time
    desc = list(
        ws.list_session_jobs(
            session_id=sid, orderby_property="CreationTime", is_asc=False
        )
    )
    for a, b in zip(desc, desc[1:]):
        assert a.details.creation_time >= b.details.creation_time


def test_list_top_level_items_basic_and_filters():
    ws = create_default_workspace()
    items = list(ws.list_top_level_items())
    assert all(i.workspace.subscription_id == ws.subscription_id for i in items)
    # name filters
    i1 = list(ws.list_top_level_items(name_match="ionq"))
    assert all(it.details.name.startswith("ionq") for it in i1)
    # exact-case only; mixed-case not supported per API
    # provider
    # combined provider AND status AND window
    before = datetime.now(UTC) + timedelta(days=1)
    combo = list(
        ws.list_sessions(provider=["ionq"], status=["Succeeded"], created_before=before)
    )
    assert combo and all(
        s._details.provider_id == "ionq" and s._details.status == "Succeeded"
        for s in combo
    )
    prov = list(ws.list_top_level_items(provider=["ionq"]))
    assert prov and all(it.details.provider_id == "ionq" for it in prov)
    # target
    tgt = list(ws.list_top_level_items(target=["microsoft.estimator", "microsoft.dft"]))
    assert all(
        it.details.target in {"microsoft.estimator", "microsoft.dft"} for it in tgt
    )
    # status
    st = list(ws.list_top_level_items(status=["Failed", "Cancelled"]))
    assert all(it.details.status in {"Failed", "Cancelled"} for it in st)
    # combined filters: provider AND target; with seeded AND-match expect results
    combo = list(
        ws.list_top_level_items(provider=["ionq"], target=["microsoft.estimator"])
    )
    assert combo and all(
        it.details.provider_id == "ionq" and it.details.target == "microsoft.estimator"
        for it in combo
    )

    # case sensitivity: lower-case item_type should return empty
    combo_case = list(ws.list_top_level_items(item_type=["job"]))
    assert len(combo_case) == 0

    # multi-value OR grouping for item_type should return both types
    both_types = list(ws.list_top_level_items(item_type=["Job", "Session"]))
    assert (
        both_types
        and any(it.item_type == "Job" for it in both_types)
        and any(it.item_type == "Session" for it in both_types)
    )

    # multi-value OR grouping for job_type should include both QuantumComputing and QuantumChemistry
    jt_multi = list(
        ws.list_top_level_items(job_type=["QuantumComputing", "QuantumChemistry"])
    )
    assert (
        jt_multi
        and any(
            getattr(it.details, "job_type", None) == "QuantumComputing"
            for it in jt_multi
        )
        and any(
            getattr(it.details, "job_type", None) == "QuantumChemistry"
            for it in jt_multi
        )
    )

    # date boundary tests: created_after/on boundary includes items; created_before/on boundary includes items
    # choose a boundary based on a known seeded item creation_time
    boundary_date = next(
        it.details.creation_time.date() for it in items if it.details.name == "msJobA"
    )
    after_inclusive = list(
        ws.list_top_level_items(
            created_after=datetime.combine(
                boundary_date, datetime.min.time(), tzinfo=UTC
            )
        )
    )
    assert any(
        it.details.creation_time.date() >= boundary_date for it in after_inclusive
    )
    before_inclusive = list(
        ws.list_top_level_items(
            created_before=datetime.combine(
                boundary_date, datetime.min.time(), tzinfo=UTC
            )
        )
    )
    assert any(
        it.details.creation_time.date() <= boundary_date for it in before_inclusive
    )
    # job_type + provider + target (AND semantics); with seeded combo expect non-empty
    jt_combo = list(
        ws.list_top_level_items(
            job_type=["QuantumComputing"],
            provider=["ionq"],
            target=["microsoft.estimator"],
        )
    )
    assert jt_combo and all(
        getattr(it.details, "job_type", None) == "QuantumComputing"
        and it.details.provider_id == "ionq"
        and it.details.target == "microsoft.estimator"
        for it in jt_combo
    )
    # negative test: no match
    none_items = list(ws.list_top_level_items(provider=["no-provider"]))
    assert len(none_items) == 0


def test_list_top_level_items_created_ordering():
    ws = create_default_workspace()
    after = datetime.now(UTC) - timedelta(days=15)
    asc = list(
        ws.list_top_level_items(
            created_after=after, orderby_property="CreationTime", is_asc=True
        )
    )
    for a, b in zip(asc, asc[1:]):
        assert a.details.creation_time <= b.details.creation_time
    desc = list(
        ws.list_top_level_items(
            created_after=after, orderby_property="CreationTime", is_asc=False
        )
    )
    for a, b in zip(desc, desc[1:]):
        assert a.details.creation_time >= b.details.creation_time
    # Ascending with created_after boundary
    start = datetime.now(UTC) - timedelta(days=365)
    items_after = list(
        ws.list_top_level_items(
            created_after=start, orderby_property="CreationTime", is_asc=True
        )
    )
    assert items_after
    prev = None
    for it in items_after:
        assert it.details.creation_time.date() >= start.date()
        if prev is None:
            prev = it.details.creation_time
        else:
            assert it.details.creation_time >= prev
            prev = it.details.creation_time


def test_filter_string_emission():
    ws = create_default_workspace()
    # pylint: disable=protected-access
    filter_string = ws._create_filter(
        job_name="name",
        item_type=["Session", "Job"],
        job_type=["Regular", "Chemistry"],
        provider_ids=["ionq", "quantinuum"],
        target=["ionq.sim", "quantinuum,sim"],
        status=["Completed", "Failed"],
        created_after=datetime(2024, 10, 1),
        created_before=datetime(2024, 11, 1),
    )
    # pylint: enable=protected-access
    expected = (
        "startswith(Name, 'name') and (ItemType eq 'Session' or ItemType eq 'Job') and "
        "(JobType eq 'Regular' or JobType eq 'Chemistry') and (ProviderId eq 'ionq' or ProviderId eq 'quantinuum') and "
        "(Target eq 'ionq.sim' or Target eq 'quantinuum,sim') and (State eq 'Completed' or State eq 'Failed') and "
        "CreationTime ge 2024-10-01 and CreationTime le 2024-11-01"
    )
    assert filter_string == expected


def test_orderby_emission_and_validation():
    ws = create_default_workspace()
    props = [
        "Name",
        "ItemType",
        "JobType",
        "ProviderId",
        "Target",
        "State",
        "CreationTime",
    ]
    # pylint: disable=protected-access
    for p in props:
        assert ws._create_orderby(p, True) == f"{p} asc"
        assert ws._create_orderby(p, False) == f"{p} desc"
    try:
        ws._create_orderby("test", True)
        assert False, "Expected ValueError for invalid property"
    except ValueError:
        pass
    # pylint: enable=protected-access
