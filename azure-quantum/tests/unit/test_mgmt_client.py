##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
"""
Unit tests for the WorkspaceMgmtClient class.
"""

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


class TestWorkspaceMgmtClient:
    """Test suite for WorkspaceMgmtClient class."""

    @pytest.fixture
    def mock_credential(self):
        """Create a mock credential."""
        return MagicMock()

    @pytest.fixture
    def base_url(self):
        """Return the ARM base URL."""
        return ConnectionConstants.ARM_PRODUCTION_ENDPOINT

    @pytest.fixture
    def mgmt_client(self, mock_credential, base_url):
        """Create a WorkspaceMgmtClient instance."""
        return WorkspaceMgmtClient(
            credential=mock_credential,
            base_url=base_url,
            user_agent="test-agent"
        )

    @pytest.fixture
    def connection_params(self):
        """Create a WorkspaceConnectionParams instance."""
        return WorkspaceConnectionParams(
            subscription_id=SUBSCRIPTION_ID,
            resource_group=RESOURCE_GROUP,
            workspace_name=WORKSPACE,
        )

    def test_init_creates_client(self, mock_credential, base_url):
        """Test that initialization creates a properly configured client."""
        client = WorkspaceMgmtClient(
            credential=mock_credential,
            base_url=base_url,
            user_agent="test-agent"
        )
        
        assert client._credential == mock_credential
        assert client._base_url == base_url
        assert client._client is not None
        assert len(client._policies) == 5

    def test_init_without_user_agent(self, mock_credential, base_url):
        """Test initialization without user agent."""
        client = WorkspaceMgmtClient(
            credential=mock_credential,
            base_url=base_url
        )
        
        assert client._credential == mock_credential
        assert client._base_url == base_url
        assert client._client is not None

    def test_context_manager_enter(self, mgmt_client):
        """Test __enter__ returns self."""
        with patch.object(mgmt_client._client, '__enter__', return_value=mgmt_client._client):
            result = mgmt_client.__enter__()
            assert result == mgmt_client

    def test_context_manager_exit(self, mgmt_client):
        """Test __exit__ calls client exit."""
        with patch.object(mgmt_client._client, '__exit__') as mock_exit:
            mgmt_client.__exit__(None, None, None)
            mock_exit.assert_called_once()

    def test_close(self, mgmt_client):
        """Test close method calls client close."""
        with patch.object(mgmt_client._client, 'close') as mock_close:
            mgmt_client.close()
            mock_close.assert_called_once()

    def test_load_workspace_from_arg_success(self, mgmt_client, connection_params):
        """Test successful workspace loading from ARG."""
        # Setup mock response
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
            # Clear some params to test ARG fills them
            connection_params.subscription_id = None
            connection_params.location = None
            connection_params.quantum_endpoint = None
            
            mgmt_client.load_workspace_from_arg(connection_params)
            
            assert connection_params.subscription_id == SUBSCRIPTION_ID
            assert connection_params.resource_group == RESOURCE_GROUP
            assert connection_params.workspace_name == WORKSPACE
            assert connection_params.location == LOCATION
            assert connection_params.quantum_endpoint == ENDPOINT_URI

    def test_load_workspace_from_arg_with_resource_group_filter(self, mgmt_client):
        """Test ARG query includes resource group filter when provided."""
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
            
            # Verify the request was made and contains resource group filter
            call_args = mock_send.call_args
            request = call_args[0][0]
            assert RESOURCE_GROUP in str(request.content)

    def test_load_workspace_from_arg_with_location_filter(self, mgmt_client):
        """Test ARG query includes location filter when provided."""
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
            
            # Verify the request was made and contains location filter
            call_args = mock_send.call_args
            request = call_args[0][0]
            assert LOCATION in str(request.content)

    def test_load_workspace_from_arg_with_subscription_filter(self, mgmt_client):
        """Test ARG query includes subscription filter when provided."""
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
            
            # Verify the request includes subscriptions filter
            call_args = mock_send.call_args
            request = call_args[0][0]
            request_body = request.content
            assert 'subscriptions' in request_body

    def test_load_workspace_from_arg_no_workspace_name(self, mgmt_client):
        """Test that missing workspace name raises ValueError."""
        connection_params = WorkspaceConnectionParams()
        
        with pytest.raises(ValueError, match="Workspace name must be specified"):
            mgmt_client.load_workspace_from_arg(connection_params)

    def test_load_workspace_from_arg_no_matching_workspace(self, mgmt_client, connection_params):
        """Test error when no matching workspace found."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': []}
        
        with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
            with pytest.raises(ValueError, match="No matching workspace found"):
                mgmt_client.load_workspace_from_arg(connection_params)

    def test_load_workspace_from_arg_multiple_workspaces(self, mgmt_client, connection_params):
        """Test error when multiple workspaces found."""
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

    def test_load_workspace_from_arg_incomplete_workspace_data(self, mgmt_client, connection_params):
        """Test error when workspace data is incomplete."""
        # Missing endpointUri
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

    def test_load_workspace_from_arg_request_exception(self, mgmt_client, connection_params):
        """Test handling of request exceptions."""
        with patch.object(mgmt_client._client, 'send_request', side_effect=Exception("Network error")):
            with pytest.raises(RuntimeError, match="Could not load workspace details from Azure Resource Graph"):
                mgmt_client.load_workspace_from_arg(connection_params)

    def test_load_workspace_from_arm_success(self, mgmt_client, connection_params):
        """Test successful workspace loading from ARM."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'location': LOCATION,
            'properties': {
                'endpointUri': ENDPOINT_URI
            }
        }
        
        with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
            # Clear location and endpoint to test ARM fills them
            connection_params.location = None
            connection_params.quantum_endpoint = None
            
            mgmt_client.load_workspace_from_arm(connection_params)
            
            assert connection_params.location == LOCATION
            assert connection_params.quantum_endpoint == ENDPOINT_URI

    def test_load_workspace_from_arm_missing_required_params(self, mgmt_client):
        """Test error when required connection parameters are missing."""
        connection_params = WorkspaceConnectionParams(
            workspace_name=WORKSPACE
        )
        
        with pytest.raises(ValueError, match="Missing required connection parameters"):
            mgmt_client.load_workspace_from_arm(connection_params)

    def test_load_workspace_from_arm_workspace_not_found(self, mgmt_client, connection_params):
        """Test error when workspace not found in ARM."""
        mock_error = HttpResponseError()
        mock_error.status_code = HTTPStatus.NOT_FOUND
        
        with patch.object(mgmt_client._client, 'send_request', side_effect=mock_error):
            with pytest.raises(ValueError, match="not found in resource group"):
                mgmt_client.load_workspace_from_arm(connection_params)

    def test_load_workspace_from_arm_http_error(self, mgmt_client, connection_params):
        """Test handling of other HTTP errors."""
        mock_error = HttpResponseError()
        mock_error.status_code = HTTPStatus.FORBIDDEN
        
        with patch.object(mgmt_client._client, 'send_request', side_effect=mock_error):
            with pytest.raises(HttpResponseError):
                mgmt_client.load_workspace_from_arm(connection_params)

    def test_load_workspace_from_arm_missing_location(self, mgmt_client, connection_params):
        """Test error when location is missing in ARM response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'properties': {
                'endpointUri': ENDPOINT_URI
            }
        }
        
        with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
            with pytest.raises(ValueError, match="Failed to retrieve location"):
                mgmt_client.load_workspace_from_arm(connection_params)

    def test_load_workspace_from_arm_missing_endpoint(self, mgmt_client, connection_params):
        """Test error when endpoint URI is missing in ARM response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'location': LOCATION,
            'properties': {}
        }
        
        with patch.object(mgmt_client._client, 'send_request', return_value=mock_response):
            with pytest.raises(ValueError, match="Failed to retrieve endpoint uri"):
                mgmt_client.load_workspace_from_arm(connection_params)

    def test_load_workspace_from_arm_request_exception(self, mgmt_client, connection_params):
        """Test handling of request exceptions from ARM."""
        with patch.object(mgmt_client._client, 'send_request', side_effect=Exception("Network error")):
            with pytest.raises(RuntimeError, match="Could not load workspace details from ARM"):
                mgmt_client.load_workspace_from_arm(connection_params)

    def test_load_workspace_from_arm_uses_custom_api_version(self, mgmt_client):
        """Test that custom API version is used when provided."""
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
            
            # Verify the custom API version was used
            call_args = mock_send.call_args
            request = call_args[0][0]
            assert "2024-01-01" in request.url

    def test_load_workspace_from_arm_uses_default_api_version(self, mgmt_client, connection_params):
        """Test that default API version is used when not provided."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'location': LOCATION,
            'properties': {
                'endpointUri': ENDPOINT_URI
            }
        }
        
        with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
            mgmt_client.load_workspace_from_arm(connection_params)
            
            # Verify the default API version was used
            call_args = mock_send.call_args
            request = call_args[0][0]
            assert ConnectionConstants.DEFAULT_WORKSPACE_API_VERSION in request.url

    def test_load_workspace_from_arg_constructs_correct_url(self, mgmt_client, connection_params):
        """Test that ARG request uses correct URL."""
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
            
            # Verify the request URL
            call_args = mock_send.call_args
            request = call_args[0][0]
            assert "/providers/Microsoft.ResourceGraph/resources" in request.url
            assert ConnectionConstants.DEFAULT_ARG_API_VERSION in request.url

    def test_load_workspace_from_arm_constructs_correct_url(self, mgmt_client, connection_params):
        """Test that ARM request uses correct URL."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'location': LOCATION,
            'properties': {
                'endpointUri': ENDPOINT_URI
            }
        }
        
        with patch.object(mgmt_client._client, 'send_request', return_value=mock_response) as mock_send:
            mgmt_client.load_workspace_from_arm(connection_params)
            
            # Verify the request URL contains expected components
            call_args = mock_send.call_args
            request = call_args[0][0]
            assert f"/subscriptions/{SUBSCRIPTION_ID}" in request.url
            assert f"/resourceGroups/{RESOURCE_GROUP}" in request.url
            assert f"/providers/Microsoft.Quantum/workspaces/{WORKSPACE}" in request.url
