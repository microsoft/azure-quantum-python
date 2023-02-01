##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import time
import json

from typing import TYPE_CHECKING, Optional, Union, Protocol, Any
from abc import abstractmethod

from azure.quantum._client.models import SessionDetails, SessionStatus, SessionJobFailurePolicy
from azure.quantum.job.workspace_item import WorkspaceItem

__all__ = ["Session", "SessionHost", "AlreadyHasASessionError"]

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
            session_details: Optional[SessionDetails] = None,
            target: Union[str, "Target", None] = None,
            provider_id: Optional[str] = None,
            session_id: Optional[str] = None,
            session_name: Optional[str] = None,
            job_failure_policy: Union[str, SessionJobFailurePolicy, None] = None,
            **kwargs):
        from azure.quantum.target import Target
        target_name = target.name if isinstance(target, Target) else target
        self._target = target if isinstance(target, Target) else None

        if (session_details is not None) and (
            (isinstance(target, str)) or
            (provider_id is not None) or
            (session_id is not None) or
            (session_name is not None) or
            (job_failure_policy is not None)):
            raise ValueError("""If `session_details` is passed, you should not pass `target`, 
                                `provider_id`, `session_id`, `session_name` or `job_failure_policy`.""")

        if (session_details is None) and (target is None):
            raise ValueError("If `session_details` is not passed, you should at least pass the `target`.")

        if session_details is None:
            import uuid
            import re
            session_id = session_id if session_id is not None else str(uuid.uuid1())
            session_name = session_name if session_name is not None else f"session-{session_id}"
            provider_id = provider_id if provider_id is not None else re.match(r"(\w+)\.", target_name).group(1)
            session_details = SessionDetails(id=session_id,
                                             name=session_name,
                                             provider_id=provider_id,
                                             target=target_name,
                                             job_failure_policy=job_failure_policy,
                                             **kwargs)

        super().__init__(
            workspace=workspace,
            details=session_details,
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

    def start(self) -> "Session":
        self.workspace.start_session(self)
        return self

    def end(self) -> "Session":
        self.workspace.end_session(self)
        return self

    def refresh(self) -> "Session":
        self.workspace.refresh_session(self)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        session = self.end()
        if isinstance(value, Exception):
            raise


class AlreadyHasASessionError(Exception):
    """Exception raised when trying to start a new session `target.start_session()`
       and the current target instance already has a session associated with it.
    """

    def __init__(self, session_id):
        self.message = f"""The current target instance already has a session ({session_id}) associated with it.
                           If you want to start a new session, you should obtain a new target instance.
                           A new target instance can be obtained with `workspace.get_targets("provider_id.target_name")`
                           Qiskit: `target` is the same concept as a Qiskit `backend`. It can be obtained with `provider.get_backend("provider_id.target_name")`.
                           Cirq: a new target instance can be obtained with `service.get_target("provider_id.target_name")`.
                           """
        super().__init__(self.message)


class SessionHost(Protocol):
    _current_session: Optional[Session] = None

    @property
    def current_session(self) -> Optional[Session]:
        return self._current_session

    @current_session.setter
    def current_session(self, session: Optional[Session]):
        self._current_session = session

    def get_current_session_id(self) -> Optional[str]:
        return self.current_session.id if self.current_session else None

    @abstractmethod
    def _get_azure_workspace(self) -> "Workspace":
        raise NotImplementedError

    @abstractmethod
    def _get_azure_target_id(self) -> str:
        raise NotImplementedError

    def start_session(
        self,
        session_details: Optional[SessionDetails] = None,
        session_id: Optional[str] = None,
        session_name: Optional[str] = None,
        job_failure_policy: Union[str, SessionJobFailurePolicy, None] = None,
        **kwargs
    ) -> Session:
        if self.current_session:
            raise AlreadyHasASessionError(session.target.current_session.id)

        session = Session(session_details=session_details,
                          session_id=session_id,
                          session_name=session_name,
                          job_failure_policy=job_failure_policy,
                          workspace=self._get_azure_workspace(),
                          target=self._get_azure_target_id(),
                          **kwargs)
        self.current_session = session
        return session.start()
