##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from __future__ import annotations

from unittest.mock import Mock

import pytest


def _freeze_workspace_client_recreation(ws) -> None:
    """Prevent WorkspaceMock from recreating (and wiping) its mock client.

    Cirq service/targets append user-agent strings which can trigger
    `Workspace._on_new_client_request()`.
    """

    if hasattr(ws, "_connection_params") and hasattr(
        ws._connection_params, "on_new_client_request"
    ):
        ws._connection_params.on_new_client_request = None


class _FakeQirProgram:
    _name = "Fake.EntryPoint"

    def _repr_qir_(self, target=None):
        return b"FAKE-QIR"


def _patch_offline_submission(
    monkeypatch: pytest.MonkeyPatch, *, assert_container_uri: bool = False
):
    """Patch blob upload + QIR translation so submission stays offline."""

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget
    from azure.quantum.job.base_job import BaseJob

    def _fake_upload_input_data(
        *,
        container_uri: str,
        input_data: bytes,
        content_type=None,
        blob_name: str = "inputData",
        encoding: str = "",
        return_sas_token: bool = False,
    ) -> str:
        if assert_container_uri:
            assert container_uri.startswith("https://example.com/")
            assert blob_name == "inputData"
            assert isinstance(input_data, (bytes, bytearray))
        return "https://example.com/inputData"

    monkeypatch.setattr(
        BaseJob, "upload_input_data", staticmethod(_fake_upload_input_data)
    )
    monkeypatch.setattr(
        AzureGenericQirCirqTarget,
        "_translate_cirq_circuit",
        staticmethod(lambda c: _FakeQirProgram()),
    )
    return None


def test_cirq_generic_from_target_status_sets_defaults():
    pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    ws = Mock()
    ws.append_user_agent = Mock()

    status = Mock()
    status.id = "foo.qir.target"
    status.target_profile = "Base"
    status.num_qubits = 4
    status.average_queue_time = 0
    status.current_availability = "Available"

    target = AzureGenericQirCirqTarget.from_target_status(ws, "foo", status)

    assert target.name == "foo.qir.target"
    assert target.provider_id == "foo"
    assert target.input_data_format == "qir.v1"
    assert target.output_data_format == "microsoft.quantum-results.v2"
    assert str(target.content_type) == "qir.v1"


def test_cirq_generic_to_cirq_result_from_structured_shots():
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    measurement_dict = {"a": [0, 1], "b": [2]}
    shots = [([0, 1], [1]), ([1, 0], [0])]

    result = AzureGenericQirCirqTarget._to_cirq_result(
        result=shots,
        param_resolver=cirq.ParamResolver({}),
        measurement_dict=measurement_dict,
    )

    assert isinstance(result, cirq.ResultDict)
    np.testing.assert_array_equal(
        result.measurements["a"], np.asarray([[0, 1], [1, 0]], dtype=np.int8)
    )
    np.testing.assert_array_equal(
        result.measurements["b"], np.asarray([[1], [0]], dtype=np.int8)
    )


def test_cirq_generic_to_cirq_result_from_string_encoded_shots():
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    measurement_dict = {"a": [0, 1], "b": [2]}
    shots = ["([0, 1], [1])", "([1, 0], [0])"]

    result = AzureGenericQirCirqTarget._to_cirq_result(
        result=shots,
        param_resolver=cirq.ParamResolver({}),
        measurement_dict=measurement_dict,
    )

    np.testing.assert_array_equal(
        result.measurements["a"], np.asarray([[0, 1], [1, 0]], dtype=np.int8)
    )
    np.testing.assert_array_equal(
        result.measurements["b"], np.asarray([[1], [0]], dtype=np.int8)
    )


def test_cirq_generic_to_cirq_result_from_flat_bitstring_shots():
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    measurement_dict = {"a": [0, 1], "b": [2]}
    shots = ["011", "100"]

    result = AzureGenericQirCirqTarget._to_cirq_result(
        result=shots,
        param_resolver=cirq.ParamResolver({}),
        measurement_dict=measurement_dict,
    )

    np.testing.assert_array_equal(
        result.measurements["a"], np.asarray([[0, 1], [1, 0]], dtype=np.int8)
    )
    np.testing.assert_array_equal(
        result.measurements["b"], np.asarray([[1], [0]], dtype=np.int8)
    )


