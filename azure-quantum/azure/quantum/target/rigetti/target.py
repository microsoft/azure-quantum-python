"""Defines targets and helper functions for the Rigetti provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "InputParams",
    "Rigetti",
    "RigettiTarget",
]

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Union, Any, Dict

from ..target import Target
from ... import Job
from ...workspace import Workspace


class RigettiTarget(str, Enum):
    """The known targets for the Rigetti provider

    See https://qcs.rigetti.com/qpus for details on a QPU target.
    """

    QVM = "rigetti.sim.qvm"
    """A simulator target for Quil. See https://github.com/quil-lang/qvm for more info."""

    ASPEN_11 = "rigetti.qpu.aspen-11"
    ASPEN_M_1 = "rigetti.qpu.aspen-m-1"


@dataclass
class InputParams:
    count: int = 1
    """The number of times to run the experiment. 
    
    Will correspond to the length of each ``azure.quantum.target.rigetti.Readout``
    """

    skip_quilc: bool = False
    """If set to True, `quilc <https://github.com/quil-lang/quilc>`_ will not be run.
    
    This **must** be set true if using `Quil-T <https://pyquil-docs.rigetti.com/en/stable/quilt.html>`_.
    """


class Rigetti(Target):
    """Rigetti target, defaults to the simulator RigettiTarget.QVM

    In order to process the results of a Quil input to this target, we recommend using the included Result class.
    """

    target_names = tuple(target.value for target in RigettiTarget)

    def __init__(
            self,
            workspace: Workspace,
            name: Union[RigettiTarget, str] = RigettiTarget.QVM,
            input_data_format: str = "rigetti.quil.v1",
            output_data_format: str = "rigetti.quil-results.v1",
            provider_id: str = "rigetti",
            encoding: str = "",
            **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type="text/plain",
            encoding=encoding,
            **kwargs
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
        :param input_params: Input parameters, see :class:`azure.quantum.target.rigetti.InputParams` for details.
        :type input_params: Union[InputParams, None, Dict[str, Any]]
        :return: Azure Quantum job
        :rtype: Job
        """
        if isinstance(input_params, InputParams):
            input_params = {
                "count": input_params.count,
                "skipQuilc": input_params.skip_quilc,
            }
        return super().submit(input_data, name, input_params, **kwargs)
