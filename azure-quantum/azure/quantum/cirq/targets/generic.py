##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from __future__ import annotations

import ast
import cirq
import json
import re

# from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

from azure.quantum.cirq.job import Job as CirqJob
from azure.quantum.cirq.targets.target import Target as CirqTarget
from azure.quantum.target.target import QirRepresentable, Target as AzureTarget


if TYPE_CHECKING:
    from azure.quantum import Workspace
    from azure.quantum._client.models import TargetStatus


class _AzureCirqResultDict(cirq.ResultDict):
    __slots__ = ("raw_shots", "_measurement_dict", "_raw_measurements_cache")

    def __init__(
        self,
        *,
        params: "cirq.ParamResolver",
        measurements: Dict[str, "Any"],
        raw_shots: List[Any],
        measurement_dict: Dict[str, Sequence[int]],
    ) -> None:
        super().__init__(params=params, measurements=measurements)
        self.raw_shots = raw_shots
        self._measurement_dict = measurement_dict
        self._raw_measurements_cache = None

    def raw_measurements(self) -> Dict[str, Any]:
        """Return unfiltered per-shot measurement symbols.

        This is parsed from `raw_shots` using the same register splitting logic
        as the binary `measurements` field, but preserves non-binary markers
        (e.g. qubit loss symbols).

        The returned structure mirrors Cirq's `measurements` mapping:
        `{key: 2D array-like (shots x bits)}`.

        Note: These values are not guaranteed to be integer-convertible, so they
        should not be fed into Cirq tooling that assumes `{0,1}` bit data.
        """

        if self._raw_measurements_cache is not None:
            return self._raw_measurements_cache

        measurement_dict = self._measurement_dict or {"m": []}
        measurement_keys = list(measurement_dict.keys())
        key_lengths = [len(measurement_dict[k]) for k in measurement_keys]

        rows_by_key: Dict[str, List[List[str]]] = {k: [] for k in measurement_keys}
        for shot in self.raw_shots:
            bitstring = AzureGenericQirCirqTarget._qir_display_to_bitstring(shot)
            registers = AzureGenericQirCirqTarget._split_registers(
                bitstring, key_lengths
            )

            if len(registers) == len(measurement_keys):
                parts = registers
            else:
                flattened = "".join(registers)
                parts = AzureGenericQirCirqTarget._split_registers(
                    flattened, key_lengths
                )

            # Ensure a fixed-width row per key.
            for key_index, key in enumerate(measurement_keys):
                width = key_lengths[key_index]
                if width == 0:
                    rows_by_key[key].append([])
                    continue

                bits = parts[key_index] if key_index < len(parts) else ""
                chars = list(str(bits).strip())
                if len(chars) < width:
                    chars = chars + ([""] * (width - len(chars)))
                elif len(chars) > width:
                    chars = chars[:width]
                rows_by_key[key].append(chars)

        try:
            import numpy as np

            raw_meas = {
                k: np.asarray(v, dtype="<U1") if v else np.zeros((0, 0), dtype="<U1")
                for k, v in rows_by_key.items()
            }
        except Exception:
            raw_meas = rows_by_key

        self._raw_measurements_cache = raw_meas
        return raw_meas


