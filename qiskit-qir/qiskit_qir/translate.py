# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from types import MethodType
from typing import Optional
from qiskit import QuantumCircuit
from qiskit_qir.quantumcircuit import QirQuantumCircuit


def to_qir(
    circuit: QuantumCircuit,
    filename: Optional[str] = None,
    encoding: Optional[str] = None
) -> str:
    """Convert a qiskit.QuantumCircuit to QIR (see qir-alliance.org).

    :param circuit: Quantum circuit to convert
    :type circuit: QuantumCircuit
    :param filename: Output file name to save bitcode to, defaults to None
    :type filename: Optional[str], optional
    :param encoding: Specify output file encoding, defaults to system default
        (see https://docs.python.org/3/library/codecs.html#standard-encodings)
    :type encoding: Optional[str], optional
    :return: QIR bitcode
    :rtype: str
    """
    circuit.qir = MethodType( QirQuantumCircuit.qir, circuit )
    return circuit.qir(filename=filename, encoding=encoding)
