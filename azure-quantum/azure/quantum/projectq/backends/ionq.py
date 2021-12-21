##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
import uuid

from azure.quantum import __version__
from azure.quantum.projectq.job import (
    AzureQuantumJob, 
    IONQ_PROVIDER, 
    IONQ_INPUT_DATA_FORMAT, 
    IONQ_OUTPUT_DATA_FORMAT
)

try:
    from projectq.backends import IonQBackend as _IonQBackend
    import projectq.setups.ionq
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
)

import logging
logger = logging.getLogger(__name__)

__all__ = ["IonQQPUBackend", "IonQSimulatorBackend"]


class IonQBackend(_IonQBackend):
    projectq_backend_name = None
    azure_quantum_backend_name = None

    def __init__(
        self, 
        use_hardware=False, 
        num_runs=100, 
        verbose=False, 
        device="ionq_simulator", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ backend in Azure Quantum"""
        logger.info("Initializing IonQBackend for ProjectQ")

        super().__init__(
            use_hardware=use_hardware, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device, 
            retrieve_execution=retrieve_execution
        )
        
    def get_engine_list(self):
        """Return the default list of compiler engine for the IonQ platform."""
        return projectq.setups.ionq.get_engine_list(
            device=self.projectq_backend_name
        )

    def run(self, name=None, **kwargs):
        """Submits the given circuit to run on an IonQ target."""
        logger.info(f"Submitting new job for backend {self.device}")

        if name is None:
            random_suffix = str(uuid.uuid4())[:8]
            name = "projectq-ionq-circuit-{}".format(random_suffix)

        qubit_mapping = self.main_engine.mapper.current_mapping

        num_qubits = len(qubit_mapping.keys())
        meas_map = [qubit_mapping[qubit_id] for qubit_id in self._measured_ids]

        input_data = json.dumps({
            "qubits": num_qubits,
            "circuit": self._circuit,
        })

        input_params = {
            "shots": self._num_runs
        }

        metadata = {
            "name": name, 
            "num_qubits": num_qubits, 
            "meas_map": meas_map,
        }

        job = AzureQuantumJob(
            backend=self,
            name=name,
            target=self.azure_quantum_backend_name, 
            input_data=input_data,
            blob_name="inputData",
            content_type="application/json",
            job_id=self._retrieve_execution,
            provider_id=IONQ_PROVIDER,
            input_data_format=IONQ_INPUT_DATA_FORMAT,
            output_data_format=IONQ_OUTPUT_DATA_FORMAT,
            input_params=input_params,
            metadata=metadata,
            **kwargs
        ) 

        logger.info(f"Submitted job with id '{job.id()}' for circuit '{name}':")
        logger.info(input_data)

        return job

    def _run(self):
        """
        Overriding Projectq run method with empty function.
        This disables circuit execution using default ProjectQ logic. Use engine.run() to submit job to Azure Quantum.
        """
        pass


class IonQQPUBackend(IonQBackend):
    projectq_backend_name = "ionq_qpu"
    azure_quantum_backend_name = "ionq.qpu"

    def __init__(
        self, 
        num_runs=100, 
        verbose=False, 
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ QPU backend"""
        logger.info("Initializing IonQQPUBackend for ProjectQ")

        super().__init__(
            use_hardware=True, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=self.projectq_backend_name, 
            retrieve_execution=retrieve_execution
        )

        
class IonQSimulatorBackend(IonQBackend):
    projectq_backend_name = "ionq_simulator"
    azure_quantum_backend_name = "ionq.simulator"

    def __init__(
        self, 
        num_runs=100, 
        verbose=False, 
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ Simulator backend"""
        logger.info("Initializing IonQSimulatorBackend for ProjectQ")

        super().__init__(
            use_hardware=False, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=self.projectq_backend_name, 
            retrieve_execution=retrieve_execution
        )
