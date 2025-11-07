##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Dict, List, Union
from azure.quantum import __version__
from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.target.ionq import IonQ
from abc import abstractmethod
from qsharp import TargetProfile
from qiskit import QuantumCircuit

from .backend import (
    AzureBackend,
    AzureBackendConfig,
    AzureQirBackend,
    _ensure_backend_config,
    _get_shots_or_deprecated_count_input_param,
)
from qiskit.providers import Options


#####################################################################
#####################################################################
#####################################################################
# Vendored from qiskit_ionq


# the qiskit gates that the IonQ backend can serialize to our IR
# not the actual hardware basis gates for the system — we do our own transpilation pass.
# also not an exact/complete list of the gates IonQ's backend takes
#   by name — please refer to IonQ docs for that.
#
# Some of these gates may be deprecated or removed in qiskit 1.0
ionq_basis_gates = [
    "ccx",
    "ch",
    "cnot",
    "cp",
    "crx",
    "cry",
    "crz",
    "csx",
    "cx",
    "cy",
    "cz",
    "h",
    "i",
    "id",
    "mcp",
    "mcphase",
    "mct",
    "mcx",
    "measure",
    "p",
    "rx",
    "rxx",
    "ry",
    "ryy",
    "rz",
    "rzz",
    "s",
    "sdg",
    "swap",
    "sx",
    "sxdg",
    "t",
    "tdg",
    "toffoli",
    "x",
    "y",
    "z",
    "PauliEvolution",
]

# https://ionq.com/docs/getting-started-with-native-gates
ionq_native_basis_gates = [
    "gpi",
    "gpi2",
    "ms",  # Pairwise MS gate
    "zz",  # ZZ gate
]

# Each language corresponds to a different set of basis gates.
GATESET_MAP = {
    "qis": ionq_basis_gates,
    "native": ionq_native_basis_gates,
}

ionq_api_aliases = {  # todo fix alias bug
    "cp": "cz",
    "csx": "cv",
    "mcphase": "cz",
    "ccx": "cx",  # just one C for all mcx
    "mcx": "cx",  # just one C for all mcx
    "tdg": "ti",
    "p": "z",
    "PauliEvolution": "pauliexp",
    "rxx": "xx",
    "ryy": "yy",
    "rzz": "zz",
    "sdg": "si",
    "sx": "v",
    "sxdg": "vi",
}

from qiskit.circuit import (
    controlledgate as q_cgates,
    QuantumCircuit,
)

from typing import Literal, Any

from qiskit.exceptions import QiskitError

class IonQError(QiskitError):
    """Base class for errors raised by an IonQProvider."""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.message!r})"

    def __repr__(self) -> str:
        return repr(str(self))

class JobError(QiskitError):
    """Base class for errors raised by Jobs."""

    pass

