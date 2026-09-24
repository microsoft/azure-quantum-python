##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, call, patch

import pytest

from azure.quantum import Job, JobDetails


JOB_ID = "job-id"
DEFAULT_CONTAINER_NAME = f"job-{JOB_ID}"
UNSIGNED_CONTAINER_URI = f"https://acct.blob.core.windows.net/{DEFAULT_CONTAINER_NAME}"
SIGNED_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?sp=racwdl&se=2099-01-01T00%3A00%3A00Z&sig=signature"
)
EXPIRED_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?sp=racwdl&se=2000-01-01T00%3A00%3A00Z&sig=signature"
)
FUTURE_START_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?sp=racwdl&st=2098-01-01T00%3A00%3A00Z"
    "&se=2099-01-01T00%3A00%3A00Z&sig=signature"
)
MALFORMED_EXPIRY_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?sp=racwdl&se=not-a-date&sig=signature"
)
MINIMUM_EXPIRY_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?sp=racwdl&se=0001-01-01T00%3A00%3A00Z&sig=signature"
)
NO_PERMISSIONS_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?se=2099-01-01T00%3A00%3A00Z&sig=signature"
)
NO_SIGNATURE_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?se=2099-01-01T00%3A00%3A00Z"
)
WRITE_ONLY_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?sp=w&se=2099-01-01T00%3A00%3A00Z&sig=signature"
)
READ_LIST_CONTAINER_URI = (
    f"{UNSIGNED_CONTAINER_URI}?sp=rl&se=2099-01-01T00%3A00%3A00Z&sig=signature"
)
HTTP_SIGNED_CONTAINER_URI = SIGNED_CONTAINER_URI.replace("https://", "http://")


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
def test_attachment_methods_refresh_signed_job_uri_once(mock_container_client):
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(container_uri=SIGNED_CONTAINER_URI, workspace=workspace)
    job.upload_input_data = Mock(return_value="uploaded-uri")
    container_client = mock_container_client.from_container_url.return_value
    container_client.list_blobs.return_value = []
    container_client.get_blob_client.return_value.download_blob.return_value.readall.return_value = b"data"

    job.upload_attachment("upload", b"data")
    attachments = job.list_attachments()
    downloaded = job.download_attachment("download")

    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )
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


def test_cached_uri_is_reused_regardless_of_sas_start_time():
    workspace = Mock()
    job = _job_with_container(workspace=workspace)
    job._attachment_container_uri_cache = FUTURE_START_CONTAINER_URI
    job._attachment_container_uri_cache_container_name = DEFAULT_CONTAINER_NAME
    job.upload_input_data = Mock(return_value="uploaded-uri")

    job.upload_attachment("attachment", b"data")

    workspace.get_container_uri.assert_not_called()
    job.upload_input_data.assert_called_once_with(
        container_uri=FUTURE_START_CONTAINER_URI,
        blob_name="attachment",
        input_data=b"data",
    )


def test_upload_attachment_logs_and_refreshes_malformed_sas_expiry(caplog):
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(workspace=workspace)
    job._attachment_container_uri_cache = MALFORMED_EXPIRY_CONTAINER_URI
    job._attachment_container_uri_cache_container_name = DEFAULT_CONTAINER_NAME
    job.upload_input_data = Mock(return_value="uploaded-uri")

    with caplog.at_level("DEBUG", logger="azure.quantum.job.base_job"):
        job.upload_attachment("attachment", b"data")

    assert "Unable to parse attachment SAS expiry time" in caplog.text
    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )


def test_cached_uri_inside_expiry_buffer_is_refreshed():
    near_expiry_container_uri = (
        f"{UNSIGNED_CONTAINER_URI}?se="
        f"{(datetime.now(timezone.utc) + timedelta(minutes=4)).isoformat().replace('+00:00', 'Z')}"
    )
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(workspace=workspace)
    job._attachment_container_uri_cache = near_expiry_container_uri
    job._attachment_container_uri_cache_container_name = DEFAULT_CONTAINER_NAME
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


@pytest.mark.parametrize(
    "cached_container_uri",
    [UNSIGNED_CONTAINER_URI, EXPIRED_CONTAINER_URI, MINIMUM_EXPIRY_CONTAINER_URI],
)
def test_cached_uri_without_reusable_expiry_is_refreshed(cached_container_uri):
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(workspace=workspace)
    job._attachment_container_uri_cache = cached_container_uri
    job._attachment_container_uri_cache_container_name = DEFAULT_CONTAINER_NAME
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


@pytest.mark.parametrize(
    "cached_container_uri",
    [
        FUTURE_START_CONTAINER_URI,
        HTTP_SIGNED_CONTAINER_URI,
        NO_PERMISSIONS_CONTAINER_URI,
        NO_SIGNATURE_CONTAINER_URI,
        WRITE_ONLY_CONTAINER_URI,
        READ_LIST_CONTAINER_URI,
    ],
)
def test_unexpired_cached_uri_is_reused_without_prevalidation(cached_container_uri):
    workspace = Mock()
    job = _job_with_container(workspace=workspace)
    job._attachment_container_uri_cache = cached_container_uri
    job._attachment_container_uri_cache_container_name = DEFAULT_CONTAINER_NAME
    job.upload_input_data = Mock(return_value="uploaded-uri")

    job.upload_attachment("attachment", b"data")

    workspace.get_container_uri.assert_not_called()
    job.upload_input_data.assert_called_once_with(
        container_uri=cached_container_uri,
        blob_name="attachment",
        input_data=b"data",
    )


