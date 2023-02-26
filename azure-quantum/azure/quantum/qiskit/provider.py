##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

try:
    from qiskit.providers import ProviderV1 as Provider
    from qiskit.providers.exceptions import QiskitBackendNotFoundError
    from qiskit.providers import BackendV1 as Backend
    from qiskit.exceptions import QiskitError
except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )


from typing import Dict, List, Tuple, Type
from azure.quantum import Workspace
from azure.quantum.qiskit.backends.backend import AzureBackendBase
from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.qiskit.backends import *
from itertools import groupby
import warnings

# Target ID keyword for parameter-free solvers
PARAMETER_FREE = "parameterfree"

QISKIT_USER_AGENT = "azure-quantum-qiskit"


class AzureQuantumProvider(Provider):
    def __init__(self, workspace=None, **kwargs):
        if workspace is None:
            workspace = Workspace(**kwargs)

        workspace.append_user_agent(QISKIT_USER_AGENT)

        self._workspace = workspace
        self._backends = None

    def get_workspace(self) -> Workspace:
        return self._workspace

    def get_backend(self, name=None, **kwargs):
        """Return a single backend matching the specified filtering.
        Args:
            name (str): name of the backend.
            **kwargs: dict used for filtering.
        Returns:
            Backend: a backend matching the filtering.
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
            list[Backend]: a list of Backends that match the filtering
                criteria.
        """

        # Lazy load backends
        if self._backends is None:
            self._backends = self._init_backends()

        if name:
            if name not in self._backends:
                raise QiskitBackendNotFoundError(
                    f"The '{name}' backend is not installed in your system."
                )

        provider_id = kwargs.get("provider_id", None)

        allowed_targets = self._get_allowed_targets_from_workspace(name, provider_id)

        workspace_allowed = lambda backend: self._is_available_in_ws(
            allowed_targets, backend
        )

        # flatten the available backends
        backend_list = [x for v in self._backends.values() for x in v]

        # filter by properties specified in the kwargs and filter function
        backends: List[Backend] = self._filter_backends(
            backend_list, filters=workspace_allowed, **kwargs
        )

        return backends

    def get_job(self, job_id) -> AzureQuantumJob:
        """Returns the Job instance associated with the given id."""
        azure_job = self._workspace.get_job(job_id)
        backend = self.get_backend(azure_job.details.target)
        return AzureQuantumJob(backend, azure_job)

    def _is_available_in_ws(
        self, allowed_targets: List[Tuple[str, str]], backend: Backend
    ):
        for name, provider in allowed_targets:
            if backend.name() == name:
                config = backend.configuration().to_dict()
                if "azure" in config and "provider_id" in config["azure"]:
                    if config["azure"]["provider_id"] == provider:
                        return True
        return False

    def _get_allowed_targets_from_workspace(
        self, name: str, provider_id: str
    ) -> List[Tuple[str, str]]:
        target_statuses = self._workspace._get_target_status(name, provider_id)
        candidates: List[Tuple[str, str]] = []
        for provider_id, status in target_statuses:
            candidates.append((status.id, provider_id))
        return candidates

    def _get_leaf_subclasses(self, subtype: Type[Backend]):
        subclasses = subtype.__subclasses__()
        if subclasses:
            for subclass in subclasses:
                for leaf in self._get_leaf_subclasses(subclass):
                    yield leaf
        else:
            yield subtype

    def _init_backends(self) -> Dict[str, List[Backend]]:
        instances: Dict[str, List[Backend]] = {}
        subclasses = list(self._get_leaf_subclasses(subtype=AzureBackendBase))

        for backend_cls in subclasses:
            backend_names = self._backend_names(backend_cls)
            if backend_names is None:
                continue

            for name in backend_names:
                backend_instance: Backend = self._get_backend_instance(
                    backend_cls, name
                )
                backend_name: str = backend_instance.name()
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

        def _match_all(obj, criteria):
            """Return True if all items in criteria matches items in obj."""
            return all(
                _match_config(obj, key_, value_) for key_, value_ in criteria.items()
            )

        def _match_config(obj, key, value):
            """Return True if the criteria matches the base config or azure config."""
            return getattr(obj, key, None) == value or _match_azure_config(
                obj, key, value
            )

        def _match_azure_config(obj, key, value):
            """Return True if the criteria matches the azure config."""
            azure_config = obj.to_dict().get("azure", {})
            return azure_config.get(key, None) == value

        def _has_config_value(obj, key):
            """Return True if the key is found in the root config or azure config."""
            return key in obj or key in obj.to_dict().get("azure", {})

        configuration_filters = {}
        unknown_filters = {}
        for key, value in kwargs.items():
            if all(
                _has_config_value(backend.configuration(), key) for backend in backends
            ):
                configuration_filters[key] = value
            else:
                unknown_filters[key] = value

        if configuration_filters:
            backends = list(
                filter(
                    lambda backend: _match_all(
                        backend.configuration(), configuration_filters
                    ),
                    backends,
                )
            )

        if unknown_filters:
            warnings.warn(
                f"Specified filters {unknown_filters} are not supported by the available backends."
            )

        backends = list(filter(filters, backends))
        
        if len(backends) > 1:
            def all_same(iterable):
                group_iter = groupby(iterable)
                return next(group_iter, True) and not next(group_iter, False)

            # If all backends have the same name, filter for default backend
            if all_same(backend.name() for backend in backends):
                backends = list(
                    filter(
                        lambda backend: _match_all(
                            backend.configuration(), {"is_default": True}
                        ),
                        backends,
                    )
                )
        return backends
