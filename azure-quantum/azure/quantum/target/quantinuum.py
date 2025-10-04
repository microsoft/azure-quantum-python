##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import Any, Dict, Union
from warnings import warn

from azure.quantum.job.job import Job
from azure.quantum.target.target import Target
from azure.quantum.workspace import Workspace


class Quantinuum(Target):
    """Quantinuum target."""
    target_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.qpu.h2-1",
        "quantinuum.sim.h2-1sc",
        "quantinuum.sim.h2-1e",
        "quantinuum.qpu.h2-2",
        "quantinuum.sim.h2-2sc",
        "quantinuum.sim.h2-2e",
    )

    _SHOTS_PARAM_NAME = "count"

    def __init__(
        self,
        workspace: Workspace,
        name: str = "quantinuum.sim.h2-1sc",
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        capability: str = "",
        provider_id: str = "quantinuum",
        content_type: str = "application/qasm",
        encoding: str = "",
        target_profile: Union[str, "TargetProfile"] = "Adaptive_RI",
        **kwargs
    ):
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
            content_type=content_type,
            encoding=encoding,
            target_profile=target_profile,
            **kwargs
        )

    def submit(
        self,
        circuit: str = None,
        name: str = "quantinuum-job",
        shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Quantinuum program (OpenQASM 2.0 format)

        :param circuit: Quantum circuit in Quantinuum OpenQASM 2.0 format
        :type circuit: str
        :param name: Job name
        :type name: str
        :param shots: Number of shots, defaults to None
        :type shots: int
        :param input_params: Optional input params dict
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        input_data = kwargs.pop("input_data", circuit)
        if input_data is None:
            raise ValueError(
                "Either the `circuit` parameter or the `input_data` parameter must have a value."
            )
        if input_params is None:
            input_params = {}

        return super().submit(
            input_data=input_data,
            name=name,
            shots=shots,
            input_params=input_params,
            **kwargs
        )
