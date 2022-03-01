##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from abc import ABCMeta, abstractmethod
from typing import Any
from qiskit import ClassicalRegister, QuantumRegister

from qiskit.qasm.exceptions import QasmError
from qiskit.circuit.quantumcircuit import (
    QuantumCircuit,
    VALID_QASM2_IDENTIFIER
)
from pyqir.generator import SimpleModule, BasicQisBuilder

EXISTING_GATE_NAMES = [
    "barrier",
    "measure",
    "reset",
    "u3",
    "u2",
    "u1",
    "cx",
    "id",
    "u0",
    "u",
    "p",
    "x",
    "y",
    "z",
    "h",
    "s",
    "sdg",
    "t",
    "tdg",
    "rx",
    "ry",
    "rz",
    "sx",
    "sxdg",
    "cz",
    "cy",
    "swap",
    "ch",
    "ccx",
    "cswap",
    "crx",
    "cry",
    "crz",
    "cu1",
    "cp",
    "cu3",
    "csx",
    "cu",
    "rxx",
    "rzz",
    "rccx",
    "rc3x",
    "c3x",
    "c3sx",
    "c4x",
]


# def _qasm_escape_gate_name(name: str) -> str:
#     """Returns a valid OpenQASM gate identifier"""
#     # Replace all non-ASCII-word characters with the underscore.
#     import re
#     import string
#     escaped_name = re.sub(r"\W", "_", name, flags=re.ASCII)
#     if not escaped_name or escaped_name[0] not in string.ascii_lowercase:
#         # Add an arbitrary, guaranteed-to-be-valid prefix.
#         escaped_name = "gate_" + escaped_name

#     return escaped_name


# def _add_sub_instruction_to_existing_composite_circuits(
#     instruction: Instruction,
#     existing_gate_names: List[str],
#     existing_composite_circuits: List[Instruction],
# ) -> None:
#     """Recursively add undefined sub-instructions in the definition of the given
#     instruction to existing_composite_circuit list.
#     """
#     for sub_instruction, _, _ in instruction.definition:
#         # Check instructions names are valid
#         if not VALID_QASM2_IDENTIFIER.fullmatch(sub_instruction.name):
#             sub_instruction = sub_instruction.copy(
#                 name=_qasm_escape_gate_name(sub_instruction.name)
#             )
#         if (
#             sub_instruction.name not in existing_gate_names
#             and sub_instruction not in existing_composite_circuits
#         ):
#             existing_composite_circuits.insert(0, sub_instruction)
#             _add_sub_instruction_to_existing_composite_circuits(
#                 sub_instruction, existing_gate_names, existing_composite_circuits
#             )


# def _decompose(instruction, existing_composite_circuits):
#     # Check instructions names or label are valid
#     if not VALID_QASM2_IDENTIFIER.fullmatch(instruction.name):
#         instruction = instruction.copy(name=_qasm_escape_gate_name(instruction.name))

#     # decompose gate using definitions if they are not defined in OpenQASM2
#     if (
#         instruction.name not in EXISTING_GATE_NAMES
#         and instruction not in existing_composite_circuits
#     ):
#         if instruction.name in [
#             instruction.name for instruction in existing_composite_circuits
#         ]:
#             # append instruction id to name of instruction copy to make it unique
#             instruction = instruction.copy(name=f"{instruction.name}_{id(instruction)}")

#         existing_composite_circuits.append(instruction)
#         _add_sub_instruction_to_existing_composite_circuits(
#             instruction, EXISTING_GATE_NAMES, existing_composite_circuits
#         )
    
#     return instruction


def _bit_label(bit, regs):
    bit_labels = {
        bit: "%s%d" % (reg.name, idx)
        for reg in regs
        for (idx, bit) in enumerate(reg)
    }
    return bit_labels[bit]


class QuantumCircuitElementVisitor(metaclass=ABCMeta):
    @abstractmethod
    def visitRegister(self, register):
        raise NotImplementedError

    @abstractmethod
    def visitInstruction(self, instruction):
        raise NotImplementedError


class BasicQisVisitor(QuantumCircuitElementVisitor):
    def __init__(self):
        self._module = None
        self._builder = None
        self._bit_labels = {}

    def visitQuantumCircuit(self, circuit):
        self._module = SimpleModule(
            name=circuit.name,
            num_qubits=circuit.num_qubits,
            num_results=circuit.num_clbits,
        )
        self._builder = BasicQisBuilder(self._module.builder)
        print(f"Visiting quantum circuit '{circuit.name}' ({circuit.num_qubits}, {circuit.num_clbits})")

    def visitRegister(self, register):
        self._bit_labels.update({
            bit: "%s%d" % (register.name, idx) for (idx, bit) in enumerate(register)
        })
        print(f"Visiting register '{register.name}'")

    def visitInstruction(self, instruction, qargs, cargs):
        qlabels = ", ".join([self._bit_labels.get(bit) for bit in qargs + cargs])
        print(f"Visiting instruction '{instruction.name}' ({qlabels})")
