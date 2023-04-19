##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Any, Dict, Optional, Union, Type,  Protocol, runtime_checkable
import io
import json
import abc

from azure.quantum._client.models import TargetStatus, SessionDetails
from azure.quantum._client.models._enums import SessionJobFailurePolicy
from azure.quantum.job.job import Job, BaseJob
from azure.quantum.job.session import Session, SessionHost
from azure.quantum.job.base_job import ContentType
from azure.quantum.target.params import InputParams
if TYPE_CHECKING:
    from azure.quantum import Workspace


@runtime_checkable
class QirRepresentable(Protocol):
    _name: str

    @abc.abstractmethod
    def _repr_qir_(self, **kwargs: Any) -> bytes:
        raise NotImplementedError


class Target(abc.ABC, SessionHost):
    """Azure Quantum Target."""
    # Target IDs that are compatible with this Target class.
    # This variable is used by TargetFactory. To set the default
    # target class for a given provider, specify the
    # default_targets constructor argument.
    #
    # If you provide a custom job class (derived from
    # azurem.quantum.job.job.Job) for this target, you must pass this type to
    # __init__ via the job_cls parameter.  This is then used by the target's
    # submit and get_job method.
    target_names = ()

    def __init__(
        self,
        workspace: "Workspace",
        name: str,
        input_data_format: str = "",
        output_data_format: str = "",
        capability: str = "",
        provider_id: str = "",
        content_type: ContentType = ContentType.json,
        encoding: str = "",
        average_queue_time: Union[float, None] = None,
        current_availability: str = ""
    ):
        """
        Initializes a new target.
        """
        if not provider_id and "." in name:
            provider_id = name.split(".")[0]
        self.workspace = workspace
        self.name = name
        self.input_data_format = input_data_format
        self.output_data_format = output_data_format
        self.capability = capability
        self.provider_id = provider_id
        self.content_type = content_type
        self.encoding = encoding
        self._average_queue_time = average_queue_time
        self._current_availability = current_availability

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

    @classmethod
    def _get_job_class(cls) -> Type[Job]:
        """
        Returns the job class associated to this target.

        The job class used by submit and get_job.  The default is Job.
        """
        return Job

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
        
    def _qir_output_data_format(self) -> str:
        """"Fallback output data format in case of QIR job submission."""
        return "microsoft.quantum-results.v1"

    def submit(
        self,
        input_data: Any,
        name: str = "azure-quantum-job",
        input_params: Union[Dict[str, Any], InputParams, None] = None,
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

        if isinstance(input_params, InputParams):
            input_params = input_params.as_dict()
        else:
            input_params = input_params or {}
        input_data_format = None
        output_data_format = None
        content_type = None

        # If the input_data is `QirRepresentable`
        # we need to convert it to QIR bitcode and set the necessary parameters for a QIR job.
        if input_data and isinstance(input_data, QirRepresentable):
            input_data_format = kwargs.pop("input_data_format", "qir.v1")
            output_data_format = kwargs.pop("output_data_format", self._qir_output_data_format())
            content_type = kwargs.pop("content_type", "qir.v1")

            def _get_entrypoint(input_data):
                # TODO: this method should be part of QirRepresentable protocol
                # and will later move to the QSharpCallable class in the qsharp package
                import re
                method_name = re.search(r"(?:^|\.)([^.]*)$", input_data._name).group(1)
                return f'ENTRYPOINT__{method_name}'

            input_params["entryPoint"] = input_params.get("entryPoint", _get_entrypoint(input_data))
            input_params["arguments"] = input_params.get("arguments", [])
            targetCapability = input_params.get("targetCapability", kwargs.pop("target_capability", self.capability))
            if targetCapability:
                input_params["targetCapability"] = targetCapability
            input_data = input_data._repr_qir_(target=self.name, target_capability=targetCapability)
        else:
            input_data_format = kwargs.pop("input_data_format", self.input_data_format)
            output_data_format = kwargs.pop("output_data_format", self.output_data_format)
            content_type = kwargs.pop("content_type", self.content_type)

        encoding = kwargs.pop("encoding", self.encoding)
        blob = self._encode_input_data(data=input_data)
        job_cls = type(self)._get_job_class()
        return job_cls.from_input_data(
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
            session_id=self.get_latest_session_id(),
            **kwargs
        )

    def make_params(self):
        """
        Returns an input parameter object for convenient creation of input
        parameters.
        """
        return InputParams()

    def supports_protobuf(self):
        """
        Return whether or not the Solver class supports protobuf serialization.
        This should be overridden by Solver subclasses which do support protobuf.
        """
        return False
    
    def estimate_cost(
        self,
        input_data: Any,
        input_params: Union[Dict[str, Any], None] = None
    ):
        return NotImplementedError("Price estimation is not implemented yet for this target.")

    def _get_azure_workspace(self) -> "Workspace":
        return self.workspace

    def _get_azure_target_id(self) -> str:
        return self.name
