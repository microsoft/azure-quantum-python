##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING
from azure.quantum.version import __version__

from .backend import AzureQirBackend

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options

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
    "id"
]

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "MicrosoftBackend", "MicrosoftResourceEstimationBackend"
]

class MicrosoftBackend(AzureQirBackend):
    """Base class for interfacing with a Microsoft backend in Azure Quantum"""

    @classmethod
    def _default_options(cls):
        return Options(entryPoint="main", arguments=[], targetCapability="AdaptiveExecution")

    def _azure_config(self):
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "microsoft-qc",
                "output_data_format": "microsoft.resource-estimates.v1",
                "to_qir_kwargs": {"record_output": False}
            }
        )
        return config

class MicrosoftResourceEstimationBackend(MicrosoftBackend):
    """Backend class for interfacing with the resource estimator target"""

    backend_names = ("microsoft.estimator",)

    @classmethod
    def _default_options(cls):
        return Options(
            entryPoint="main",
            arguments=[],
            targetCapability="AdaptiveExecution",
            errorBudget=1e-3,
            qubitParams={"name":"qubit_gate_ns_e3"},
            qecScheme={"name":"surface_code"},
            items=None
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
                "n_qubits": 0xffffffffffffffff, # NOTE: maximum 64-bit unsigned value
                "conditional": True,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}], # NOTE: copied from other backends
                "azure": self._azure_config()
            }
        )
        logger.info("Initializing MicrosoftResourceEstimationBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)

    def _translate_input(self, circuit, input_data_format, input_params, to_qir_kwargs={}):
        # Delete `items` key from input_data_format if it hasn't been set
        if not input_params.get("items", None):
            del input_params["items"]

        return MicrosoftBackend._translate_input(self, circuit, input_data_format, input_params, to_qir_kwargs)
