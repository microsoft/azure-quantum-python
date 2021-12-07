##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

# %% Get all one-qubit and two-qubit gates
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from qiskit import QuantumCircuit


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
    "cnot",	# Convenient alias for controlled-not gate
    "xx",	# Ising XX gate: e^(-iθ X⊗X /2)
    "yy",	# Ising YY gate: e^(-iθ Y⊗Y /2)
    "zz",	# Ising ZZ gate: e^(-iθ Z⊗Z /2)
    "swap",	# Swaps two qubits
]


def is_1q_gate(gate: Dict[str, Any]):
    return gate.get("gate") in GATES_1Q


def is_multi_q_gate(gate):
    return gate.get("gate") in GATES_MULTI


def num_2q_gates(gate):
    controls = gate.get("controls")
    if controls is None:
        # Only one control qubit
        return 1
    # Multiple control qubits
    return 6 * (len(controls) - 2)


def estimate_cost_ionq(
    circuit: Dict[str, Any],
    num_shots: int,
    cost_1q: float=0.00003,
    cost_2q: float=0.0003
) -> float:
    """Estimate the costs of running a circuit on IonQ.

    :param circuit: IonQ JSON circuit
    :type circuit: Dict[str, Any]
    :param num_shots: Number of shots
    :type num_shots: int
    :param cost_1q: Cost for a single qubit gate-shot, defaults to 0.00003
    :type cost_1q: float, optional
    :param cost_2q: Cost for a double qubit gate-shot, defaults to 0.0003
    :type cost_2q: float, optional
    :return: Calculate the cost for running the circuit
    :rtype: float
    """
    gates = circuit.get("circuit", [])
    N_1q = sum(map(is_1q_gate, gates))
    N_2q = sum(map(num_2q_gates, filter(is_multi_q_gate, gates)))
    cost = (cost_1q * N_1q + cost_2q * N_2q) * num_shots
    return max(cost, 1.0)


def estimate_cost_ionq_qiskit(circuit: "QuantumCircuit", num_shots: int):
    """
    Estimate costs for a qiskit circuit
    """
    import json
    from qiskit_ionq.helpers import qiskit_circ_to_ionq_circ

    ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit)
    input_data = json.dumps({
        "qubits": circuit.num_qubits,
        "circuit": ionq_circ,
    })
    estimate_cost_ionq(circuit=input_data, num_shots=num_shots)


if __name__ == "__main__":
    test_circuit = {
        "qubits": 3,
        "circuit": [
            {
            "gate": "h",
            "target": 0
            },
            {
            "gate": "cnot",
            "control": 0,
            "target": 1
            },
            {
            "gate": "cnot",
            "control": 0,
            "target": 2
            },
        ]
    }

    cost = estimate_cost_ionq(circuit=test_circuit, num_shots=1024)
    print(f"Estimated cost: ${cost}")
