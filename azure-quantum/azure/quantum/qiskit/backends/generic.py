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
        target_profile: Optional[TargetProfile | str] = None,
        num_qubits: Optional[int] = None,
        description: Optional[str] = None,
        **kwargs: Any,
    ):
        self._provider_id = provider_id

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
                "azure": self._azure_config(),
            }
        )

        super().__init__(config, provider, **kwargs)

        # Prefer an instance-specific target profile discovered from the workspace target metadata.
        default_target_profile = self._coerce_target_profile(target_profile)
        if default_target_profile is not None:
            self.set_options(target_profile=default_target_profile)

    @staticmethod
    def _coerce_target_profile(
        value: Optional[TargetProfile | str],
    ) -> Optional[TargetProfile]:
        if value is None:
            return None
        if isinstance(value, TargetProfile):
            return value
        if not isinstance(value, str):
            return None

        raw = value.strip()
        if not raw:
            return None

        # Prefer the qsharp helper when available.
        from_str = getattr(TargetProfile, "from_str", None)
        if callable(from_str):
            try:
                parsed = from_str(raw)
                if isinstance(parsed, TargetProfile):
                    return parsed
            except Exception:
                pass

        # Best-effort: try enum attribute lookup.
        normalized = raw.replace("-", "_")
        return getattr(TargetProfile, normalized, None)

    @classmethod
    def _default_options(cls) -> Options:
        # Default to the most conservative QIR profile; users can override per-run via
        # `target_profile=` in backend.run(...).
        return Options(
            **{cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT},
            target_profile=TargetProfile.Base,
        )

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update({"provider_id": self._provider_id, "is_default": False})
        return config