def test_cirq_generic_to_cirq_result_from_space_delimited_shots():
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    measurement_dict = {"a": [0, 1], "b": [2]}
    shots = ["01 1", "10 0"]

    result = AzureGenericQirCirqTarget._to_cirq_result(
        result=shots,
        param_resolver=cirq.ParamResolver({}),
        measurement_dict=measurement_dict,
    )

    np.testing.assert_array_equal(
        result.measurements["a"], np.asarray([[0, 1], [1, 0]], dtype=np.int8)
    )
    np.testing.assert_array_equal(
        result.measurements["b"], np.asarray([[1], [0]], dtype=np.int8)
    )


def test_cirq_generic_to_cirq_result_default_measurement_key():
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    shots = [[0, 1], [1, 0]]

    result = AzureGenericQirCirqTarget._to_cirq_result(
        result=shots,
        param_resolver=cirq.ParamResolver({}),
        measurement_dict=None,
    )

    np.testing.assert_array_equal(
        result.measurements["m"], np.asarray([[0, 1], [1, 0]], dtype=np.int8)
    )


def test_cirq_generic_to_cirq_result_drops_non_binary_shots_and_exposes_raw():
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    # Some targets may return non-binary outcomes (e.g., qubit loss markers).
    measurement_dict = {"m": [0]}
    shots = [".", "1", "0", "2", "-"]

    result = AzureGenericQirCirqTarget._to_cirq_result(
        result=shots,
        param_resolver=cirq.ParamResolver({}),
        measurement_dict=measurement_dict,
    )

    # Only binary outcomes are kept in the Cirq measurements.
    np.testing.assert_array_equal(
        result.measurements["m"],
        np.asarray([[1], [0]], dtype=np.int8),
    )

    # Raw shots remain available for loss/invalid inspection.
    assert result.raw_shots == shots

    raw_meas = result.raw_measurements()
    assert set(raw_meas.keys()) == {"m"}
    np.testing.assert_array_equal(
        raw_meas["m"],
        np.asarray([["."], ["1"], ["0"], ["2"], ["-"]], dtype="<U1"),
    )


def test_cirq_generic_to_cirq_result_non_binary_shots_filtered_and_raw_preserved():
    """Non-binary shots are excluded from measurements[] but kept in raw_shots.

    Known backend-specific outcome strings ("Loss", "True", "False", "One", "Zero")
    are mapped to their single-character equivalents before register splitting.
    Single-char non-binary markers like "." pass through unchanged.
    """
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    measurement_dict = {"m": [0]}
    # "Loss" -> mapped to "-"
    # "."    -> preserved as "."
    # "1"/"0" -> binary, appear in measurements
    shots = ["Loss", ".", "1", "0"]

    result = AzureGenericQirCirqTarget._to_cirq_result(
        result=shots,
        param_resolver=cirq.ParamResolver({}),
        measurement_dict=measurement_dict,
    )

    # Only binary outcomes in measurements.
    np.testing.assert_array_equal(
        result.measurements["m"],
        np.asarray([[1], [0]], dtype=np.int8),
    )

    # Original shot objects kept verbatim in raw_shots.
    assert result.raw_shots == shots

    # raw_measurements: "Loss" -> "-", "." -> ".", binary values unchanged.
    raw_meas = result.raw_measurements()
    np.testing.assert_array_equal(
        raw_meas["m"],
        np.asarray([["-"], ["."], ["1"], ["0"]], dtype="<U1"),
    )


