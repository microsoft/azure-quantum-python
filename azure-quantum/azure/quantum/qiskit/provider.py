##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import warnings
import inspect
from typing import Dict, List, Optional, Tuple, Type, Mapping, Any

from abc import ABC
from azure.quantum import Workspace

try:
    from qiskit.providers.exceptions import QiskitBackendNotFoundError
    from qiskit.providers import BackendV2 as Backend
    from qiskit.exceptions import QiskitError
except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

from azure.quantum.qiskit.backends.backend import AzureBackendBase
from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.qiskit.backends import *
from azure.quantum.qiskit.backends.generic import AzureGenericQirBackend
from azure.quantum._client.models import TargetStatus

QISKIT_USER_AGENT = "azure-quantum-qiskit"


class AzureQuantumProvider(ABC):
    def __init__(self, workspace: Optional[Workspace] = None, **kwargs):
        """Class for interfacing with the Azure Quantum service
        using Qiskit quantum circuits.

        :param workspace: Azure Quantum workspace. If missing it will create a new Workspace passing `kwargs` to the constructor. Defaults to None.
        :type workspace: Workspace
        """
        if kwargs is not None and len(kwargs) > 0:
            from warnings import warn

            warn(
                f"""Consider passing \"workspace\" argument explicitly. 
                 The ability to initialize AzureQuantumProvider with arguments {', '.join(f'"{argName}"' for argName in kwargs)} is going to be deprecated in future versions.""",
                DeprecationWarning,
                stacklevel=2,
            )

        if workspace is None:
            workspace = Workspace(**kwargs)

        workspace.append_user_agent(QISKIT_USER_AGENT)

        self._workspace = workspace
        self._backends = None

    def get_workspace(self) -> Workspace:
        """Return Azure Quantum Workspace"""

        return self._workspace

    def get_backend(self, name=None, **kwargs) -> AzureBackendBase:
        """Return a single backend matching the specified filtering.

        Args:
            name (str): name of the backend.
            **kwargs: dict used for filtering.
        Returns:
            azure.quantum.qiskit.backends.AzureBackendBase: a backend matching the filtering.
        Raises:
            QiskitBackendNotFoundError: if no backend could be found or
                more than one backend matches the filtering criteria.
        """

        backends = self.backends(name=name, **kwargs)

        if len(backends) > 1:
            raise QiskitBackendNotFoundError(
                "More than one backend matches the criteria"
            )
        if not backends:
            raise QiskitBackendNotFoundError(
                f"Could not find target '{name}'. \
Please make sure the target name is valid and that the associated provider is added to your Workspace. \
To add a provider to your quantum workspace on the Azure Portal, \
see https://aka.ms/AQ/Docs/AddProvider"
            )
        return backends[0]

    def backends(self, name=None, **kwargs):
        """Return a list of backends matching the specified filtering.

        Args:
            name (str): name of the backend.
            **kwargs: dict used for filtering.
        Returns:
            typing.List[azure.quantum.qiskit.backends.AzureBackendBase]: a list of Backends that match the filtering
                criteria.
        """

        # Lazy load backends
        if self._backends is None:
            self._backends = self._init_backends()

        provider_id = kwargs.get("provider_id", None)

        # Query targets available in the workspace. We'll use this both for workspace
        # filtering and to synthesize fallback backends for targets without dedicated
        # Qiskit backend classes.
        status_by_target = self._get_workspace_target_status_map(name, provider_id)
        allowed_targets: List[Tuple[str, str]] = list(status_by_target.keys())

        # If a user asks for a specific backend name and it isn't installed,
        # raise a clear error. With generic backends, a name can still be valid
        # even if it isn't installed, as long as the target exists in the workspace.
        if name and name not in self._backends and not allowed_targets:
            provider_clause = f" for provider_id '{provider_id}'" if provider_id else ""
            raise QiskitBackendNotFoundError(
                f"The '{name}' backend is not installed in your system, nor is it a valid target{provider_clause} in your Azure Quantum workspace."
            )

        workspace_allowed = lambda backend: self._is_available_in_ws(
            allowed_targets, backend
        )

        # flatten the available backends
        backend_list = [x for v in self._backends.values() for x in v]

        # Add a generic QIR backend for targets that exist in the workspace but are
        # missing from the installed backend classes.
        existing_pairs = set()
        for backend in backend_list:
            try:
                config = backend.configuration().to_dict()
            except Exception:
                continue
            azure_cfg = config.get("azure", {}) or {}
            existing_pairs.add((backend.name, azure_cfg.get("provider_id")))

        for target_id, pid in allowed_targets:
            if (target_id, pid) in existing_pairs:
                continue
            status = status_by_target.get((target_id, pid))
            backend_list.append(
                AzureGenericQirBackend(
                    name=target_id,
                    provider=self,
                    provider_id=pid,
                    target_profile=(
                        status.target_profile if status is not None else None
                    ),
                    num_qubits=status.num_qubits if status is not None else None,
                )
            )

        # filter by properties specified in the kwargs and filter function
        filtered_backends: List[Backend] = self._filter_backends(
            backend_list, filters=workspace_allowed, **kwargs
        )

        # Also filter out non-default backends.
        default_backends = list(
            filter(
                lambda backend: self._match_all(
                    backend.configuration().to_dict(), {"is_default": True}
                ),
                filtered_backends,
            )
        )
        # If default backends were found - return them, otherwise return the filtered_backends collection.
        # The latter case could happen where there's no default backend defined for the specified target.
        if len(default_backends) > 0:
            return default_backends

        return filtered_backends

    def get_job(self, job_id) -> AzureQuantumJob:
        """Returns the Job instance associated with the given id.

        Args:
            job_id (str): Id of the Job to return.
        Returns:
            AzureQuantumJob: Job instance.
        """
        azure_job = self._workspace.get_job(job_id)
        backend = self.get_backend(azure_job.details.target)
        return AzureQuantumJob(backend, azure_job)

    def _is_available_in_ws(
        self, allowed_targets: List[Tuple[str, str]], backend: Backend
    ):
        for name, provider in allowed_targets:
            if backend.name == name:
                config = backend.configuration().to_dict()
                if "azure" in config and "provider_id" in config["azure"]:
                    if config["azure"]["provider_id"] == provider:
                        return True
        return False

    def _get_workspace_target_status_map(
        self, name: Optional[str] = None, provider_id: Optional[str] = None
    ) -> Dict[Tuple[str, str], TargetStatus]:
        """Return workspace targets keyed by (target_id, provider_id).

        This is a thin wrapper over `Workspace._get_target_status` that preserves
        the full status objects so callers can read metadata (e.g. num qubits)
        without needing additional workspace queries.
        """
        target_statuses = self._workspace._get_target_status(name, provider_id)
        by_target: Dict[Tuple[str, str], TargetStatus] = {}
        for pid, status in target_statuses:
            by_target[(status.id, pid)] = status
        return by_target

    def _get_candidate_subclasses(self, subtype: Type[Backend]):
        if not inspect.isabstract(subtype):
            yield subtype

        subclasses = subtype.__subclasses__()
        if subclasses:
            for subclass in subclasses:
                for leaf in self._get_candidate_subclasses(subclass):
                    yield leaf

    def _init_backends(self) -> Dict[str, List[Backend]]:
        instances: Dict[str, List[Backend]] = {}
        subclasses = list(self._get_candidate_subclasses(subtype=AzureBackendBase))

        for backend_cls in subclasses:
            backend_names = self._backend_names(backend_cls)
            if backend_names is None:
                continue

            for name in backend_names:
                backend_instance: Backend = self._get_backend_instance(
                    backend_cls, name
                )
                backend_name: str = backend_instance.name
                instances.setdefault(backend_name, []).append(backend_instance)

        return instances

    def _backend_names(self, backend_cls: Type[Backend]) -> List[str]:
        if hasattr(backend_cls, "backend_names"):
            return list(backend_cls.backend_names)
        return None

    def _get_backend_instance(self, backend_cls: Type[Backend], name: str) -> Backend:
        try:
            return backend_cls(name=name, provider=self)
        except Exception as err:
            raise QiskitError(
                f"Backend {backend_cls} could not be instantiated: {err}"
            ) from err

    def _match_all(self, obj, criteria):
        """Return True if all items in criteria matches items in obj."""
        return all(
            self._match_config(obj, key_, value_) for key_, value_ in criteria.items()
        )

    def _match_config(self, obj, key, value):
        """Return True if the criteria matches the base config or azure config."""
        return obj.get(key, None) == value or self._match_azure_config(obj, key, value)

    def _match_azure_config(self, obj, key, value):
        """Return True if the criteria matches the azure config."""
        azure_config = obj.get("azure", {})
        return azure_config.get(key, None) == value

    def _has_config_value(self, obj, key):
        """Return True if the key is found in the root config or azure config."""
        return key in obj or key in obj.get("azure", {})

    def _filter_backends(
        self, backends: List[Backend], filters=None, **kwargs
    ) -> List[Backend]:
        """Return the backends matching the specified filtering.
        Filter the `backends` list by their `configuration` attributes,
        or from a boolean callable. The criteria for filtering can
        be specified via `**kwargs` or as a callable via `filters`, and the
        backends must fulfill all specified conditions.

        Args:
            backends (list[Backend]): list of backends.
            filters (callable): filtering conditions as a callable.
            **kwargs: dict of criteria.
        Returns:
            list[Backend]: a list of backend instances matching the
                conditions.
        """

        configuration_filters = {}
        unknown_filters = {}
        for key, value in kwargs.items():
            # If `any` of the backends has the key in its configuration, filter by it.
            # qiskit API for this requires `all` backends to have the key in
            # their configuration to be considered for filtering
            print(f"Looking for {key} with {value}")
            if any(
                self._has_config_value(backend.configuration().to_dict(), key)
                for backend in backends
            ):
                configuration_filters[key] = value
            else:
                unknown_filters[key] = value

        if configuration_filters:
            backends = list(
                filter(
                    lambda backend: self._match_all(
                        backend.configuration().to_dict(), configuration_filters
                    ),
                    backends,
                )
            )

        if unknown_filters:
            warnings.warn(
                f"Specified filters {unknown_filters} are not supported by the available backends."
            )

        backends = list(filter(filters, backends))

        return backends

    def __eq__(self, other):
        """
        Equality comparison.
        """
        return type(self).__name__ == type(other).__name__
