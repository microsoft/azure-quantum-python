# ##
# # Copyright (c) Microsoft Corporation.
# # Licensed under the MIT License.
# ##

# import pytest
# import unittest
# from typing import Union, Tuple

# import cirq
# import qiskit
# from  pyquil import quil
# import qsharp
# import azure.quantum.optimization as optimization
# from qsharp.loader import QSharpCallable

# class JobPayloadFactory():
#     @staticmethod
#     def get_cirq_circuit_bell_state() -> cirq.Circuit:
#         q0 = cirq.LineQubit(0)
#         q1 = cirq.LineQubit(1)
#         circuit = cirq.Circuit(
#             cirq.H(q0),
#             cirq.CNOT(q0, q1),
#             cirq.measure(q0, key='q0'),
#             cirq.measure(q1, key='q1')
#         )
#         return circuit

#     @staticmethod
#     def get_qsharp_code_bell_state() -> Tuple[str, str]:
#         return ("""
#         open Microsoft.Quantum.Intrinsic;

#         operation BellState() : (Result,Result) {
#             use q0 = Qubit();
#             use q1 = Qubit();
#             H(q0);
#             CNOT(q0, q1);
#             return (M(q0), M(q1));
#         }
#         """, "ENTRYPOINT__BellState")

#     @staticmethod
#     def get_qsharp_callable_bell_state() -> Tuple[QSharpCallable, str]:
#         (qsharp_code, entrypoint) = JobPayloadFactory.get_qsharp_code_bell_state()
#         return (qsharp.compile(qsharp_code), entrypoint)

#     @staticmethod
#     def get_qsharp_qir_bitcode_bell_state(target:Union[None,str] = None) -> Tuple[bytes, str]:
#         (qsharpCallable, entrypoint) = JobPayloadFactory.get_qsharp_callable_bell_state()
#         qir_bitcode = qsharpCallable._repr_qir_(target=target)
#         return (qir_bitcode, entrypoint)

#     @staticmethod
#     def get_qsharp_qir_text_bell_state(target:Union[None,str] = None) -> Tuple[str, str]:
#         (qsharpCallable, entrypoint) = JobPayloadFactory.get_qsharp_callable_bell_state()
#         qir_text = qsharpCallable.as_qir(output_format="IR", target=target)
#         return (qir_text, entrypoint)

#     @staticmethod
#     def get_qiskit_circuit_bell_state() -> qiskit.QuantumCircuit:
#         circuit = qiskit.QuantumCircuit(2, 2)
#         circuit.name = "BellState"
#         circuit.h(0)
#         circuit.cnot(0,1)
#         circuit.measure([0,1], [0,1])
#         return circuit

#     @staticmethod
#     def get_quil_code_bell_state() -> str:
#         return """
#         DECLARE ro BIT[2]
#         H 0
#         CNOT 0 1
#         MEASURE 0 ro [0]
#         MEASURE 1 ro [1]
#         """

#     @staticmethod
#     def get_pyquil_program_bell_state() -> quil.Program:
#         from pyquil.gates import MEASURE, H, CNOT
#         from pyquil.quilbase import Declare
#         program = quil.Program(
#             Declare("ro", "BIT", 2),
#             H(0),
#             CNOT(0,1),
#             MEASURE(0, ("ro", 0)),
#             MEASURE(1, ("ro", 1)),
#         )
#         return program

#     @staticmethod
#     def get_qir_bitcode_bell_state() -> bytes:
#         from pyqir.generator import BasicQisBuilder, SimpleModule, types
#         def record_output(module : SimpleModule):
#             array_start_record_output = module.add_external_function(
#                 "__quantum__rt__array_start_record_output", types.Function([], types.VOID)
#             )
#             array_end_record_output = module.add_external_function(
#                 "__quantum__rt__array_end_record_output", types.Function([], types.VOID)
#             )
#             result_record_output = module.add_external_function(
#                 "__quantum__rt__result_record_output",
#                 types.Function([types.RESULT], types.VOID),
#             )    
#             module.builder.call(array_start_record_output, [])
#             for index in range(0, len(module.results)):
#                 result_ref = module.results[index]
#                 module.builder.call(result_record_output, [result_ref])
#             module.builder.call(array_end_record_output, [])

#         qir_module = SimpleModule("BellState", num_qubits=2, num_results=2)
#         qis = BasicQisBuilder(qir_module.builder)
#         qis.h(qir_module.qubits[0])
#         qis.cx(qir_module.qubits[0], qir_module.qubits[1])
#         qis.m(qir_module.qubits[0], qir_module.results[0])
#         qis.m(qir_module.qubits[1], qir_module.results[1])
#         record_output(qir_module)
#         qir_bitcode = qir_module.bitcode()
#         return qir_bitcode
    
#     @staticmethod
#     def get_qio_ising_problem() -> optimization.Problem:
#         problem = optimization.Problem(name="Ising Problem",
#                                        problem_type=optimization.ProblemType.ising)
#         terms = [
#             optimization.Term(c=1, indices=[0]),
#             optimization.Term(c=2, indices=[1,0]),
#         ]
#         problem.add_terms(terms=terms)
#         return problem


@pytest.skip(allow_module_level=True)
class TestJobPayloadFactory(unittest.TestCase):
    @pytest.mark.cirq
    def test_get_cirq_circuit_bell_state(self):
        self.assertIsInstance(JobPayloadFactory.get_cirq_circuit_bell_state(), cirq.Circuit)

#     @pytest.mark.qsharp
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_qsharp_code_bell_state(), str)

#     @pytest.mark.qsharp
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_qsharp_callable_bell_state(), Tuple[QSharpCallable, str])

#     @pytest.mark.qsharp
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_qsharp_qir_bitcode_bell_state("rigetti.sim.qvm"), Tuple[bytes, str])

#     @pytest.mark.qiskit
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_qiskit_circuit_bell_state(), qiskit.QuantumCircuit)

#     @pytest.mark.quil
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_quil_code_bell_state(), str)

#     @pytest.mark.quil
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_pyquil_program_bell_state(), quil.Program)

#     @pytest.mark.qir
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_qir_bitcode_bell_state(), bytes)

#     @pytest.mark.qio
#     def test_get_cirq_circuit_bell_state(self):
#         self.assertIsInstance(JobPayloadFactory.get_qio_ising_problem(), optimization.Problem)
