##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import warnings

from typing import TYPE_CHECKING, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.target.rigetti import RigettiTarget

from .backend import AzureBackend

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options
from qiskit_qir import SUPPORTED_INSTRUCTIONS as QIR_BASIS_GATES

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "RigettiSimulatorBackend"
    "RigettiQPUBackend"
]

class RigettiBackend(AzureBackend):
    """Base class for interfacing with a Rigetti backend in Azure Quantum"""

    @classmethod
    def _default_options(cls):
        return Options(count=500, entryPoint="main", arguments=[], targetCapability="BasicExecution")

    @classmethod
    def _azure_config(cls):
        return {
            "blob_name": "inputData",
            "content_type": "qir.v1",
            "provider_id": "rigetti",
            "input_data_format": "qir.v1",
            "output_data_format": "microsoft.quantum-results.v1",
        }


class RigettiSimulatorBackend(RigettiBackend):
    backend_names = RigettiTarget.simulators()

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        """Base class for interfacing with an Rigetti Simulator backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Rigetti simulator on Azure Quantum",
                "basis_gates": QIR_BASIS_GATES,
                "memory": False,
                "n_qubits": RigettiTarget.num_qubits(name),
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing RigettiSimulatorBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class RigettiQPUBackend(RigettiBackend):
    backend_names = RigettiTarget.qpus()

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        """Base class for interfacing with a Rigetti QPU backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "Rigetti QPU on Azure Quantum",
                "basis_gates": QIR_BASIS_GATES,
                "memory": False,
                "n_qubits": RigettiTarget.num_qubits(name),
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing RigettiQPUBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)
