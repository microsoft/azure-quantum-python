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

from dataclasses import dataclass
from enum import Enum
from typing import Union, Any, Dict, List, Optional

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
    ASPEN_M_2 = "rigetti.qpu.aspen-m-2"
    ASPEN_M_3 = "rigetti.qpu.aspen-m-3"
    ANKAA_@ = "rigetti.qpu.ankaa-2"

    def simulators() -> List[str]:
        """Returns a list of simulator targets"""
        return [
            RigettiTarget.QVM.value,
        ]

    def qpus() -> List[str]:
        """Returns a list of QPU targets"""
        return [
            RigettiTarget.ASPEN_11.value,
            RigettiTarget.ASPEN_M_2.value,
            RigettiTarget.ASPEN_M_3.value,
            RigettiTarget.ANKAA_2.value,
        ]

    def num_qubits(target_name) -> int:
        """Returns the number of qubits supported by the given target"""
        if target_name == RigettiTarget.QVM.value:
            return 20
        elif target_name == RigettiTarget.ASPEN_11.value:
            return 38
        elif target_name == RigettiTarget.ASPEN_M_2.value:
            return 80
        elif target_name == RigettiTarget.ASPEN_M_3.value:
            return 80
        elif target_name == RigettiTarget.ANKAA_2.value:
            return 84
        else:
            raise ValueError(f"Unknown target {target_name}")


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

    substitutions: Optional[Dict[str, List[List[float]]]] = None
    """A dictionary of memory region names to the list of value vectors to write to that region.
    
    For example, a job with this Quil program:
    
    .. code-block::
        
        DECLARE ro BIT[2]
        DECLARE theta REAL[2]
        DECLARE beta REAL[1]
        RX(theta[0]) 0
        RX(theta[1]) 1
        RX(beta) 2
        MEASURE 0 ro[0]
        MEASURE 1 ro[1]
        MEASURE 2 ro[2]
    
    might be run with 
    
    .. highlight:: python
    .. code-block::
    
        InputParams(
            substitutions={
                "theta": [
                    [0.0, np.pi],
                    [np.pi, 0.0],
                ],
                "beta": [
                    [2 * np.pi],
                    [2 * np.pi],
                ]
            },
            count=2,
        )
        
    The resulting job will be run for each set of parameters in the list. So in the first run, theta[0] will be set to 
    0.0, theta[1] will be set to np.pi, and beta will be set to 2 * np.pi. Each run is executed for ``count`` 
    shots, so you'd expect a result like ``{"ro": [[0, 1, 0], [0, 1, 0], [1, 0, 0], [1, 0, 0]]} for a total of 4 
    measurement vectors.
    
    Note that the length of the inner list must equal the length of the memory region—that's the ``2`` in 
    ``DECLARE theta REAL[2]``. 
    
    The length of the (outer) list comprising substitution vectors for each region must be equal. So 
    if you are passing two sets of parameters to ``theta`` (list of length two) and you have another region named 
    ``beta``, then ``beta`` must also be a list of length two. 
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
        **kwargs,
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type="text/plain",
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
        :param input_params: Input parameters, see :class:`azure.quantum.target.rigetti.InputParams` for details.
        :type input_params: Union[InputParams, None, Dict[str, Any]]
        :return: Azure Quantum job
        :rtype: Job
        """
        if isinstance(input_params, InputParams):
            typed_input_params = input_params
            input_params = {
                "count": typed_input_params.count,
                "skipQuilc": typed_input_params.skip_quilc,
            }
            if typed_input_params.substitutions is not None:
                input_params["substitutions"] = typed_input_params.substitutions

        return super().submit(input_data, name, input_params, **kwargs)
