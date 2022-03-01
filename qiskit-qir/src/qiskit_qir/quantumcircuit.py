# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# This code was based on the qiskit.circuit.quantumcircuit.QuantumCircuit.qasm
# method and modified to use the QirBuilder instead of building a QASM string.

from typing import Any

from qiskit.qasm.exceptions import QasmError
from qiskit.circuit.quantumcircuit import (
    QuantumCircuit,
    VALID_QASM2_IDENTIFIER, 
    _qasm_escape_gate_name,
    _add_sub_instruction_to_existing_composite_circuits
)

from qiskit_qir.builder import QiskitToQirBuilder
from sympy import true


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


class QirQuantumCircuit(QuantumCircuit):
    @classmethod
    def from_quantum_circuit(cls, circuit: QuantumCircuit) -> "QirQuantumCircuit":
        """Create a new QirQuantumCircuit instance from a QuantumCircuit object.
        This adds a method circuit.qir that can be used to translate the Qiskit
        circuit to QIR.

        :param circuit: Quantum circuit
        :type circuit: QuantumCircuit
        :return: QuantumCircuit that can be translated to QIR.
        :rtype: QirQuantumCircuit
        """
        regs = circuit.registers
        new_circuit = cls(
            *regs,
            circuit.name,
            circuit.global_phase,
            circuit.metadata
        )
        return new_circuit

    def qir(self, ir_string: bool = False) -> Any:
        """Return QIR bitcode.

        Args:
            ir_string (bool): Flag to set if the returned QIR should
            be a readable string rather than base 64 encoded bitcode.

        Returns:
            str

        Raises:
            QasmError: If circuit has free parameters.
            ValueError: If circuit has classical control.
        """

        if self.num_parameters > 0:
            raise QasmError("Cannot represent circuits with unbound parameters in OpenQASM 2.")

        existing_composite_circuits = []

        builder = QiskitToQirBuilder(module=self.name)

        for register in self.qregs:
            builder.add_register(register)

        for register in self.cregs:
            builder.add_register(register)

        bit_labels = {
            bit: "%s%d" % (reg.name, idx)
            for reg in self.qregs + self.cregs
            for (idx, bit) in enumerate(reg)
        }

        regless_qubits = set(self.qubits) - {bit for reg in self.qregs for bit in reg}
        regless_clbits = set(self.clbits) - {bit for reg in self.cregs for bit in reg}

        if regless_qubits:
            register_name = self._unique_register_name("qregless_")
            builder.add_quantum_register(register_name, len(regless_qubits))
            bit_labels.update(
                {bit: f"{register_name}{idx}" for idx, bit in enumerate(regless_qubits)}
            )
        if regless_clbits:
            register_name = self._unique_register_name("cregless_")
            builder.add_classical_register(register_name, len(regless_clbits))
            bit_labels.update(
                {bit: f"{register_name}{idx}" for idx, bit in enumerate(regless_clbits)}
            )

        for instruction, qargs, cargs in self._data:
            if instruction.name == "measure":
                qubit = qargs[0]
                clbit = cargs[0]
                builder.add_instruction(instruction, [bit_labels[qubit], bit_labels[clbit]])

            else:
                # Check instructions names or label are valid
                if not VALID_QASM2_IDENTIFIER.fullmatch(instruction.name):
                    instruction = instruction.copy(name=_qasm_escape_gate_name(instruction.name))

                # decompose gate using definitions if they are not defined in OpenQASM2
                if (
                    instruction.name not in EXISTING_GATE_NAMES
                    and instruction not in existing_composite_circuits
                ):
                    if instruction.name in [
                        instruction.name for instruction in existing_composite_circuits
                    ]:
                        # append instruction id to name of instruction copy to make it unique
                        instruction = instruction.copy(name=f"{instruction.name}_{id(instruction)}")

                    existing_composite_circuits.append(instruction)
                    _add_sub_instruction_to_existing_composite_circuits(
                        instruction, EXISTING_GATE_NAMES, existing_composite_circuits
                    )

                # Insert qasm representation of the original instruction
                builder.add_instruction(instruction, [bit_labels[j] for j in qargs + cargs])

        if ir_string is true:
            # Get QIR LLVM code
            qir_bitcode = builder.get_ir_string()
        else:
            qir_bitcode = builder.get_bitcode_base64_string()

        return qir_bitcode
 