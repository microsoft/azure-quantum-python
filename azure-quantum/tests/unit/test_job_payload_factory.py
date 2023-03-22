##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
import unittest
from typing import Union, Tuple

import cirq
import qiskit
import azure.quantum.optimization as optimization


class JobPayloadFactory():
    @staticmethod
    def get_cirq_circuit_bell_state() -> cirq.Circuit:
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
    def get_qsharp_code_bell_state() -> Tuple[str, str]:
        return ("""
        open Microsoft.Quantum.Intrinsic;

        operation BellState() : (Result,Result) {
            use q0 = Qubit();
            use q1 = Qubit();
            H(q0);
            CNOT(q0, q1);
            return (M(q0), M(q1));
        }
        """, "ENTRYPOINT__BellState")

    @staticmethod
    def get_qiskit_circuit_bell_state() -> qiskit.QuantumCircuit:
        circuit = qiskit.QuantumCircuit(2, 2)
        circuit.name = "BellState"
        circuit.h(0)
        circuit.cnot(0, 1)
        circuit.measure([0, 1], [0, 1])
        return circuit

    @staticmethod
    def get_qio_ising_problem() -> optimization.Problem:
        problem = optimization.Problem(name="Ising Problem",
                                       problem_type=optimization.ProblemType.ising)
        terms = [
            optimization.Term(c=1, indices=[0]),
            optimization.Term(c=2, indices=[1, 0]),
        ]
        problem.add_terms(terms=terms)
        return problem


class TestJobPayloadFactory(unittest.TestCase):
    @pytest.mark.cirq
    def test_get_cirq_circuit_bell_state(self):
        self.assertIsInstance(JobPayloadFactory.get_cirq_circuit_bell_state(), cirq.Circuit)

    @pytest.mark.qiskit
    def test_get_qiskit_circuit_bell_state(self):
        self.assertIsInstance(JobPayloadFactory.get_qiskit_circuit_bell_state(), qiskit.QuantumCircuit)

    @pytest.mark.qio
    def test_get_qio_ising_problem(self):
        self.assertIsInstance(JobPayloadFactory.get_qio_ising_problem(), optimization.Problem)
