##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import warnings

from typing import TYPE_CHECKING, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import AzureQuantumJob

from .backend import AzureBackend

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options
from qiskit_qir import SUPPORTED_INSTRUCTIONS as QIR_BASIS_GATES

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "QCISimulatorBackend"
    "QCIQPUBackend"
]

class QCIBackend(AzureBackend):
    """Base class for interfacing with a QCI backend in Azure Quantum"""

    @classmethod
    def _default_options(cls):
        return Options(shots=500, entryPoint="main", arguments=[], targetCapability="AdaptiveExecution")

    @classmethod
    def _azure_config(cls):
        return {
            "blob_name": "inputData",
            "content_type": "qir.v1",
            "provider_id": "qci",
            "input_data_format": "qir.v1",
            "output_data_format": "microsoft.quantum-results.v1",
        }


class QCISimulatorBackend(QCIBackend):
    backend_names = ("qci.simulator",)

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
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
                "conditional": False,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing QCISimulatorBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class QCIQPUBackend(QCIBackend):
    backend_names = ("qci.machine1",)

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
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
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing QCIQPUBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)