def test_cirq_generic_qir_display_to_bitstring_unexpected_scalar_becomes_loss_marker():
    """Only the literal string 'Loss' gets special-cased to the loss marker.
    All other strings follow normal procedure: digit strings bypass
    ast.literal_eval; non-digit strings are evaled or returned verbatim.
    """
    pytest.importorskip("cirq")

    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    fn = AzureGenericQirCirqTarget._qir_display_to_bitstring

    # Digit strings bypass ast.literal_eval entirely.
    assert fn("0") == "0"
    assert fn("1") == "1"
    assert fn("011") == "011"

    # Non-digit strings that fail literal_eval are returned verbatim.
    assert fn(".") == "."
    assert fn("-") == "-"
    assert fn("1.1") == "1.1"  # evaluated to float 1.1, str() -> "1.1"
    assert fn(".1.0.1") == ".1.0.1"  # fails eval, returned as-is
    assert fn("-10") == "-10"  # evals to int -10, str() -> "-10"
    assert fn("1-0-1") == "1-0-1"  # fails eval, returned as-is

    # Known multi-character per-qubit outcome strings are mapped explicitly.
    assert fn("Zero") == "0"
    assert fn("False") == "0"
    assert fn("One") == "1"
    assert fn("True") == "1"
    assert fn("Loss") == "-"

    # List elements are processed recursively, so special-case strings inside
    # a list are also mapped correctly.
    assert fn(["Zero", "Loss", "Loss"]) == "0--"
    assert fn(["One", "Zero", "One"]) == "101"


def test_cirq_service_targets_excludes_non_qir_target():
    """Targets without a target_profile (e.g. Pasqal) must not be wrapped as
    AzureGenericQirCirqTarget — they use pulse-level input formats incompatible
    with QIR submission.
    """
    pytest.importorskip("cirq")
    pytest.importorskip("cirq_ionq")

    from azure.quantum.cirq.service import AzureQuantumService
    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

    from mock_client import create_default_workspace

    ws = create_default_workspace()
    _freeze_workspace_client_recreation(ws)
    service = AzureQuantumService(workspace=ws)

    targets = service.targets()
    target_names = [t.name for t in targets]

    # The Pasqal target (target_profile=None) should be completely absent.
    assert not any(
        "pasqal" in name for name in target_names
    ), f"Non-QIR Pasqal target unexpectedly appeared in service.targets(): {target_names}"
    # Specifically, no AzureGenericQirCirqTarget should have been created for it.
    assert not any(
        isinstance(t, AzureGenericQirCirqTarget) and "pasqal" in t.name for t in targets
    )
    # QIR-capable targets should still be present.
    assert any("microsoft.estimator" in name for name in target_names)


def test_cirq_service_targets_discovers_provider_specific_and_generic_wrappers(
    monkeypatch: pytest.MonkeyPatch,
):
    pytest.importorskip("cirq")
    pytest.importorskip("cirq_ionq")

    from azure.quantum.cirq.service import AzureQuantumService
    from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget
    from azure.quantum.cirq.targets.ionq import IonQTarget
    from azure.quantum.cirq.targets.quantinuum import QuantinuumTarget

    from mock_client import create_default_workspace

    ws = create_default_workspace()
    _freeze_workspace_client_recreation(ws)
    service = AzureQuantumService(workspace=ws)

    targets = service.targets()
    assert any(isinstance(t, QuantinuumTarget) for t in targets)
    assert any(isinstance(t, IonQTarget) for t in targets)
    assert any(isinstance(t, AzureGenericQirCirqTarget) for t in targets)

    assert isinstance(
        service.targets(name="quantinuum.sim", provider_id="quantinuum"),
        QuantinuumTarget,
    )
    assert isinstance(
        service.targets(name="microsoft.estimator", provider_id="microsoft"),
        AzureGenericQirCirqTarget,
    )


def test_cirq_service_submit_to_generic_wrapped_target_creates_job(
    monkeypatch: pytest.MonkeyPatch,
):
    cirq = pytest.importorskip("cirq")
    pytest.importorskip("cirq_ionq")

    from azure.quantum.cirq.job import Job as CirqJob
    from azure.quantum.cirq.service import AzureQuantumService

    from mock_client import create_default_workspace

    ws = create_default_workspace()
    _freeze_workspace_client_recreation(ws)
    service = AzureQuantumService(workspace=ws)

    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="m"),
    )

    _patch_offline_submission(monkeypatch, assert_container_uri=True)
    job = service.create_job(
        program=circuit,
        repetitions=3,
        name="generic-cirq-job",
        target="microsoft.estimator",
    )

    assert isinstance(job, CirqJob)
    assert job.azure_job.details.target == "microsoft.estimator"
    assert job.azure_job.details.provider_id == "microsoft"
    assert job.measurement_dict() == {"m": [0, 1]}

    metadata = job.azure_job.details.metadata or {}
    assert str(metadata.get("cirq", "")).strip().lower() == "true"
    assert all(isinstance(v, str) for v in metadata.values())


