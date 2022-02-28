##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    from qiskit.providers import ProviderV1 as Provider
    from qiskit.providers.exceptions import QiskitBackendNotFoundError
except ImportError:
    raise ImportError(
    "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

from typing import Dict, Iterable
from azure.quantum import Workspace

from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.qiskit.backends import *

QISKIT_USER_AGENT = "azure-quantum-qiskit"


class AzureQuantumProvider(Provider):
    def __init__(self, workspace=None, **kwargs):
        self._backends = None
        if workspace is None:
            workspace = Workspace(**kwargs)

        workspace.append_user_agent(QISKIT_USER_AGENT)

        self._workspace = workspace

    def get_workspace(self) -> Workspace:
        return self._workspace

    def _get_all_subclasses(self, cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(self._get_all_subclasses(subclass))
        return all_subclasses

    def get_backend(self, name=None, **kwargs):
        """
        Return a single backend matching the specified filtering.
        """
        backends = self.backends(name, **kwargs)
        if len(backends) > 1:
            raise QiskitBackendNotFoundError("More than one backend matches the criteria")
        if not backends:
            raise QiskitBackendNotFoundError(f"Could not find target '{name}'. \
Please make sure the target name is valid and that the associated provider is added to your Workspace. \
To add a provider to your quantum workspace on the Azure Portal, \
see https://aka.ms/AQ/Docs/AddProvider")
        return backends[0]

    def backends(self, name=None, provider_id=None, **kwargs):
        """Return a list of backends matching the specified filtering.
        Args:
            name (str): name of the backend.
            **kwargs: dict used for filtering.
        Returns:
            list[Backend]: a list of Backends that match the filtering
                criteria.
        """
        from azure.quantum.target.target_factory import TargetFactory
        from qiskit.providers import BackendV1 as Backend
        from azure.quantum.qiskit.backends import DEFAULT_TARGETS

        all_targets = {
            name: _t for t in self._get_all_subclasses(Backend)
            for _t in [t]
            if hasattr(_t, "backend_names")
            for name in _t.backend_names
        }

        target_factory = TargetFactory(
            base_cls=Backend,
            workspace=self._workspace,
            default_targets=DEFAULT_TARGETS,
            all_targets=all_targets
        )

        targets = target_factory.get_targets(
            name=name,
            provider_id=provider_id,
            provider=self,
            **kwargs
        )

        # Always return an iterable
        if isinstance(targets, Iterable):
            return targets
        return [targets]

    def get_job(self, job_id) -> AzureQuantumJob:
        """ Returns the Job instance associated with the given id."""
        azure_job = self._workspace.get_job(job_id)
        backend = self.get_backend(azure_job.details.target)
        return AzureQuantumJob(backend, azure_job)
