##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import warnings

from typing import TYPE_CHECKING, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import AzureQuantumJob

from .backend import AzureBackend

from qiskit import QuantumCircuit
from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "QuantinuumBackend",
    "QuantinuumQPUBackend",
    "QuantinuumAPIValidatorBackend",
    "QuantinuumSimulatorBackend"
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
    "ccx",
    "cz",
    "s",
    "sdg",
    "t",
    "tdg",
    "v",
    "vdg",
    "zz",
    "measure",
    "reset"
]

QUANTINUUM_PROVIDER_ID = "quantinuum"
QUANTINUUM_PROVIDER_NAME = "Quantinuum"

HONEYWELL_PROVIDER_ID = "honeywell"
HONEYWELL_PROVIDER_NAME = "Honeywell"

class QuantinuumBackend(AzureBackend):
    """Base class for interfacing with a Quantinuum (formerly Quantinuum) backend in Azure Quantum"""

    def __init__(self, **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME
        if kwargs.pop("provider_id", None) == HONEYWELL_PROVIDER_ID:
            self._provider_id = HONEYWELL_PROVIDER_ID
            self._provider_name = HONEYWELL_PROVIDER_NAME
        super().__init__(**kwargs)

    @classmethod
    def _default_options(cls):
        return Options(count=500)

    def _azure_config(self):
        return {
            "blob_name": "inputData",
            "content_type": "application/qasm",
            "provider_id": self._provider_id,
            "input_data_format": "honeywell.openqasm.v1",
            "output_data_format": "honeywell.quantum-results.v1",
        }

    def _translate_input(self, circuit, data_format, input_params):
        """ Translates the input values to the format expected by the AzureBackend. """
        if data_format == "honeywell.openqasm.v1":
            return (circuit.qasm(), data_format, input_params)
        else:
            super()._translate_input(circuit, data_format, input_params)
        

    def estimate_cost(self, circuit: QuantumCircuit, shots: int = None, count: int = None):
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


class QuantinuumAPIValidatorBackend(QuantinuumBackend):
    backend_names = (
        "quantinuum.hqs-lt-s1-apival",
        "quantinuum.hqs-lt-s2-apival"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME
        if kwargs.pop("provider_id", None) == "honeywell":
            self._provider_id = HONEYWELL_PROVIDER_ID
            self._provider_name = HONEYWELL_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum (formerly Honeywell) API validator on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": 10,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        logger.info(f"Initializing {self._provider_name}APIValidatorBackend")
        super().__init__(configuration=configuration,
                         provider=provider,
                         provider_id=self._provider_id,
                         **kwargs)


class QuantinuumSimulatorBackend(QuantinuumBackend):
    backend_names = (
        "quantinuum.hqs-lt-s1-sim",
        "quantinuum.hqs-lt-s2-sim"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME
        if kwargs.pop("provider_id", None) == "honeywell":
            self._provider_id = HONEYWELL_PROVIDER_ID
            self._provider_name = HONEYWELL_PROVIDER_NAME

        configuration: BackendConfiguration = kwargs.pop("configuration", None)
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum (formerly Honeywell) simulator on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": 10,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        logger.info(f"Initializing {self._provider_name}APIValidatorBackend")
        super().__init__(configuration=configuration,
                         provider=provider,
                         provider_id=self._provider_id,
                         **kwargs)


class QuantinuumQPUBackend(QuantinuumBackend):
    backend_names = (
        "quantinuum.hqs-lt-s1",
        "quantinuum.hqs-lt-s2"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME
        if kwargs.pop("provider_id", None) == "honeywell":
            self._provider_id = HONEYWELL_PROVIDER_ID
            self._provider_name = HONEYWELL_PROVIDER_NAME

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum (formerly Honeywell) QPU on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": 10,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        logger.info(f"Initializing {self._provider_name}QPUBackend")
        super().__init__(configuration=configuration,
                         provider=provider, 
                         provider_id=self._provider_id,
                         **kwargs)