class IonQGateError(IonQError, JobError):
    """Errors generated from invalid gate defs

    Attributes:
        gate_name: The name of the gate which caused this error.
    """

    def __init__(self, gate_name: str, gateset: Literal["qis", "native"]):
        self.gate_name = gate_name
        self.gateset = gateset
        super().__init__(
            (
                f"gate '{gate_name}' is not supported on the '{gateset}' IonQ backends. "
                "Please use the qiskit.transpile method, manually rewrite to remove the gate, "
                "or change the gateset selection as appropriate."
            )
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(gate_name={self.gate_name!r}, gateset={self.gateset!r})"

class IonQMidCircuitMeasurementError(IonQError, JobError):
    """Errors generated from attempting mid-circuit measurement, which is not supported.
    Measurement must come after all instructions.

    Attributes:
        qubit_index: The qubit index to be measured mid-circuit
    """

    def __init__(self, qubit_index: int, gate_name: str):
        self.qubit_index = qubit_index
        self.gate_name = gate_name
        super().__init__(
            f"Attempting to put '{gate_name}' after a measurement on qubit {qubit_index}. "
            "Mid-circuit measurement is not supported."
        )

    def __str__(self):
        kwargs = f"qubit_index={self.qubit_index!r}, gate_name={self.gate_name!r}"
        return f"{self.__class__.__name__}({kwargs})"

class IonQPauliExponentialError(IonQError):
    """Errors generated from improper usage of Pauli exponentials."""

def paulis_commute(pauli_terms: list[str]) -> bool:
    """Check if a list of Pauli terms commute.

    Args:
        pauli_terms (list): A list of Pauli terms.

    Returns:
        bool: Whether the Pauli terms commute.
    """
    for i, term in enumerate(pauli_terms):
        for other_term in pauli_terms[i:]:
            assert len(term) == len(other_term)
            anticommutation_parity = 0
            for index, char in enumerate(term):
                other_char = other_term[index]
                if "I" not in (char, other_char):
                    if char != other_char:
                        anticommutation_parity += 1
            if anticommutation_parity % 2 == 1:
                return False
    return True

def qiskit_circ_to_ionq_circ(
    input_circuit: QuantumCircuit,
    gateset: Literal["qis", "native"] = "qis",
    ionq_compiler_synthesis: bool = False,
):
    """Build a circuit in IonQ's instruction format from qiskit instructions.

    .. ATTENTION:: This function ignores the following compiler directives:
       * ``barrier``

    Parameters:
        input_circuit (:class:`qiskit.circuit.QuantumCircuit`): A Qiskit quantum circuit.
        gateset (string): Set of gates to target. It can be QIS (required transpilation pass in
          IonQ backend, which is sent standard gates) or native (only IonQ native gates are
          allowed, in the future we may provide transpilation to these gates in Qiskit).
        ionq_compiler_synthesis (bool): Whether to opt-in to IonQ compiler's intelligent
          trotterization.

    Raises:
        IonQGateError: If an unsupported instruction is supplied.
        IonQMidCircuitMeasurementError: If a mid-circuit measurement is detected.
        IonQPauliExponentialError: If non-commuting PauliExponentials are found without
          the appropriate flag.

    Returns:
        list[dict]: A list of instructions in a converted dict format.
        int: The number of measurements.
        dict: The measurement map from qubit number to classical bit number.
    """
    compiler_directives = ["barrier"]
    output_circuit = []
    num_meas = 0
    meas_map = [None] * len(input_circuit.clbits)
    for inst in input_circuit.data:
        instruction, qargs, cargs = inst.operation, inst.qubits, inst.clbits

        # Don't process compiler directives.
        instruction_name = instruction.name
        if instruction_name in compiler_directives:
            continue

        # Don't process measurement instructions.
        if instruction_name == "measure":
            meas_map[input_circuit.clbits.index(cargs[0])] = input_circuit.qubits.index(
                qargs[0]
            )
            num_meas += 1
            continue

        # serialized identity gate is a no-op
        if instruction_name == "id":
            continue

        # Raise out for instructions we don't support.
        if instruction_name not in GATESET_MAP[gateset]:
            raise IonQGateError(instruction_name, gateset)

        # Process the instruction and convert.
        rotation: dict[str, Any] = {}
        if len(instruction.params) > 0:
            if gateset == "qis" or (
                len(instruction.params) == 1 and instruction_name != "zz"
            ):
                # The float is here to cast Qiskit ParameterExpressions to numbers
                rotation = {
                    ("rotation" if gateset == "qis" else "phase"): float(
                        instruction.params[0]
                    )
                }
                if instruction_name == "PauliEvolution":
                    # rename rotation to time
                    rotation["time"] = rotation.pop("rotation")
            elif instruction_name in {"zz"}:
                rotation = {"angle": instruction.params[0]}
            else:
                rotation = {
                    "phases": [float(t) for t in instruction.params[:2]],
                    "angle": instruction.params[2],
                }

        # Default conversion is simple, just gate & target(s).
        targets = [input_circuit.qubits.index(qargs[0])]
        if instruction_name in {"ms", "zz"}:
            targets.append(input_circuit.qubits.index(qargs[1]))

        converted = (
            {"gate": instruction_name, "targets": targets}
            if instruction_name not in {"gpi", "gpi2"}
            else {
                "gate": instruction_name,
                "target": targets[0],
            }
        )

        # re-alias certain names
        if instruction_name in ionq_api_aliases:
            instruction_name = ionq_api_aliases[instruction_name]
            converted["gate"] = instruction_name

        # Make sure uncontrolled multi-targets use all qargs.
        if instruction.num_qubits > 1 and not hasattr(instruction, "num_ctrl_qubits"):
            converted["targets"] = [
                input_circuit.qubits.index(qargs[i])
                for i in range(instruction.num_qubits)
            ]

        # If this is a controlled gate, make sure to set control qubits.
        if isinstance(instruction, q_cgates.ControlledGate):
            gate = instruction_name[1:]  # trim the leading c
            controls = [input_circuit.qubits.index(qargs[0])]
            targets = [input_circuit.qubits.index(qargs[1])]
            # If this is a multi-control, use more than one qubit.
            if instruction.num_ctrl_qubits > 1:
                controls = [
                    input_circuit.qubits.index(qargs[i])
                    for i in range(instruction.num_ctrl_qubits)
                ]
                targets = [
                    input_circuit.qubits.index(qargs[instruction.num_ctrl_qubits])
                ]
            if gate == "swap":
                # If this is a cswap, we have two targets:
                targets = [
                    input_circuit.qubits.index(qargs[-2]),
                    input_circuit.qubits.index(qargs[-1]),
                ]

            # Update converted gate values.
            converted.update(
                {
                    "gate": gate,
                    "controls": controls,
                    "targets": targets,
                }
            )

        if instruction_name == "pauliexp":
            imag_coeff = any(coeff.imag for coeff in instruction.operator.coeffs)
            assert not imag_coeff, (
                "PauliEvolution gate must have real coefficients, "
                f"but got {imag_coeff}"
            )
            terms = [term[0] for term in instruction.operator.to_list()]
            if not ionq_compiler_synthesis and not paulis_commute(terms):
                raise IonQPauliExponentialError(
                    f"You have included a PauliEvolutionGate with non-commuting terms: {terms}."
                    "To decompose it with IonQ hardware-aware synthesis, resubmit with the "
                    "IONQ_COMPILER_SYNTHESIS flag."
                )
            targets = [
                input_circuit.qubits.index(qargs[i])
                for i in range(instruction.num_qubits)
            ]
            coefficients = [coeff.real for coeff in instruction.operator.coeffs]
            gate = {
                "gate": instruction_name,
                "targets": targets,
                "terms": terms,
                "coefficients": coefficients,
            }
            converted.update(gate)

        # if there's a valid instruction after a measurement,
        if num_meas > 0:
            # see if any of the involved qubits have been measured,
            # and raise if so — no mid-circuit measurement!
            controls_and_targets = converted.get("targets", []) + converted.get(
                "controls", []
            )
            if any(i in meas_map for i in controls_and_targets):
                raise IonQMidCircuitMeasurementError(
                    input_circuit.qubits.index(qargs[0]), instruction_name
                )

        output_circuit.append({**converted, **rotation})

    return output_circuit, num_meas, meas_map

#####################################################################
#####################################################################
#####################################################################

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import json

import logging

logger = logging.getLogger(__name__)

__all__ = [
    "IonQBackend",
    "IonQSimulatorBackend",
    "IonQAriaBackend",
    "IonQForteBackend",
    "IonQQirBackend",
    "IonQSimulatorQirBackend",
    "IonQSimulatorNativeBackend",
    "IonQAriaQirBackend",
    "IonQForteQirBackend",
    "IonQAriaNativeBackend",
    "IonQForteNativeBackend",
]

_IONQ_SHOTS_INPUT_PARAM_NAME = "shots"
_DEFAULT_SHOTS_COUNT = 500

class IonQQirBackendBase(AzureQirBackend):
    """Base class for interfacing with an IonQ QIR backend"""

    _SHOTS_PARAM_NAME = _IONQ_SHOTS_INPUT_PARAM_NAME

    @abstractmethod
    def __init__(
        self, configuration: AzureBackendConfig, provider: "AzureQuantumProvider" = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls) -> Options:
        return Options(
            **{
                cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT,
            },
            target_profile=TargetProfile.Base,
            )

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "ionq",
            }
        )
        return config

    def run(
        self, 
        run_input: Union[QuantumCircuit, List[QuantumCircuit]] = [],
        shots: int = None,
        **options,
    ) -> AzureQuantumJob:
        
        # In earlier versions, backends for all providers accepted the 'count' option,
        # but now we accept it only for a compatibility reasons and do not recommend using it.
        count = options.pop("count", None)

        final_shots = _get_shots_or_deprecated_count_input_param(
            param_name=self.__class__._SHOTS_PARAM_NAME,
            shots=shots,
            count=count,
        )
        
        return super().run(run_input, shots=final_shots, **options)


