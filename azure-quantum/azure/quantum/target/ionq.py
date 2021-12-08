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


class IonQ(Target):
    """IonQ target."""
    target_names = (
        "ionq.qpu",
        "ionq.simulator",
    )

    # Get all one-qubit, two-qubit gates
    GATES_1Q = [
        "x",	# Pauli X gate
        "y",	# Pauli Y gate
        "z",	# Pauli Z gate
        "rx",	# X-axis rotation
        "ry",	# Y-axis rotation
        "rz",	# Z-axis rotation
        "h",	# Hadamard gate
        "not",	# Convenient alias for Pauli-X gate
        "s",	# S gate
        "si",	# Conjugate transpose of S gate
        "t",	# T gate
        "ti",	# Conjugate transpose of T gate
        "v",	# Square root of not gate
        "vi",	# Conjugate transpose of square-root-of-not gate
    ]


    GATES_MULTI = [
        "x",	# Pauli X gate
        "y",	# Pauli Y gate
        "z",	# Pauli Z gate
        "cnot",	# Convenient alias for controlled-not gate
        "xx",	# Ising XX gate: e^(-iθ X⊗X /2)
        "yy",	# Ising YY gate: e^(-iθ Y⊗Y /2)
        "zz",	# Ising ZZ gate: e^(-iθ Z⊗Z /2)
        "swap",	# Swaps two qubits
    ]

    def __init__(
        self,
        workspace: Workspace,
        name: str = "ionq.simulator",
        input_data_format: str = "ionq.circuit.v1",
        output_data_format: str = "ionq.quantum-results.v1",
        provider_id: str = "IonQ",
        content_type: str = "application/json",
        encoding: str = "",
        **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding,
            **kwargs
        )

    @staticmethod
    def _encode_input_data(data: Dict[Any, Any]) -> bytes:
        stream = io.BytesIO()
        data = json.dumps(data)
        stream.write(data.encode())
        return stream.getvalue()

    def submit(
        self,
        circuit: Dict[str, Any],
        name: str = "ionq-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format (for examples,
            see: https://docs.ionq.com/#section/Sample-JSON-Circuits)
        :type circuit: Dict[str, Any]
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

        return super().submit(
            input_data=circuit,
            name=name,
            input_params=input_params,
            **kwargs
        )

    def estimate_price(
        self,
        circuit: Dict[str, Any],
        num_shots: int,
        price_1q: float=0.00003,
        price_2q: float=0.0003,
        min_price: float=1.0
    ) -> float:
        """Estimate the price of submittng a circuit to IonQ targets.
        Optionally, you can provide the number of gate and measurement operations
        manually.
        The actual price charged by the provider may differ from this calculation.
        
        Specify pricing details for your area to get most accurate results.
        By default, this function charges price_1q=0.00003 USD for a single-qubit gate,
        price_2q=0.0003 USD for a two-qubit gate with a total minimum price of $1.-
        per circuit.

        For the most current pricing details, see
        https://docs.microsoft.com/en-us/azure/quantum/provider-ionq#pricing
        Or find your workspace and view pricing options in the "Provider" tab
        of your workspace: http://aka.ms/aq/myworkspaces

        :param circuit: Quantum circuit in IonQ JSON format (for examples,
            see: https://docs.ionq.com/#section/Sample-JSON-Circuits)
        :type circuit: Dict[str, Any]
        :param num_shots: Number of shots, defaults to None
        :type num_shots: int
        :param price_1q: The price of running a single-qubit gate
            for one shot, defaults to 0.00003
        :type price_1q: float, optional
        :param price_2q: The price of running a double-qubit gate
            for one shot, defaults to 0.0003
        :type price_2q: float, optional
        :param min_price: The minimum price for running a job, defaults to 1.0
        :type min_price: float, optional
        """
        if self.name == "ionq.simulator": 
            return 0.0

        def is_1q_gate(gate: Dict[str, Any]):
            return gate.get("gate") in self.GATES_1Q and (
                "controls" not in gate and "control" not in gate
            )

        def is_multi_q_gate(gate):
            return gate.get("gate") in self.GATES_MULTI and (
                "controls" in gate or "control" in gate
            )

        def num_2q_gates(gate):
            controls = gate.get("controls")
            if controls is None or len(controls) == 1:
                # Only one control qubit
                return 1
            # Multiple control qubits
            return 6 * (len(controls) - 2)

        gates = circuit.get("circuit", [])
        N_1q = sum(map(is_1q_gate, gates))
        N_2q = sum(map(num_2q_gates, filter(is_multi_q_gate, gates)))
        price = (price_1q * N_1q + price_2q * N_2q) * num_shots

        return max(price, min_price)
