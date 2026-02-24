##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

"""Offline-only Qiskit plugin tests.

These tests must not require Azure Quantum service access, recordings, or
environment configuration.

They are intended to be executed under tox across Qiskit major versions.
"""

from __future__ import annotations

from typing import Iterable, Set

import pytest


qiskit = pytest.importorskip("qiskit")
pytest.importorskip("azure.core")

from qiskit import QuantumCircuit, transpile

from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.qiskit.backends.backend import QIR_BASIS_GATES
from azure.quantum.qiskit.backends.generic import AzureGenericQirBackend
from azure.quantum.qiskit.backends.ionq import (
    IonQSimulatorBackend,
    IonQSimulatorQirBackend,
)
from azure.quantum.qiskit.provider import AzureQuantumProvider
from azure.quantum.job.base_job import BaseJob
from azure.quantum.qiskit.backends.quantinuum import (
    QuantinuumEmulatorBackend,
    QuantinuumEmulatorQirBackend,
)
from azure.quantum._client.models import TargetStatus

from mock_client import create_default_workspace, _paged

from types import SimpleNamespace


def _seed_workspace_target(
    monkeypatch: pytest.MonkeyPatch,
    ws,
    *,
    provider_id: str,
    target_id: str,
    num_qubits: int | None = None,
    target_profile: str | None = None,
) -> None:
    """Inject a provider+target into the offline Workspace mock.

    The Qiskit provider discovers targets via `Workspace._get_target_status()`,
    which iterates `ws._client.services.providers.list()`.
    """

    # `AzureQuantumProvider.__init__` appends a user agent to the Workspace, which
    # recreates the underlying client (and would wipe our patched providers.list).
    # For this offline-only test, keep the existing mock client.
    if hasattr(ws, "_connection_params") and hasattr(
        ws._connection_params, "on_new_client_request"
    ):
        ws._connection_params.on_new_client_request = None

    target_status = TargetStatus(
        {
            "id": target_id,
            "currentAvailability": "Available",
            "averageQueueTime": 0,
            "numQubits": num_qubits,
            "targetProfile": target_profile,
        }
    )
    provider = SimpleNamespace(id=provider_id, targets=[target_status])
    monkeypatch.setattr(
        ws._client.services.providers,
        "list",
        lambda *args, **kwargs: _paged([provider]),
    )