class AzureGenericQirCirqTarget(AzureTarget, CirqTarget):
    """Fallback Cirq target that submits Cirq circuits via QIR.

    This target is synthesized dynamically by `AzureQuantumService` for workspace targets
    that do not have dedicated Cirq target classes.

    Translation pipeline:
    - Cirq circuit -> OpenQASM 3 (via `cirq.Circuit.to_qasm(version="3.0")`)
    - OpenQASM -> QIR (via `qsharp.openqasm.compile`)

    Dependencies: requires `qsharp` to be installed.
    """

    def __init__(
        self,
        workspace: "Workspace",
        name: str,
        *,
        provider_id: str,
        target_profile: Optional[str] = None,
        num_qubits: Optional[int] = None,
        **kwargs: Any,
    ):
        self._num_qubits = num_qubits
        super().__init__(
            workspace=workspace,
            name=name,
            provider_id=provider_id,
            input_data_format="qir.v1",
            output_data_format="microsoft.quantum-results.v2",
            content_type="qir.v1",
            target_profile=target_profile or "Base",
            **kwargs,
        )

    @classmethod
    def from_target_status(
        cls,
        workspace: "Workspace",
        provider_id: str,
        status: "TargetStatus",
        **kwargs: Any,
    ) -> "AzureGenericQirCirqTarget":
        return cls(
            workspace=workspace,
            name=status.id,
            provider_id=provider_id,
            target_profile=status.target_profile,
            num_qubits=status.num_qubits,
            average_queue_time=status.average_queue_time,
            current_availability=status.current_availability,
            **kwargs,
        )

    @staticmethod
    def _translate_cirq_circuit(circuit: "cirq.Circuit") -> QirRepresentable:
        try:
            from qsharp.openqasm import compile  # type: ignore
        except ImportError as exc:
            raise ImportError(
                "Generic Cirq-to-QIR submission requires the optional 'qsharp' dependency. "
                "Install with: pip install azure-quantum[cirq,qsharp]"
            ) from exc

        if cirq.is_parameterized(circuit):
            raise ValueError(
                "Cannot serialize a parameterized Cirq circuit to OpenQASM 3. "
                "Resolve parameters first (e.g. via cirq.resolve_parameters)."
            )

        qasm = circuit.to_qasm(version="3.0")

        return compile(qasm)

    @staticmethod
    def _measurement_dict(program: "cirq.Circuit") -> Dict[str, Sequence[int]]:
        import cirq

        ordered_qubits = sorted(program.all_qubits())
        index_by_qubit = {q: i for i, q in enumerate(ordered_qubits)}

        keys_in_order: List[str] = []
        key_to_qubits: Dict[str, List[int]] = {}
        for op in program.all_operations():
            if isinstance(op.gate, cirq.MeasurementGate):
                key = op.gate.key
                if key not in key_to_qubits:
                    keys_in_order.append(key)
                    key_to_qubits[key] = []
                key_to_qubits[key].extend(index_by_qubit[q] for q in op.qubits)

        return {k: key_to_qubits[k] for k in keys_in_order}

    def _to_cirq_job(self, azure_job, program: "cirq.Circuit" = None):
        measurement_dict = None
        try:
            measurement_dict_raw = (azure_job.details.metadata or {}).get(
                "measurement_dict"
            )
            if measurement_dict_raw is not None:
                measurement_dict = json.loads(measurement_dict_raw)
        except Exception:
            measurement_dict = None

        return CirqJob(
            azure_job=azure_job,
            program=program,
            measurement_dict=measurement_dict,
            target=self,
        )

    # Some backends emit verbose strings for individual qubit outcomes instead of
    # single-character values.  Map the known ones explicitly so they don't corrupt
    # the per-qubit register split.
    _SHOT_STRING_MAP: Dict[str, str] = {
        "Zero": "0",
        "False": "0",
        "One": "1",
        "True": "1",
        "Loss": "-",
    }

    @staticmethod
    def _qir_display_to_bitstring(obj: Any) -> str:
        if isinstance(obj, str):
            mapped = AzureGenericQirCirqTarget._SHOT_STRING_MAP.get(obj)
            if mapped is not None:
                return mapped

        if isinstance(obj, str) and not re.match(r"[\d\s]+$", obj):
            try:
                obj = ast.literal_eval(obj)
            except Exception:
                return str(obj)

        if isinstance(obj, tuple):
            return " ".join(
                AzureGenericQirCirqTarget._qir_display_to_bitstring(t) for t in obj
            )
        if isinstance(obj, list):
            return "".join(
                AzureGenericQirCirqTarget._qir_display_to_bitstring(bit) for bit in obj
            )
        return str(obj)

    @staticmethod
    def _split_registers(bitstring: str, key_lengths: List[int]) -> List[str]:
        raw = str(bitstring).strip()
        if " " in raw:
            return raw.split(" ")

        if not key_lengths:
            return [raw]

        total_len = sum(key_lengths)
        if total_len == len(raw):
            regs: List[str] = []
            start = 0
            for length in key_lengths:
                regs.append(raw[start : start + length])
                start += length
            return regs

        return [raw]

    @staticmethod
    def _shots_to_rows(
        shots: Sequence[Any],
        measurement_dict: Optional[Dict[str, Sequence[int]]] = None,
    ) -> Dict[str, List[List[int]]]:
        if measurement_dict is None:
            measurement_dict = {"m": []}

        measurement_keys = list(measurement_dict.keys())
        key_lengths = [len(measurement_dict[k]) for k in measurement_keys]

        shots_by_key: Dict[str, List[List[int]]] = {k: [] for k in measurement_keys}

        for shot in shots:
            bitstring = AzureGenericQirCirqTarget._qir_display_to_bitstring(shot)
            registers = AzureGenericQirCirqTarget._split_registers(
                bitstring, key_lengths
            )

            if len(registers) == len(measurement_keys):
                parts = registers
            else:
                flattened = "".join(registers)
                parts = AzureGenericQirCirqTarget._split_registers(
                    flattened, key_lengths
                )

            per_key_rows: Dict[str, List[int]] = {}
            is_valid_shot = True

            for key, bits in zip(measurement_keys, parts):
                bit_chars = list(str(bits).strip())
                if not all(ch in "01" for ch in bit_chars):
                    is_valid_shot = False
                    break
                per_key_rows[key] = [1 if ch == "1" else 0 for ch in bit_chars]

            if not is_valid_shot:
                continue

            for key in measurement_keys:
                shots_by_key[key].append(per_key_rows.get(key, []))

        return shots_by_key

    @staticmethod
    def _to_cirq_result(
        result: Any,
        param_resolver,
        measurement_dict: Optional[Dict[str, Sequence[int]]] = None,
        **_: Any,
    ):
        if not isinstance(result, list):
            raise ValueError(
                f"Unsupported result type for generic QIR Cirq target: {type(result)}"
            )

        import numpy as np

        normalized_measurement_dict = measurement_dict or {"m": []}

        shots_by_key = AzureGenericQirCirqTarget._shots_to_rows(
            shots=result,
            measurement_dict=normalized_measurement_dict,
        )

        measurement_keys = list(normalized_measurement_dict.keys())

        measurements: Dict[str, "np.ndarray"] = {}
        for key in measurement_keys:
            rows = shots_by_key.get(key, [])
            if not rows:
                measurements[key] = np.zeros((0, 0), dtype=np.int8)
            else:
                measurements[key] = np.asarray(rows, dtype=np.int8)

        return _AzureCirqResultDict(
            params=param_resolver,
            measurements=measurements,
            raw_shots=list(result),
            measurement_dict=normalized_measurement_dict,
        )

    def submit(
        self,
        program: "cirq.Circuit",
        name: str = "cirq-job",
        repetitions: int = 500,
        **kwargs: Any,
    ) -> CirqJob:
        qir_program = self._translate_circuit(program)

        measurement_dict = self._measurement_dict(program)
        metadata = {
            "cirq": str(True),
            "qubits": str(len(program.all_qubits())),
            "repetitions": str(repetitions),
            "measurement_dict": json.dumps(measurement_dict),
        }
        metadata.update(kwargs.get("metadata", {}))

        # Service-side validation expects metadata values to be strings.
        coerced_metadata: Dict[str, str] = {}
        for k, v in metadata.items():
            if v is None:
                continue
            if isinstance(v, str):
                coerced_metadata[k] = v
            elif isinstance(v, (dict, list)):
                coerced_metadata[k] = json.dumps(v)
            else:
                coerced_metadata[k] = str(v)
        metadata = coerced_metadata

        input_params = kwargs.pop("input_params", None) or {}

        azure_job = super().submit(
            qir_program,
            name=name,
            shots=repetitions,
            input_params=input_params,
            metadata=metadata,
            **kwargs,
        )

        return self._to_cirq_job(azure_job=azure_job, program=program)
