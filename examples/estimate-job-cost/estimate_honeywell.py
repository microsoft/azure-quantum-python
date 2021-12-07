##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit.circuit.quantumcircuit import Qasm
from qiskit.converters import ast_to_dag
from qiskit import QuantumCircuit

# Get all one-qubit and two-qubit gates
GATES_1Q = [
    "x",
    "y",
    "z",
    "rx",
    "ry",
    "rz",
    "h",
    "s",
    "sdg",
    "t",
    "tdg",
    "v",
    "vdg",
]

GATES_MULTI = [
    "cx",
    "ccx",
    "cz",
    "zz",
]

GATES_M = [
    "measure",
    "reset"
]


def estimate_cost_honeywell(qasm_str: str, num_shots: int) -> float:
    """Estimate cost for QASM job on Honeywell

    :param qasm_str: QASM description
    :type qasm_str: str
    :param num_shots: Number of shots
    :type num_shots: int
    :return: Cost estimation
    :rtype: float
    """
    qasm = Qasm(data=qasm_str)
    ast = qasm.parse()
    dag = ast_to_dag(ast)
    ops = dag.count_ops()
    N_1q = sum([value for key, value in ops.items() if key in GATES_1Q])
    N_2q = sum([value for key, value in ops.items() if key in GATES_MULTI])
    N_m = sum([value for key, value in ops.items() if key in GATES_M])
    HQC = 5 + num_shots * (N_1q + 10 * N_2q + 5 * N_m) / 5000
    return HQC


def estimate_cost_honeywell_qiskit(circuit: QuantumCircuit, num_shots: int):
    """
    Estimate costs for a qiskit circuit
    """
    input_data = circuit.qasm()
    return estimate_cost_honeywell(input_data, num_shots)


if __name__ == "__main__":
    test_circuit = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[4];
    creg c[4];
    h q[0];
    h q[1];
    h q[2];
    h q[3];
    cx q[0],q[1];
    cx q[2],q[3];
    ry(2) q[0];
    cx q[1],q[0];
    measure q[0] -> c[0];
    measure q[1] -> c[1];
    measure q[2] -> c[2];
    measure q[3] -> c[3];"""

    cost = estimate_cost_honeywell(test_circuit, 1024)
    print(f"Estimated cost: HQC {cost}")

    circuit = QuantumCircuit(4, 4)
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)
    circuit.h(3)
    circuit.cx(0, 1)
    circuit.cx(2, 3)
    circuit.ry(2, 0)
    circuit.cx(1, 0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    circuit.measure(2, 2)
    circuit.measure(3, 3)

    cost = estimate_cost_honeywell_qiskit(circuit, 1024)
    print(f"Estimated cost: HQC {cost}")
