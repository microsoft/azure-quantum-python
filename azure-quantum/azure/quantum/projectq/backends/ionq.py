##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
from typing import TYPE_CHECKING

from azure.quantum import __version__
from azure.quantum.projectq.job import (
    AzureQuantumJob, 
    IONQ_INPUT_DATA_FORMAT, 
    IONQ_OUTPUT_DATA_FORMAT
)

try:
    from projectq.backends import IonQBackend as ProjectQIonQBackend
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
)

if TYPE_CHECKING:
    from azure.quantum.projectq import AzureQuantumEngine

import logging
logger = logging.getLogger(__name__)

__all__ = ["IonQBackend", "IonQSimulatorBackend", "IonQQPUBackend"]


class IonQBackend(ProjectQIonQBackend):
    backend_name = None

    def __init__(
        self, 
        use_hardware=False, 
        num_runs=100, 
        verbose=False, 
        token=None, 
        device='ionq_simulator', 
        num_retries=3000, 
        interval=1, 
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ backend in Azure Quantum"""
        logger.info("Initializing IonQBackend")

        super().__init__(
            use_hardware=use_hardware, 
            num_runs=num_runs, 
            verbose=verbose, 
            token=token, 
            device=device, 
            num_retries=num_retries, 
            interval=interval, 
            retrieve_execution=retrieve_execution
        )

        self._provider_id = "ionq"

    def _job_metadata(self, name, num_qubits, meas_map):
        return {
            "projectq": True,
            "name": name,
            "num_qubits": num_qubits,
            "meas_map": meas_map,
        }

    def provider_id(self):
        return self._provider_id

    def run(self, name, **kwargs):
        """Submits the given circuit to run on an IonQ target."""
        logger.info(f"Submitting new job for backend {self.device}")

        qubit_mapping = self.main_engine.mapper.current_mapping
        measured_ids = self._measured_ids[:]

        num_qubits = len(qubit_mapping.keys())
        meas_map = [qubit_mapping[qubit_id] for qubit_id in measured_ids]

        ionq_circ = self._circuit

        input_data = json.dumps({
            "qubits": num_qubits,
            "circuit": ionq_circ,
        })

        # todo: get input_params
        input_params = dict()

        job = AzureQuantumJob(
            backend=self,
            name=name,
            target="",  # todo: what is target?
            input_data=input_data,
            blob_name="inputData",
            content_type="application/json",
            provider_id=self.provider_id(),
            input_data_format=IONQ_INPUT_DATA_FORMAT,
            output_data_format=IONQ_OUTPUT_DATA_FORMAT,
            input_params = input_params,
            metadata= self._job_metadata(name=name, num_qubits=num_qubits, meas_map=meas_map),
            **kwargs
        ) 

        logger.info(f"Submitted job with id '{job.id()}' for circuit '{name}':")
        logger.info(input_data)

        return job

        
class IonQSimulatorBackend(IonQBackend):
    backend_name = "ionq_simulator"

    def __init__(
        self, 
        num_runs=100, 
        verbose=False, 
        token=None, 
        num_retries=3000, 
        interval=1, 
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ Simulator backend"""
        logger.info("Initializing IonQSimulatorBackend")

        super().__init__(
            use_hardware=False, 
            num_runs=num_runs, 
            verbose=verbose, 
            token=token, 
            device=self.backend_name, 
            num_retries=num_retries, 
            interval=interval, 
            retrieve_execution=retrieve_execution
        )


class IonQQPUBackend(IonQBackend):
    backend_name = "ionq_qpu"

    def __init__(
        self, 
        num_runs=100, 
        verbose=False, 
        token=None, 
        num_retries=3000, 
        interval=1, 
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ QPU backend"""
        logger.info("Initializing IonQQPUBackend")

        super().__init__(
            use_hardware=True, 
            num_runs=num_runs, 
            verbose=verbose, 
            token=token, 
            device=self.backend_name, 
            num_retries=num_retries, 
            interval=interval, 
            retrieve_execution=retrieve_execution
        )
