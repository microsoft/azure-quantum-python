##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import abc
from typing import TYPE_CHECKING, Union

from azure.quantum._client.models import ItemDetails, ItemType, SessionDetails, JobDetails

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace

__all__ = ["WorkspaceItem"]

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
