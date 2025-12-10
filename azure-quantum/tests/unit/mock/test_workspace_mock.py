from datetime import datetime, UTC
from typing import Any

from azure.quantum.workspace import Workspace
from azure.quantum._client import ServicesClient
from azure.quantum._client.models import JobDetails

from mock_client import MockServicesClient


class WorkspaceMock(Workspace):
    def _create_client(self) -> ServicesClient:
        # Return mock ServicesClient so real Workspace methods operate on in-memory data
        return MockServicesClient()


def test_list_jobs_with_mock_client():
    ws = WorkspaceMock(
        subscription_id="sub", resource_group="rg", name="ws", location="westus"
    )
    # Seed a job via client create_or_replace
    details = JobDetails(
        id="job-1",
        name="J1",
        provider_id="ionq",
        target="ionq.simulator",
        creation_time=datetime.now(UTC),
        status="Succeeded",
    )
    ws._client.jobs.create_or_replace(
        ws.subscription_id,
        ws.resource_group,
        ws.name,
        job_id=details.id,
        job_details=details,
    )
    # Validate list_jobs returns Job instances
    jobs = ws.list_jobs(orderby_property="CreationTime", is_asc=True)
    assert all(j.details is not None for j in jobs)
    assert [j.details.name for j in jobs] == ["J1"]
