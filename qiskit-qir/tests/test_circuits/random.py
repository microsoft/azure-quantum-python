##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest

from qiskit import transpile
from qiskit.circuit.random import random_circuit
from qiskit_qir.visitor import SUPPORTED_INSTRUCTIONS


def generate_random_fixture(num_qubits, depth):
    @pytest.fixture()
    def random():
        circuit = random_circuit(num_qubits, depth, measure=True)
        return transpile(circuit, basis_gates = SUPPORTED_INSTRUCTIONS)   
    return random


# Generate random fixtures
__all__ = []
for num_qubits, depth in [(i+2,j+2) for i in range(9) for j in range(9)]:
    name = f"random_{num_qubits}x{depth}"
    locals()[name] = generate_random_fixture(num_qubits, depth)
    __all__.append(name)
