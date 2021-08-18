##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    from qiskit.providers import ProviderV1 as Provider
except ImportError:
    raise ImportError(
    "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

from azure.quantum import Workspace
from azure.quantum.plugins.qiskit.backends.honeywell import (
    HoneywellSimulatorBackend
)

from azure.quantum.plugins.qiskit.job import AzureQuantumJob
from azure.quantum.plugins.qiskit.backends import (
    IonQSimulatorBackend,
    IonQQPUBackend,
    HoneywellQPUBackend,
    HoneywellAPIValidatorBackend
)

class AzureQuantumProvider(Provider):
    def __init__(self, workspace = None, **kwargs):
        self._backends = None
        if workspace is None:
            kwargs.setdefault('user_agent', 'azure-quantum-qiskit')
            workspace = Workspace(**kwargs)

        self._workspace = workspace

    def get_workspace(self) -> Workspace:
        return self._workspace

    def backends(self, name=None, **kwargs):
        """Return a list of backends matching the specified filtering.
        Args:
            name (str): name of the backend.
            **kwargs: dict used for filtering.
        Returns:
            list[Backend]: a list of Backends that match the filtering
                criteria.
        """
        if not self._backends:
            self._init_backends()

        if not name:
            return [backend for backend in self._backends]

        return [backend for backend in self._backends if backend.name() == name]

    def get_job(self, job_id) -> AzureQuantumJob:
        """ Returns the Job instance associated with the given id."""
        azure_job = self._workspace.get_job(job_id)
        backend = self.get_backend(azure_job.details.target)
        return AzureQuantumJob(backend, azure_job)

    def _init_backends(self):
        backends = [
            IonQSimulatorBackend,
            IonQQPUBackend,
            HoneywellQPUBackend,
            HoneywellAPIValidatorBackend,
            HoneywellSimulatorBackend
        ]

        targets = [
            target.get("id") for targets in self._workspace.get_targets().values()
            for target in targets]
        self._backends = [
            cls(self) for cls in backends if cls.backend_name in targets
        ]
