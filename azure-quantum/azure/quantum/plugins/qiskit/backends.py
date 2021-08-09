##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
from azure.quantum import __version__
from .job import AzureQuantumJob

try:
    from qiskit.providers import BackendV1 as Backend
    from qiskit.providers.models import BackendConfiguration
    from qiskit.providers import Options

    from qiskit_ionq.helpers import ionq_basis_gates, qiskit_circ_to_ionq_circ
except ImportError:
    raise ImportError(
    "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
)

import logging
logger = logging.getLogger(__name__)


class IonQBackend(Backend):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""

    @classmethod
    def _default_options(cls):
        return Options(shots=500)

    def _job_metadata(self, circuit):
        return {
            "qiskit": True,
            "name": circuit.name,
            "num_qubits": circuit.num_qubits,
        }

    def run(self, circuit, **kwargs):
        """Submits the given circuit for execution on an IonQ target."""
        ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit)
        input_data = json.dumps({
            "qubits": circuit.num_qubits,
            "circuit": ionq_circ,
        })

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
            content_type="application/json",
            provider_id="ionq",
            input_data_format="ionq.circuit.v1",
            output_data_format="ionq.quantum-results.v1",
            input_params = input_params,
            metadata= self._job_metadata(circuit),
            **kwargs
        )

        logger.info(f"Submitted job with id '{job.id()}' for circuit '{circuit.name}':")
        logger.info(input_data)

        return job

    def retrieve_job(self, job_id) -> AzureQuantumJob:
        """ Returns the Job instance associated with the given id."""
        return self._provider.get_job(job_id)


class IonQSimulatorBackend(IonQBackend):
    def __init__(self, provider):
        """Base class for interfacing with an IonQ Simulator backend"""
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
        """Base class for interfacing with an IonQ QPU backend"""
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
