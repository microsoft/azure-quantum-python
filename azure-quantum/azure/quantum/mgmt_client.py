##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
"""
Module providing the WorkspaceMgmtClient class for managing workspace operations.
"""

import logging
from typing import Optional
from azure.core.exceptions import ClientAuthenticationError
from azure.quantum._workspace_connection_params import WorkspaceConnectionParams
from azure.core import PipelineClient
from azure.core.pipeline.policies import (
    BearerTokenCredentialPolicy,
    RetryPolicy,
    HeadersPolicy,
    UserAgentPolicy,
    NetworkTraceLoggingPolicy,
)
from azure.core.rest import HttpRequest
from azure.core.exceptions import (
    ClientAuthenticationError,
    ResourceNotFoundError,
    HttpResponseError,
)

logger = logging.getLogger(__name__)

__all__ = ["WorkspaceMgmtClient"]


class WorkspaceMgmtClient:
    """
    Wrapper client for Azure Resource Graph operations related to Azure Quantum workspaces.
    
    :param credential:
        The credential to use to connect to Azure services.
    
    :param base_url:
        The base URL for the ARM endpoint.
    
    :param user_agent:
        Add the specified value as a prefix to the HTTP User-Agent header
        when communicating to the ARG/ARM.
    """
    
    def __init__(self, credential, base_url: str, user_agent: Optional[str] = None):
        """
        Initialize the WorkspaceMgmtClient.
        
        :param credential:
            The credential to use to connect to Azure services.
        
        :param base_url:
            The base URL for the ARM endpoint.
        """
        self._credential = credential
        self._base_url = base_url
        # Configure pipeline policies
        self._policies = [
            HeadersPolicy(),
            UserAgentPolicy(user_agent),
            BearerTokenCredentialPolicy(self._credential, "https://management.azure.com/.default"),
            RetryPolicy(retry_total=3),
            NetworkTraceLoggingPolicy(),
        ]
    
    def load_workspace_from_arg(self, connection_params: WorkspaceConnectionParams) -> None:
        """
        Queries Azure Resource Graph to find a workspace by name.
        Populates subscription_id, resource_group, location, and quantum_endpoint params if found.
        
        :param connection_params:
            The workspace connection parameters to populate.
        """
        if not connection_params.workspace_name:
            raise ValueError("Workspace name must be specified.")

        # Escape single quotes in parameters to prevent KQL injection
        workspace_name = self._escape_kql_string(connection_params.workspace_name)
        
        query = f"""
            Resources
            | where type =~ 'microsoft.quantum/workspaces'
            | where name =~ '{workspace_name}'
        """
        
        if connection_params.resource_group:
            resource_group = self._escape_kql_string(connection_params.resource_group)
            query += f"\n                | where resourceGroup =~ '{resource_group}'"
        
        if connection_params.location:
            location = self._escape_kql_string(connection_params.location)
            query += f"\n                | where location =~ '{location}'"

        query += """
            | extend endpointUri = tostring(properties.endpointUri)
            | project name, subscriptionId, resourceGroup, location, endpointUri
        """

        subscriptions = None
        if connection_params.subscription_id:
            subscriptions = [self._escape_kql_string(connection_params.subscription_id)]
        
        # Build the request payload
        request_body = {
            "query": query
        }
        if subscriptions:
            request_body["subscriptions"] = subscriptions
        
        # Create pipeline client
        client = PipelineClient(base_url=self._base_url, policies=self._policies)
        
        try:
            # Create request to Azure Resource Graph API
            request = HttpRequest(
                method="POST",
                url=f"{self._base_url}/providers/Microsoft.ResourceGraph/resources",
                params={"api-version": "2021-03-01"},
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json=request_body
            )
            
            # Send request through pipeline
            response = client.send_request(request)
            response.raise_for_status()
            result = response.json()
            
        except ClientAuthenticationError as e:
            raise ClientAuthenticationError(
                f"Authentication failed when querying workspace '{connection_params.workspace_name}'. "
                f"Please check your credentials and permissions."
            ) from e
        except HttpResponseError as e:
            error_message = f"Failed to query workspace using ARG (HTTP {e.status_code})"
            if e.error and hasattr(e.error, 'message'):
                error_message = f"{error_message}: {e.error.message}"
            raise RuntimeError(
                f"{error_message}.\n"
                "Please retry later or try to specify subscription id and resource group."
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to query workspace using ARG: {str(e)}.\n"
                "Please retry later or try to specify subscription id and resource group."
            ) from e
        finally:
            client.close()
        
        # Extract data from response
        data = result.get('data', [])
        
        if not data or len(data) == 0:
            raise ValueError(f"No matching workspace found with name '{connection_params.workspace_name}'.\n"
                             "Please specify correct workspace name.")
        
        if len(data) > 1:
            if not connection_params.location:
                raise ValueError(
                    f"Multiple Azure Quantum workspaces found with name '{connection_params.workspace_name}'.\n"
                    "Please specify location."
                )
            # not expected to reach here, so ask user to use all params
            raise RuntimeError(
                f"Multiple Azure Quantum workspaces found with name '{connection_params.workspace_name}' in location '{connection_params.location}'.\n"
                "Please specify subscription id and resource group."
            )
        
        workspace_data = data[0]
        
        connection_params.subscription_id = workspace_data.get('subscriptionId')
        connection_params.resource_group = workspace_data.get('resourceGroup')
        connection_params.location = workspace_data.get('location')
        connection_params.quantum_endpoint = workspace_data.get('endpointUri')

        logger.debug(
            "Found workspace '%s' in subscription '%s', resource group '%s', location '%s', endpoint '%s'",
            connection_params.workspace_name,
            connection_params.subscription_id,
            connection_params.resource_group,
            connection_params.location,
            connection_params.quantum_endpoint
        )

        # If one of the required parameters is missing, probably workspace in failed provisioning state
        if not connection_params.is_complete():
            raise ValueError(
                f"Failed to retrieve complete workspace details for workspace '{connection_params.workspace_name}'.\n"
                "Please check that workspace is in valid state."
            )
        
    def load_workspace_from_arm(self, connection_params: WorkspaceConnectionParams) -> None:
        """
        Fetches the workspace resource from ARM using Azure SDK pipeline and sets 
        location and endpoint URI params.
        
        :param connection_params:
            The workspace connection parameters to populate.
        
        :raises ValueError:
            If the workspace is not found or workspace details cannot be retrieved.
        
        :raises RuntimeError:
            If the API call fails or authentication fails.
        """
        if not all([connection_params.subscription_id, connection_params.resource_group, connection_params.workspace_name]):
            raise ValueError("Missing required connection parameters for ARM request.")
        
        api_version = connection_params.api_version or "2023-11-13-preview"
        
        # Build resource URL
        url = (
            f"{connection_params.arm_endpoint}/subscriptions/{connection_params.subscription_id}"
            f"/resourceGroups/{connection_params.resource_group}"
            f"/providers/Microsoft.Quantum/workspaces/{connection_params.workspace_name}"
        )
        
        # Create pipeline client
        client = PipelineClient(base_url=self._base_url, policies=self._policies)
        
        try:
            # Create request
            request = HttpRequest(
                method="GET",
                url=url,
                params={"api-version": api_version},
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
            )
            
            # Send request through pipeline
            response = client.send_request(request)
            response.raise_for_status()
            workspace_data = response.json()
            
        except ResourceNotFoundError as e:
            raise ValueError(
                f"Azure Quantum workspace '{connection_params.workspace_name}' "
                f"not found in resource group '{connection_params.resource_group}' "
                f"and subscription '{connection_params.subscription_id}'."
            ) from e
        except ClientAuthenticationError as e:
            raise ClientAuthenticationError(
                f"Authentication failed when accessing workspace '{connection_params.workspace_name}'. "
                f"Please check your credentials and permissions."
            ) from e
        except HttpResponseError as e:
            error_message = f"Failed to fetch workspace from ARM (HTTP {e.status_code})"
            if e.error and hasattr(e.error, 'message'):
                error_message = f"{error_message}: {e.error.message}"
            raise RuntimeError(f"{error_message}.\nPlease retry later.") from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch workspace from ARM: {str(e)}.\nPlease retry later."
            ) from e
        finally:
            client.close()

        # Extract and apply location
        location = workspace_data.get("location")
        if location:
            connection_params.location = location
            logger.debug(
                "Updated workspace location from ARM: %s",
                location
            )
        else:
            raise ValueError(
                f"Failed to retrieve location for workspace '{connection_params.workspace_name}'.\n"
                f"Please check that workspace is in valid state."
            )

        # Extract and apply endpoint URI from properties
        properties = workspace_data.get("properties", {})
        endpoint_uri = properties.get("endpointUri")
        if endpoint_uri:
            connection_params.quantum_endpoint = endpoint_uri
            logger.debug(
                "Updated workspace endpoint from ARM: %s", connection_params.quantum_endpoint
            )
        else:
            raise ValueError(
                f"Failed to retrieve endpoint uri for workspace '{connection_params.workspace_name}'.\n"
                f"Please check that workspace is in valid state."
            )
    
    @staticmethod
    def _escape_kql_string(value: str) -> str:
        """Escape a string value for use in KQL queries."""
        if not value:
            return value
        # Escape backslashes first, then single quotes
        return value.replace('\\', '\\\\').replace("'", "\\'")
