##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING, Dict, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import AzureQuantumJob
from abc import abstractmethod
from .backend import (
    AzureBackendConfig,
    AzureQirBackend,
    _ensure_backend_config,
    _get_shots_or_deprecated_count_input_param,
)
from qiskit.providers import Options
from qsharp import TargetProfile


if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging

logger = logging.getLogger(__name__)

__all__ = ["QCISimulatorBackend", "QCIQPUBackend"]


_DEFAULT_SHOTS_COUNT = 500

class QCIBackend(AzureQirBackend):

    _SHOTS_PARAM_NAME = "shots"

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
            target_profile=TargetProfile.Adaptive_RI,
        )

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "qci",
            }
        )
        return config

    def _basis_gates(self) -> List[str]:
        return super()._basis_gates() + ["barrier"]

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


class QCISimulatorBackend(QCIBackend):
    backend_names = ("qci.simulator", "qci.simulator.noisy")

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an QCI Simulator backend"""
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "QCI simulator on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 29,
                "conditional": True,
                "max_shots": 1e6,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "is_default": True,
            }
        )
        logger.info("Initializing QCISimulatorBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QCIQPUBackend(QCIBackend):
    backend_names = ("qci.machine1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an QCI QPU backend"""
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "QCI QPU on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 11,
                "conditional": True,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "is_default": True,
            }
        )
        logger.info("Initializing QCIQPUBackend")
        configuration = _ensure_backend_config(
            kwargs.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)
