##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING, Any, Dict, List
from azure.quantum.version import __version__
from qiskit import QuantumCircuit
from abc import abstractmethod
from .backend import AzureQirBackend

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options, Provider

QIR_BASIS_GATES = [
    "measure",
    "m",
    "ccx",
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

__all__ = ["MicrosoftBackend", "MicrosoftResourceEstimationBackend"]


class MicrosoftBackend(AzureQirBackend):
    """Base class for interfacing with a Microsoft backend in Azure Quantum"""

    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls):
        return Options(targetCapability="AdaptiveExecution")

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "microsoft-qc",
                "output_data_format": "microsoft.resource-estimates.v1",
                "to_qir_kwargs": {"record_output": False},
            }
        )
        return config


class MicrosoftResourceEstimationBackend(MicrosoftBackend):
    """Backend class for interfacing with the resource estimator target"""

    backend_names = ("microsoft.estimator",)

    @classmethod
    def _default_options(cls):
        return Options(
            targetCapability="AdaptiveExecution",
            errorBudget=1e-3,
            qubitParams={"name": "qubit_gate_ns_e3"},
            qecScheme={"name": "surface_code"}
        )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Constructor for class to interface with the resource estimator target"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Resource estimator on Azure Quantum",
                "basis_gates": QIR_BASIS_GATES,
                "memory": False,
                "n_qubits": 0xFFFFFFFFFFFFFFFF,  # NOTE: maximum 64-bit unsigned value
                "conditional": True,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [
                    {"name": "TODO", "parameters": [], "qasm_def": "TODO"}
                ],  # NOTE: copied from other backends
                "azure": self._azure_config(),
                "is_default": True,
            }
        )
        logger.info("Initializing MicrosoftResourceEstimationBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)
