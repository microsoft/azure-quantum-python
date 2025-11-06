##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING, Dict
from azure.quantum.version import __version__
import warnings

from .backend import (
    AzureBackend,
    AzureBackendConfig,
    AzureQirBackend,
    _ensure_backend_config,
)
from abc import abstractmethod
from qiskit.providers import Options
from qiskit.providers import Provider
from qiskit.qasm2 import dumps
from qsharp import TargetProfile
import logging

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

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
    if ".h2-" in name:
        return 56
    warnings.warn(
        UserWarning(f"Number of qubits not known for target {name}. Defaulting to 20."))
    return 20

_QUANTINUUM_COUNT_INPUT_PARAM_NAME = "count"
_DEFAULT_SHOTS_COUNT = 500

class QuantinuumQirBackendBase(AzureQirBackend):

    _SHOTS_PARAM_NAME = _QUANTINUUM_COUNT_INPUT_PARAM_NAME

    @abstractmethod
    def __init__(
        self, configuration: AzureBackendConfig, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls) -> Options:
        return Options(
            **{
                cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT
            },
            target_profile=TargetProfile.Adaptive_RI,
        )

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
        "quantinuum.sim.h2-1sc",
        "quantinuum.sim.h2-2sc"
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Quantinuum Syntax Checker on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": True,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        logger.info(
            "Initializing %sSyntaxCheckerQirBackend", self._provider_name
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumEmulatorQirBackend(QuantinuumQirBackendBase):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.sim.h2-1e",
        "quantinuum.sim.h2-2e"
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Quantinuum emulator on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": True,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        logger.info(
            "Initializing %sEmulatorQirBackend", self._provider_name
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumQPUQirBackend(QuantinuumQirBackendBase):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.qpu.h2-1",
        "quantinuum.qpu.h2-2"
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "Quantinuum QPU on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": True,
                "n_qubits": self._get_n_qubits(name),
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        logger.info("Initializing %sQPUQirBackend", self._provider_name)
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumBackend(AzureBackend):
    """Base class for interfacing with a Quantinuum (formerly Honeywell) backend in Azure Quantum"""

    _SHOTS_PARAM_NAME = _QUANTINUUM_COUNT_INPUT_PARAM_NAME

    @abstractmethod
    def __init__(
        self, configuration: AzureBackendConfig, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

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
            "content_type": "application/qasm",
            "provider_id": self._provider_id,
            "input_data_format": "honeywell.openqasm.v1",
            "output_data_format": "honeywell.quantum-results.v1",
            "is_default": False,
        }

    def _translate_input(self, circuit):
        """Translates the input values to the format expected by the AzureBackend."""
        return dumps(circuit)

    def _get_n_qubits(self, name):
        return _get_n_qubits(name)


class QuantinuumSyntaxCheckerBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.sim.h2-1sc",
        "quantinuum.sim.h2-2sc"
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Quantinuum Syntax Checker on Azure Quantum",
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
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        logger.info("Initializing %sSyntaxCheckerBackend", self._provider_name)
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumEmulatorBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.sim.h2-1e",
        "quantinuum.sim.h2-2e"
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Quantinuum emulator on Azure Quantum",
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
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        logger.info("Initializing %sEmulatorBackend", self._provider_name)
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QuantinuumQPUBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.qpu.h2-1",
        "quantinuum.qpu.h2-2"
    )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "Quantinuum QPU on Azure Quantum",
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
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        logger.info("Initializing %sQPUBackend", self._provider_name)
        super().__init__(configuration=configuration, provider=provider, **kwargs)
