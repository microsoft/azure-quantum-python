##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Any, Dict, Union, Optional
import io
import json

from azure.quantum._client.models import TargetStatus, SessionDetails
from azure.quantum._client.models._enums import SessionJobFailurePolicy
from azure.quantum.job.job import Job
from azure.quantum.job.session import Session
from azure.quantum.job.base_job import ContentType
if TYPE_CHECKING:
    from azure.quantum import Workspace

class TargetAlreadyHasASessionError(Exception):
    """Exception raised when trying to start a new session `target.start_session()`
       and the current target instance already has a session associated with it.
    
    Attributes:
        session_id -- the id of the existing session associated with the current target instance
    """

    def __init__(self, session_id):
        self.message = f"""The current target instance already has a session ({session_id}) associated with it. 
                           If you want to start a new session, you should obtain a new target instance.
                           A new target instance can be obtained with `workspace.get_targets("provider_id.target_name")`
                           Qiskit: `target` is the same concept as a Qiskit `backend`. It can be obtained with `provider.get_backend("provider_id.target_name")`.
                           Cirq: a new target instance can be obtained with `service.get_target("provider_id.target_name")`.
                           """
        super().__init__(self.message)


class Target:
    """Azure Quantum Target."""
    # Target IDs that are compatible with this Target class.
    # This variable is used by TargetFactory. To set the default
    # target class for a given provider, specify the
    # default_targets constructor argument.
    target_names = ()

    def __init__(
        self,
        workspace: "Workspace",
        name: str,
        input_data_format: str = "",
        output_data_format: str = "",
        provider_id: str = "",
        content_type: ContentType = ContentType.json,
        encoding: str = "",
        average_queue_time: float = None,
        current_availability: str = ""
    ):
        if not provider_id and "." in name:
            provider_id = name.split(".")[0]
        self.workspace = workspace
        self.name = name
        self.input_data_format = input_data_format
        self.output_data_format = output_data_format
        self.provider_id = provider_id
        self.content_type = content_type
        self.encoding = encoding
        self._average_queue_time = average_queue_time
        self._current_availability = current_availability
        self.current_session: Session = None

    def __repr__(self):
        return f"<Target name=\"{self.name}\", \
avg. queue time={self._average_queue_time} s, {self._current_availability}>"

    @classmethod
    def from_target_status(
        cls, workspace: "Workspace", status: TargetStatus, **kwargs
    ):
        """Create a Target instance from a given workspace and target status.

        :param workspace: Associated workspace
        :type workspace: Workspace
        :param status: Target status with availability and current queue time
        :type status: TargetStatus
        :return: Target instance
        :rtype: Target
        """
        return cls(
            workspace=workspace,
            name=status.id,
            average_queue_time=status.average_queue_time,
            current_availability=status.current_availability,
            **kwargs
        )
    
    def refresh(self):
        """Update the target availability and queue time"""
        targets = self.workspace._get_target_status(self.name, self.provider_id)
        if len(targets) > 0:
            _, target_status = targets[0]
            self._current_availability = target_status.current_availability
            self._average_queue_time = target_status.average_queue_time
        else:
            raise ValueError(
                f"Cannot refresh the Target status: \
target '{self.name}' of provider '{self.provider_id}' not found."
            )

    @property
    def current_availability(self):
        return self._current_availability
    
    @property
    def average_queue_time(self):
        return self._average_queue_time

    @staticmethod
    def _encode_input_data(data: Any) -> bytes:
        """Encode input data to bytes.
        If the data is already in bytes format, return it.

        :param data: Input data
        :type data: Any
        :return: Encoded input data
        :rtype: bytes
        """
        if isinstance(data, bytes):
            return data
        else:
            stream = io.BytesIO()
            if isinstance(data, dict):
                data = json.dumps(data)
            stream.write(data.encode())
            return stream.getvalue()

    def submit(
        self,
        input_data: Any,
        name: str = "azure-quantum-job",
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit input data and return Job.

        Provide input_data_format, output_data_format and content_type
        keyword arguments to override default values.

        :param input_data: Input data
        :type input_data: Any
        :param name: Job name
        :type name: str
        :param input_params: Input parameters
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        input_params = input_params or {}
        input_data_format = kwargs.pop("input_data_format", self.input_data_format)
        output_data_format = kwargs.pop("output_data_format", self.output_data_format)
        content_type = kwargs.pop("content_type", self.content_type)
        encoding = kwargs.pop("encoding", self.encoding)
        blob = self._encode_input_data(data=input_data)
        return Job.from_input_data(
            workspace=self.workspace,
            name=name,
            target=self.name,
            input_data=blob,
            content_type=content_type,
            encoding=encoding,
            provider_id=self.provider_id,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            input_params=input_params,
            session_id=self.get_current_session_id(),
            **kwargs
        )

    def supports_protobuf(self):
        """
        Return whether or not the Solver class supports protobuf serialization.
        This should be overridden by Solver subclasses which do support protobuf.
        """
        return False
    
    def estimate_cost(
        self,
        input_data: Any,
        input_params: Dict[str, Any] = None
    ):
        return NotImplementedError("Price estimation is not implemented yet for this target.")

    def get_current_session_id(self) -> Optional[str]:
        return self.current_session.id if self.current_session else None

    def start_session(
        self,
        session_details: Optional[SessionDetails] = None,
        session_id: Optional[str] = None,
        session_name: Optional[str] = None,
        job_failure_policy: Union[str, SessionJobFailurePolicy, None] = None,
        **kwargs
    ) -> Session:
        session = Session(session_details=session_details,
                          session_id=session_id,
                          session_name=session_name,
                          job_failure_policy=job_failure_policy,
                          target=self,
                          workspace=self.workspace,
                          **kwargs)
        return session.start()
