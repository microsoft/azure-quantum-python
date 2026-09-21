##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from unittest.mock import Mock, patch

from azure.storage.blob import ContainerSasPermissions

from azure.quantum.storage import get_container_uri


@patch("azure.quantum.storage.generate_container_sas", return_value="sas-token")
@patch("azure.quantum.storage.create_container")
def test_get_container_uri_sas_allows_listing(mock_create_container, mock_generate_sas):
    container = Mock()
    container.account_name = "account"
    container.container_name = "container"
    container.url = "https://account.blob.core.windows.net/container"
    container.credential.account_key = "account-key"
    mock_create_container.return_value = container

    result = get_container_uri("connection-string", "container")

    permission = mock_generate_sas.call_args.kwargs["permission"]
    assert isinstance(permission, ContainerSasPermissions)
    assert str(permission) == "racwl"
    assert result == "https://account.blob.core.windows.net/container?sas-token"