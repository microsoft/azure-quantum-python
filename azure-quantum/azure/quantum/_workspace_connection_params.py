##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from __future__ import annotations
import re
import os
from re import Match
from typing import (
    Optional,
    Callable,
    Union
)
from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.policies import AzureKeyCredentialPolicy
from azure.quantum._authentication import _DefaultAzureCredential
from azure.quantum._constants import (
    EnvironmentKind,
    EnvironmentVariables,
    QUANTUM_BASE_URL,
    QUANTUM_CANARY_BASE_URL,
    QUANTUM_DOGFOOD_BASE_URL,
    ARM_BASE_URL,
    DOGFOOD_ARM_BASE_URL,
    QUANTUM_API_KEY_HEADER,
)

class WorkspaceConnectionParams:
    CONNECTION_STRING_REGEX = re.compile(
        r"""
            ^
            SubscriptionId=(?P<subscription_id>[a-fA-F0-9-]*);
            ResourceGroupName=(?P<resource_group>[^\s/]*);
            WorkspaceName=(?P<workspace_name>[^\s/]*);
            ApiKey=(?P<api_key>[^\s/]*);
            QuantumEndpoint=(?P<base_url>https://(?P<location>[^\s/]*).quantum(?:-test)?.azure.com/);
        """,
        re.VERBOSE | re.IGNORECASE)

    RESOURCE_ID_REGEX = re.compile(
        r"""
            ^
            /subscriptions/(?P<subscription_id>[a-fA-F0-9-]*)
            /resourceGroups/(?P<resource_group>[^\s/]*)
            /providers/Microsoft\.Quantum
            /Workspaces/(?P<workspace_name>[^\s/]*)
            $
        """,
        re.VERBOSE | re.IGNORECASE)

    def __init__(
        self,
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        workspace_name: Optional[str] = None,
        location: Optional[str] = None,
        base_url: Optional[str] = None,
        arm_base_url: Optional[str] = None,
        environment: Union[str, EnvironmentKind, None] = None,
        credential: Optional[object] = None,
        resource_id: Optional[str] = None,
        user_agent: Optional[str] = None,
        user_agent_app_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        connection_string: Optional[str] = None,
        on_new_client_request: Optional[Callable] = None,
        **kwargs
    ):
        self._location = None
        self._resource_id = None
        self._environment = None
        self._base_url = None
        self._arm_base_url = None
        self._connection_string = None
        self._api_key = None

        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        self.location = location
        self.base_url = base_url
        self.arm_base_url = arm_base_url
        self.environment = environment
        self.credential = credential
        self.resource_id = resource_id
        self.user_agent = user_agent
        self.user_agent_app_id = user_agent_app_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.api_version = api_version
        self.connection_string = connection_string
        self.api_key = api_key
        self.on_new_client_request = on_new_client_request
        self.merge(**kwargs)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = (value.replace(" ", "").lower()
                          if isinstance(value, str)
                          else value)

    @property
    def connection_string(self):
        return self._connection_string

    @connection_string.setter
    def connection_string(self, value: str):
        self._connection_string = value
        if value:
            match = re.search(
                WorkspaceConnectionParams.CONNECTION_STRING_REGEX,
                value)
            if not match:
                raise ValueError("Invalid connection string")
            self._merge_re_match(match)

    @property
    def resource_id(self):
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str):
        self._resource_id = value
        if value:
            match = re.search(
                WorkspaceConnectionParams.RESOURCE_ID_REGEX,
                value)
            if not match:
                raise ValueError("Invalid resource id")
            self._merge_re_match(match)

    @property
    def environment(self):
        return self._environment or EnvironmentKind.PRODUCTION

    @environment.setter
    def environment(self, value: Union[str, EnvironmentKind]):
        self._environment = (EnvironmentKind[value.upper()]
                             if isinstance(value, str)
                             else value)

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        if value:
            self.credential = AzureKeyCredential(value)
        self._api_key = value

    @property
    def base_url(self):
        if self._base_url:
            return self._base_url
        if not self.location:
            raise ValueError("Location not specified")
        if self.environment is EnvironmentKind.PRODUCTION:
            return QUANTUM_BASE_URL(self.location)
        if self.environment is EnvironmentKind.CANARY:
            return QUANTUM_CANARY_BASE_URL(self.location)
        if self.environment is EnvironmentKind.DOGFOOD:
            return QUANTUM_DOGFOOD_BASE_URL(self.location)
        raise ValueError(f"Unknown environment `{self.environment}`.")

    @base_url.setter
    def base_url(self, value: str):
        self._base_url = value

    @property
    def arm_base_url(self):
        if self._arm_base_url:
            return self._arm_base_url
        if self.environment is EnvironmentKind.DOGFOOD:
            return DOGFOOD_ARM_BASE_URL
        if self.environment in [EnvironmentKind.PRODUCTION,
                                EnvironmentKind.CANARY]:
            return ARM_BASE_URL
        raise ValueError(f"Unknown environment `{self.environment}`.")

    @arm_base_url.setter
    def arm_base_url(self, value: str):
        self._arm_base_url = value

    def _apply_args_to_kwargs(self, args, kwargs):
        """
        Store all `not None` named parameters
        into the kwargs dictionary.
        """
        for key in args.keys():
            if (
                key not in ["self", "kwargs",
                            "merge_default_mode"]
                and not key.startswith("_")
            ):
                value = args[key]
                if value:
                    kwargs[key] = value

    def __repr__(self):
        """
        Print all fields and properties.
        """
        info = []
        for key in vars(self):
            info.append(f"    {key}: {self.__dict__[key]}")
        cls = type(self)
        for key in dir(self):
            attr = getattr(cls, key, None)
            if attr and isinstance(attr, property) and attr.fget:
                info.append(f"    {key}: {attr.fget(self)}")
        info.sort()
        info.insert(0, super().__repr__())
        return "\n".join(info)

    def merge(
        self,
        # Listing the named parameters for the
        # convenience of code completion.
        # pylint: disable=unused-argument
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        workspace_name: Optional[str] = None,
        location: Optional[str] = None,
        base_url: Optional[str] = None,
        arm_base_url: Optional[str] = None,
        environment: Union[str, EnvironmentKind, None] = None,
        credential: Optional[object] = None,
        resource_id: Optional[str] = None,
        user_agent: Optional[str] = None,
        user_agent_app_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_version: Optional[str] = None,
        connection_string: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Set all fields/properties with `not None` values
        passed in the (named or key-valued) arguments
        into this instance.
        """
        self._apply_args_to_kwargs(locals(), kwargs)
        self._merge(merge_default_mode=False,
                    **kwargs)
        return self

    def apply_defaults(
        self,
        # Listing the named parameters for the
        # convenience of code completion.
        # pylint: disable=unused-argument
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        workspace_name: Optional[str] = None,
        location: Optional[str] = None,
        base_url: Optional[str] = None,
        arm_base_url: Optional[str] = None,
        environment: Union[str, EnvironmentKind, None] = None,
        credential: Optional[object] = None,
        resource_id: Optional[str] = None,
        user_agent: Optional[str] = None,
        user_agent_app_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_version: Optional[str] = None,
        connection_string: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Set all fields/properties with `not None` values
        passed in the (named or key-valued) arguments
        into this instance IF the instance does not have
        the corresponding parameter set yet.
        """
        self._apply_args_to_kwargs(locals(), kwargs)
        self._merge(merge_default_mode=True,
                    **kwargs)
        return self

    def _merge(
        self,
        merge_default_mode: bool,
        **kwargs
    ):
        """
        Set all fields/properties with `not None` values
        passed in the (named or key-valued) arguments
        into this instance.
        """
        self._apply_args_to_kwargs(locals(), kwargs)
        cls = type(self)
        for (key, value) in kwargs.items():
            if value:
                if merge_default_mode and self._has_value(key):
                    continue

                is_public_field = key in vars(self)
                if is_public_field:
                    setattr(self, key, value)
                elif hasattr(cls, key):
                    attr = getattr(cls, key, None)
                    if attr and isinstance(attr, property) and attr.fset:
                        attr.fset(self, value)

    def _has_value(self, key):
        if key in vars(self):
            return getattr(self, key) is not None
        # re-try to get from a private field
        key = "_" + key
        return getattr(self, key) is not None

    def merge_connection_params(
            self,
            connection_params: WorkspaceConnectionParams,
            merge_default_mode: bool = False,
    ):
        """
        Set all fields/properties with `not None` values
        from the `connection_params` into this instance.
        """
        kwargs = {}
        for key in vars(connection_params):
            kwargs[key] = connection_params.__dict__[key]
        self._merge(
            merge_default_mode=merge_default_mode,
            **kwargs)
        return self

    def get_credential_or_default(self):
        return (self.credential
                or _DefaultAzureCredential(
                    subscription_id=self.subscription_id,
                    arm_base_url=self.arm_base_url,
                    tenant_id=self.tenant_id))

    def get_auth_policy(self):
        if isinstance(self.credential, AzureKeyCredential):
            return AzureKeyCredentialPolicy(self.credential,
                                            QUANTUM_API_KEY_HEADER)
        return None

    def append_user_agent(self, value: str):
        """
        Append a new value to the Workspace's UserAgent and re-initialize the
        QuantumClient. The values are appended using a dash.

        :param value: UserAgent value to add, e.g. "azure-quantum-<plugin>"
        """
        new_user_agent = None

        if (
            value
            and value not in (self.user_agent or "")
        ):
            new_user_agent = (f"{self.user_agent}-{value}"
                              if self.user_agent else value)

        if new_user_agent != self.user_agent:
            self.user_agent = new_user_agent
            if self.on_new_client_request:
                self.on_new_client_request()

    def get_full_user_agent(self):
        """
        Get the full Azure Quantum Python SDK UserAgent
        that is sent to the service via the header.
        """
        full_user_agent = self.user_agent
        app_id = self.user_agent_app_id
        if self.user_agent_app_id:
            full_user_agent = (f"{app_id} {full_user_agent}"
                               if full_user_agent else app_id)
        return full_user_agent

    def is_complete(self) -> bool:
        return (self.location
                and self.subscription_id
                and self.resource_group
                and self.workspace_name
                and self.get_credential_or_default())

    def assert_complete(self):
        if not self.is_complete():
            raise ValueError(
                """
                    Azure Quantum workspace not fully specified.
                    Please specify one of the following:
                    1) A valid combination of location and resource ID.
                    2) A valid combination of location, subscription ID,
                    resource group name, and workspace name.
                    3) A valid connection string (via Workspace.from_connection_string()).
                """)

    def default_from_env_vars(self):
        """
        Merge values found in the environment variables
        """
        return self.merge_connection_params(
            connection_params=WorkspaceConnectionParams.from_env_vars(),
            merge_default_mode=True,
        )

    @classmethod
    def from_env_vars(
        cls,
    ):
        """
        Initialize the WorkspaceConnectionParams from values found
        in the environment variables.
        """
        return WorkspaceConnectionParams(
            subscription_id=(
                os.environ.get(EnvironmentVariables.QUANTUM_SUBSCRIPTION_ID)
                or os.environ.get(EnvironmentVariables.SUBSCRIPTION_ID)),
            resource_group=(
                os.environ.get(EnvironmentVariables.QUANTUM_RESOURCE_GROUP)
                or os.environ.get(EnvironmentVariables.RESOURCE_GROUP)),
            workspace_name=(
                os.environ.get(EnvironmentVariables.WORKSPACE_NAME)),
            location=(
                os.environ.get(EnvironmentVariables.QUANTUM_LOCATION)
                or os.environ.get(EnvironmentVariables.LOCATION)),
            environment=os.environ.get(EnvironmentVariables.QUANTUM_ENV),
            base_url=os.environ.get(EnvironmentVariables.QUANTUM_BASE_URL),
            user_agent_app_id=os.environ.get(EnvironmentVariables.USER_AGENT_APPID),
            tenant_id=os.environ.get(EnvironmentVariables.AZURE_TENANT_ID),
            client_id=os.environ.get(EnvironmentVariables.AZURE_CLIENT_ID),
            client_secret=os.environ.get(EnvironmentVariables.AZURE_CLIENT_SECRET),
            connection_string=os.environ.get(EnvironmentVariables.CONNECTION_STRING),
            api_key=os.environ.get(EnvironmentVariables.QUANTUM_API_KEY),
        )

    def _merge_re_match(self, re_match: Match[str]):
        def get_value(group_name):
            return re_match.groupdict().get(group_name)
        self.merge(
            subscription_id=get_value('subscription_id'),
            resource_group=get_value('resource_group'),
            workspace_name=get_value('workspace_name'),
            location=get_value('location'),
            base_url=get_value('base_url'),
            arm_base_url=get_value('arm_base_url'),
            api_key=get_value('api_key'),
        )
