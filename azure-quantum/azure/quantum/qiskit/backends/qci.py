##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING, Dict
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import AzureQuantumJob
from abc import abstractmethod
from .backend import (
    AzureQirBackend, 
    QIR_BASIS_GATES,
    _get_shots_or_deprecated_count_input_param,
)

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options, Provider

QIR_BASIS_GATES  = [
    "measure",
    "m",
    "barrier",
    "cx",
    "cz",
    "h",
    "reset",
    "rx",
    "ry",
    "rz",
    "s",
    "sdg",
    "swap",
    "t",
    "tdg",
    "x",
    "y",
    "z",
    "id",
]

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging

logger = logging.getLogger(__name__)

__all__ = ["QCISimulatorBackend" "QCIQPUBackend"]


_DEFAULT_SHOTS_COUNT = 500

class QCIBackend(AzureQirBackend):

    _SHOTS_PARAM_NAME = "shots"

    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls) -> Options:
        return Options(
            **{
                cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT, 
            },
            targetCapability="AdaptiveExecution",
        )

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "qci",
            }
        )
        return config
    
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
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "QCI simulator on Azure Quantum",
                "basis_gates": QIR_BASIS_GATES,
                "memory": False,
                "n_qubits": 29,
                "conditional": True,
                "max_shots": 1e6,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing QCISimulatorBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QCIQPUBackend(QCIBackend):
    backend_names = ("qci.machine1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an QCI QPU backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "QCI QPU on Azure Quantum",
                "basis_gates": QIR_BASIS_GATES,
                "memory": False,
                "n_qubits": 11,
                "conditional": True,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing QCIQPUBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)
