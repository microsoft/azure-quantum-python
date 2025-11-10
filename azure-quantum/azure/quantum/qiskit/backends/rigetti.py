##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING, Dict
from azure.quantum.version import __version__
from azure.quantum.target.rigetti import RigettiTarget
from abc import abstractmethod
from .backend import AzureBackendConfig, AzureQirBackend, _ensure_backend_config
from qiskit.providers import Options
from qsharp import TargetProfile

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging

logger = logging.getLogger(__name__)

__all__ = ["RigettiSimulatorBackend", "RigettiQPUBackend"]


_DEFAULT_SHOTS_COUNT = 500

class RigettiBackend(AzureQirBackend):
    """Base class for interfacing with a Rigetti backend in Azure Quantum"""

    _SHOTS_PARAM_NAME = "count"

    @abstractmethod
    def __init__(
        self, configuration: AzureBackendConfig, provider: "AzureQuantumProvider" = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls):
        other_options = {
            cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT,
        }
        return Options(target_profile=TargetProfile.Base, **other_options)

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "rigetti",
            }
        )
        return config


class RigettiSimulatorBackend(RigettiBackend):
    backend_names = RigettiTarget.simulators()

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an Rigetti Simulator backend"""
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Rigetti simulator on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": True,
                "n_qubits": RigettiTarget.num_qubits(name),
                "conditional": False,
                "max_shots": 10000,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "is_default": True,
            }
        )
        logger.info("Initializing RigettiSimulatorBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class RigettiQPUBackend(RigettiBackend):
    backend_names = RigettiTarget.qpus()

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with a Rigetti QPU backend"""
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "Rigetti QPU on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": True,
                "n_qubits": RigettiTarget.num_qubits(name),
                "conditional": False,
                "max_shots": 10000,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "is_default": True,
            }
        )
        logger.info("Initializing RigettiQPUBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)
