##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, Type,  Protocol, runtime_checkable
from dataclasses import dataclass
import io
import json
import abc
import warnings

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

@dataclass
class GateStats:
    one_qubit_gates: int
    multi_qubit_gates: int
    measurement_gates: int

    def __iter__(self):
        return iter((self.one_qubit_gates, self.multi_qubit_gates, self.measurement_gates))

class Target(abc.ABC, SessionHost):

    _QSHARP_USER_AGENT = "azure-quantum-qsharp"

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
    """Tuple of target names."""

    # Name of the provider's input parameter which specifies number of shots for a submitted job.
    # If None, target will not pass this input parameter. 
    _SHOTS_PARAM_NAME = None

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

        :param workspace: Associated workspace
        :type workspace: Workspace
        :param name: Target name
        :type name: str
        :param input_data_format: Format of input data (ex. "qir.v1")
        :type input_data_format: str
        :param output_data_format: Format of output data (ex. "microsoft.resource-estimates.v1")
        :type output_data_format: str
        :param capability: QIR capability
        :type capability: str
        :param provider_id: Id of provider (ex. "microsoft-qc")
        :type provider_id: str
        :param content_type: "Content-Type" attribute value to set on input blob (ex. "application/json")
        :type content_type: azure.quantum.job.ContentType
        :param encoding: "Content-Encoding" attribute value to set on input blob (ex. "gzip")
        :type encoding: str
        :param average_queue_time: Set average queue time (for internal use)
        :type average_queue_time: float
        :param current_availability: Set current availability (for internal use)
        :type current_availability: str
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
    
    @classmethod
    def _can_send_shots_input_param(cls) -> bool:
        """
        Tells if provider's target class is able to specify shots number for its jobs.
        """
        return cls._SHOTS_PARAM_NAME is not None

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
        """
        Current availability.
        """

        return self._current_availability

    @property
    def average_queue_time(self):
        """
        Average queue time.
        """
        
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
        return "microsoft.quantum-results.v2"

    def submit(
        self,
        input_data: Any,
        name: str = "azure-quantum-job",
        shots: int = None,
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
        :param shots: Number of shots, defaults to None
        :type shots: int
        :param input_params: Input parameters
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: azure.quantum.job.Job
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
            # setting UserAgent header to indicate Q# submission
            # TODO: this is a temporary solution. We should be setting the User-Agent header
            # on per-job basis as targets of different types could be submitted using the same Workspace object
            self.workspace.append_user_agent(self._QSHARP_USER_AGENT)

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
            # re-setting UserAgent header to None for passthrough
            self.workspace.append_user_agent(None)
        
        # Set shots number, if possible.
        if self._can_send_shots_input_param():
            input_params_shots = input_params.pop(self.__class__._SHOTS_PARAM_NAME, None)

            # If there is a parameter conflict, choose 'shots'.
            if shots is not None and input_params_shots is not None:
                warnings.warn(
                    f"Parameter 'shots' conflicts with the '{self.__class__._SHOTS_PARAM_NAME}' field of the 'input_params' "
                    "parameter. Please, provide only one option for setting shots. Defaulting to 'shots' parameter."
                )
                final_shots = shots
            
            # The 'shots' parameter has highest priority.
            elif shots is not None:
                final_shots = shots
            # if 'shots' parameter is not specified, try a provider-specific option.
            elif input_params_shots is not None:
                warnings.warn(
                    f"Field '{self.__class__._SHOTS_PARAM_NAME}' from the 'input_params' parameter is subject to change in future versions. "
                    "Please, use 'shots' parameter instead."
                )
                final_shots = input_params_shots
            else:
                final_shots = None
            
            if final_shots is not None:
                input_params[self.__class__._SHOTS_PARAM_NAME] = final_shots

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

    def _get_azure_workspace(self) -> "Workspace":
        return self.workspace

    def _get_azure_target_id(self) -> str:
        return self.name

    def _get_azure_provider_id(self) -> str:
        return self.provider_id

    @classmethod
    def _calculate_qir_module_gate_stats(self, qir_module) -> GateStats:
        try:
            from pyqir import Module, is_qubit_type, is_result_type, entry_point, is_entry_point, Function

        except ImportError:
            raise ImportError(
                "Missing optional 'qiskit' dependencies. \
        To install run: pip install azure-quantum[qiskit]"
            )
        
        module: Module = qir_module

        one_qubit_gates = 0
        multi_qubit_gates = 0
        measurement_gates = 0

        function_entry_points: list[Function] = filter(is_entry_point, module.functions)
        
        # Iterate over the blocks and their instructions
        for function in function_entry_points:
            for block in function.basic_blocks:
                for instruction in block.instructions:
                    qubit_count = 0
                    result_count = 0
                    
                    # If the instruction is of type quantum rt, do not include this is the price calculation
                    if len(instruction.operands) > 0 and "__quantum__rt" not in instruction.operands[-1].name:
                        # Check each operand in the instruction
                        for operand in instruction.operands:
                            value_type = operand.type
                            
                            if is_qubit_type(value_type):
                                qubit_count += 1
                            elif is_result_type(value_type):
                                result_count += 1

                    # Determine the type of gate based on the counts
                    if qubit_count == 1 and result_count == 0:
                        one_qubit_gates += 1
                    if qubit_count >= 2 and result_count == 0:
                        multi_qubit_gates += 1
                    if result_count > 0:
                        measurement_gates += 1

        return GateStats (
            one_qubit_gates, 
            multi_qubit_gates, 
            measurement_gates
        )


def _determine_shots_or_deprecated_num_shots(
    shots: int = None,
    num_shots: int = None,
) -> int:
    """
    This helper function checks if the deprecated 'num_shots' parameter is specified.
    In earlier versions it was possible to pass this parameter to specify shots number for a job,
    but now we only check for it for compatibility reasons.  
    """
    final_shots = None
    if shots is not None and num_shots is not None:
        warnings.warn(
            "Both 'shots' and 'num_shots' parameters were specified. Defaulting to 'shots' parameter. "
            "Please, use 'shots' since 'num_shots' will be deprecated.",
            category=DeprecationWarning,
        )
        final_shots = shots
        
    elif shots is not None:
        final_shots = shots
    elif num_shots is not None:
        warnings.warn(
            "The 'num_shots' parameter will be deprecated. Please, use 'shots' parameter instead.",
            category=DeprecationWarning,
        )
        final_shots = num_shots

    return final_shots