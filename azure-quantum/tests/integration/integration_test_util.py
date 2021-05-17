import os
from azure.quantum import Workspace
from azure.common.credentials import ServicePrincipalCredentials


def create_workspace() -> Workspace:
    """Create workspace using credentials stored in config file

    :return: Workspace
    :rtype: Workspace
    """

    client_id = os.environ.get("AZURE_CLIENT_ID", "")
    client_secret = os.environ.get("AZURE_CLIENT_SECRET", "")
    tenant_id = os.environ.get("AZURE_TENANT_ID", "")
    resource_group = os.environ.get("RESOURCE_GROUP", "")
    subscription_id = os.environ.get("SUBSCRIPTION_ID", "")
    workspace_name = os.environ.get("WORKSPACE_NAME", "")

    assert (
        len(client_id) > 0
    ), "AZURE_CLIENT_ID not found in environment variables."
    assert (
        len(client_secret) > 0
    ), "AZURE_CLIENT_SECRET not found in environment variables."
    assert (
        len(tenant_id) > 0
    ), "AZURE_TENANT_ID not found in environment variables."
    assert (
        len(resource_group) > 0
    ), "RESOURCE_GROUP not found in environment variables."
    assert (
        len(subscription_id) > 0
    ), "SUBSCRIPTION_ID not found in environment variables."
    assert (
        len(workspace_name) > 0
    ), "WORKSPACE_NAME not found in environment variables."

    if len(client_secret) > 0:
        workspace = Workspace(
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=workspace_name,
        )
        workspace.credentials = ServicePrincipalCredentials(
            tenant=tenant_id,
            client_id=client_id,
            secret=client_secret,
            resource="https://quantum.microsoft.com",
        )

    workspace.login()
    return workspace
