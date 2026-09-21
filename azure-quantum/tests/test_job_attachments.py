##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from unittest.mock import Mock, call, patch

import pytest

from azure.quantum import Job, JobDetails


JOB_ID = "job-id"
DEFAULT_CONTAINER_NAME = f"job-{JOB_ID}"
UNSIGNED_CONTAINER_URI = f"https://acct.blob.core.windows.net/{DEFAULT_CONTAINER_NAME}"
SIGNED_CONTAINER_URI = f"{UNSIGNED_CONTAINER_URI}?se=2099-01-01T00%3A00%3A00Z&sig=signature"
EXPIRED_CONTAINER_URI = f"{UNSIGNED_CONTAINER_URI}?se=2000-01-01T00%3A00%3A00Z&sig=signature"


def _job_with_container(container_uri=UNSIGNED_CONTAINER_URI, workspace=None) -> Job:
    job_details = JobDetails(
        id=JOB_ID,
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
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(workspace=workspace)

    blob_a = Mock()
    blob_b = Mock()
    container = mock_container_client.from_container_url.return_value
    container.list_blobs.return_value = [blob_a, blob_b]

    result = job.list_attachments()

    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )
    mock_container_client.from_container_url.assert_called_once_with(SIGNED_CONTAINER_URI)
    assert result == [blob_a, blob_b]


@patch("azure.quantum.job.base_job.ContainerClient")
def test_list_attachments_uses_workspace_container_when_unset(mock_container_client):
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(container_uri=None, workspace=workspace)

    container = mock_container_client.from_container_url.return_value
    container.list_blobs.return_value = []

    result = job.list_attachments()

    workspace.get_container_uri.assert_called_once_with(job_id=JOB_ID)
    mock_container_client.from_container_url.assert_called_once_with(SIGNED_CONTAINER_URI)
    assert result == []


def test_upload_attachment_uses_fresh_workspace_container_uri():
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(workspace=workspace)
    job.upload_input_data = Mock(return_value="uploaded-uri")

    result = job.upload_attachment("attachment", b"data")

    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )
    job.upload_input_data.assert_called_once_with(
        container_uri=SIGNED_CONTAINER_URI,
        blob_name="attachment",
        input_data=b"data",
    )
    assert result == "uploaded-uri"


@patch("azure.quantum.job.base_job.ContainerClient")
def test_download_attachment_uses_fresh_workspace_container_uri(mock_container_client):
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(workspace=workspace)
    blob_client = mock_container_client.from_container_url.return_value.get_blob_client.return_value
    blob_client.download_blob.return_value.readall.return_value = b"data"

    result = job.download_attachment("attachment")

    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )
    mock_container_client.from_container_url.assert_called_once_with(SIGNED_CONTAINER_URI)
    assert result == b"data"


@patch("azure.quantum.job.base_job.ContainerClient")
def test_attachment_methods_honor_explicit_container_uri(mock_container_client):
    workspace = Mock()
    job = _job_with_container(workspace=workspace)
    job.upload_input_data = Mock(return_value="uploaded-uri")
    blob_client = mock_container_client.from_container_url.return_value.get_blob_client.return_value
    blob_client.download_blob.return_value.readall.return_value = b"data"
    explicit_uri = "https://custom.blob.core.windows.net/container?sas"

    job.upload_attachment("upload", b"data", container_uri=explicit_uri)
    job.download_attachment("download", container_uri=explicit_uri)

    workspace.get_container_uri.assert_not_called()
    job.upload_input_data.assert_called_once_with(
        container_uri=explicit_uri,
        blob_name="upload",
        input_data=b"data",
    )
    mock_container_client.from_container_url.assert_called_once_with(explicit_uri)


@patch("azure.quantum.job.base_job.ContainerClient")
def test_attachment_methods_reuse_valid_signed_job_uri(mock_container_client):
    workspace = Mock()
    job = _job_with_container(container_uri=SIGNED_CONTAINER_URI, workspace=workspace)
    job.upload_input_data = Mock(return_value="uploaded-uri")
    container_client = mock_container_client.from_container_url.return_value
    container_client.list_blobs.return_value = []
    container_client.get_blob_client.return_value.download_blob.return_value.readall.return_value = b"data"

    job.upload_attachment("upload", b"data")
    attachments = job.list_attachments()
    downloaded = job.download_attachment("download")

    workspace.get_container_uri.assert_not_called()
    job.upload_input_data.assert_called_once_with(
        container_uri=SIGNED_CONTAINER_URI,
        blob_name="upload",
        input_data=b"data",
    )
    assert mock_container_client.from_container_url.call_args_list == [
        call(SIGNED_CONTAINER_URI),
        call(SIGNED_CONTAINER_URI),
    ]
    assert attachments == []
    assert downloaded == b"data"


def test_upload_attachment_refreshes_expired_job_uri():
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(container_uri=EXPIRED_CONTAINER_URI, workspace=workspace)
    job.upload_input_data = Mock(return_value="uploaded-uri")

    job.upload_attachment("attachment", b"data")

    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )
    job.upload_input_data.assert_called_once_with(
        container_uri=SIGNED_CONTAINER_URI,
        blob_name="attachment",
        input_data=b"data",
    )


def test_upload_attachment_rejects_refreshed_storage_hostname_mismatch():
    workspace = Mock()
    workspace.get_container_uri.return_value = (
        f"https://other-acct.blob.core.windows.net/{DEFAULT_CONTAINER_NAME}?sas"
    )
    job = _job_with_container(workspace=workspace)

    with pytest.raises(ValueError, match="does not match job container hostname"):
        job.upload_attachment("attachment", b"data")


@patch("azure.quantum.job.base_job.ContainerClient")
def test_attachment_methods_preserve_custom_container_name(mock_container_client):
    custom_container_name = "custom-container"
    custom_unsigned_uri = f"https://acct.blob.core.windows.net/{custom_container_name}"
    custom_signed_uri = f"{custom_unsigned_uri}?sas"
    workspace = Mock()
    workspace.get_container_uri.return_value = custom_signed_uri
    job = _job_with_container(container_uri=custom_unsigned_uri, workspace=workspace)
    job.upload_input_data = Mock(return_value="uploaded-uri")
    container_client = mock_container_client.from_container_url.return_value
    container_client.list_blobs.return_value = []
    container_client.get_blob_client.return_value.download_blob.return_value.readall.return_value = b"data"

    job.upload_attachment("upload", b"data")
    attachments = job.list_attachments()
    downloaded = job.download_attachment("download")

    workspace.get_container_uri.assert_has_calls(
        [
            call(job_id=JOB_ID, container_name=custom_container_name),
            call(job_id=JOB_ID, container_name=custom_container_name),
            call(job_id=JOB_ID, container_name=custom_container_name),
        ]
    )
    assert workspace.get_container_uri.call_count == 3
    job.upload_input_data.assert_called_once_with(
        container_uri=custom_signed_uri,
        blob_name="upload",
        input_data=b"data",
    )
    assert mock_container_client.from_container_url.call_args_list == [
        call(custom_signed_uri),
        call(custom_signed_uri),
    ]
    assert attachments == []
    assert downloaded == b"data"
