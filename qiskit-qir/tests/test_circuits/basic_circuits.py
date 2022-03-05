##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

@pytest.fixture()
def ghz():
    circuit = QuantumCircuit(4, 3)
    circuit.name = "Qiskit Sample - 3-qubit GHZ circuit"
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.measure([0,1,2], [0, 1, 2])

    return circuit


@pytest.fixture()
def teleport():
    q = QuantumRegister(3, name="q")
    cr = ClassicalRegister(2, name="cr")
    circuit = QuantumCircuit(q, cr, name="Teleport")
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    circuit.x(2).c_if(cr, int("10", 2))
    circuit.z(2).c_if(cr, int("01", 2))

    return circuit


@pytest.fixture()
def unroll():
    circ = QuantumCircuit(3)
    circ.ccx(0, 1, 2)
    circ.crz(theta=0.1, control_qubit=0, target_qubit=1)
    circ.id(0)

    return circ.decompose()
