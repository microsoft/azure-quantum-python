##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import abc
from typing import TYPE_CHECKING, Union

from azure.quantum._client.models import ItemDetails, ItemType, SessionDetails, JobDetails

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace

__all__ = ["WorkspaceItem", "WorkspaceItemFilter"]

class WorkspaceItem(abc.ABC):
    """

    :param workspace: Workspace instance to submit job to
    :type workspace: Workspace
    :param item_details: Item details model,
            contains item ID, name and other details
    :type item_details: ItemDetails
    """

    def __init__(self, workspace: "Workspace", details: ItemDetails, **kwargs):
        self._workspace = workspace
        self._details = details
        self._id = details.id
        self._item_type = details.item_type

    @property
    def workspace(self) -> "Workspace":
        return self._workspace

    @property
    def details(self) -> Union[SessionDetails, JobDetails]:
        return self._details

    @property
    def id(self) -> str:
        return self._id

    @property
    def item_type(self) -> ItemType:
        return self._item_type


class WorkspaceItemFilter():
    """

    :param workspace: Workspace instance to submit job to
    :type workspace: Workspace
    :param item_details: Item details model,
            contains item ID, name and other details
    :type item_details: ItemDetails
    """

    #OData filter expression supporting eq operator on id, 
    # name, providerId, target, status, itemType, jobType and
    #  lt/gt operators on creationTime, endExecutionTime.",

    def __init__(self,
                 as_odata: str = None,
                 eq_id: str = None,
                 eq_name: str = None,
                 eq_provider_id: str = None,
                 eq_target: str = None,
                 eq_status: str = None,
                 eq_item_type: str = None,
                 eq_job_type: str = None,
                 lt_creation_time: str = None,
                 gt_creation_time: str = None,
                 lt_end_execution_time: str = None,
                 gt_end_execution_time: str = None):
        self.as_odata = as_odata
        self.eq_id = eq_id
        self.eq_name = eq_name
        self.eq_provider_id = eq_provider_id
        self.eq_target = eq_target
        self.eq_status = eq_status
        self.eq_item_type = eq_item_type
        self.eq_job_type = eq_job_type
        self.lt_creation_time = lt_creation_time
        self.gt_creation_time = gt_creation_time
        self.lt_end_execution_time = lt_end_execution_time
        self.gt_end_execution_time = gt_end_execution_time

