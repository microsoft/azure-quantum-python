##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import pytest
from unittest.mock import MagicMock, patch
from http import HTTPStatus
from azure.core.exceptions import HttpResponseError
from azure.quantum._mgmt_client import WorkspaceMgmtClient
from azure.quantum._workspace_connection_params import WorkspaceConnectionParams
from azure.quantum._constants import ConnectionConstants
from common import (
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
    LOCATION,
    ENDPOINT_URI,
)


def test_init_creates_client():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    
    client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    assert client._credential == mock_credential
    assert client._base_url == base_url
    assert client._client is not None
    assert len(client._policies) == 5


def test_init_without_user_agent():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    
    client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url
    )
    
    assert client._credential == mock_credential
    assert client._base_url == base_url
    assert client._client is not None


def test_context_manager_enter():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    with patch.object(mgmt_client._client, '__enter__', return_value=mgmt_client._client):
        result = mgmt_client.__enter__()
        assert result == mgmt_client


def test_context_manager_exit():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    with patch.object(mgmt_client._client, '__exit__') as mock_exit:
        mgmt_client.__exit__(None, None, None)
        mock_exit.assert_called_once()


def test_close():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    with patch.object(mgmt_client._client, 'close') as mock_close:
        mgmt_client.close()
        mock_close.assert_called_once()


def test_load_workspace_from_arg_success():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': [{
            'name': WORKSPACE,
            'subscriptionId': SUBSCRIPTION_ID,
            'resourceGroup': RESOURCE_GROUP,
            'location': LOCATION,
            'endpointUri': ENDPOINT_URI
        }]
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
        connection_params.subscription_id = None
        connection_params.location = None
        connection_params.quantum_endpoint = None
        
        mgmt_client.load_workspace_from_arg(connection_params)
        
        assert connection_params.subscription_id == SUBSCRIPTION_ID
        assert connection_params.resource_group == RESOURCE_GROUP
        assert connection_params.workspace_name == WORKSPACE
        assert connection_params.location == LOCATION
        assert connection_params.quantum_endpoint == ENDPOINT_URI


def test_load_workspace_from_arg_with_resource_group_filter():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        workspace_name=WORKSPACE,
        resource_group=RESOURCE_GROUP
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': [{
            'name': WORKSPACE,
            'subscriptionId': SUBSCRIPTION_ID,
            'resourceGroup': RESOURCE_GROUP,
            'location': LOCATION,
            'endpointUri': ENDPOINT_URI
        }]
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
        mgmt_client.load_workspace_from_arg(connection_params)
        
        call_args = mock_send.call_args
        request = call_args[0][0]
        assert RESOURCE_GROUP in str(request.content)


def test_load_workspace_from_arg_with_location_filter():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        workspace_name=WORKSPACE,
        location=LOCATION
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': [{
            'name': WORKSPACE,
            'subscriptionId': SUBSCRIPTION_ID,
            'resourceGroup': RESOURCE_GROUP,
            'location': LOCATION,
            'endpointUri': ENDPOINT_URI
        }]
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
        mgmt_client.load_workspace_from_arg(connection_params)
        
        call_args = mock_send.call_args
        request = call_args[0][0]
        assert LOCATION in str(request.content)


def test_load_workspace_from_arg_with_subscription_filter():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        workspace_name=WORKSPACE,
        subscription_id=SUBSCRIPTION_ID
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': [{
            'name': WORKSPACE,
            'subscriptionId': SUBSCRIPTION_ID,
            'resourceGroup': RESOURCE_GROUP,
            'location': LOCATION,
            'endpointUri': ENDPOINT_URI
        }]
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
        mgmt_client.load_workspace_from_arg(connection_params)
        
        call_args = mock_send.call_args
        request = call_args[0][0]
        request_body = request.content
        assert 'subscriptions' in request_body


def test_load_workspace_from_arg_no_workspace_name():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams()
    
    with pytest.raises(ValueError, match="Workspace name must be specified"):
        mgmt_client.load_workspace_from_arg(connection_params)


def test_load_workspace_from_arg_no_matching_workspace():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {'data': []}
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
        with pytest.raises(ValueError, match="No matching workspace found"):
            mgmt_client.load_workspace_from_arg(connection_params)


def test_load_workspace_from_arg_multiple_workspaces():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': [
            {
                'name': WORKSPACE,
                'subscriptionId': SUBSCRIPTION_ID,
                'resourceGroup': RESOURCE_GROUP,
                'location': LOCATION,
                'endpointUri': ENDPOINT_URI
            },
            {
                'name': WORKSPACE,
                'subscriptionId': 'another-sub-id',
                'resourceGroup': 'another-rg',
                'location': 'westus',
                'endpointUri': 'https://another.endpoint.com/'
            }
        ]
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
        with pytest.raises(ValueError, match="Multiple Azure Quantum workspaces found"):
            mgmt_client.load_workspace_from_arg(connection_params)


