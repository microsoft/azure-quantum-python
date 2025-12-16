##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import unittest
from azure.quantum._workspace_connection_params import WorkspaceConnectionParams


class TestWorkspaceConnectionParamsValidation(unittest.TestCase):
    """Test validation of WorkspaceConnectionParams fields."""

    def test_valid_subscription_ids(self):
        """Test that valid subscription_ids are accepted."""
        valid_ids = [
            "12345678-1234-1234-1234-123456789abc",
            "ABCDEF01-2345-6789-ABCD-EF0123456789",
            "abcdef01-2345-6789-abcd-ef0123456789",
        ]
        for subscription_id in valid_ids:
            params = WorkspaceConnectionParams(subscription_id=subscription_id)
            self.assertEqual(params.subscription_id, subscription_id)

    def test_invalid_subscription_ids(self):
        """Test that invalid subscription_ids raise ValueError."""
        invalid_ids = [
            ("not-a-guid", "Subscription ID must be a valid GUID."),
            (12345, "Subscription ID must be a string."),
        ]
        for subscription_id, expected_message in invalid_ids:
            with self.assertRaises(ValueError) as context:
                WorkspaceConnectionParams(subscription_id=subscription_id)
            self.assertIn(expected_message, str(context.exception))

    def test_valid_resource_groups(self):
        """Test that valid resource_groups are accepted."""
        valid_groups = [
            "my-resource-group",
            "MyResourceGroup",
            "resource_group_123",
            "rg123",
            "a" * 90,  # Max length (90 chars)
            "a",  # Min length (1 char)
            "Resource_Group-1",
            "my.resource.group",  # Periods allowed (except at end)
            "group(test)",  # Parentheses allowed
            "group(test)name",
            "(parentheses)",
            "test-group_name",
            "GROUP-123",
            "123-group",
            "Test.Group.Name",
            "my-group.v2",
            "rg_test(prod)-v1.2",
            "café",  # Unicode letters (Lo)
            "日本語",  # Unicode letters (Lo)
            "Казан",  # Unicode letters (Lu, Ll)
            "αβγ",  # Greek letters (Ll)
            "test-café-123",  # Mixed ASCII and Unicode
            "group_名前",  # Mixed ASCII and Unicode
            "test.group(1)-name_v2",  # Multiple special chars
        ]
        for resource_group in valid_groups:
            params = WorkspaceConnectionParams(resource_group=resource_group)
            self.assertEqual(params.resource_group, resource_group)

    def test_invalid_resource_groups(self):
        """Test that invalid resource_groups raise ValueError."""
        rg_invalid_chars_msg = "Resource group name can only include alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters that match the allowed characters."
        invalid_groups = [
            ("my/resource/group", rg_invalid_chars_msg),
            ("my\\resource\\group", rg_invalid_chars_msg),
            ("my resource group", rg_invalid_chars_msg),
            (12345, "Resource group name must be a string."),
            ("group.", rg_invalid_chars_msg),  # Period at end
            ("my-group.", rg_invalid_chars_msg),  # Period at end
            ("test.group.", rg_invalid_chars_msg),  # Period at end
            ("a" * 91, "Resource group name must be between 1 and 90 characters long."),  # Too long
            ("group@test", rg_invalid_chars_msg),  # @ symbol
            ("group#test", rg_invalid_chars_msg),  # # symbol
            ("group$test", rg_invalid_chars_msg),  # $ symbol
            ("group%test", rg_invalid_chars_msg),  # % symbol
            ("group^test", rg_invalid_chars_msg),  # ^ symbol
            ("group&test", rg_invalid_chars_msg),  # & symbol
            ("group*test", rg_invalid_chars_msg),  # * symbol
            ("group+test", rg_invalid_chars_msg),  # + symbol
            ("group=test", rg_invalid_chars_msg),  # = symbol
            ("group[test]", rg_invalid_chars_msg),  # Square brackets
            ("group{test}", rg_invalid_chars_msg),  # Curly brackets
            ("group|test", rg_invalid_chars_msg),  # Pipe
            ("group:test", rg_invalid_chars_msg),  # Colon
            ("group;test", rg_invalid_chars_msg),  # Semicolon
            ("group\"test", rg_invalid_chars_msg),  # Quote
            ("group'test", rg_invalid_chars_msg),  # Single quote
            ("group<test>", rg_invalid_chars_msg),  # Angle brackets
            ("group,test", rg_invalid_chars_msg),  # Comma
            ("group?test", rg_invalid_chars_msg),  # Question mark
            ("group!test", rg_invalid_chars_msg),  # Exclamation mark
            ("group`test", rg_invalid_chars_msg),  # Backtick
            ("group~test", rg_invalid_chars_msg),  # Tilde
            ("test\ngroup", rg_invalid_chars_msg),  # Newline
            ("test\tgroup", rg_invalid_chars_msg),  # Tab
        ]
        for resource_group, expected_message in invalid_groups:
            with self.assertRaises(ValueError) as context:
                WorkspaceConnectionParams(resource_group=resource_group)
            self.assertIn(expected_message, str(context.exception))

    def test_empty_resource_group(self):
        """Test that empty resource_group is treated as None (not set)."""
        # Empty strings are treated as falsy in the merge logic and not set
        params = WorkspaceConnectionParams(resource_group="")
        self.assertIsNone(params.resource_group)

    def test_valid_workspace_names(self):
        """Test that valid workspace names are accepted."""
        valid_names = [
            "12",
            "a1",
            "1a",
            "ab",
            "myworkspace",
            "WORKSPACE",
            "MyWorkspace",
            "myWorkSpace",
            "myworkspacE",
            "1234567890",
            "123workspace",
            "workspace123",
            "w0rksp4c3",
            "123abc456def",
            "abc123",
            # with hyphens
            "my-workspace",
            "my-work-space",
            "workspace-with-a-long-name-that-is-still-valid",
            "a-b-c-d-e",
            "my-workspace-2",
            "workspace-1-2-3",
            "1-a",
            "b-2",
            "1-2",
            "a-b",
            "1-b-2",
            "a-1-b",
            "workspace" + "-" * 10 + "test",
            "a" * 54,  # Max length (54 chars)
            "1" * 54,  # Max length with numbers
        ]
        for workspace_name in valid_names:
            params = WorkspaceConnectionParams(workspace_name=workspace_name)
            self.assertEqual(params.workspace_name, workspace_name)

    def test_invalid_workspace_names(self):
        """Test that invalid workspace names raise ValueError."""
        not_valid_names = [
            ("a", "Workspace name must be between 2 and 54 characters long."),
            ("1", "Workspace name must be between 2 and 54 characters long."),
            ("a" * 55, "Workspace name must be between 2 and 54 characters long."),
            ("1" * 55, "Workspace name must be between 2 and 54 characters long."),
            ("my_workspace", "Workspace name can only include alphanumerics (a-zA-Z0-9) and hyphens, and cannot start or end with hyphen."),
            ("my/workspace", "Workspace name can only include alphanumerics (a-zA-Z0-9) and hyphens, and cannot start or end with hyphen."),
            ("my workspace", "Workspace name can only include alphanumerics (a-zA-Z0-9) and hyphens, and cannot start or end with hyphen."),
            ("-myworkspace", "Workspace name can only include alphanumerics (a-zA-Z0-9) and hyphens, and cannot start or end with hyphen."),
            ("myworkspace-", "Workspace name can only include alphanumerics (a-zA-Z0-9) and hyphens, and cannot start or end with hyphen."),
            (12345, "Workspace name must be a string."),
        ]
        for workspace_name, expected_message in not_valid_names:
            with self.assertRaises(ValueError) as context:
                WorkspaceConnectionParams(workspace_name=workspace_name)
            self.assertIn(expected_message, str(context.exception))

    def test_empty_workspace_name(self):
        """Test that empty workspace_name is treated as None (not set)."""
        # Empty strings are treated as falsy in the merge logic and not set
        params = WorkspaceConnectionParams(workspace_name="")
        self.assertIsNone(params.workspace_name)

    def test_valid_locations(self):
        """Test that valid locations are accepted and normalized."""
        valid_locations = [
            ("East US", "eastus"),
            ("West Europe", "westeurope"),
            ("eastus", "eastus"),
            ("westus2", "westus2"),
            ("EASTUS", "eastus"),
            ("WestUs2", "westus2"),
            ("South Central US", "southcentralus"),
            ("North Europe", "northeurope"),
            ("Southeast Asia", "southeastasia"),
            ("Japan East", "japaneast"),
            ("UK South", "uksouth"),
            ("Australia East", "australiaeast"),
            ("Central India", "centralindia"),
            ("France Central", "francecentral"),
            ("Germany West Central", "germanywestcentral"),
            ("Switzerland North", "switzerlandnorth"),
            ("UAE North", "uaenorth"),
            ("Brazil South", "brazilsouth"),
            ("Korea Central", "koreacentral"),
            ("South Africa North", "southafricanorth"),
            ("Norway East", "norwayeast"),
            ("Sweden Central", "swedencentral"),
            ("Qatar Central", "qatarcentral"),
            ("Poland Central", "polandcentral"),
            ("Italy North", "italynorth"),
            ("Israel Central", "israelcentral"),
            ("Spain Central", "spaincentral"),
            ("Austria East", "austriaeast"),
            ("Belgium Central", "belgiumcentral"),
            ("Chile Central", "chilecentral"),
            ("Indonesia Central", "indonesiacentral"),
            ("Malaysia West", "malaysiawest"),
            ("Mexico Central", "mexicocentral"),
            ("New Zealand North", "newzealandnorth"),
            ("westus3", "westus3"),
            ("canadacentral", "canadacentral"),
            ("westcentralus", "westcentralus"),
        ]
        for location, expected in valid_locations:
            params = WorkspaceConnectionParams(location=location)
            self.assertEqual(params.location, expected)

    def test_invalid_locations(self):
        """Test that invalid locations raise ValueError."""
        location_invalid_region_msg = "Location must be one of the Azure regions listed in https://learn.microsoft.com/en-us/azure/reliability/regions-list."
        invalid_locations = [
            ("   ", location_invalid_region_msg),
            ("invalid-region", location_invalid_region_msg),
            ("us-east", location_invalid_region_msg),
            ("east-us", location_invalid_region_msg),
            ("westus4", location_invalid_region_msg),
            ("southus", location_invalid_region_msg),
            ("centraleurope", location_invalid_region_msg),
            ("asiaeast", location_invalid_region_msg),
            ("chinaeast", location_invalid_region_msg),
            ("usgovtexas", location_invalid_region_msg),
            ("East US 3", location_invalid_region_msg),
            ("not a region", location_invalid_region_msg),
            (12345, "Location must be a string."),
            (3.14, "Location must be a string."),
            (True, "Location must be a string."),
        ]
        for location, expected_message in invalid_locations:
            with self.assertRaises(ValueError) as context:
                WorkspaceConnectionParams(location=location)
            self.assertIn(expected_message, str(context.exception))

    def test_empty_location(self):
        """Test that empty location is treated as None (not set)."""
        # Empty strings are treated as falsy in the merge logic and not set
        params = WorkspaceConnectionParams(location="")
        self.assertIsNone(params.location)
        
        # None is also allowed and treated as not set
        params = WorkspaceConnectionParams(location=None)
        self.assertIsNone(params.location)

    def test_none_values_are_allowed(self):
        """Test that None values for optional fields are allowed."""
        # This should not raise any exceptions
        params = WorkspaceConnectionParams(
            subscription_id=None,
            resource_group=None,
            workspace_name=None,
            location=None,
            user_agent=None,
        )
        self.assertIsNone(params.subscription_id)
        self.assertIsNone(params.resource_group)
        self.assertIsNone(params.workspace_name)
        self.assertIsNone(params.location)
        self.assertIsNone(params.user_agent)

    def test_multiple_valid_parameters(self):
        """Test that multiple valid parameters work together."""
        params = WorkspaceConnectionParams(
            subscription_id="12345678-1234-1234-1234-123456789abc",
            resource_group="my-resource-group",
            workspace_name="my-workspace",
            location="East US",
            user_agent="my-app/1.0",
        )
        self.assertEqual(params.subscription_id, "12345678-1234-1234-1234-123456789abc")
        self.assertEqual(params.resource_group, "my-resource-group")
        self.assertEqual(params.workspace_name, "my-workspace")
        self.assertEqual(params.location, "eastus")
        self.assertEqual(params.user_agent, "my-app/1.0")

    def test_validation_on_resource_id(self):
        """Test that validation works when using resource_id."""
        # Valid resource_id should work
        resource_id = (
            "/subscriptions/12345678-1234-1234-1234-123456789abc"
            "/resourceGroups/my-rg"
            "/providers/Microsoft.Quantum"
            "/Workspaces/my-ws"
        )
        params = WorkspaceConnectionParams(resource_id=resource_id)
        self.assertEqual(params.subscription_id, "12345678-1234-1234-1234-123456789abc")
        self.assertEqual(params.resource_group, "my-rg")
        self.assertEqual(params.workspace_name, "my-ws")

    def test_validation_on_connection_string(self):
        """Test that validation works when using connection_string."""
        # Valid connection string should work
        connection_string = (
            "SubscriptionId=12345678-1234-1234-1234-123456789abc;"
            "ResourceGroupName=my-rg;"
            "WorkspaceName=my-ws;"
            "ApiKey=test-key;"
            "QuantumEndpoint=https://eastus.quantum.azure.com/;"
        )
        params = WorkspaceConnectionParams(connection_string=connection_string)
        self.assertEqual(params.subscription_id, "12345678-1234-1234-1234-123456789abc")
        self.assertEqual(params.resource_group, "my-rg")
        self.assertEqual(params.workspace_name, "my-ws")
        self.assertEqual(params.location, "eastus")


if __name__ == "__main__":
    unittest.main()
