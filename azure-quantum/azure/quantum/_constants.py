##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from enum import Enum
from azure.identity._constants import EnvironmentVariables as SdkEnvironmentVariables


class EnvironmentVariables:
    USER_AGENT_APPID = "AZURE_QUANTUM_PYTHON_APPID"
    CONNECTION_STRING = "AZURE_QUANTUM_CONNECTION_STRING"
    QUANTUM_API_KEY = "AZURE_QUANTUM_API_KEY"
    QUANTUM_LOCATION = "AZURE_QUANTUM_WORKSPACE_LOCATION"
    LOCATION = "LOCATION"
    QUANTUM_RESOURCE_GROUP = "AZURE_QUANTUM_WORKSPACE_RG"
    RESOURCE_GROUP = "RESOURCE_GROUP"
    QUANTUM_SUBSCRIPTION_ID = "AZURE_QUANTUM_SUBSCRIPTION_ID"
    SUBSCRIPTION_ID = "SUBSCRIPTION_ID"
    WORKSPACE_NAME = "AZURE_QUANTUM_WORKSPACE_NAME"
    QUANTUM_BASE_URL = "AZURE_QUANTUM_BASEURL"
    QUANTUM_ENV = "AZURE_QUANTUM_ENV"
    AZURE_CLIENT_ID = SdkEnvironmentVariables.AZURE_CLIENT_ID
    AZURE_CLIENT_SECRET = SdkEnvironmentVariables.AZURE_CLIENT_SECRET
    AZURE_TENANT_ID = SdkEnvironmentVariables.AZURE_TENANT_ID
    QUANTUM_TOKEN_FILE = "AZURE_QUANTUM_TOKEN_FILE"
    ALL = [
        QUANTUM_API_KEY,
        USER_AGENT_APPID,
        CONNECTION_STRING,
        QUANTUM_LOCATION,
        LOCATION,
        QUANTUM_RESOURCE_GROUP,
        RESOURCE_GROUP,
        QUANTUM_SUBSCRIPTION_ID,
        SUBSCRIPTION_ID,
        WORKSPACE_NAME,
        QUANTUM_BASE_URL,
        QUANTUM_ENV,
        AZURE_CLIENT_ID,
        AZURE_CLIENT_SECRET,
        AZURE_TENANT_ID,
    ]


class EnvironmentKind(Enum):
    PRODUCTION = 1,
    CANARY = 2,
    DOGFOOD = 3


DATA_PLANE_CREDENTIAL_SCOPE = "https://quantum.microsoft.com/.default"
ARM_CREDENTIAL_SCOPE = "https://management.azure.com/.default"
ARM_BASE_URL = "https://management.azure.com/"
DOGFOOD_ARM_BASE_URL = "https://api-dogfood.resources.windows-int.net/"
# pylint: disable=unnecessary-lambda-assignment
QUANTUM_BASE_URL = lambda location: f"https://{location}.quantum.azure.com/"
QUANTUM_CANARY_BASE_URL = lambda location: f"https://{location or 'eastus2euap'}.quantum.azure.com/"
QUANTUM_DOGFOOD_BASE_URL = lambda location: f"https://{location}.quantum-test.azure.com/"
QUANTUM_API_KEY_HEADER = "x-ms-quantum-api-key"
VALID_CONNECTION_STRING = (
    lambda subscription_id, resource_group, workspace_name, api_key, quantum_endpoint:
    f"SubscriptionId={subscription_id};" +
    f"ResourceGroupName={resource_group};" +
    f"WorkspaceName={workspace_name};" +
    f"ApiKey={api_key};" +
    f"QuantumEndpoint={quantum_endpoint};"
)
VALID_RESOURCE_ID = (
    lambda subscription_id, resource_group, workspace_name:
    f"/subscriptions/{subscription_id}" +
    f"/resourceGroups/{resource_group}" +
    "/providers/Microsoft.Quantum/" +
    f"Workspaces/{workspace_name}"
)
