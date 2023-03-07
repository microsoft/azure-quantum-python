##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING, Optional, Union, Protocol, Any
from abc import abstractmethod

from azure.quantum._client.models import SessionDetails, SessionStatus, SessionJobFailurePolicy
from azure.quantum.job.workspace_item import WorkspaceItem

__all__ = ["Session", "SessionHost"]

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace
    from azure.quantum.workspace import Target

class Session(WorkspaceItem):
    """Azure Quantum Job Session: a logical grouping of jobs.

    :param workspace: Workspace instance to submit job to
    :type workspace: Workspace
    :param job_details: Job details model,
            contains Job ID, name and other details
    :type job_details: JobDetails
    """

    def __init__(
            self,
            workspace: "Workspace",
            details: Optional[SessionDetails] = None,
            target: Union[str, "Target", None] = None,
            provider_id: Optional[str] = None,
            id: Optional[str] = None,
            name: Optional[str] = None,
            job_failure_policy: Union[str, SessionJobFailurePolicy, None] = None,
            **kwargs):
        from azure.quantum.target import Target
        target_name = target.name if isinstance(target, Target) else target
        self._target = target if isinstance(target, Target) else None

        if (details is not None) and (
            (isinstance(target, str)) or
            (provider_id is not None) or
            (id is not None) or
            (name is not None) or
            (job_failure_policy is not None)):
            raise ValueError("""If `session_details` is passed, you should not pass `target`, 
                                `provider_id`, `session_id`, `session_name` or `job_failure_policy`.""")

        if (details is None) and (target is None):
            raise ValueError("If `session_details` is not passed, you should at least pass the `target`.")

        if details is None:
            import uuid
            import re
            id = id if id is not None else str(uuid.uuid1())
            name = name if name is not None else f"session-{id}"
            provider_id = provider_id if provider_id is not None else re.match(r"(\w+)\.", target_name).group(1)
            details = SessionDetails(id=id,
                                             name=name,
                                             provider_id=provider_id,
                                             target=target_name,
                                             job_failure_policy=job_failure_policy,
                                             **kwargs)

        super().__init__(
            workspace=workspace,
            details=details,
            **kwargs
        )

    @property
    def details(self) -> SessionDetails:
        return self._details

    @details.setter
    def details(self, value: SessionDetails):
        self._details = value

    @property
    def target(self) -> "Target":
        return self._target

    def open(self) -> "Session":
        self.workspace.open_session(self)
        return self

    def close(self) -> "Session":
        self.workspace.close_session(self)
        return self

    def refresh(self) -> "Session":
        self.workspace.refresh_session(self)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        session = self.close()
        if isinstance(value, Exception):
            raise


class SessionHost(Protocol):
    _current_session: Optional[Session] = None

    @property
    def latest_session(self) -> Optional[Session]:
        return self._current_session

    @latest_session.setter
    def latest_session(self, session: Optional[Session]):
        self._current_session = session

    def get_latest_session_id(self) -> Optional[str]:
        return self.latest_session.id if self.latest_session else None

    @abstractmethod
    def _get_azure_workspace(self) -> "Workspace":
        raise NotImplementedError

    @abstractmethod
    def _get_azure_target_id(self) -> str:
        raise NotImplementedError

    def open_session(
        self,
        details: Optional[SessionDetails] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        job_failure_policy: Union[str, SessionJobFailurePolicy, None] = None,
        **kwargs
    ) -> Session:
        if self.latest_session:
            self.latest_session.close()

        session = Session(details=details,
                          id=id,
                          name=name,
                          job_failure_policy=job_failure_policy,
                          workspace=self._get_azure_workspace(),
                          target=self._get_azure_target_id(),
                          **kwargs)
        self.latest_session = session
        return session.open()
