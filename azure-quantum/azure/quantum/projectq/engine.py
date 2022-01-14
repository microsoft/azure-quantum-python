##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    from projectq import MainEngine
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
    )

from azure.quantum import Workspace

from azure.quantum.projectq.job import AzureQuantumJob

PROJECTQ_USER_AGENT = "azure-quantum-projectq"


class AzureQuantumEngine(MainEngine):
    def __init__(
        self, 
        backend=None, 
        verbose=False,
        workspace=None, 
        **kwargs
    ):
        super().__init__(
            backend=backend,
            engine_list=backend.get_engine_list(),
            verbose=verbose
        )

        if workspace is None:
            workspace = Workspace(**kwargs)
            
        workspace.append_user_agent(PROJECTQ_USER_AGENT)
        
        self._workspace = workspace

    @property
    def workspace(self) -> Workspace:
        return self._workspace

    def get_backend(self):
        return self.backend

    def submit_job(self, name=None, **kwargs) -> AzureQuantumJob:
        """Submits the circuit to run on associated backend."""
        return self.backend.submit_job(name, **kwargs)

    def get_job(self, job_id) -> AzureQuantumJob:
        """Returns the Job instance associated with the given id."""
        azure_job = self._workspace.get_job(job_id)
        return AzureQuantumJob(self.backend, azure_job)
