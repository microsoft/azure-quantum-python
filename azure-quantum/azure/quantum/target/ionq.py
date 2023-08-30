##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict, List

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace
from azure.quantum._client.models import CostEstimate, UsageEvent

COST_1QUBIT_GATE_MAP = {
    "ionq.simulator" : 0.0,
    "ionq.qpu" : 0.00003,
    "ionq.qpu.aria-1" : 0.0002205
}

COST_2QUBIT_GATE_MAP = {
    "ionq.simulator" : 0.0,
    "ionq.qpu" : 0.0003,
    "ionq.qpu.aria-1" : 0.00098
}

MIN_PRICE_MAP = {
    "ionq.simulator" : 0.0,
    "ionq.qpu" : 1.0,
    "ionq.qpu.aria-1" : 97.5
}

def int_to_bitstring(k: int, num_qubits: int, measured_qubit_ids: List[int]):
    # flip bitstring to convert to little Endian
    bitstring = format(int(k), f"0{num_qubits}b")[::-1]
    # flip bitstring to convert back to big Endian
    return "".join([bitstring[n] for n in measured_qubit_ids])[::-1]


class IonQ(Target):
    """IonQ target."""
    target_names = (
        "ionq.qpu",
        "ionq.simulator",
        "ionq.qpu.aria-1"
    )

    def __init__(
        self,
        workspace: Workspace,
        name: str = "ionq.simulator",
        input_data_format: str = "ionq.circuit.v1",
        output_data_format: str = "ionq.quantum-results.v1",
        capability: str = "BasicExecution",
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
            capability=capability,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding,
            **kwargs
        )

    def submit(
        self,
        circuit: Dict[str, Any] = None,
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
        input_data = kwargs.pop("input_data", circuit)
        if input_data is None:
            raise ValueError(
                "Either the `circuit` parameter or the `input_data` parameter must have a value."
            )
        if input_params is None:
            input_params = {}
        if num_shots is not None:
            input_params = input_params.copy()
            input_params["shots"] = num_shots

        return super().submit(
            input_data=input_data,
            name=name,
            input_params=input_params,
            **kwargs
        )

    def estimate_cost(
        self,
        circuit: Dict[str, Any],
        num_shots: int,
        price_1q: float = None,
        price_2q: float = None,
        min_price: float = None
    ) -> CostEstimate:
        """Estimate the cost of submitting a circuit to IonQ targets.
        Optionally, you can provide the number of gate and measurement operations
        manually.
        The actual price charged by the provider may differ from this calculation.
        
        Specify pricing details for your area to get most accurate results.
        By default, this function charges depending on the target:
            ionq.qpu:
                price_1q = 0.00003 USD for a single-qubit gate.
                price_2q = 0.0003  USD for a two-qubit gate.
                min_price = 1 USD, total minimum price per circuit.
            ionq.qpu.aria-1:
                price_1q = 0.00022 USD for a single-qubit gate.
                price_2q = 0.00098 USD for a two-qubit gate.
                min_price = 1 USD, total minimum price per circuit.

        For the most current pricing details, see
        https://docs.microsoft.com/azure/quantum/provider-ionq#pricing
        Or find your workspace and view pricing options in the "Provider" tab
        of your workspace: https://aka.ms/aq/myworkspaces

        :param circuit: Quantum circuit in IonQ JSON format (for examples,
            see: https://docs.ionq.com/#section/Sample-JSON-Circuits)
        :type circuit: Dict[str, Any]
        :param num_shots: Number of shots, defaults to None
        :type num_shots: int
        :param price_1q: The price of running a single-qubit gate
            for one shot.
        :type price_1q: float, optional
        :param price_2q: The price of running a double-qubit gate
            for one shot.
        :type price_2q: float, optional
        :param min_price: The minimum price for running a job.
        :type min_price: float, optional
        """
        def is_1q_gate(gate: Dict[str, Any]):
            return "controls" not in gate and "control" not in gate

        def is_multi_q_gate(gate):
            return "controls" in gate or "control" in gate

        def num_2q_gates(gate):
            controls = gate.get("controls")
            if controls is None or len(controls) == 1:
                # Only one control qubit
                return 1
            # Multiple control qubits
            return 6 * (len(controls) - 2)

        # Get the costs for the gates depending on the provider if not specified
        if price_1q is None:
            price_1q = COST_1QUBIT_GATE_MAP[self.name]

        if price_2q is None:
            price_2q = COST_2QUBIT_GATE_MAP[self.name]

        if min_price is None:
            min_price = MIN_PRICE_MAP[self.name]

        gates = circuit.get("circuit", [])
        N_1q = sum(map(is_1q_gate, gates))
        N_2q = sum(map(num_2q_gates, filter(is_multi_q_gate, gates)))

        price = (price_1q * N_1q + price_2q * N_2q) * num_shots
        price = max(price, min_price)

        return CostEstimate(
            events = [
                UsageEvent(
                    dimension_id="gs1q",
                    dimension_name="1Q Gate Shot",
                    measure_unit="1q gate shot",
                    amount_billed=0.0,
                    amount_consumed=N_1q * num_shots,
                    unit_price=0.0
                ),
                UsageEvent(
                    dimension_id="gs2q",
                    dimension_name="2Q Gate Shot",
                    measure_unit="2q gate shot",
                    amount_billed=0.0,
                    amount_consumed=N_2q * num_shots,
                    unit_price=0.0
                )
            ],
            currency_code="USD",
            estimated_total=price
        )
