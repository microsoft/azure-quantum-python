##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import abc
import pytest
import unittest
from typing import TYPE_CHECKING, Protocol, Tuple, runtime_checkable
from import_qsharp import skip_if_no_qsharp

if TYPE_CHECKING:
    import cirq
    import qiskit


@runtime_checkable
class QirInputData(Protocol):
    _name: str

    @abc.abstractmethod
    def _repr_qir_(self, **kwargs) -> bytes:
        raise NotImplementedError
    
    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class JobPayloadFactory():
    @staticmethod
    def get_cirq_circuit_bell_state() -> "cirq.Circuit":
        import cirq
        q0 = cirq.LineQubit(0)
        q1 = cirq.LineQubit(1)
        circuit = cirq.Circuit(
            cirq.H(q0),
            cirq.CNOT(q0, q1),
            cirq.measure(q0, key='q0'),
            cirq.measure(q1, key='q1')
        )
        return circuit

    @staticmethod
    def get_qsharp_inline_code_bell_state() -> Tuple[str, str]:
        return ("""
        open Microsoft.Quantum.Intrinsic;

        operation BellState_Inline() : (Result,Result) {
            use q0 = Qubit();
            use q1 = Qubit();
            H(q0);
            CNOT(q0, q1);
            return (M(q0), M(q1));
        }
        """, "BellState_Inline()")

    qsharp_inline_callable_bell_state: QirInputData = None

    @staticmethod
    def get_qsharp_inline_callable_bell_state() -> QirInputData:
        if not JobPayloadFactory.qsharp_inline_callable_bell_state:
            (qsharp_code, entrypoint) = JobPayloadFactory.get_qsharp_inline_code_bell_state()
            import qsharp
            qsharp.eval(qsharp_code)
            JobPayloadFactory.qsharp_inline_callable_bell_state = qsharp.compile(entrypoint)
        return JobPayloadFactory.qsharp_inline_callable_bell_state

    @staticmethod
    def get_qsharp_inline_qir_bitcode_bell_state() -> bytes:
        qirInputData = JobPayloadFactory.get_qsharp_inline_callable_bell_state()
        qir_bitcode = qirInputData._repr_qir_()
        return qir_bitcode 

    qsharp_file_callable_bell_state: QirInputData = None

    @staticmethod
    def get_qsharp_file_callable_bell_state() -> QirInputData:
        if not JobPayloadFactory.qsharp_file_callable_bell_state:
            import qsharp
            with open('QSharpBellState.qs') as file:
                qsharp.eval(file.read())
            JobPayloadFactory.qsharp_file_callable_bell_state = qsharp.compile("QSharpBellState.BellState_File()")
        return JobPayloadFactory.qsharp_file_callable_bell_state

    qsharp_file_qir_bitcode_bell_state: bytes = None

    @staticmethod
    def get_qsharp_file_qir_bitcode_bell_state() -> bytes:
        if not JobPayloadFactory.qsharp_file_qir_bitcode_bell_state:
            qirInputData = JobPayloadFactory.get_qsharp_file_callable_bell_state()
            qir_bitcode = qirInputData._repr_qir_()
            JobPayloadFactory.qsharp_file_qir_bitcode_bell_state = qir_bitcode
        return JobPayloadFactory.qsharp_file_qir_bitcode_bell_state

    @staticmethod
    def get_qiskit_circuit_bell_state() -> "qiskit.QuantumCircuit":
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(2, 2)
        circuit.name = "BellState"
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure([0, 1], [0, 1])
        return circuit


class TestJobPayloadFactory(unittest.TestCase):
    @pytest.mark.cirq
    def test_get_cirq_circuit_bell_state(self):
        import cirq
        self.assertIsInstance(JobPayloadFactory.get_cirq_circuit_bell_state(), cirq.Circuit)

    @pytest.mark.qiskit
    def test_get_qiskit_circuit_bell_state(self):
        # Qiskit tests are run separately to avoid import issues when Qiskit is not installed.
        pass

    @pytest.mark.qsharp
    @skip_if_no_qsharp
    def test_get_qsharp_inline_callable_bell_state(self):
        result = JobPayloadFactory.get_qsharp_inline_callable_bell_state()
        self.assertIsInstance(result, QirInputData)

    @pytest.mark.qsharp
    @pytest.mark.qir
    @skip_if_no_qsharp
    def test_get_qsharp_inline_qir_bell_state(self):
        result = JobPayloadFactory.get_qsharp_inline_qir_bitcode_bell_state()
        self.assertIsInstance(result, bytes)

    @pytest.mark.qsharp
    @skip_if_no_qsharp
    def test_get_qsharp_file_callable_bell_state(self):
        result = JobPayloadFactory.get_qsharp_file_callable_bell_state()
        self.assertIsInstance(result, QirInputData)

    @pytest.mark.qsharp
    @pytest.mark.qir
    @skip_if_no_qsharp
    def test_get_qsharp_file_qir_bell_state(self):
        result = JobPayloadFactory.get_qsharp_file_qir_bitcode_bell_state()
        self.assertIsInstance(result, bytes)
