from datetime import datetime, UTC, timedelta

from azure.quantum.workspace import Workspace
from azure.quantum._client import ServicesClient
from azure.quantum._client.models import JobDetails, SessionDetails

from mock_client import MockServicesClient


class WorkspaceMock(Workspace):
    def _create_client(self) -> ServicesClient:
        return MockServicesClient()


def seed_jobs(ws: WorkspaceMock):
    base = datetime.now(UTC) - timedelta(days=10)
    samples = [
        JobDetails(
            id="j-ionq-1",
            name="ionqJobA",
            provider_id="ionq",
            target="ionq.simulator",
            status="Succeeded",
            creation_time=base + timedelta(days=1),
            session_id="s-ionq-1",
            job_type="QuantumComputing",
        ),
        JobDetails(
            id="j-ionq-2",
            name="ionqJobB",
            provider_id="ionq",
            target="ionq.simulator",
            status="Failed",
            creation_time=base + timedelta(days=2),
            session_id="s-ionq-1",
        ),
        JobDetails(
            id="j-qh-1",
            name="qhJobA",
            provider_id="quantinuum",
            target="quantinuum.sim",
            status="Cancelled",
            creation_time=base + timedelta(days=3),
            session_id="s-ionq-2",
            job_type="QuantumChemistry",
        ),
        JobDetails(
            id="j-ms-1",
            name="msJobA",
            provider_id="microsoft",
            target="microsoft.estimator",
            status="Succeeded",
            creation_time=base + timedelta(days=4),
            # explicit missing job_type
        ),
        # Rigetti-like shape: different target format, missing creation_time to test default handling
        JobDetails(
            id="j-rig-1",
            name="rigJobA",
            provider_id="rigetti",
            target="rigetti.qpu",
            status="Succeeded",
            # creation_time omitted deliberately
        ),
    ]
    for d in samples:
        ws._client.jobs.create_or_replace(
            ws.subscription_id, ws.resource_group, ws.name, job_id=d.id, job_details=d
        )


def seed_sessions(ws: WorkspaceMock):
    base = datetime.now(UTC) - timedelta(days=5)
    samples = [
        SessionDetails(
            id="s-ionq-1",
            name="sessionA",
            provider_id="ionq",
            target="ionq.simulator",
            status="Succeeded",
            creation_time=base + timedelta(days=1),
        ),
        SessionDetails(
            id="s-ionq-2",
            name="sessionB",
            provider_id="ionq",
            target="ionq.test",
            status="Succeeded",
            creation_time=base + timedelta(days=2),
        ),
    ]
    for s in samples:
        ws._client.sessions.create_or_replace(
            ws.subscription_id,
            ws.resource_group,
            ws.name,
            session_id=s.id,
            session_details=s,
        )


def test_list_jobs_basic():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_jobs(ws)
    jobs = list(ws.list_jobs())
    assert all(j.item_type == "Job" for j in jobs)
    assert len(jobs) >= 4


def test_list_jobs_filters():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_jobs(ws)
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
    # job_type presence/absence
    jt = list(ws.list_jobs(job_type=["QuantumComputing", "QuantumChemistry"]))
    assert any(getattr(j.details, "job_type", None) == "QuantumComputing" for j in jt)
    assert any(getattr(j.details, "job_type", None) == "QuantumChemistry" for j in jt)
    # target format variety
    rv = list(ws.list_jobs(target=["rigetti.qpu"]))
    assert rv and all(j.details.target == "rigetti.qpu" for j in rv)


def test_list_jobs_created_window_and_ordering():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_jobs(ws)
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
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_jobs(ws)
    jobs = ws.list_jobs(orderby_property="CreationTime", is_asc=True)
    # Ensure iterable and ordered
    jobs_list = list(jobs)
    assert len(jobs_list) >= 1
    for a, b in zip(jobs_list, jobs_list[1:]):
        assert a.details.creation_time <= b.details.creation_time


def test_list_sessions_basic_and_filters():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_sessions(ws)
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


def test_list_sessions_created_ordering():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_sessions(ws)
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
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_sessions(ws)
    seed_jobs(ws)
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
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_jobs(ws)
    seed_sessions(ws)
    items = list(ws.list_top_level_items())
    assert all(i.workspace.subscription_id == ws.subscription_id for i in items)
    # name filters
    i1 = list(ws.list_top_level_items(name_match="ionq"))
    assert all(it.details.name.startswith("ionq") for it in i1)
    i2 = list(ws.list_top_level_items(name_match="session"))
    assert all(it.details.name.startswith("session") for it in i2)
    # item type
    jobs_only = list(ws.list_top_level_items(item_type=["job"]))
    assert jobs_only and all(it.item_type == "Job" for it in jobs_only)
    sess_only = list(ws.list_top_level_items(item_type=["session"]))
    assert sess_only and all(it.item_type == "Session" for it in sess_only)
    # provider
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
    # verify ItemDetails projection of job_type across shapes
    items_with_jt = list(
        ws.list_top_level_items(job_type=["QuantumComputing", "QuantumChemistry"])
    )
    assert any(
        getattr(it.details, "job_type", None) == "QuantumComputing"
        for it in items_with_jt
    )
    assert any(
        getattr(it.details, "job_type", None) == "QuantumChemistry"
        for it in items_with_jt
    )


def test_list_top_level_items_created_ordering():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_jobs(ws)
    seed_sessions(ws)
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


def test_top_level_items_iterable_and_ordered():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    seed_jobs(ws)
    seed_sessions(ws)
    items = ws.list_top_level_items(orderby_property="CreationTime", is_asc=True)
    items_list = list(items)
    assert len(items_list) >= 1
    for a, b in zip(items_list, items_list[1:]):
        assert a.details.creation_time <= b.details.creation_time
