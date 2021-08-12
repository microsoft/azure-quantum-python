##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
from azure.quantum.version import __version__
from azure.quantum.plugins.qiskit.job import AzureQuantumJob

from qiskit import QuantumCircuit
from qiskit.providers import BackendV1 as Backend
from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "HoneywellBackend",
    "HoneywellQPUBackend",
    "HoneywellAPIValidatorBackend",
    "HoneywellSimulatorBackend"
]

HONEYWELL_BASIS_GATES = [
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


class HoneywellBackend(Backend):
    """Base class for interfacing with an Honeywell backend in Azure Quantum"""

    @classmethod
    def _default_options(cls):
        return Options(count=500)

    def run(self, circuit: QuantumCircuit, **kwargs):
        """Submits the given circuit for execution on an Honeywell target."""
        input_data = circuit.qasm()

        # Options are mapped to input_params
        # Take also into consideration options passed in the kwargs, as the take precedence
        # over default values:
        input_params = vars(self.options)
        for opt in kwargs.copy():
            if opt in input_params:
                input_params[opt] = kwargs.pop(opt)

        logger.info(f"Submitting new job for backend {self.name()}")
        job = AzureQuantumJob(
            backend=self,
            name=circuit.name,
            target=self.name(),
            input_data=input_data,
            blob_name="inputData",
            content_type="application/qasm",
            provider_id="honeywell",
            input_data_format="honeywell.openqasm.v1",
            output_data_format="honeywell.quantum-results.v1",
            input_params = input_params,
            metadata={ "qubits": str(circuit.num_qubits) },
            **kwargs
        )
        
        logger.info(f"Submitted job with id '{job.id()}' for circuit '{circuit.name}':")
        logger.info(input_data)

        return job


class HoneywellAPIValidatorBackend(HoneywellBackend):
    def __init__(self, provider):
        config = BackendConfiguration.from_dict(
            {
                "backend_name": "honeywell.hqs-lt-s1-apival",
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Honeywell API validator on Azure Quantum",
                "basis_gates": HONEYWELL_BASIS_GATES,
                "memory": False,
                "n_qubits": 10,
                "conditional": False,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
            }
        )
        logger.info("Initializing HoneywellAPIValidatorBackend")
        super().__init__(configuration=config, provider=provider)


class HoneywellSimulatorBackend(HoneywellBackend):
    def __init__(self, provider):
        config = BackendConfiguration.from_dict(
            {
                "backend_name": "honeywell.hqs-lt-s1-sim",
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Honeywell simulator on Azure Quantum",
                "basis_gates": HONEYWELL_BASIS_GATES,
                "memory": False,
                "n_qubits": 10,
                "conditional": False,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
            }
        )
        logger.info("Initializing HoneywellAPIValidatorBackend")
        super().__init__(configuration=config, provider=provider)


class HoneywellQPUBackend(HoneywellBackend):
    def __init__(self, provider):
        """Base class for interfacing with an Honeywell backend"""
        config = BackendConfiguration.from_dict(
            {
                "backend_name": "honeywell.hqs-lt-s1",
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "Honeywell QPU on Azure Quantum",
                "basis_gates": HONEYWELL_BASIS_GATES,
                "memory": False,
                "n_qubits": 10,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
            }
        )
        logger.info("Initializing HoneywellQPUBackend")
        super().__init__(configuration=config, provider=provider)
