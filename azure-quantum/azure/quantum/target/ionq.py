##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
import json

from typing import Any, Dict, Union

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace
from azure.quantum.plugins.cirq import (
    _is_cirq_circuit,
    translate_ionq_circuit
)

# Circuit type accepted by IonQ.submit
# if it is not installed, only accept JSON dict
try:
    from cirq.circuits import Circuit as CirqCircuit
    Circuit = Union[Dict[str, Any], CirqCircuit]
except ImportError:
    Circuit = Dict[str, Any]


class IonQ(Target):
    """IonQ target."""

    def __init__(
        self,
        workspace: Workspace,
        target: str = "ionq.simulator",
        input_data_format: str = "ionq.circuit.v1",
        output_data_format: str = "ionq.quantum-results.v1",
        provider_id: str = "IonQ",
        content_type: str = "application/json",
        encoding: str = ""
    ):
        super().__init__(
            workspace=workspace,
            target=target,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding
        )

    @staticmethod
    def _encode_input_data(data: Dict[Any, Any]) -> bytes:
        stream = io.BytesIO()
        data = json.dumps(data)
        stream.write(data.encode())
        return stream.getvalue()
    
    @staticmethod
    def _is_ionq_circuit(circuit: Any):
        return isinstance(circuit, dict) and "circuit" in circuit
    
    @classmethod
    def _translate_circuit(cls, circuit: Any):
        """Translate circuit into IonQ JSON format"""
        if cls._is_ionq_circuit(circuit):
            return circuit
        elif _is_cirq_circuit(circuit):
            try:
                return translate_ionq_circuit(circuit)
            except Exception as e:
                raise ValueError(
                    f"Cannot translate circuit of type {circuit.__class__}: {e}")
        else:
            raise ValueError(f"Circuit of type {circuit.__class__} is not supported. \
Please provide IonQ JSON as described in: https://ionq.com/docs.")

    def submit(
        self,
        circuit: Circuit,
        name: str = "ionq-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format
        :type circuit: Union[Dict[str, Any], CirqCircuit]
        :param name: Job name
        :type name: str
        :param num_shots: Number of shots, defaults to None
        :type num_shots: int
        :param input_params: Optional input params dict
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        if input_params is None:
            input_params = {}
        if num_shots is not None:
            input_params = input_params.copy()
            input_params["shots"] = num_shots

        # Translate circuit to IonQ JSON format if needed
        circuit = self._translate_circuit(circuit)

        return super().submit(
            input_data=circuit,
            name=name,
            input_params=input_params,
            **kwargs
        )
