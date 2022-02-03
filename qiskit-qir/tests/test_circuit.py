##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import os
import pytest
import tempfile

from qiskit_qir.quantumcircuit import QirQuantumCircuit
from qiskit_qir import to_qir


@pytest.fixture()
def circuit():
    circuit = QirQuantumCircuit(4, 3)
    circuit.name = "Qiskit Sample - 3-qubit GHZ circuit"
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.h(3) # Dummy helper qubit that is not measured
    circuit.measure([0,1,2], [0, 1, 2])

    return circuit


def test_circuit_qir(circuit):
    qir_bitcode = circuit.qir()
    assert qir_bitcode is not None


def test_to_qir(circuit):
    qir_bitcode = to_qir(circuit)
    assert qir_bitcode is not None


def test_circuit_save_file(circuit):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = os.path.join(tmpdirname, "output.ll")
        circuit.qir(filename=filename)
        assert os.path.exists(filename)

        filename = os.path.join(tmpdirname, "output2.ll")
        to_qir(filename=filename)
        assert os.path.exists(filename)
