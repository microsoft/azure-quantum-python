##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import time
import json

from typing import TYPE_CHECKING

from azure.quantum._client.models import SessionDetails, SessionStatus, SessionJobFailurePolicy
from azure.quantum.job.workspace_item import WorkspaceItem

#__all__ = ["Session"]

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


_log = logging.getLogger(__name__)


class Session(WorkspaceItem):
    """Azure Quantum Job Session: a logical grouping of jobs.

    :param workspace: Workspace instance to submit job to
    :type workspace: Workspace
    :param job_details: Job details model,
            contains Job ID, name and other details
    :type job_details: JobDetails
    """

    def __init__(self, workspace: "Workspace", session_details: SessionDetails, **kwargs):
        super().__init__(
            workspace=workspace,
            details=session_details
        )
