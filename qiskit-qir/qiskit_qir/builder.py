# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from dis import Instruction
from typing import Union, Iterable

from pyqir_generator import QirBuilder
from qiskit.circuit.classicalregister import ClassicalRegister
from qiskit.circuit.quantumregister import QuantumRegister


INSTRUCTIONS = [
    "cx",
    "cz",
    "h",
    "m",
    "reset",
    "rx",
    "ry",
    "rz",
    "s",
    "t",
    "x",
    "y",
    "z"
]


class QiskitToQirBuilder(QirBuilder):
    """Qiskit to QIR builder."""
    def __init__(self, module: str):
        """Create QiskitToQirBuilder object

        :param module: QIR module name
        :type module: str
        """
        super().__init__(module=module)

    def add_register(self, register: Union[QuantumRegister, ClassicalRegister]):
        """Add register

        :param register: A Qiskit quantum or classical register object
        :type register: Union[QuantumRegister, ClassicalRegister]
        :raises ValueError: Throws ValueError if not a quantum or classical
            register is passed
        """
        if isinstance(register, QuantumRegister):
            self.add_quantum_register(register.name, register.size)
        elif isinstance(register, ClassicalRegister):
            self.add_classical_register(register.name, register.size)
        else:
            raise ValueError(f"Cannot add register of type {type(register)}")

    def add_instruction(self, instruction: Instruction, bit_labels: Iterable[str]):
        """Add quantum instruction.

        :param instruction: Qiskit quantum instruction
        :type instruction: Instruction
        :param bit_labels: Bit labels to apply instruction to
        :type bit_labels: Iterable[str]
        :raises ValueError: Raises ValueError if the circuit contains if statements
        :raises ValueError: Raises ValueError if the circuit contains unsupported instructions
        """
        if instruction.condition is not None:
            raise ValueError(
                f"if statements are currently not supported for OpenQASM 2.0 to \
                    QIR translation.")

        if "measure" == instruction.name:
            fn = self.m
        elif "cx" == instruction.name:
            fn = self.cx
        elif "cz" == instruction.name:
            fn = self.cz
        elif "h" == instruction.name:
            fn = self.h
        elif "m" == instruction.name:
            fn = self.m
        elif "reset" == instruction.name:
            fn = self.reset
        elif "rx" == instruction.name:
            fn = self.rx
        elif "ry" == instruction.name:
            fn = self.ry
        elif "rz" == instruction.name:
            fn = self.rz
        elif "s" == instruction.name:
            fn = self.s
        elif "t" == instruction.name:
            fn = self.t
        elif "x" == instruction.name:
            fn = self.x
        elif "y" == instruction.name:
            fn = self.y
        elif "z" == instruction.name:
            fn = self.z
        else:
            raise ValueError(f"Instruction {instruction.name} is not supported.")

        fn(*bit_labels)
