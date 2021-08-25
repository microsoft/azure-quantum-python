##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Dict, List, TYPE_CHECKING, Union
from azure.quantum.aio.target import Target as AsyncTarget
from azure.quantum.aio.target import *
from azure.quantum.target.target_factory import TargetFactory as SyncTargetFactory

if TYPE_CHECKING:
    from azure.quantum.aio import Workspace

# Target ID keyword for parameter-free solvers
PARAMETER_FREE = "parameterfree"


class TargetFactory(SyncTargetFactory):
    """Factory class for generating a Target based on a
    provider and target name
    """
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    @staticmethod
    def _get_all_target_cls() -> Dict[str, Target]:
        """Get all target classes by target name"""
        return {
            name: _t for t in AsyncTarget.__subclasses__()
            for _t in [t] + t.__subclasses__()
            for name in _t.target_names
        }

    async def get_targets(
        self,
        workspace: "Workspace",
        name: str,
        provider_id: str,
        **kwargs
    ) -> Union[Target, List[Target]]:
        """Create targets that are available to this workspace
        filtered by name and provider ID.

        :param name: Target name
        :type name: str
        :param workspace: Workspace
        :type workspace: Workspace
        :param provider_id: Provider name
        :type provider_id: str
        :return: One or more Target objects
        :rtype: Union[Target, List[Target]]
        """
        target_statuses = await workspace._get_target_status(name, provider_id, **kwargs)

        if len(target_statuses) == 1:
            return self.from_target_status(workspace, *target_statuses[0])

        else:
            # Don't return redundant parameter-free targets
            return [
                self.from_target_status(workspace, _provider_id, status, **kwargs)
                for _provider_id, status in target_statuses
                if PARAMETER_FREE not in status.id
            ]
