##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from azure.quantum import Job

import logging
logger = logging.getLogger(__name__)

# Constants for providers
IONQ_PROVIDER = "ionq"
HONEYWELL_PROVIDER = "honeywell"

# Constants for input data format
IONQ_INPUT_DATA_FORMAT = "ionq.circuit.v1"
HONEYWELL_INPUT_DATA_FORMAT = "honeywell.openqasm.v1"

# Constants for output data format
IONQ_OUTPUT_DATA_FORMAT = "ionq.quantum-results.v1"
HONEYWELL_OUTPUT_DATA_FORMAT = "honeywell.quantum-results.v1"


class AzureQuantumJob:
    def __init__(
        self,
        backend,
        azure_job=None,
        **kwargs
    ):
        """A Job running on Azure Quantum. """
        if azure_job is None:
            azure_job = Job.from_input_data(
                workspace=backend.main_engine.workspace,
                **kwargs
            )

        self._backend = backend
        self._azure_job = azure_job
        self._workspace = backend.main_engine.workspace

    def id(self):
        """ This job's id."""
        return self._azure_job.id

    def job_id(self):
        """ This job's id."""
        return self._azure_job.id

    def refresh(self):
        """ Refreshes the job metadata from the server."""
        return self._azure_job.refresh()

    def submit(self):
        """ Submits the job for execution. """
        self._azure_job.submit()

    def result(self, timeout_secs=None):
        """Return the results of the job."""
        self._azure_job.wait_until_completed(timeout_secs=timeout_secs)

        az_result = self._azure_job.get_results()
        return az_result

    def cancel(self):
        """Attempt to cancel the job."""
        self._workspace.cancel_job(self._azure_job)

    def status(self):
        """Return the status of the job, among the values of ``JobStatus``."""
        self.refresh()
        return self._azure_job.details.status

    def __str__(self) -> str:
        return f'azure.quantum.projectq.Job(job_id={self.job_id()})'
