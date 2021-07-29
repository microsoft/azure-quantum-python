##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    from qiskit.providers import JobV1, JobStatus
    from qiskit.result import Result
except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

from azure.quantum import Job

import logging
logger = logging.getLogger(__name__)

AzureJobStatusMap = {
    "Succeeded": JobStatus.DONE,
    "Waiting": JobStatus.QUEUED,
    "Executing": JobStatus.RUNNING,
    "Failed": JobStatus.ERROR,
    "Cancelled": JobStatus.CANCELLED,
}

class AzureQuantumJob(JobV1):
    def __init__(
        self,
        backend,
        azure_job=None,
        **kwargs
    ) -> None:
        """
            A Job running on Azure Quantum
        """
        if azure_job is None:
            azure_job = Job.from_input_data(
                workspace=backend.provider().get_workspace(),
                **kwargs
            )

        self._azure_job = azure_job
        self._workspace = backend.provider().get_workspace()

        super().__init__(backend, self._azure_job.id, **kwargs)

    def id(self):
        """ This job's id."""
        return self._azure_job.id

    def refresh(self):
        """ Refreshes the job metadata from the server."""
        return self._azure_job.refresh()

    def submit(self):
        """ Submits the job for execution. """
        self._azure_job.submit()
        return

    def result(self):
        """Return the results of the job."""
        azResult = self._azure_job.get_results()

        return Result(
            backend_name=self._backend.name(),
            backend_version=self._backend.version,
            qobj_id=self._azure_job.details.name,
            job_id=self._azure_job.details.id,
            success=True,
            results=azResult)

    def cancel(self):
        """Attempt to cancel the job."""
        self._workspace.cancel_job(self._azure_job)

    def status(self):
        """Return the status of the job, among the values of ``JobStatus``."""
        self._azure_job.refresh()
        return AzureJobStatusMap[self._azure_job.details.status]
