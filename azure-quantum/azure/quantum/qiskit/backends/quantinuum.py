##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import Dict
from azure.quantum.version import __version__
import warnings

from .backend import AzureBackend, AzureQirBackend
from abc import abstractmethod
from qiskit import QuantumCircuit
from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options
from qiskit.providers import Provider

import logging

logger = logging.getLogger(__name__)

__all__ = [
    "QuantinuumSyntaxCheckerBackend",
    "QuantinuumEmulatorBackend",
    "QuantinuumQPUBackend",
    "QuantinuumEmulatorQirBackend",
    "QuantinuumSyntaxCheckerQirBackend",
    "QuantinuumQPUQirBackend",
]

QUANTINUUM_BASIS_GATES = [
    "x",
    "y",
    "z",
    "rx",
    "ry",
    "rz",
    "h",
    "cx",
    "cz",
    "s",
    "sdg",
    "t",
    "tdg",
    "v",
    "vdg",
    "zz",
    "measure",
    "reset",
]

QUANTINUUM_PROVIDER_ID = "quantinuum"
QUANTINUUM_PROVIDER_NAME = "Quantinuum"


def _get_n_qubits(name):
    name = name.lower()
    if ".h1-" in name or "hqs-lt" in name:
        return 20
    if ".h2-" in name:
        return 32
    warnings.warn(
        UserWarning(f"Number of qubits not known for target {name}. Defaulting to 20."))
    return 20


class QuantinuumQirBackendBase(AzureQirBackend):
    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls) -> Options:
        return Options(shots=500, targetCapability="BasicExecution")

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": QUANTINUUM_PROVIDER_ID,
            }
        )
        return config

    def _get_n_qubits(self, name):
        return _get_n_qubits(name)


class QuantinuumSyntaxCheckerQirBackend(QuantinuumQirBackendBase):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1-apival", "quantinuum.sim.h1-1sc",
        "quantinuum.hqs-lt-s2-apival", "quantinuum.sim.h1-2sc",
        "quantinuum.sim.h2-1sc",
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum Syntax Checker on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        logger.info(f"Initializing {self._provider_name}SyntaxCheckerQirBackend")
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumEmulatorQirBackend(QuantinuumQirBackendBase):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1-sim", "quantinuum.sim.h1-1e",
        "quantinuum.hqs-lt-s2-sim", "quantinuum.sim.h1-2e",
        "quantinuum.sim.h2-1e",
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum emulator on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        logger.info(f"Initializing {self._provider_name}EmulatorQirBackend")
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumQPUQirBackend(QuantinuumQirBackendBase):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1", "quantinuum.qpu.h1-1",
        "quantinuum.hqs-lt-s2", "quantinuum.qpu.h1-2",
        "quantinuum.qpu.h2-1",
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum QPU on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        logger.info(f"Initializing {self._provider_name}QPUQirBackend")
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumBackend(AzureBackend):
    """Base class for interfacing with a Quantinuum (formerly Honeywell) backend in Azure Quantum"""

    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls):
        return Options(count=500)

    def _azure_config(self) -> Dict[str, str]:
        return {
            "blob_name": "inputData",
            "content_type": "application/qasm",
            "provider_id": self._provider_id,
            "input_data_format": "honeywell.openqasm.v1",
            "output_data_format": "honeywell.quantum-results.v1",
            "is_default": True,
        }

    def _translate_input(self, circuit):
        """Translates the input values to the format expected by the AzureBackend."""
        return circuit.qasm()

    def estimate_cost(
        self, circuit: QuantumCircuit, shots: int = None, count: int = None
    ):
        """Estimate cost for running this circuit

        :param circuit: Qiskit quantum circuit
        :type circuit: QuantumCircuit
        :param shots: Shot count
        :type shots: int
        :param count: Shot count (alternative to 'shots')
        :type count: int
        """
        if count is not None:
            shots = count

        if shots is None:
            raise ValueError("Missing input argument 'shots'.")

        input_data = circuit.qasm()
        workspace = self.provider().get_workspace()
        target = workspace.get_targets(self.name())
        return target.estimate_cost(input_data, num_shots=shots)

    def _get_n_qubits(self, name):
        return _get_n_qubits(name)


class QuantinuumSyntaxCheckerBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1-apival", "quantinuum.sim.h1-1sc",
        "quantinuum.hqs-lt-s2-apival", "quantinuum.sim.h1-2sc",
        "quantinuum.sim.h2-1sc",
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum Syntax Checker on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        logger.info(f"Initializing {self._provider_name}SyntaxCheckerBackend")
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumEmulatorBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1-sim", "quantinuum.sim.h1-1e",
        "quantinuum.hqs-lt-s2-sim", "quantinuum.sim.h1-2e",
        "quantinuum.sim.h2-1e",
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum emulator on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        logger.info(f"Initializing {self._provider_name}EmulatorBackend")
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumQPUBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1", "quantinuum.qpu.h1-1",
        "quantinuum.hqs-lt-s2", "quantinuum.qpu.h1-2",
        "quantinuum.qpu.h2-1",
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum QPU on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        logger.info(f"Initializing {self._provider_name}QPUBackend")
        super().__init__(configuration=configuration, provider=provider, **kwargs)
