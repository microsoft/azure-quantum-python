##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import warnings
from typing import Dict, List, TYPE_CHECKING, Union
from azure.quantum.target import *

if TYPE_CHECKING:
    from azure.quantum import Workspace
    from azure.quantum._client.models import TargetStatus

# Target ID keyword for parameter-free solvers
PARAMETER_FREE = "parameterfree"


def get_all_target_cls() -> Dict[str, Target]:
    """Get all target classes by target name"""
    return {
        name: _t for t in Target.__subclasses__()
        for _t in [t] + t.__subclasses__()
        for name in _t.target_names
    }


class TargetFactory:
    """Factory class for generating a Target based on a provider and target name"""
    def __init__(self, workspace: "Workspace"):
        self.workspace = workspace
    
    @staticmethod
    def _target_cls(provider_id: str, name: str):
        all_targets = get_all_target_cls()

        if name in all_targets:
            return all_targets[name]

        if provider_id in DEFAULT_TARGETS:
            return DEFAULT_TARGETS[provider_id]
 
        warnings.warn(
            "No default target specified for provider {provider_id}. \
Please check the provider name and try again or create an issue here: \
https://github.com/microsoft/qdk-python/issues.")

    def create_target(self, provider_id: str, name: str, **kwargs) -> Target:
        """Create target from provider ID and target name.

        :param provider_id: Provider name
        :type provider_id: str
        :param name: Target name
        :type name: str
        :return: Target instance
        :rtype: Target
        """
        cls = self._target_cls(provider_id, name)
        if cls is not None:
            return cls(
                workspace=self.workspace,
                name=name,
                provider_id=provider_id,
                **kwargs
            )

    def from_target_status(self, provider_id: str, status: "TargetStatus", **kwargs):
        cls = self._target_cls(provider_id, status.id)
        if cls is not None:
            return cls.from_target_status(self.workspace, status, **kwargs)

    def get_targets(
        self, name: str, provider_id: str, **kwargs
    ) -> Union[Target, List[Target]]:
        """Create targets that are available to this workspace
        filtered by name and provider ID.

        :param name: Target name
        :type name: str
        :param provider_id: Provider name
        :type provider_id: str
        :return: One or more Target objects
        :rtype: Union[Target, List[Target]]
        """
        target_statuses = self.workspace._get_target_status(name, provider_id, **kwargs)

        if len(target_statuses) == 1:
            return self.from_target_status(*target_statuses[0])

        else:
            # Don't return redundant parameter-free targets
            return [
                self.from_target_status(_provider_id, status, **kwargs)
                for _provider_id, status in target_statuses
                if PARAMETER_FREE not in status.id
            ]
