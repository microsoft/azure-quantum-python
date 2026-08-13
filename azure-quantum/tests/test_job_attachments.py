##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from unittest.mock import Mock, patch
from azure.quantum import Job, JobDetails


CONTAINER_URI = "https://acct.blob.core.windows.net/job-id?sas"


def _job_with_container(container_uri=CONTAINER_URI, workspace=None) -> Job:
    job_details = JobDetails(
        id="job-id",
        name="",
        provider_id="",
        target="",
        container_uri=container_uri,
        input_data_format="",
        output_data_format="",
    )
    return Job(workspace=workspace, job_details=job_details)


@patch("azure.quantum.job.base_job.ContainerClient")
def test_list_attachments_returns_container_blobs(mock_container_client):
    job = _job_with_container()

    blob_a = Mock()
    blob_b = Mock()
    container = mock_container_client.from_container_url.return_value
    container.list_blobs.return_value = [blob_a, blob_b]

    result = job.list_attachments()

    mock_container_client.from_container_url.assert_called_once_with(CONTAINER_URI)
    assert result == [blob_a, blob_b]


@patch("azure.quantum.job.base_job.ContainerClient")
def test_list_attachments_uses_workspace_container_when_unset(mock_container_client):
    workspace = Mock()
    workspace.get_container_uri.return_value = CONTAINER_URI
    job = _job_with_container(container_uri=None, workspace=workspace)

    container = mock_container_client.from_container_url.return_value
    container.list_blobs.return_value = []

    result = job.list_attachments()

    workspace.get_container_uri.assert_called_once_with(job_id="job-id")
    mock_container_client.from_container_url.assert_called_once_with(CONTAINER_URI)
    assert result == []
