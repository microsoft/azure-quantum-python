##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit.providers import ProviderV1 as Provider

from azure.quantum import Workspace

from .job import AzureQuantumJob
from .backends import IonQSimulatorBackend, IonQQPUBackend

class AzureQuantumProvider(Provider):
    def __init__(self, workspace):
        self._backends = None
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
        azure_job = self._workspace.get_job(job_id)
        backend = self.get_backend(azure_job.details.target)
        return AzureQuantumJob(backend, azure_job)

    def _init_backends(self):
        self._backends = [
            IonQSimulatorBackend(self),
            IonQQPUBackend(self)
        ]