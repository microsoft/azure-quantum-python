##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
import uuid

import numpy as np

from azure.quantum import __version__
from azure.quantum import Job
from azure.quantum.projectq.utils import (
    IONQ_PROVIDER, 
    IONQ_INPUT_DATA_FORMAT, 
    IONQ_OUTPUT_DATA_FORMAT,
    PROJECTQ_USER_AGENT
)
from azure.quantum.target.ionq import int_to_bitstring

try:
    from projectq.backends import IonQBackend as _IonQBackend
    from projectq.types import WeakQubitRef
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
)

import logging
logger = logging.getLogger(__name__)

__all__ = ["IonQQPUBackend", "IonQSimulatorBackend"]


class AzureIonQBackend(_IonQBackend):
    projectq_backend_name: str = None
    azure_target_name: str = None

    def __init__(
        self,
        workspace,
        use_hardware: bool=False,
        num_runs: int=100,
        verbose: bool=False,
        device: str="ionq_simulator",
        num_retries: int = 3000,
        interval: int = 1,
        retrieve_execution: str=None
    ):
        """Base class for interfacing with an IonQ backend in Azure Quantum

        :param use_hardware: Whether or not to use real IonQ hardware or just a simulator. If False, the
            ionq_simulator is used regardless of the value of ``device``. Defaults to False.
        :param num_runs: Number of times to run circuits. Defaults to 100.
        verbose: If True, print statistics after job results have been collected. Defaults to
            False.
        :param token: An IonQ API token. Defaults to None.
        :param device: Device to run jobs on.  Supported devices are ``'ionq_qpu'`` or
            ``'ionq_simulator'``.  Defaults to ``'ionq_simulator'``.
        :param num_retries: Number of times to retry fetching job results after it has been submitted. Defaults
            to 3000.
        :param interval: Number of seconds to wait inbetween result fetch retries. Defaults to 1.
        :param retrieve_execution: An IonQ API Job ID.  If provided, a job with this ID will be
            fetched. Defaults to None.
        """
        logger.info("Initializing IonQBackend for ProjectQ")
        workspace.append_user_agent(PROJECTQ_USER_AGENT)
        self._workspace = workspace

        super().__init__(
            use_hardware=use_hardware, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device,
            num_retries=num_retries,
            interval=interval,
            retrieve_execution=retrieve_execution
        )

    def submit_job(self, name=None, **kwargs) -> Job:
        """Submits the given circuit to run on an IonQ target."""
        logger.info(f"Submitting new job for backend {self.device}")

        if name is None:
            random_suffix = str(uuid.uuid4())[:8]
            name = "projectq-ionq-circuit-{}".format(random_suffix)

        qubit_mapping = self.main_engine.mapper.current_mapping

        num_qubits = len(self._measured_ids)
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

        job = Job.from_input_data(
            workspace=self._workspace,
            name=name,
            target=self.azure_target_name,
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

        logger.info(f"Submitted job with id '{job.id}' for circuit '{name}':")
        logger.info(input_data)

        return job

    def _run(self):
        """
        Run a ProjectQ circuit and wait until it is done.
        """
        job = self.submit_job()
        result = job.get_results(timeout_secs=self._num_retries * self._interval)
        self._probabilities = {int_to_bitstring(k, len(self._measured_ids), self._measured_ids): v for k, v in result["histogram"].items()}

        # Set a single measurement result
        bitstring = np.random.choice(list(self._probabilities.keys()), p=list(self._probabilities.values()))
        for qid in self._measured_ids:
            qubit_ref = WeakQubitRef(self.main_engine, qid)
            self.main_engine.set_measurement_result(qubit_ref, bitstring[qid])


class AzureIonQQPUBackend(AzureIonQBackend):
    projectq_backend_name = "ionq_qpu"
    azure_target_name = "ionq.qpu"

    def __init__(
        self,
        workspace,
        num_runs=100,
        verbose=False,
        num_retries: int = 3000,
        interval: int = 1,
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ QPU backend"""
        logger.info("Initializing IonQQPUBackend for ProjectQ")

        super().__init__(
            workspace=workspace,
            use_hardware=True, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=self.projectq_backend_name,
            num_retries=num_retries,
            interval=interval,
            retrieve_execution=retrieve_execution
        )


class AzureIonQSimulatorBackend(AzureIonQBackend):
    projectq_backend_name = "ionq_simulator"
    azure_target_name = "ionq.simulator"

    def __init__(
        self,
        workspace,
        num_runs=100, 
        verbose=False,
        num_retries: int = 3000,
        interval: int = 1,
        retrieve_execution=None
    ):
        """Base class for interfacing with an IonQ Simulator backend"""
        logger.info("Initializing IonQSimulatorBackend for ProjectQ")

        super().__init__(
            use_hardware=False,
            workspace=workspace,
            num_runs=num_runs,
            verbose=verbose,
            device=self.projectq_backend_name,
            num_retries=num_retries,
            interval=interval,
            retrieve_execution=retrieve_execution
        )
