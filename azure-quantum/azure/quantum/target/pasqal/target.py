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
    runs: int = 1
    """The number of times to run the experiment."""


class Pasqal(Target):
    """Pasqal target, defaults to the simulator PasqalTarget.SIM_EMU_TN

    In order to process the results of a Quil input to this target, we recommend using the included Result class.
    """

    target_names = tuple(target.value for target in PasqalTarget)

    def __init__(
        self,
        workspace: Workspace,
        name: Union[PasqalTarget, str] = PasqalTarget.SIM_EMU_TN,
        input_data_format: str = "pasqal.pulser.v1",
        output_data_format: str = "pasqal.pulser-results.v1",
        capability: str = "BasicExecution",
        provider_id: str = "pasqal",
        encoding: str = "",
        **kwargs,
    ):
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
        :param input_params: Input parameters, see :class:`azure.quantum.target.pasqal.InputParams` for details.
        :type input_params: Union[InputParams, None, Dict[str, Any]]
        :return: Azure Quantum job
        :rtype: Job
        """
        if isinstance(input_params, InputParams):
            typed_input_params = input_params
            input_params = {
                "runs": typed_input_params.runs,
            }

        return super().submit(input_data, name, input_params, **kwargs)
