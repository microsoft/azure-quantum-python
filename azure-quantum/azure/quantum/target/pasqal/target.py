"""Defines targets and helper functions for the Pasqal provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "InputParams",
    "Pasqal",
    "PasqalTarget",
]

from dataclasses import dataclass
from enum import Enum
from typing import Union, Any, Dict, List, Optional

from ..target import Target
from ... import Job
from ...workspace import Workspace


class PasqalTarget(str, Enum):
    """The known targets for the Pasqal provider
    """

    SIM_EMU_TN = "pasqal.sim.emu-tn"
    """pasqal.sim.emu-tn target"""

    QPU_FRESNEL = "pasqal.qpu.fresnel"
    """A simulator target for Quil. See https://github.com/quil-lang/qvm for more info."""

    def simulators() -> List[str]:
        """Returns a list of simulator targets"""
        return [
            PasqalTarget.SIM_EMU_TN.value
        ]

    def qpus() -> List[str]:
        """Returns a list of QPU targets"""
        return [
            PasqalTarget.QPU_FRESNEL.value
        ]

    def num_qubits(target_name) -> int:
        """Returns the number of qubits supported by the given target"""
        if target_name == PasqalTarget.SIM_EMU_TN.value:
            return 100
        elif target_name == PasqalTarget.QPU_FRESNEL.value:
            return 20
        else:
            raise ValueError(f"Unknown target {target_name}")


@dataclass
class InputParams:
    """Input parameters

    Args:
        runs (int): The number of times to run the experiment.
    """

    runs: int = 1
    """The number of times to run the experiment."""


class Pasqal(Target):
    """Pasqal target, defaults to the simulator PasqalTarget.SIM_EMU_TN

    In order to process the results of a Quil input to this target, we recommend using the included Result class.
    """

    target_names = tuple(target.value for target in PasqalTarget)

    _SHOTS_PARAM_NAME = "count"

    def __init__(
        self,
        workspace: Workspace,
        name: Union[PasqalTarget, str] = PasqalTarget.SIM_EMU_TN,
        input_data_format: str = "pasqal.pulser.v1",
        output_data_format: str = "pasqal.pulser-results.v1",
        capability: str = "",
        provider_id: str = "pasqal",
        encoding: str = "",
        target_profile: Union[str, "TargetProfile"] = "Base",
        **kwargs,
    ):
        """
        Initializes a new target.

        :param workspace: Associated workspace
        :type workspace: Workspace
        :param name: Target name
        :type name: str
        :param input_data_format: Format of input data (ex. "pasqal.pulser.v1")
        :type input_data_format: str
        :param output_data_format: Format of output data (ex. "pasqal.pulser-results.v1")
        :type output_data_format: str
        :param capability: QIR capability
        :type capability: str
        :param provider_id: Id of provider (ex. "pasqal")
        :type provider_id: str
        :param encoding: "Content-Encoding" attribute value to set on input blob (ex. "gzip")
        :type encoding: str
        :param target_profile: Target QIR profile.
        :type target_profile: str | TargetProfile
        """
        if capability:
            msg = "The 'capability' parameter is not used for the Quantinuum target."
            warn(msg, DeprecationWarning)

        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            capability=capability,
            provider_id=provider_id,
            content_type="application/json",
            encoding=encoding,
            **kwargs,
        )

    def submit(
        self,
        input_data: Any,
        name: str = "azure-quantum-job",
        shots: int = None,
        input_params: Union[InputParams, None, Dict[str, Any]] = None,
        **kwargs,
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
        :param input_params: Input parameters, see :class:`azure.quantum.target.pasqal.InputParams` for details.
        :type input_params: Union[InputParams, None, Dict[str, Any]]
        :return: Azure Quantum job
        :rtype: Job
        """

        if isinstance(input_params, InputParams):
            typed_input_params = input_params
            input_params = {
                self.__class__._SHOTS_PARAM_NAME: typed_input_params.runs,
            }
        
        input_params = input_params or {}

        return super().submit(
            input_data=input_data, 
            name=name,
            shots=shots, 
            input_params=input_params, 
            **kwargs
        )
