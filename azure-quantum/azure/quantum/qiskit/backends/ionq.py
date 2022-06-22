##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING
from azure.quantum import __version__
from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.target.ionq import IonQ
import json

from .backend import AzureBackend

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options
from qiskit.qobj import Qobj, QasmQobj

from qiskit_ionq.helpers import GATESET_MAP, qiskit_circ_to_ionq_circ

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = ["IonQBackend", "IonQQPUBackend", "IonQSimulatorBackend"]


class IonQBackend(AzureBackend):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""
    backend_name = None

    @classmethod
    def _default_options(cls):
        return Options(shots=500)

    @classmethod
    def _azure_config(cls):
        return {
            "blob_name": "inputData",
            "content_type": "application/json",
            "provider_id": "ionq",
            "input_data_format": "ionq.circuit.v1",
            "output_data_format": "ionq.quantum-results.v1",
        }

    def _prepare_job_metadata(self, circuit, **kwargs):
        _, _, meas_map = qiskit_circ_to_ionq_circ(circuit)
        
        metadata = super()._prepare_job_metadata(circuit, **kwargs);
        metadata["meas_map"] = meas_map
        
        return metadata

    def _translate_input(self, circuit, data_format, input_params):
        """ Translates the input values to the format expected by the AzureBackend. """
        if data_format == "ionq.circuit.v1":
            ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit, gateset=self.gateset())
            input_data = {
                "qubits": circuit.num_qubits,
                "circuit": ionq_circ,
            }
            return (IonQ._encode_input_data(input_data), data_format, input_params)
        else:
            return super()._translate_input(circuit, data_format, input_params)

    def gateset(self):
        return self._gateset

    def estimate_cost(self, circuit, shots):
        """Estimate the cost for the given circuit."""
        ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit)
        input_data = {
            "qubits": circuit.num_qubits,
            "circuit": ionq_circ,
        }
        workspace = self.provider().get_workspace()
        target = workspace.get_targets(self.name())
        return target.estimate_cost(input_data, num_shots=shots)


class IonQSimulatorBackend(IonQBackend):
    backend_names = ("ionq.simulator",)

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        """Base class for interfacing with an IonQ Simulator backend"""
        self._gateset = kwargs.pop("gateset", "qis")

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "IonQ simulator on Azure Quantum",
                "basis_gates": GATESET_MAP[self._gateset],
                "memory": False,
                "n_qubits": 29,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing IonQSimulatorBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQQPUBackend(IonQBackend):
    backend_names = ("ionq.qpu",)

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        """Base class for interfacing with an IonQ QPU backend"""
        self._gateset = kwargs.pop("gateset", "qis")

        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ QPU on Azure Quantum",
                "basis_gates": GATESET_MAP[self._gateset],
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
        logger.info("Initializing IonQQPUBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)