class IonQSimulatorQirBackend(IonQQirBackendBase):
    backend_names = ("ionq.simulator",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ QIR Simulator backend"""
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "IonQ simulator on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 29,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing IonQSimulatorQirBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQAriaQirBackend(IonQQirBackendBase):
    backend_names = ("ionq.qpu.aria-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Aria QPU backend"""
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Aria QPU on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 25,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing IonQAriaQirBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQForteQirBackend(IonQQirBackendBase):
    backend_names = ("ionq.qpu.forte-1","ionq.qpu.forte-enterprise-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Forte QPU backend"""
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Forte QPU on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 35,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing IonQForteQirBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQBackend(AzureBackend):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""

    backend_name = None

    _SHOTS_PARAM_NAME = _IONQ_SHOTS_INPUT_PARAM_NAME

    @abstractmethod
    def __init__(
        self, configuration: AzureBackendConfig, provider: "AzureQuantumProvider" = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    def run(
        self, 
        run_input=None,
        shots: int = None,
        **options,
    ) -> AzureQuantumJob:
        
        # In earlier versions, backends for all providers accepted the 'count' option,
        # but now we accept it only for a compatibility reasons and do not recommend using it.
        count = options.pop("count", None)

        final_shots = _get_shots_or_deprecated_count_input_param(
            param_name=self.__class__._SHOTS_PARAM_NAME,
            shots=shots,
            count=count,
        )
        
        return super().run(run_input, shots=final_shots, **options)

    @classmethod
    def _default_options(cls):
        return Options(
            **{
                cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT,
            },
        )

    def _azure_config(self) -> Dict[str, str]:
        return {
            "blob_name": "inputData",
            "content_type": "application/json",
            "provider_id": "ionq",
            "input_data_format": "ionq.circuit.v1",
            "output_data_format": "ionq.quantum-results.v1",
            "is_default": False,
        }

    def _prepare_job_metadata(self, circuit, **kwargs):
        _, _, meas_map = qiskit_circ_to_ionq_circ(circuit, gateset=self.gateset())

        metadata = super()._prepare_job_metadata(circuit, **kwargs)
        metadata["meas_map"] = json.dumps(meas_map)

        return metadata

    def _translate_input(self, circuit):
        """Translates the input values to the format expected by the AzureBackend."""
        ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit, gateset=self.gateset())
        input_data = {
            "gateset": self.gateset(),
            "qubits": circuit.num_qubits,
            "circuit": ionq_circ,
        }
        return IonQ._encode_input_data(input_data)

    def gateset(self):
        return self.configuration().gateset


class IonQSimulatorBackend(IonQBackend):
    backend_names = ("ionq.simulator",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Simulator backend"""
        gateset = kwargs.pop("gateset", "qis")
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "IonQ simulator on Azure Quantum",
                "basis_gates": GATESET_MAP[gateset],
                "memory": False,
                "n_qubits": 29,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "gateset": gateset,
            }
        )
        logger.info("Initializing IonQSimulatorBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQSimulatorNativeBackend(IonQSimulatorBackend):
    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        if "gateset" not in kwargs:
            kwargs["gateset"] = "native"
        super().__init__(name, provider, **kwargs)


class IonQAriaBackend(IonQBackend):
    backend_names = ("ionq.qpu.aria-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Aria QPU backend"""
        gateset = kwargs.pop("gateset", "qis")
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Aria QPU on Azure Quantum",
                "basis_gates": GATESET_MAP[gateset],
                "memory": False,
                "n_qubits": 23,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "gateset": gateset,
            }
        )
        logger.info("Initializing IonQAriaQPUBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQForteBackend(IonQBackend):
    backend_names = ("ionq.qpu.forte-1","ionq.qpu.forte-enterprise-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Forte QPU backend"""
        gateset = kwargs.pop("gateset", "qis")
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Forte QPU on Azure Quantum",
                "basis_gates": GATESET_MAP[gateset],
                "memory": False,
                "n_qubits": 35,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "gateset": gateset,
            }
        )
        logger.info("Initializing IonQForteBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQAriaNativeBackend(IonQAriaBackend):
    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        if "gateset" not in kwargs:
            kwargs["gateset"] = "native"
        super().__init__(name, provider, **kwargs)


class IonQForteNativeBackend(IonQForteBackend):
    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        if "gateset" not in kwargs:
            kwargs["gateset"] = "native"
        super().__init__(name, provider, **kwargs)