def _patch_upload_input_data(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fake_upload_input_data(
        *,
        container_uri: str,
        input_data: bytes,
        content_type=None,
        blob_name: str = "inputData",
        encoding: str = "",
        return_sas_token: bool = False,
    ) -> str:
        assert container_uri.startswith("https://example.com/")
        assert blob_name == "inputData"
        assert isinstance(input_data, (bytes, bytearray))
        return "https://example.com/inputData"

    monkeypatch.setattr(
        BaseJob, "upload_input_data", staticmethod(_fake_upload_input_data)
    )


def _target_op_names(backend) -> Set[str]:
    return {instruction.name for instruction in backend.target.operations}


def _circuit_op_names(circuit: QuantumCircuit) -> list[str]:
    return [instruction.operation.name for instruction in circuit.data]


def _assert_transpiled_ops_supported(
    backend, circuit: QuantumCircuit
) -> QuantumCircuit:
    transpiled = transpile(circuit, backend=backend, target=backend.target)

    target_ops = _target_op_names(backend)
    transpiled_ops = _circuit_op_names(transpiled)

    allowed_virtual_ops = {"barrier"}
    unsupported = {
        name
        for name in transpiled_ops
        if name not in target_ops and name not in allowed_virtual_ops
    }

    assert not unsupported, (
        f"Transpiled circuit for backend '{backend.name}' contains unsupported operations: "
        f"{sorted(unsupported)}"
    )
    return transpiled


def _build_non_qir_test_circuit() -> tuple[QuantumCircuit, Set[str]]:
    """Create a circuit that includes gates absent from `QIR_BASIS_GATES`.

    Returns the circuit plus the set of non-QIR operation names we expect
    transpilation to remove/decompose for QIR backends.
    """
    circuit = QuantumCircuit(2)
    # A mix of common gates that (depending on Qiskit version) are likely not
    # all in the QIR basis set.
    circuit.p(0.123, 0)
    circuit.cp(0.456, 0, 1)
    circuit.iswap(0, 1)
    circuit.rzx(0.789, 0, 1)
    circuit.measure_all()

    initial_ops = {
        instruction.operation.name
        for instruction in circuit.data
        if instruction.operation.name != "measure"
    }
    non_qir_ops = {
        name
        for name in initial_ops
        if name not in set(QIR_BASIS_GATES) and name != "barrier"
    }

    # Keep the test meaningful: if Qiskit changes and all gates become QIR-basis,
    # we should revisit this test.
    assert non_qir_ops

    return circuit, non_qir_ops


def test_qir_to_qiskit_bitstring_roundtrip():
    bits = "010011"
    azure_register = "[0,1,0,0,1,1]"
    assert AzureQuantumJob._qir_to_qiskit_bitstring(azure_register) == bits
    assert AzureQuantumJob._qir_to_qiskit_bitstring(bits) == bits


def test_ionq_qir_transpile_decomposes_non_qir_gates():
    backend = IonQSimulatorQirBackend(name="ionq.simulator", provider=None)
    circuit, non_qir_ops = _build_non_qir_test_circuit()

    transpiled = _assert_transpiled_ops_supported(backend, circuit)
    transpiled_ops = set(_circuit_op_names(transpiled))

    # Ensure the non-QIR ops were decomposed away.
    assert not (non_qir_ops & transpiled_ops)


def test_quantinuum_qir_transpile_removes_initialize():
    backend = QuantinuumEmulatorQirBackend(name="quantinuum.sim.h2-1e", provider=None)

    circuit = QuantumCircuit(1)
    circuit.initialize([0, 1], 0)

    transpiled = transpile(
        circuit, backend=backend, target=backend.target, optimization_level=2
    )
    transpiled_ops = _circuit_op_names(transpiled)

    assert "initialize" not in transpiled_ops
    # These are the expected primitive building blocks for the decomposition.
    assert "reset" in transpiled_ops
    assert "ry" in transpiled_ops


def test_quantinuum_transpile_supports_native_instructions():
    backend = QuantinuumEmulatorBackend(name="quantinuum.sim.h2-1e", provider=None)

    # Create simple instructions that should be native for this backend.
    from qiskit.circuit import Instruction

    circuit = QuantumCircuit(2)
    circuit.append(Instruction("v", 1, 0, []), [0])
    circuit.append(Instruction("vdg", 1, 0, []), [1])
    circuit.append(Instruction("zz", 2, 0, [0.5]), [0, 1])

    _assert_transpiled_ops_supported(backend, circuit)


def test_rigetti_transpile_supports_standard_gates():
    pytest.importorskip("qsharp")
    from azure.quantum.qiskit.backends.rigetti import RigettiSimulatorBackend
    from azure.quantum.target.rigetti import RigettiTarget

    backend = RigettiSimulatorBackend(name=RigettiTarget.QVM.value, provider=None)

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    _assert_transpiled_ops_supported(backend, circuit)


def test_ionq_backend_run_submits_job_details_offline(monkeypatch: pytest.MonkeyPatch):
    _patch_upload_input_data(monkeypatch)

    ws = create_default_workspace()
    provider = AzureQuantumProvider(workspace=ws)
    backend = IonQSimulatorBackend(name="ionq.simulator", provider=provider)

    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)

    job = backend.run(circuit, shots=123, foo="bar")
    job_id = job.id()

    # Assert via the mocked data-plane client store, similar to other local tests.
    details = ws._client.services.jobs.get(
        ws.subscription_id,
        ws.resource_group,
        ws.name,
        job_id,
    )

    assert details.provider_id == "ionq"
    assert details.target == "ionq.simulator"
    assert details.input_data_format == "ionq.circuit.v1"
    assert details.output_data_format == "ionq.quantum-results.v1"

    # Ensure shots are part of the request payload (input_params), not left in options.
    assert details.input_params["shots"] == 123

    # Unknown options are carried into metadata.
    assert details.metadata.get("foo") == "bar"

    # IonQ backend enriches metadata with a measurement map.
    assert "meas_map" in details.metadata


def test_backend_run_includes_latest_session_id(monkeypatch: pytest.MonkeyPatch):
    _patch_upload_input_data(monkeypatch)

    ws = create_default_workspace()
    provider = AzureQuantumProvider(workspace=ws)
    backend = IonQSimulatorBackend(name="ionq.simulator", provider=provider)

    # Ensure `AzureQuantumJob` passes the latest session id through.
    monkeypatch.setattr(backend, "get_latest_session_id", lambda: "s-ionq-1")

    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)

    job = backend.run(circuit, shots=1)
    details = ws._client.services.jobs.get(
        ws.subscription_id,
        ws.resource_group,
        ws.name,
        job.id(),
    )
    assert details.session_id == "s-ionq-1"


def test_quantinuum_request_construction_offline(monkeypatch: pytest.MonkeyPatch):
    _patch_upload_input_data(monkeypatch)

    ws = create_default_workspace()
    provider = AzureQuantumProvider(workspace=ws)
    backend = QuantinuumEmulatorBackend(name="quantinuum.sim.h2-1e", provider=provider)

    with pytest.warns(UserWarning, match="conflicts"):
        input_params = backend._get_input_params({"shots": 999}, shots=123)

    job = backend._run(
        job_name="offline-quantinuum",
        input_data=b"OPENQASM 2.0;",
        input_params=input_params,
        metadata={"meta": "value"},
        foo="bar",
    )

    details = ws._client.services.jobs.get(
        ws.subscription_id,
        ws.resource_group,
        ws.name,
        job.id(),
    )

    assert details.provider_id == "quantinuum"
    assert details.target == "quantinuum.sim.h2-1e"
    assert details.input_data_format == "honeywell.openqasm.v1"
    assert details.output_data_format == "honeywell.quantum-results.v1"
    assert details.input_params["shots"] == 123
    assert details.metadata.get("foo") == "bar"
    assert details.metadata.get("meta") == "value"


