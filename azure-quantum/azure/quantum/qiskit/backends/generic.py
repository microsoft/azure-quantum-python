##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from azure.quantum.version import __version__

try:
    from qiskit.providers import Options
    from qsharp import TargetProfile
except ImportError as exc:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    ) from exc

from .backend import AzureBackendConfig, AzureQirBackend

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider


_DEFAULT_SHOTS_COUNT = 500


class AzureGenericQirBackend(AzureQirBackend):
    """Fallback QIR backend for arbitrary Azure Quantum workspace targets.

    This backend is created dynamically by :class:`~azure.quantum.qiskit.provider.AzureQuantumProvider`
    for targets present in the workspace that do not have a dedicated Qiskit backend class.

    It submits Qiskit circuits using QIR (`qir.v1`) payloads.
    """

    _SHOTS_PARAM_NAME = "shots"

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        *,
        provider_id: str,
        num_qubits: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs: Any,
    ):
        self._provider_id = provider_id

        azure_config: Dict[str, Any] = self._azure_config()
        azure_config.update({"provider_id": provider_id, "is_default": False})

        config = AzureBackendConfig.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": description
                or f"Azure Quantum target '{name}' (generic QIR backend)",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": num_qubits,
                "conditional": False,
                "max_shots": None,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": azure_config,
            }
        )

        super().__init__(config, provider, **kwargs)

    @classmethod
    def _default_options(cls) -> Options:
        # Default to the most conservative QIR profile; users can override per-run via
        # `target_profile=` in backend.run(...).
        return Options(
            **{cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT},
            target_profile=TargetProfile.Base,
        )