@pytest.mark.parametrize(
    "refreshed_container_uri",
    [
        UNSIGNED_CONTAINER_URI,
        HTTP_SIGNED_CONTAINER_URI,
        NO_PERMISSIONS_CONTAINER_URI,
        WRITE_ONLY_CONTAINER_URI,
        READ_LIST_CONTAINER_URI,
        f"https://other-acct.blob.core.windows.net/{DEFAULT_CONTAINER_NAME}?sas",
    ],
)
def test_workspace_issued_uri_is_used_without_prevalidation(refreshed_container_uri):
    workspace = Mock()
    workspace.get_container_uri.return_value = refreshed_container_uri
    job = _job_with_container(workspace=workspace)
    original_container_uri = job.details.container_uri
    job.upload_input_data = Mock(return_value="uploaded-uri")

    job.upload_attachment("attachment", b"data")

    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )
    job.upload_input_data.assert_called_once_with(
        container_uri=refreshed_container_uri,
        blob_name="attachment",
        input_data=b"data",
    )
    assert job._attachment_container_uri_cache == refreshed_container_uri
    assert job._attachment_container_uri_cache_container_name == DEFAULT_CONTAINER_NAME
    assert job.details.container_uri == original_container_uri


def test_upload_attachment_rejects_job_uri_without_container_name():
    pathless_uri = (
        "https://acct.blob.core.windows.net"
        "?sp=racwdl&se=2099-01-01T00%3A00%3A00Z&sig=signature"
    )
    workspace = Mock()
    job = _job_with_container(container_uri=pathless_uri, workspace=workspace)

    with pytest.raises(ValueError, match="does not include a container name"):
        job.upload_attachment("attachment", b"data")

    workspace.get_container_uri.assert_not_called()


@patch("azure.quantum.job.base_job.ContainerClient")
def test_attachment_methods_preserve_custom_container_name(mock_container_client):
    custom_container_name = "custom-container"
    custom_unsigned_uri = f"https://acct.blob.core.windows.net/{custom_container_name}"
    custom_signed_uri = (
        f"{custom_unsigned_uri}?sp=racwdl&se=2099-01-01T00%3A00%3A00Z&sig=signature"
    )
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

    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=custom_container_name,
    )
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


@patch("azure.quantum.job.base_job.ContainerClient")
def test_replacing_job_details_invalidates_cached_container_uri(mock_container_client):
    workspace = Mock()
    workspace.get_container_uri.side_effect = [SIGNED_CONTAINER_URI, SIGNED_CONTAINER_URI]
    job = _job_with_container(workspace=workspace)
    mock_container_client.from_container_url.return_value.list_blobs.return_value = []

    job.list_attachments()
    job.details = JobDetails(
        id=JOB_ID,
        name="",
        provider_id="",
        target="",
        container_uri=UNSIGNED_CONTAINER_URI,
        input_data_format="",
        output_data_format="",
    )
    job.list_attachments()

    assert workspace.get_container_uri.call_count == 2


@patch("azure.quantum.job.base_job.ContainerClient")
def test_cache_reuse_after_hostname_mutation_never_queries_by_hostname(mock_container_client):
    other_account_same_name_uri = f"https://other-acct.blob.core.windows.net/{DEFAULT_CONTAINER_NAME}"
    workspace = Mock()
    workspace.get_container_uri.return_value = SIGNED_CONTAINER_URI
    job = _job_with_container(workspace=workspace)
    mock_container_client.from_container_url.return_value.list_blobs.return_value = []

    job.list_attachments()
    job.details.container_uri = other_account_same_name_uri
    job.list_attachments()

    # container_name-only cache key reuses the cache despite the hostname mutation.
    workspace.get_container_uri.assert_called_once_with(
        job_id=JOB_ID,
        container_name=DEFAULT_CONTAINER_NAME,
    )
    # get_container_uri never received a hostname, so both calls used the same real account SAS.
    assert mock_container_client.from_container_url.call_args_list == [
        call(SIGNED_CONTAINER_URI),
        call(SIGNED_CONTAINER_URI),
    ]


@patch("azure.quantum.job.base_job.ContainerClient")
def test_mutating_job_container_uri_invalidates_cached_container_uri(mock_container_client):
    other_container_uri = "https://acct.blob.core.windows.net/other-container"
    other_signed_uri = (
        f"{other_container_uri}?sp=racwdl&se=2099-01-01T00%3A00%3A00Z&sig=signature"
    )
    workspace = Mock()
    workspace.get_container_uri.side_effect = [SIGNED_CONTAINER_URI, other_signed_uri]
    job = _job_with_container(workspace=workspace)
    mock_container_client.from_container_url.return_value.list_blobs.return_value = []

    job.list_attachments()
    job.details.container_uri = other_container_uri
    job.list_attachments()

    assert workspace.get_container_uri.call_args_list == [
        call(job_id=JOB_ID, container_name=DEFAULT_CONTAINER_NAME),
        call(job_id=JOB_ID, container_name="other-container"),
    ]
    assert mock_container_client.from_container_url.call_args_list == [
        call(SIGNED_CONTAINER_URI),
        call(other_signed_uri),
    ]