def test_cirq_service_get_job_returns_cirq_job_wrapper_for_generic_target(
    monkeypatch: pytest.MonkeyPatch,
):
    cirq = pytest.importorskip("cirq")
    pytest.importorskip("cirq_ionq")

    from azure.quantum.cirq.job import Job as CirqJob
    from azure.quantum.cirq.service import AzureQuantumService

    from mock_client import create_default_workspace

    ws = create_default_workspace()
    _freeze_workspace_client_recreation(ws)
    service = AzureQuantumService(workspace=ws)

    q0 = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.X(q0), cirq.measure(q0, key="m"))

    _patch_offline_submission(monkeypatch)
    submitted = service.create_job(
        program=circuit,
        repetitions=1,
        name="generic-cirq-job",
        target="microsoft.estimator",
    )

    fetched = service.get_job(submitted.job_id())
    assert isinstance(fetched, CirqJob)
    assert fetched.job_id() == submitted.job_id()
    assert fetched.azure_job.details.target == "microsoft.estimator"
    assert str(fetched.azure_job.details.metadata.get("cirq")).lower() == "true"


def test_cirq_job_results_converts_generic_target_shots(
    monkeypatch: pytest.MonkeyPatch,
):
    np = pytest.importorskip("numpy")
    cirq = pytest.importorskip("cirq")
    pytest.importorskip("cirq_ionq")

    from azure.quantum.cirq.service import AzureQuantumService

    from mock_client import create_default_workspace

    ws = create_default_workspace()
    _freeze_workspace_client_recreation(ws)
    service = AzureQuantumService(workspace=ws)

    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="m"),
    )

    _patch_offline_submission(monkeypatch)
    job = service.create_job(
        program=circuit,
        repetitions=3,
        name="generic-cirq-job",
        target="microsoft.estimator",
    )

    # Avoid any blob downloads; provide per-shot results directly.
    monkeypatch.setattr(
        job.azure_job, "get_results_shots", lambda *a, **k: ["01", "10", "00"]
    )

    result = job.results()
    assert isinstance(result, cirq.ResultDict)
    np.testing.assert_array_equal(
        result.measurements["m"],
        np.asarray([[0, 1], [1, 0], [0, 0]], dtype=np.int8),
    )


def test_cirq_to_qasm_supports_openqasm3_program():
    cirq = pytest.importorskip("cirq")

    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="m"),
    )

    qasm = circuit.to_qasm(version="3.0")

    # Cirq's exporter may include a leading comment header.
    assert "OPENQASM 3.0;" in qasm
    assert 'include "stdgates.inc";' in qasm
    assert "qubit[2] q;" in qasm
    assert "h q[0];" in qasm
    assert "cx q[0],q[1];" in qasm
    assert "measure q[0];" in qasm
    assert "measure q[1];" in qasm


def test_cirq_ionq_serializer_api_compatibility():
    cirq = pytest.importorskip("cirq")
    pytest.importorskip("cirq_ionq")

    from azure.quantum.cirq.targets.ionq import IonQTarget

    q0 = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.X(q0), cirq.measure(q0, key="m"))

    serialized = IonQTarget._translate_cirq_circuit(circuit)

    assert hasattr(serialized, "body")
    assert isinstance(serialized.body, dict)
    assert "qubits" in serialized.body


def test_cirq_ionq_to_cirq_result_accepts_singleton_list():
    cirq = pytest.importorskip("cirq")
    pytest.importorskip("cirq_ionq")

    from cirq_ionq.results import SimulatorResult
    from azure.quantum.cirq.targets.ionq import IonQTarget

    sim_result = SimulatorResult(
        probabilities={0: 0.5, 1: 0.5},
        num_qubits=1,
        measurement_dict={"m": [0]},
        repetitions=10,
    )

    cirq_result = IonQTarget._to_cirq_result(
        [sim_result], param_resolver=cirq.ParamResolver({})
    )
    assert hasattr(cirq_result, "measurements")
