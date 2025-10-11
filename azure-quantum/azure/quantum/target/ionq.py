##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict, List
from warnings import warn

from azure.quantum.job.job import Job
from azure.quantum.target.target import Target
from azure.quantum.workspace import Workspace
from typing import Union


def int_to_bitstring(k: int, num_qubits: int, measured_qubit_ids: List[int]):
    # flip bitstring to convert to little Endian
    bitstring = format(int(k), f"0{num_qubits}b")[::-1]
    # flip bitstring to convert back to big Endian
    return "".join([bitstring[n] for n in measured_qubit_ids])[::-1]


class IonQ(Target):
    """IonQ target."""
    target_names = (
        "ionq.simulator",
        "ionq.qpu.aria-1",
        "ionq.qpu.forte-1",
        "ionq.qpu.forte-enterprise-1",
    )

    _SHOTS_PARAM_NAME = "shots"

    def __init__(
        self,
        workspace: Workspace,
        name: str = "ionq.simulator",
        input_data_format: str = "ionq.circuit.v1",
        output_data_format: str = "ionq.quantum-results.v1",
        capability: str = "",
        provider_id: str = "IonQ",
        content_type: str = "application/json",
        encoding: str = "",
        target_profile: Union[str, "TargetProfile"] = "Base",
        **kwargs,
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
            **kwargs,
        )

    def submit(
        self,
        circuit: Dict[str, Any] = None,
        name: str = "ionq-job",
        shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format (for examples,
            see: https://docs.ionq.com/#section/Sample-JSON-Circuits)
        :type circuit: Dict[str, Any]
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
