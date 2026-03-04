##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from __future__ import annotations

import ast
import json
import re

# from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

from azure.quantum.cirq.job import Job as CirqJob
from azure.quantum.cirq.targets.target import Target as CirqTarget
from azure.quantum.target.target import QirRepresentable, Target as AzureTarget


if TYPE_CHECKING:
    import cirq
    from azure.quantum import Workspace
    from azure.quantum._client.models import TargetStatus


class AzureGenericQirCirqTarget(AzureTarget, CirqTarget):
    """Fallback Cirq target that submits Cirq circuits via QIR.

    This target is synthesized dynamically by `AzureQuantumService` for workspace targets
    that do not have dedicated Cirq target classes.

    Translation pipeline:
    - Cirq circuit -> OpenQASM (via `cirq.Circuit.to_qasm()`)
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

        qasm = circuit.to_qasm()

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
        )

    @staticmethod
    def _qir_display_to_bitstring(obj: Any) -> str:
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
            return "".join(str(bit) for bit in obj)
        return str(obj)

    @staticmethod
    def _sample_histogram(
        histogram: Dict[str, float],
        repetitions: int,
        seed: Any = None,
    ) -> List[str]:
        import numpy as np

        if repetitions <= 0:
            return []

        items = list(histogram.items())
        keys = [k for k, _ in items]
        probs = np.array([float(p) for _, p in items], dtype=float)
        total = float(probs.sum())
        if total <= 0:
            raise ValueError("Result histogram has no probability mass.")
        probs = probs / total

        rng = (
            np.random.RandomState(seed) if seed is not None else np.random.RandomState()
        )
        draws = rng.choice(len(keys), size=repetitions, p=probs)
        return [keys[int(i)] for i in draws]

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
    def _to_cirq_result(
        result: Any,
        param_resolver,
        seed: Any = None,
        measurement_dict: Optional[Dict[str, Sequence[int]]] = None,
        repetitions: Optional[int] = None,
        **_: Any,
    ):
        import numpy as np
        import cirq

        if not isinstance(result, dict):
            raise ValueError(
                f"Unsupported result type for generic QIR Cirq target: {type(result)}"
            )

        histogram: Dict[str, float] = {str(k): float(v) for k, v in result.items()}

        if measurement_dict is None:
            measurement_dict = {"m": []}

        measurement_keys = list(measurement_dict.keys())
        key_lengths = [len(measurement_dict[k]) for k in measurement_keys]

        if repetitions is None:
            repetitions = 1

        sampled_displays = AzureGenericQirCirqTarget._sample_histogram(
            histogram, repetitions=repetitions, seed=seed
        )

        shots_by_key: Dict[str, List[List[int]]] = {k: [] for k in measurement_keys}

        for display in sampled_displays:
            bitstring = AzureGenericQirCirqTarget._qir_display_to_bitstring(display)
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

            for key, bits in zip(measurement_keys, parts):
                row = [1 if ch == "1" else 0 for ch in str(bits).strip()]
                shots_by_key[key].append(row)

        measurements: Dict[str, "np.ndarray"] = {}
        for key in measurement_keys:
            rows = shots_by_key.get(key, [])
            if not rows:
                measurements[key] = np.zeros((0, 0), dtype=np.int8)
            else:
                measurements[key] = np.asarray(rows, dtype=np.int8)

        return cirq.ResultDict(params=param_resolver, measurements=measurements)

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
