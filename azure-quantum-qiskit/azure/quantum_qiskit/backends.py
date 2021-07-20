##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
from azure.storage import blob
from .version import __version__
from .job import AzureQuantumJob

from azure.quantum import Job

from qiskit.providers import BackendV1 as Backend
from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options

from qiskit_ionq.helpers import ionq_basis_gates, qiskit_circ_to_ionq_circ

import logging
logger = logging.getLogger(__name__)


class IonQBackend(Backend):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""

    @classmethod
    def _default_options(cls):
        return Options(shots=1024)

    def run(self, circuit, **options):
        """Submits the given circuit for execution on an IonQ target."""
        ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit)
        input_data = json.dumps({
            "qubits": circuit.num_qubits,
            "circuit": ionq_circ,
        })

        logger.info(f"Submitting new job for backend {self.name()}")
        job = AzureQuantumJob(
            backend=self,
            name=circuit.name,
            target=self.name(),
            input_data=input_data,
            blob_name="inputData",
            content_type="application/json",
            provider_id="ionq",
            input_data_format="ionq.circuit.v1",
            output_data_format="ionq.quantum-results.v1"
        )

        logger.info(f"Submitting job with id '{job.id()}' for circuit '{circuit.name}':")
        logger.info(input_data)

        job._azure_job.details.metadata = { "qubits": str(circuit.num_qubits) }
        job.submit()
        return job


class IonQSimulatorBackend(IonQBackend):
    def __init__(self, provider):
        config = BackendConfiguration.from_dict(
            {
                "backend_name": "ionq.simulator",
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "IonQ simulator on Azure Quantum",
                "basis_gates": ionq_basis_gates,
                "memory": False,
                "n_qubits": 29,
                "conditional": False,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
            }
        )
        logger.info("Initializing IonQSimulatorBackend")
        super().__init__(configuration=config, provider=provider)


class IonQQPUBackend(IonQBackend):
    def __init__(self, provider):
        """Base class for interfacing with an IonQ backend"""
        config = BackendConfiguration.from_dict(
            {
                "backend_name": "ionq.qpu",
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ QPU on Azure Quantum",
                "basis_gates": ionq_basis_gates,
                "memory": False,
                "n_qubits": 11,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
            }
        )
        logger.info("Initializing IonQQPUBackend")
        super().__init__(configuration=config, provider=provider)

__all__ = ["IonQBackend", "IonQQPUBackend", "IonQSimulatorBackend"]