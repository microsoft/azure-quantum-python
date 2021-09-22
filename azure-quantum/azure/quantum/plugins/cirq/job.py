##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Dict, Sequence

if TYPE_CHECKING:
    import cirq
    from azure.quantum import Job as AzureJob


class Job:
    """
    Thin wrapper around an Azure Quantum Job that supports
    returning results in Cirq format.
    """
    def __init__(self, azure_job: "AzureJob", program: "cirq.Circuit"):
        """Construct a Job."""
        self._azure_job = azure_job
        self._program = program

    def job_id(self) -> str:
        """Returns the job id (UID) for the job."""
        return self._azure_job.id

    def status(self) -> str:
        """Gets the current status of the job."""
        self._azure_job.refresh()
        return self._azure_job.details.status

    def target(self) -> str:
        """Returns the target where the job was run."""
        return self._azure_job.details.target

    def name(self) -> str:
        """Returns the name of the job which was supplied during job creation."""
        return self._azure_job.details.name

    def num_qubits(self) -> int:
        """Returns the number of qubits for the job."""
        return self._azure_job.details.metadata["qubits"]

    def repetitions(self) -> int:
        """Returns the number of repetitions for the job."""
        return self._azure_job.details.metadata["repetitions"]

    def measurement_dict(self) -> Dict[str, Sequence[int]]:
        """Returns a dictionary of measurement keys to target qubit index."""
        from cirq import MeasurementGate
        measurements = [op for op in self._program.all_operations() if isinstance(op.gate, MeasurementGate)]
        return {
            meas.gate.key: [q.x for q in meas.qubits] for meas in measurements
        }

    def results(self, timeout_seconds: int = 7200) -> "cirq.Result":
        """Poll the Azure Quantum API for results."""
        return self._azure_job.get_results(timeout_secs=timeout_seconds)

    def cancel(self):
        """Cancel the given job."""
        self._azure_job.workspace.cancel_job(self._azure_job)

    def delete(self):
        """Delete the given job."""
        self._azure_job.workspace.cancel_job(self._azure_job)

    def __str__(self) -> str:
        return f'azure.quantum.cirq.Job(job_id={self.job_id()})'