def test_rigetti_request_construction_offline(monkeypatch: pytest.MonkeyPatch):
    pytest.importorskip("qsharp")
    from azure.quantum.qiskit.backends.rigetti import RigettiSimulatorBackend
    from azure.quantum.target.rigetti import RigettiTarget

    _patch_upload_input_data(monkeypatch)

    ws = create_default_workspace()
    provider = AzureQuantumProvider(workspace=ws)
    backend = RigettiSimulatorBackend(name=RigettiTarget.QVM.value, provider=provider)

    with pytest.warns(UserWarning, match="subject to change"):
        input_params = backend._get_input_params({"shots": 10}, shots=None)

    job = backend._run(
        job_name="offline-rigetti",
        input_data=b"; QIR placeholder",
        input_params=input_params,
        metadata={},
        foo="bar",
    )

    details = ws._client.services.jobs.get(
        ws.subscription_id,
        ws.resource_group,
        ws.name,
        job.id(),
    )

    assert details.provider_id == "rigetti"
    assert details.input_data_format == "qir.v1"
    assert details.output_data_format == "microsoft.quantum-results.v2"
    assert details.input_params["shots"] == 10
    assert details.metadata.get("foo") == "bar"


def test_ionq_qir_request_construction_offline(monkeypatch: pytest.MonkeyPatch):
    _patch_upload_input_data(monkeypatch)

    ws = create_default_workspace()
    provider = AzureQuantumProvider(workspace=ws)
    backend = IonQSimulatorQirBackend(name="ionq.simulator", provider=provider)

    input_params = backend._get_input_params({}, shots=7)

    job = backend._run(
        job_name="offline-ionq-qir",
        input_data=b"; QIR placeholder",
        input_params=input_params,
        metadata={},
        foo="bar",
    )

    details = ws._client.services.jobs.get(
        ws.subscription_id,
        ws.resource_group,
        ws.name,
        job.id(),
    )

    assert details.provider_id == "ionq"
    assert details.target == "ionq.simulator"
    assert details.input_data_format == "qir.v1"
    assert details.output_data_format == "microsoft.quantum-results.v2"
    assert details.input_params["shots"] == 7
    assert details.metadata.get("foo") == "bar"


def test_non_qir_target_capability_raises(monkeypatch: pytest.MonkeyPatch):
    _patch_upload_input_data(monkeypatch)

    ws = create_default_workspace()
    provider = AzureQuantumProvider(workspace=ws)
    backend = IonQSimulatorBackend(name="ionq.simulator", provider=provider)

    with pytest.raises(ValueError, match="targetCapability"):
        backend._run(
            job_name="offline-ionq-invalid",
            input_data=b"{}",
            input_params={"targetCapability": "AdaptiveExecution"},
            metadata={},
        )


def test_qir_target_profile_from_deprecated_target_capability():
    pytest.importorskip("qsharp")
    from qsharp import TargetProfile

    backend = IonQSimulatorQirBackend(name="ionq.simulator", provider=None)

    with pytest.warns(DeprecationWarning):
        input_params = {"targetCapability": "AdaptiveExecution"}
        profile = backend._get_target_profile(input_params)

    assert profile == TargetProfile.Adaptive_RI
    assert "targetCapability" not in input_params

    input_params = {"target_profile": TargetProfile.Base}
    profile = backend._get_target_profile(input_params)
    assert profile == TargetProfile.Base
    assert "target_profile" not in input_params


def test_generic_qir_backend_created_for_unknown_workspace_target(
    monkeypatch: pytest.MonkeyPatch,
):
    _patch_upload_input_data(monkeypatch)

    ws = create_default_workspace()
    _seed_workspace_target(
        monkeypatch,
        ws,
        provider_id="acme",
        target_id="acme.qpu",
        num_qubits=5,
        target_profile="Adaptive_RI",
    )

    provider = AzureQuantumProvider(workspace=ws)
    backend = provider.get_backend("acme.qpu")

    assert isinstance(backend, AzureGenericQirBackend)

    from qsharp import TargetProfile

    assert backend.options.get("target_profile") == TargetProfile.Adaptive_RI

    # Avoid calling `backend.run()` (requires qsharp for QIR generation).
    input_params = backend._get_input_params({}, shots=11)
    job = backend._run(
        job_name="offline-generic",
        input_data=b"; QIR placeholder",
        input_params=input_params,
        metadata={},
    )

    details = ws._client.services.jobs.get(
        ws.subscription_id,
        ws.resource_group,
        ws.name,
        job.id(),
    )

    assert details.provider_id == "acme"
    assert details.target == "acme.qpu"
    assert details.input_data_format == "qir.v1"
    assert details.output_data_format == "microsoft.quantum-results.v2"
    assert details.input_params["shots"] == 11
