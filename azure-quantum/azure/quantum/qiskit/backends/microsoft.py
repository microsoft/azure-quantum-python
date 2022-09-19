##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING
from azure.quantum.version import __version__

from .backend import AzureBackend

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options
from qiskit_qir import SUPPORTED_INSTRUCTIONS as QIR_BASIS_GATES

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "MicrosoftBackend", "MicrosoftResourcesEstimatorBackend"
]

class MicrosoftBackend(AzureBackend):
    """Base class for interfacing with a Microsoft backend in Azure Quantum"""

    @classmethod
    def _default_options(cls):
        return Options(entryPoint="main", arguments=[], targetCapibility="BasicExecution")

    @classmethod
    def _azure_config(cls):
        return {
            "blob_name": "inputData",
            "content_type": "qir.v1",
            "provider_id": "microsoft-qc",
            "input_data_format": "qir.v1",
            "output_data_format": "microsoft.resource-estimates.v1",
            "to_qir_kwargs": {"record_output": False, "use_static_qubit_alloc": False, "use_static_result_alloc": False}
        }

class MicrosoftResourcesEstimatorBackend(MicrosoftBackend):
    """Backend class for interfacing with the resources estimator target"""

    backend_names = ("microsoft.estimator",)

    @classmethod
    def _default_options(cls):
        return Options(entryPoint="main", arguments=[], targetCapability="BasicExecution", errorBudget=1e-3, qubit={}, faultToleranceProtocol="surface_code")

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Constructor for class to interface with the resources estimator target"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Resources estimator on Azure Quantum",
                "basis_gates": QIR_BASIS_GATES,
                "memory": False,
                "n_qubits": 0xffffffffffffffff, # NOTE: maximum 64-bit unsigned value
                "conditional": True,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}], # NOTE: copied from other backends
                "azure": self._azure_config()
            }
        )
        logger.info("Initializing MicrosoftResourcesEstimatorBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)