def test_load_workspace_from_arg_incomplete_workspace_data():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': [{
            'name': WORKSPACE,
            'subscriptionId': SUBSCRIPTION_ID,
            'resourceGroup': RESOURCE_GROUP,
            'location': LOCATION,
        }]
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
        with pytest.raises(ValueError, match="Failed to retrieve complete workspace details"):
            mgmt_client.load_workspace_from_arg(connection_params)


def test_load_workspace_from_arg_request_exception():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    with patch.object(mgmt_client._client, 'send_request', side_effect=Exception("Network error")):
        with pytest.raises(RuntimeError, match="Could not load workspace details from Azure Resource Graph"):
            mgmt_client.load_workspace_from_arg(connection_params)


def test_load_workspace_from_arm_success():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'location': LOCATION,
        'properties': {
            'endpointUri': ENDPOINT_URI
        }
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
        connection_params.location = None
        connection_params.quantum_endpoint = None
        
        mgmt_client.load_workspace_from_arm(connection_params)
        
        assert connection_params.location == LOCATION
        assert connection_params.quantum_endpoint == ENDPOINT_URI


def test_load_workspace_from_arm_missing_required_params():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        workspace_name=WORKSPACE
    )
    
    with pytest.raises(ValueError, match="Missing required connection parameters"):
        mgmt_client.load_workspace_from_arm(connection_params)


def test_load_workspace_from_arm_workspace_not_found():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_error = HttpResponseError()
    mock_error.status_code = HTTPStatus.NOT_FOUND
    
    with patch.object(mgmt_client._client, 'send_request', side_effect=mock_error):
        with pytest.raises(ValueError, match="not found in resource group"):
            mgmt_client.load_workspace_from_arm(connection_params)


def test_load_workspace_from_arm_http_error():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_error = HttpResponseError()
    mock_error.status_code = HTTPStatus.FORBIDDEN
    
    with patch.object(mgmt_client._client, 'send_request', side_effect=mock_error):
        with pytest.raises(HttpResponseError):
            mgmt_client.load_workspace_from_arm(connection_params)


def test_load_workspace_from_arm_missing_location():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'properties': {
            'endpointUri': ENDPOINT_URI
        }
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
        with pytest.raises(ValueError, match="Failed to retrieve location"):
            mgmt_client.load_workspace_from_arm(connection_params)


def test_load_workspace_from_arm_missing_endpoint():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'location': LOCATION,
        'properties': {}
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
        with pytest.raises(ValueError, match="Failed to retrieve endpoint uri"):
            mgmt_client.load_workspace_from_arm(connection_params)


def test_load_workspace_from_arm_request_exception():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    with patch.object(mgmt_client._client, 'send_request', side_effect=Exception("Network error")):
        with pytest.raises(RuntimeError, match="Could not load workspace details from ARM"):
            mgmt_client.load_workspace_from_arm(connection_params)


def test_load_workspace_from_arm_uses_custom_api_version():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
        api_version="2024-01-01"
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'location': LOCATION,
        'properties': {
            'endpointUri': ENDPOINT_URI
        }
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
        mgmt_client.load_workspace_from_arm(connection_params)
        
        call_args = mock_send.call_args
        request = call_args[0][0]
        assert "2024-01-01" in request.url


def test_load_workspace_from_arm_uses_default_api_version():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'location': LOCATION,
        'properties': {
            'endpointUri': ENDPOINT_URI
        }
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
        mgmt_client.load_workspace_from_arm(connection_params)
        
        call_args = mock_send.call_args
        request = call_args[0][0]
        assert ConnectionConstants.DEFAULT_ARM_WORKSPACE_API_VERSION in request.url


def test_load_workspace_from_arg_constructs_correct_url():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'data': [{
            'name': WORKSPACE,
            'subscriptionId': SUBSCRIPTION_ID,
            'resourceGroup': RESOURCE_GROUP,
            'location': LOCATION,
            'endpointUri': ENDPOINT_URI
        }]
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
        mgmt_client.load_workspace_from_arg(connection_params)
        
        call_args = mock_send.call_args
        request = call_args[0][0]
        assert "/providers/Microsoft.ResourceGraph/resources" in request.url
        assert ConnectionConstants.DEFAULT_ARG_API_VERSION in request.url


def test_load_workspace_from_arm_constructs_correct_url():
    mock_credential = MagicMock()
    base_url = ConnectionConstants.ARM_PRODUCTION_ENDPOINT
    mgmt_client = WorkspaceMgmtClient(
        credential=mock_credential,
        base_url=base_url,
        user_agent="test-agent"
    )
    
    connection_params = WorkspaceConnectionParams(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        workspace_name=WORKSPACE,
    )
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'location': LOCATION,
        'properties': {
            'endpointUri': ENDPOINT_URI
        }
    }
    
    with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
        mgmt_client.load_workspace_from_arm(connection_params)
        
        call_args = mock_send.call_args
        request = call_args[0][0]
        assert f"/subscriptions/{SUBSCRIPTION_ID}" in request.url
        assert f"/resourceGroups/{RESOURCE_GROUP}" in request.url
        assert f"/providers/Microsoft.Quantum/workspaces/{WORKSPACE}" in request.url
