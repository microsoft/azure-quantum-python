##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest
import logging

from qiskit_qir.elements import QiskitModule
from qiskit_qir.visitor import BasicQisVisitor
from qiskit_qir.translate import to_qir, to_qir_bitcode
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

_log = logging.getLogger(__name__)


@pytest.fixture()
def circuit():
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


def test_visitor(circuit):
    module = QiskitModule.from_quantum_circuit(circuit=circuit)
    visitor = BasicQisVisitor()
    module.accept(visitor)
    generated_ir = visitor.ir()
    _log.debug(generated_ir)
    assert generated_ir is not None


def test_to_qir(circuit):
    generated_ir = to_qir(circuit)
    _log.debug(generated_ir)
    assert generated_ir is not None


def test_to_qir(circuit):
    generated_bitcode = to_qir_bitcode(circuit)
    _log.debug(generated_bitcode)
    assert generated_bitcode is not None


def test_circuit_unroll():
    circ = QuantumCircuit(3)
    circ.ccx(0, 1, 2)
    circ.crz(theta=0.1, control_qubit=0, target_qubit=1)
    with pytest.raises(ValueError):
        to_qir(circ)
    new_circ = circ.decompose()
    generated_ir = to_qir(new_circ)
    _log.debug(generated_ir)
    assert generated_ir is not None


def test_teleport(teleport):
    generated_ir = to_qir(teleport)
    _log.debug(generated_ir)
    assert generated_ir is not None
