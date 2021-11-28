##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    from projectq import MainEngine as ProjectQMainEngine
    from projectq.backends import IonQBackend
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
    )

from azure.quantum import Workspace

from azure.quantum.projectq.job import AzureQuantumJob

PROJECTQ_USER_AGENT = "azure-quantum-projectq"


class AzureQuantumEngine(ProjectQMainEngine):
    def __init__(
        self, 
        backend=None, 
        engine_list=None, 
        verbose=False,
        workspace=None, 
        **kwargs
    ):
        super().__init__(
            backend=backend,
            engine_list=engine_list,
            verbose=verbose
        )

        if workspace is None:
            workspace = Workspace(**kwargs)

        workspace.append_user_agent(PROJECTQ_USER_AGENT)

        self._workspace = workspace

    def get_backend(self) -> IonQBackend:
        return self.backend

    def get_workspace(self) -> Workspace:
        return self._workspace

    def run(self, **kwargs) -> AzureQuantumJob:
        """Submits the circuit to run on associated backend."""
        return self.backend.run(kwargs)

    def get_job(self, job_id) -> AzureQuantumJob:
        """ Returns the Job instance associated with the given id."""
        backend = self.get_backend()
        azure_job = self._workspace.get_job(job_id)
        return AzureQuantumJob(backend, azure_job)
