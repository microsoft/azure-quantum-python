##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import logging
from abc import ABCMeta, abstractmethod
from qiskit import ClassicalRegister, QuantumRegister
from pyqir.generator import SimpleModule, BasicQisBuilder

_log = logging.getLogger(name=__name__)

SUPPORTED_INSTRUCTIONS = [
    "measure",
    "m",
    "cx",
    "cz",
    "h",
    "reset",
    "rx",
    "ry",
    "rz",
    "s",
    "sdg",
    "t",
    "tdg",
    "x",
    "y",
    "z",
    "id"
]


class QuantumCircuitElementVisitor(metaclass=ABCMeta):
    @abstractmethod
    def visit_register(self, register):
        raise NotImplementedError

    @abstractmethod
    def visit_instruction(self, instruction):
        raise NotImplementedError


class BasicQisVisitor(QuantumCircuitElementVisitor):
    def __init__(self):
        self._module = None
        self._builder = None
        self._qubit_labels = {}
        self._clbit_labels = {}

    def visit_qiskit_module(self, module):
        _log.debug(f"Visiting Qiskit module '{module.name}' ({module.num_qubits}, {module.num_clbits})")
        self._module = SimpleModule(
            name=module.name,
            num_qubits=module.num_qubits,
            num_results=module.num_clbits,
        )
        self._builder = BasicQisBuilder(self._module.builder)

    def visit_register(self, register):
        _log.debug(f"Visiting register '{register.name}'")
        if isinstance(register, QuantumRegister):
            self._qubit_labels.update({
                bit: n + len(self._qubit_labels) for n, bit in enumerate(register)
            })
        elif isinstance(register, ClassicalRegister):
            self._clbit_labels.update({
                bit: n + len(self._clbit_labels) for n, bit in enumerate(register)
            })
        else:
            raise ValueError(f"Register of type {type(register)} not supported.")

    def visit_instruction(self, instruction, qargs, cargs, skip_condition=False):
        if instruction.name not in SUPPORTED_INSTRUCTIONS:
            raise ValueError(f"Gate {instruction.name} is not supported. \
Please transpile using the list of supported gates: {SUPPORTED_INSTRUCTIONS}.")

        qlabels = [self._qubit_labels.get(bit) for bit in qargs]
        clabels = [self._clbit_labels.get(bit) for bit in cargs]
        qubits = [self._module.qubits[n] for n in qlabels]
        results = [self._module.results[n] for n in clabels]

        labels = ", ".join([str(l) for l in qlabels + clabels])
        if instruction.condition is None or skip_condition:
            _log.debug(f"Visiting instruction '{instruction.name}' ({labels})")

        if instruction.condition is not None and skip_condition is False:
            _log.debug(f"Visiting condition for instruction '{instruction.name}' ({labels})")
            conditions = [self._module.results[self._clbit_labels.get(bit)] for bit in instruction.condition[0]]

            # Convert value into a bitstring of the same length as classical register
            values = format(instruction.condition[1], f'0{len(results)}b')

            # Add branches recursively for each bit in the bitstring
            def __visit():
                self.visit_instruction(instruction, qargs, cargs, skip_condition=True)

            def _branch(conditions_values):
                try:
                    result, val = next(conditions_values)
                    def __branch():
                        self._builder.if_result(
                            result=result,
                            one=_branch(conditions_values) if val == "1" else None,
                            zero=_branch(conditions_values) if val == "0" else None
                        )
                except StopIteration:
                    return __visit
                else:
                    return __branch

            _branch(zip(conditions, values))()
        elif "measure" == instruction.name or "m" == instruction.name:
            self._builder.m(*qubits, *results)
        elif "cx" == instruction.name:
            self._builder.cx(*qubits)
        elif "cz" == instruction.name:
            self._builder.cz(*qubits)
        elif "h" == instruction.name:
            self._builder.h(*qubits)
        elif "reset" == instruction.name:
            self._builder.reset(qubits[0])
        elif "rx" == instruction.name:
            self._builder.rx(*instruction.params, *qubits)
        elif "ry" == instruction.name:
            self._builder.ry(*instruction.params, *qubits)
        elif "rz" == instruction.name:
            self._builder.rz(*instruction.params, *qubits)
        elif "s" == instruction.name:
            self._builder.s(*qubits)
        elif "sdg" == instruction.name:
            self._builder.s_adj(*qubits)
        elif "t" == instruction.name:
            self._builder.t(*qubits)
        elif "tdg" == instruction.name:
            self._builder.t_adj(*qubits)
        elif "x" == instruction.name:
            self._builder.x(*qubits)
        elif "y" == instruction.name:
            self._builder.y(*qubits)
        elif "z" == instruction.name:
            self._builder.z(*qubits)
        elif "id" == instruction.name:
            # See: https://github.com/qir-alliance/pyqir/issues/74
            self._builder.x(self._module.qubits[0])
            self._builder.x(self._module.qubits[0])

    def ir(self):
        return self._module.ir()

    def bitcode(self):
        return self._module.bitcode()
