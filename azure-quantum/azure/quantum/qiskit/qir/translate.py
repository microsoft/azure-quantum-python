##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from ctypes import Union
from types import MethodType
from typing import Optional
from qiskit import QuantumCircuit

from azure.quantum.qiskit.qir.quantumcircuit import QirQuantumCircuit


def to_qir(
    circuit: Union[QuantumCircuit, QirQuantumCircuit],
    ir_string: bool = False
) -> str:
    """Convert a qiskit.QuantumCircuit to QIR (see qir-alliance.org).

    :param circuit: Quantum circuit to convert
    :type circuit: QuantumCircuit
    :param ir_string: Flag to set if the returned QIR should
        be a readable string rather than base 64 encoded bitcode.
    :return: QIR bitcode
    :rtype: str
    """
    circuit.qir = MethodType( QirQuantumCircuit.qir, circuit )
    return circuit.qir(ir_string=ir_string)
