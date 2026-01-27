##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict, List, Tuple, Union
import unittest
import warnings
import random
import json
import pytest
import numpy as np

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.providers import JobStatus
from qiskit.providers import BackendV2 as Backend
from qiskit.providers import Options
from qiskit.providers.exceptions import QiskitBackendNotFoundError

# from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS
# from test_workspace import SIMPLE_RESOURCE_ID
from local.common import (
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
)

from azure.quantum.workspace import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from azure.quantum.qiskit.job import (
    MICROSOFT_OUTPUT_DATA_FORMAT,
    MICROSOFT_OUTPUT_DATA_FORMAT_V2,
    AzureQuantumJob,
)
from azure.quantum.qiskit.backends.backend import (
    AzureBackend,
    AzureBackendConfig,
    AzureQirBackend,
    _ensure_backend_config,
    QIR_BASIS_GATES,
)
from qiskit.circuit import Instruction
from qiskit.circuit.library import UGate, U1Gate, U2Gate, U3Gate

from azure.quantum.qiskit.backends.quantinuum import (
    QuantinuumEmulatorBackend,
    QuantinuumEmulatorQirBackend,
    QuantinuumQirBackendBase,
)
from azure.quantum.qiskit.backends.ionq import (
    IonQSimulatorNativeBackend,
    IonQSimulatorQirBackend,
)
from azure.quantum.qiskit.backends._qiskit_ionq import (
    IonQGateError,
)
from azure.quantum.qiskit.backends.qci import QCISimulatorBackend
from azure.quantum.qiskit.backends.rigetti import RigettiSimulatorBackend
from azure.quantum.target.rigetti import RigettiTarget
from azure.quantum._constants import ConnectionConstants


_HEADER_MISSING = object()
DEFAULT_TIMEOUT_SECS = 300
SIMPLE_RESOURCE_ID = ConnectionConstants.VALID_RESOURCE_ID(
    subscription_id=SUBSCRIPTION_ID,
    resource_group=RESOURCE_GROUP,
    workspace_name=WORKSPACE,
)


def _get_header_field(header: Any, key: str, default: Any = _HEADER_MISSING) -> Any:
    # Helper to read ExperimentResult.header across Qiskit 1.x and 2.x shapes.
    if header is None:
        return default
    if isinstance(header, dict):
        return header.get(key, default)
    if hasattr(header, key):
        return getattr(header, key)
    if hasattr(header, "to_dict"):
        header_dict = header.to_dict()
        if isinstance(header_dict, dict):
            return header_dict.get(key, default)
    return default


def _header_has_field(header: Any, key: str) -> bool:
    return _get_header_field(header, key) is not _HEADER_MISSING


# This provider is used to stub out calls to the AzureQuantumProvider
# There are live tests that use the available backends in the workspace
# This provider is used to test the Qiskit plugin without making any
# calls to Azure and just allows for filtering on the backends with the
# given name for installed local backends and filtering criteria.
class DummyProvider(AzureQuantumProvider):
    def __init__(self, workspace=None, **kwargs):
        self._available_in_ws = kwargs.get("available_in_ws", True)
        self._backends = None
        # don't init the parent class, we aren't going to use it
        # super().__init__(workspace, **kwargs)

    # Used to stub out calls to getting available targets
    def _get_allowed_targets_from_workspace(
        self, name: str, provider_id: str
    ) -> List[Tuple[str, str]]:
        backend_list = [x for v in self._backends.values() for x in v]
        selection = []
        for backend in backend_list:
            if backend.name == name:
                selection.append(
                    (name, backend.configuration().to_dict()["azure"]["provider_id"])
                )
        return selection

    # Used to stub out calls to filtering available targets
    def _is_available_in_ws(
        self, allowed_targets: List[Tuple[str, str]], backend: Backend
    ):
        # only return true if the backend name is in the list of allowed targets
        return any(
            tup
            for tup in allowed_targets
            if tup[0] == backend.name
            and tup[1] == backend.configuration().to_dict()["azure"]["provider_id"]
        )


class NoopQirBackend(AzureQirBackend):
    def __init__(
        self,
        configuration: AzureBackendConfig,
        provider: "AzureQuantumProvider",
        **fields,
    ):
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": fields.pop("name", "sample"),
                "backend_version": fields.pop("version", "1.0"),
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "Simple backend for testing",
                "basis_gates": [],
                "memory": True,
                "n_qubits": 11,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": fields.pop("max_experiments", 1),
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(fields.pop("output_data_format", None)),
            }
        )

        configuration = _ensure_backend_config(
            fields.pop("configuration", default_config)
        )

        super().__init__(configuration=configuration, provider=provider, **fields)

    def run(
        self, run_input: Union[QuantumCircuit, List[QuantumCircuit]] = [], **options
    ):
        return self._normalize_run_input_params(run_input, **options)

    def _azure_config(self, output_data_format=None) -> Dict[str, str]:
        values = {
            "blob_name": "inputData",
            "content_type": "qir.v1",
            "input_data_format": "qir.v1",
        }
        if output_data_format:
            values["output_data_format"] = output_data_format
        return values

    def _default_options(cls):
        return Options()

    def _translate_input(
        self, circuit: QuantumCircuit, input_params: Dict[str, Any]
    ) -> bytes:
        return None


class NoopPassThruBackend(AzureBackend):
    def __init__(
        self,
        configuration: AzureBackendConfig,
        provider: "AzureQuantumProvider",
        **fields,
    ):
        default_config = AzureBackendConfig.from_dict(
            {
                "backend_name": fields.pop("name", "sample"),
                "backend_version": fields.pop("version", "1.0"),
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "Simple backend for testing",
                "basis_gates": [],
                "memory": False,
                "n_qubits": 11,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": fields.pop("max_experiments", 1),
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(fields),
            }
        )

        configuration = _ensure_backend_config(
            fields.pop("configuration", default_config)
        )
        super().__init__(configuration=configuration, provider=provider, **fields)

    def run(self, run_input=None, **kwargs):
        return self._normalize_run_input_params(run_input, **kwargs)

    def _azure_config(self, fields) -> Dict[str, str]:
        return fields

    def _default_options(cls):
        return Options()

    def _translate_input(self, circuit):
        return None


class TestQiskit(unittest.TestCase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """

    def _3_qubit_ghz(self):
        circuit = QuantumCircuit(4, 3)
        circuit.name = "Qiskit Sample - 3-qubit GHZ circuit"
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.cx(1, 2)
        circuit.h(3)  # Helper qubit that is not measured
        circuit.measure([0, 1, 2], [0, 1, 2])
        return circuit

    def _5_qubit_superposition(self):
        circuit = QuantumCircuit(5, 1)
        for q in range(5):
            circuit.h(q)
        circuit.measure([0], [0])
        return circuit

    def _assert_transpile_respects_target(
        self,
        backend,
        circuit: QuantumCircuit,
        expected_ops: set[str] | None = None,
        **kwargs,
    ) -> QuantumCircuit:
        """Transpile ``circuit`` for ``backend`` and assert only supported gates remain.

        Parameters
        ----------
        backend:
            The Azure Quantum backend under test whose ``Target`` defines the
            supported operation set.
        circuit: QuantumCircuit
            The input circuit to transpile.
        expected_ops: set[str] | None
            Optional collection of gate names that must appear in the
            transpiled output.

        Returns
        -------
        QuantumCircuit
            The transpiled circuit, validated to contain only target-supported
            operations (aside from virtual barriers).
        """
        transpiled_circuit = transpile(
            circuit, backend=backend, target=backend.target, **kwargs
        )

        target_ops = {instruction.name for instruction in backend.target.operations}
        transpiled_ops = [
            instruction.operation.name for instruction in transpiled_circuit.data
        ]

        allowed_virtual_ops = {"barrier"}
        unsupported = {
            name
            for name in transpiled_ops
            if name not in target_ops and name not in allowed_virtual_ops
        }
        self.assertFalse(
            unsupported,
            msg=(
                f"Transpiled circuit for backend '{backend.name}' contains unsupported "
                f"operations: {sorted(unsupported)}"
            ),
        )

        if expected_ops:
            missing = set(expected_ops) - set(transpiled_ops)
            self.assertFalse(
                missing,
                msg=(
                    f"Transpiled circuit for backend '{backend.name}' is missing expected "
                    f"operations: {sorted(missing)}, found: {sorted(transpiled_ops)}"
                ),
            )

        return transpiled_circuit

    def _build_non_qir_test_circuit(self) -> Tuple[QuantumCircuit, set[str]]:
        """Create a circuit exercising gates absent from ``QIR_BASIS_GATES``.

        Returns
        -------
        Tuple[QuantumCircuit, set[str]]
            A two-qubit circuit populated with standard gates not listed in the
            QIR basis, along with the set of those non-QIR gate names. The
            helper fails if no such gates are present, ensuring test coverage
            stays meaningful.
        """
        circuit = QuantumCircuit(2)
        circuit.append(UGate(np.pi / 3, np.pi / 5, np.pi / 7), [0])
        circuit.append(U1Gate(np.pi / 9), [0])
        circuit.append(U2Gate(np.pi / 8, np.pi / 6), [1])
        circuit.append(U3Gate(np.pi / 4, np.pi / 3, np.pi / 2), [1])
        circuit.p(np.pi / 7, 0)
        circuit.cp(np.pi / 6, 0, 1)
        circuit.iswap(0, 1)
        circuit.rzx(np.pi / 5, 0, 1)
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
        self.assertTrue(
            non_qir_ops,
            "Non-QIR gates should be present in the test circuit before transpilation.",
        )
        return circuit, non_qir_ops

    def _assert_qir_transpile_decomposes_non_qir_gates(self, backend) -> set[str]:
        """Ensure QIR transpilation removes all non-QIR gates for ``backend``.

        Parameters
        ----------
        backend:
            The QIR backend whose transpilation behavior is being validated.

        Returns
        -------
        set[str]
            The set of operation names found in the transpiled circuit,
            guaranteed not to intersect with the generated non-QIR gate set.
        """
        circuit, non_qir_ops = self._build_non_qir_test_circuit()
        transpiled = self._assert_transpile_respects_target(backend, circuit)
        transpiled_ops = {instruction.operation.name for instruction in transpiled.data}
        intersection = non_qir_ops & transpiled_ops
        self.assertFalse(
            intersection,
            msg=(
                f"Transpiled circuit for backend '{backend.name}' contains non-QIR gates "
                f"that should have been decomposed: {sorted(intersection)}"
            ),
        )
        return transpiled_ops

    def _controlled_s(self):
        circuit = QuantumCircuit(3)
        circuit.t(0)
        circuit.t(1)
        circuit.cx(0, 1)
        circuit.tdg(1)
        circuit.cx(0, 1)
        return circuit

    def test_provider_uses_lightweight_backend_config(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            config = backend.configuration()

        self.assertIsInstance(config, AzureBackendConfig)
        self.assertEqual("ionq.simulator", config.backend_name)

        # Returned copies should be isolated from the internal state.
        azure_copy = config.get("azure")
        azure_copy["provider_id"] = "mutated"
        self.assertEqual("ionq", config.azure["provider_id"])

        basis_copy = config.get("basis_gates")
        basis_copy.append("__sentinel__")
        self.assertNotIn("__sentinel__", config.basis_gates)

        target_ops = {instruction.name for instruction in backend.target.operations}
        self.assertIn("measure", target_ops)
        self.assertIn("reset", target_ops)

    def test_qir_backend_config_aliases_num_qubits(self):
        backend = IonQSimulatorQirBackend(
            name="ionq.simulator", provider=DummyProvider()
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            config = backend.configuration()

        self.assertIsInstance(config, AzureBackendConfig)
        # The alias should surface the recorded qubit count.
        self.assertEqual(29, config.num_qubits)

        config.num_qubits = 31
        self.assertEqual(31, config.n_qubits)

        output_format = backend._get_output_data_format({})
        self.assertEqual(MICROSOFT_OUTPUT_DATA_FORMAT_V2, output_format)

        target_ops = {instruction.name for instruction in backend.target.operations}
        self.assertTrue({"measure", "reset"}.issubset(target_ops))

    def test_unnamed_run_input_passes_through(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run("default"), "default")
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run("default"), "default")

    def test_named_run_input_passes_through(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run(run_input="default"), "default")
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run(run_input="default"), "default")

    def test_named_circuit_passes_through(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run(circuit="default"), "default")
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run(circuit="default"), "default")

    def test_both_named_circuit_and_run_input_chooses_run_input(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run(run_input="a", circuit="b"), "a")
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        self.assertEqual(backend.run(run_input="a", circuit="b"), "a")

    def test_no_input_raises(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        with pytest.raises(ValueError) as exc_info:
            backend.run()
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        with pytest.raises(ValueError) as exc_info:
            backend.run()

    def test_empty_input_raises(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        with pytest.raises(ValueError) as exc_info:
            backend.run([])
        with pytest.raises(ValueError) as exc_info:
            backend.run(run_input=[])
        with pytest.raises(ValueError) as exc_info:
            backend.run(circuit=[])
        with pytest.raises(ValueError) as exc_info:
            backend.run(run_input=[], circuit=[])
        with pytest.raises(ValueError) as exc_info:
            backend.run([], circuit=[])

        backend = NoopQirBackend(None, "AzureQuantumProvider")
        with pytest.raises(ValueError) as exc_info:
            backend.run([])
        with pytest.raises(ValueError) as exc_info:
            backend.run(run_input=[])
        with pytest.raises(ValueError) as exc_info:
            backend.run(circuit=[])
        with pytest.raises(ValueError) as exc_info:
            backend.run(run_input=[], circuit=[])
        with pytest.raises(ValueError) as exc_info:
            backend.run([], circuit=[])

    def test_qir_to_qiskit_bitstring(self):
        bits = random.choices(["0", "1"], k=50)
        bitstring = "".join(bits)
        azure_register = f"[{','.join(bits)}]"
        azure_registers = ",".join(f"[{bit}, 1, 0]" for bit in bits)

        self.assertEqual(
            AzureQuantumJob._qir_to_qiskit_bitstring(azure_register), bitstring
        )
        self.assertEqual(
            AzureQuantumJob._qir_to_qiskit_bitstring(azure_registers),
            " ".join(f"{bit}10" for bit in bits),
        )
        self.assertEqual(AzureQuantumJob._qir_to_qiskit_bitstring(bitstring), bitstring)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_qiskit_submit_ionq_5_qubit_superposition(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("ionq.simulator")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)
        shots = 1000

        circuit = self._5_qubit_superposition()
        circuit.metadata = {"some": "data"}

        qiskit_job = backend.run(circuit, shots=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "ionq.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "ionq")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "qir.v1")
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            MICROSOFT_OUTPUT_DATA_FORMAT_V2,
        )
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertAlmostEqual(result.data()["counts"]["0"], shots // 2, delta=50)
            self.assertAlmostEqual(result.data()["counts"]["1"], shots // 2, delta=50)
            self.assertEqual(result.data()["probabilities"], {"0": 0.5, "1": 0.5})
            counts = result.get_counts()
            self.assertEqual(counts, result.data()["counts"])
            header = result.results[0].header
            num_qubits = _get_header_field(header, "num_qubits")
            self.assertEqual(str(num_qubits), "5")
            metadata = _get_header_field(header, "metadata", {})
            self.assertEqual(metadata.get("some"), "data")

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_qiskit_submit_ionq_5_qubit_superposition_passthrough(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend(
            "ionq.simulator", input_data_format="ionq.circuit.v1", gateset="qis"
        )
        shots = 1000

        circuit = self._5_qubit_superposition()
        circuit.metadata = {"some": "data"}

        qiskit_job = backend.run(circuit, shots=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "ionq.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "ionq")
        self.assertEqual(
            qiskit_job._azure_job.details.input_data_format, "ionq.circuit.v1"
        )
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format, "ionq.quantum-results.v1"
        )
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("meas_map", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertAlmostEqual(result.data()["counts"]["0"], shots // 2, delta=50)
            self.assertAlmostEqual(result.data()["counts"]["1"], shots // 2, delta=50)
            self.assertEqual(result.data()["probabilities"], {"0": 0.5, "1": 0.5})
            counts = result.get_counts()
            self.assertEqual(counts, result.data()["counts"])
            header = result.results[0].header
            num_qubits = _get_header_field(header, "num_qubits")
            self.assertEqual(str(num_qubits), "5")
            metadata = _get_header_field(header, "metadata", {})
            self.assertEqual(metadata.get("some"), "data")

    def test_qiskit_provider_init_with_workspace_not_raises_deprecation(self):
        # testing warning according to https://docs.python.org/3/library/warnings.html#testing-warnings
        import warnings

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Try to trigger a warning.
            workspace = self.create_workspace_with_params(resource_id=SIMPLE_RESOURCE_ID)
            AzureQuantumProvider(workspace)

            warns = [
                warn
                for warn in w
                if 'Consider passing "workspace" argument explicitly.'
                in warn.message.args[0]
            ]

            # Verify
            assert len(warns) == 0

    def test_qiskit_provider_init_without_workspace_raises_deprecation(self):
        # testing warning according to https://docs.python.org/3/library/warnings.html#testing-warnings
        from unittest.mock import patch
        
        # Create mock mgmt_client to avoid ARM calls
        mock_mgmt_client = self.create_mock_mgmt_client()
        
        with patch('azure.quantum.workspace.WorkspaceMgmtClient', return_value=mock_mgmt_client):
            with warnings.catch_warnings(record=True) as w:
                # Cause all warnings to always be triggered.
                warnings.simplefilter("always")
                # Try to trigger a warning.
                AzureQuantumProvider(resource_id=SIMPLE_RESOURCE_ID)

                warns = [
                    warn
                    for warn in w
                    if 'Consider passing "workspace" argument explicitly.'
                    in warn.message.args[0]
                ]

                # Verify
                assert len(warns) == 1
                assert issubclass(warns[0].category, DeprecationWarning)

            # Validate rising deprecation warning even if workspace is passed, but other parameters are also passed
            with warnings.catch_warnings(record=True) as w:
                # Cause all warnings to always be triggered.
                warnings.simplefilter("always")
                # Try to trigger a warning.
                workspace = Workspace(
                    resource_id=SIMPLE_RESOURCE_ID,
                    _mgmt_client=mock_mgmt_client)

                AzureQuantumProvider(
                    workspace=workspace, resource_id=SIMPLE_RESOURCE_ID
                )

                warns = [
                    warn
                    for warn in w
                    if 'Consider passing "workspace" argument explicitly.'
                    in warn.message.args[0]
                ]

                # Verify
                assert len(warns) == 1
                assert issubclass(warns[0].category, DeprecationWarning)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq(circuit)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_circuit_as_list_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq([circuit])

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_ionq(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("ionq.simulator")

        with pytest.raises(NotImplementedError) as exc:
            backend.run(circuit=[circuit, circuit], shots=500)
        self.assertEqual(
            str(exc.value),
            "This backend only supports running a single circuit per job.",
        )

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_qobj_to_ionq(self):
        import qiskit

        if not qiskit.__version__.startswith("1."):
            self.skipTest(
                "Qiskit 2.0 removes Qobj support; skipping assemble coverage."
            )
            return

        from qiskit import assemble

        circuit = self._3_qubit_ghz()
        qobj = assemble(circuit)
        self._test_qiskit_submit_ionq_passthrough(circuit=qobj, shots=1024)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_qiskit_qir_submit_ionq(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = IonQSimulatorQirBackend("ionq.simulator", provider)
        input_params = backend._get_input_params({})

        payload = backend._translate_input(circuit, input_params)
        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        output_data_format = backend._get_output_data_format()

        self.assertIsInstance(payload, bytes)
        self.assertEqual(input_data_format, "qir.v1")
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT_V2)
        self.assertIn("items", input_params)
        self.assertEqual(len(input_params["items"]), 1)
        item = input_params["items"][0]
        self.assertIn("entryPoint", item)
        self.assertIn("arguments", item)

        shots = 100

        qiskit_job = backend.run(circuit, shots=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "ionq.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "ionq")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "qir.v1")
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            MICROSOFT_OUTPUT_DATA_FORMAT_V2,
        )
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertAlmostEqual(result.data()["counts"]["000"], shots // 2, delta=20)
            self.assertAlmostEqual(result.data()["counts"]["111"], shots // 2, delta=20)
            self.assertEqual(result.data()["probabilities"], {"000": 0.5, "111": 0.5})
            counts = result.get_counts()
            memory = result.get_memory()

            self.assertEqual(len(memory), shots)
            self.assertTrue(all([shot == "000" or shot == "111" for shot in memory]))
            self.assertEqual(counts, result.data()["counts"])

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq_passthrough(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq_passthrough(circuit)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_circuit_as_list_to_ionq_passthrough(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq_passthrough([circuit])

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_ionq_passthrough(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend(
            "ionq.simulator", input_data_format="ionq.circuit.v1", gateset="qis"
        )

        with pytest.raises(NotImplementedError) as exc:
            backend.run(circuit=[circuit, circuit], shots=500)
        self.assertEqual(str(exc.value), "Multi-experiment jobs are not supported!")

    def _qiskit_wait_to_complete(
        self, qiskit_job, provider, expected_status=JobStatus.DONE
    ):
        job = qiskit_job._azure_job
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertEqual(expected_status, qiskit_job.status())
        qiskit_job = provider.get_job(job.id)
        self.assertEqual(expected_status, qiskit_job.status())

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq_with_shots_param(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)

        shots = 10
        qiskit_job = backend.run(circuit, shots=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq_with_default_shots(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)

        qiskit_job = backend.run(circuit)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], 500)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq_with_deprecated_count_param(self):
        """
        Verify that a warning message is printed when the 'count' option is specified.
        This option was allowed in earlier versions, but now it is accepted only to keep existing
        user codebase compatible.
        """
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)

        shots = 10

        with pytest.warns(
            DeprecationWarning,
            match="The 'count' parameter will be deprecated. Please, use 'shots' parameter instead.",
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq_with_shots_param_passthrough(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            "ionq.simulator", input_data_format="ionq.circuit.v1", gateset="qis"
        )

        shots = 10
        qiskit_job = backend.run(circuit, shots=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq_with_default_shots_passthrough(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            "ionq.simulator", input_data_format="ionq.circuit.v1", gateset="qis"
        )

        qiskit_job = backend.run(circuit)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], 500)

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_submit_qiskit_to_ionq_with_deprecated_count_param_passthrough(
        self,
    ):
        """
        Verify that a warning message is printed when the 'count' option is specified.
        This option was allowed in earlier versions, but now it is accepted only to keep existing
        user codebase compatible.
        """
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            "ionq.simulator", input_data_format="ionq.circuit.v1", gateset="qis"
        )

        shots = 10

        with pytest.warns(
            DeprecationWarning,
            match="The 'count' parameter will be deprecated. Please, use 'shots' parameter instead.",
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)

    def _test_qiskit_submit_ionq(self, circuit, **kwargs):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("ionq.simulator")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)
        expected_data_format = (
            kwargs["input_data_format"] if "input_data_format" in kwargs else "qir.v1"
        )

        shots = kwargs.get("shots", backend.options.shots)

        qiskit_job = backend.run(circuit, **kwargs)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "ionq.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "ionq")
        self.assertEqual(
            qiskit_job._azure_job.details.input_data_format, expected_data_format
        )
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            MICROSOFT_OUTPUT_DATA_FORMAT_V2,
        )
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertAlmostEqual(result.data()["counts"]["000"], shots // 2, delta=50)
            self.assertAlmostEqual(result.data()["counts"]["111"], shots // 2, delta=50)
            self.assertEqual(result.data()["probabilities"], {"000": 0.5, "111": 0.5})
            counts = result.get_counts()
            self.assertEqual(counts, result.data()["counts"])
            header = result.results[0].header
            self.assertTrue(_header_has_field(header, "num_qubits"))
            self.assertTrue(_header_has_field(header, "metadata"))

    def _test_qiskit_submit_ionq_passthrough(self, circuit, **kwargs):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend(
            "ionq.simulator", input_data_format="ionq.circuit.v1", gateset="qis"
        )

        expected_data_format = (
            kwargs["input_data_format"]
            if "input_data_format" in kwargs
            else "ionq.circuit.v1"
        )

        shots = kwargs.get("shots", backend.options.shots)

        qiskit_job = backend.run(circuit, **kwargs)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "ionq.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "ionq")
        self.assertEqual(
            qiskit_job._azure_job.details.input_data_format, expected_data_format
        )
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format, "ionq.quantum-results.v1"
        )
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)
        self.assertIn("meas_map", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertAlmostEqual(result.data()["counts"]["000"], shots // 2, delta=50)
            self.assertAlmostEqual(result.data()["counts"]["111"], shots // 2, delta=50)
            self.assertEqual(result.data()["probabilities"], {"000": 0.5, "111": 0.5})
            counts = result.get_counts()
            self.assertEqual(counts, result.data()["counts"])
            header = result.results[0].header
            self.assertTrue(_header_has_field(header, "num_qubits"))
            self.assertTrue(_header_has_field(header, "metadata"))

    @pytest.mark.live_test
    def test_provider_returns_only_default_backends(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backends = provider.backends()

        # Check that all names are unique
        backend_names = [b.name for b in backends]
        assert sorted(set(backend_names)) == sorted(backend_names)

        # Also check that all backends are default
        for b in backends:
            backend_config = b.configuration().to_dict()

            is_default_key_name = "is_default"

            if is_default_key_name in backend_config:
                continue

            if is_default_key_name in backend_config["azure"]:
                continue

            raise AssertionError(f"Backend '{str(b)}' is not default")

    @pytest.mark.live_test
    def test_get_backends_throws_on_more_than_one_backend_found(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        all_backends = provider.backends()
        if len(all_backends) > 1:
            with pytest.raises(QiskitBackendNotFoundError):
                provider.get_backend()
        else:
            # if there's 0 or 1 provider registered in the workspace
            pytest.skip()

    @pytest.mark.ionq
    def test_ionq_simulator_has_default(self):
        workspace = self.create_workspace()
        provider = DummyProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)

    @pytest.mark.ionq
    def test_ionq_simulator_has_qir_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator", input_data_format="qir.v1")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)
        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        self.assertEqual(input_data_format, "qir.v1")

    @pytest.mark.ionq
    def test_ionq_simulator_has_native_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator", gateset="native")
        config = backend.configuration()
        self.assertEqual(config.gateset, "native")

    @pytest.mark.ionq
    def test_ionq_simulator_has_qis_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator", gateset="qis")
        config = backend.configuration()
        self.assertEqual(config.gateset, "qis")

    @pytest.mark.ionq
    def test_ionq_transpile_supports_native_instructions(self):
        from _qiskit_ionq import MSGate, GPIGate, GPI2Gate

        backend = IonQSimulatorNativeBackend(
            name="ionq.simulator", provider=None, gateset="native"
        )

        circuit = QuantumCircuit(2)
        circuit.append(MSGate(0.1, 0.2), [0, 1])
        circuit.append(GPIGate(0.3), [0])
        circuit.append(GPI2Gate(0.4), [1])

        self._assert_transpile_respects_target(
            backend,
            circuit,
            expected_ops={"ms", "gpi", "gpi2"},
        )

    @pytest.mark.ionq
    def test_ionq_qir_transpile_converts_non_qir_gates(self):
        backend = IonQSimulatorQirBackend(name="ionq.simulator", provider=None)

        transpiled_ops = self._assert_qir_transpile_decomposes_non_qir_gates(backend)
        self.assertGreater(
            len(transpiled_ops - {"measure"}),
            0,
            "Expected decomposed operations besides measurement.",
        )

    @pytest.mark.ionq
    def test_ionq_qpu_has_default(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-1")

    @pytest.mark.ionq
    def test_ionq_qpu_has_qir_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu.aria-1", input_data_format="qir.v1")
        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        self.assertEqual(input_data_format, "qir.v1")

    @pytest.mark.ionq
    def test_ionq_qpu_has_native_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu.aria-1", gateset="native")
        config = backend.configuration()
        self.assertEqual(config.gateset, "native")

    @pytest.mark.ionq
    def test_ionq_qpu_has_qis_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu.aria-1", gateset="qis")
        config = backend.configuration()
        self.assertEqual(config.gateset, "qis")

    @pytest.mark.ionq
    def test_ionq_forte_enterprise_has_default(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-enterprise-1")

    @pytest.mark.ionq
    def test_ionq_forte_enterprise_has_qir_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-enterprise-1", input_data_format="qir.v1")

    @pytest.mark.ionq
    def test_ionq_forte_enterprise_has_native_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-enterprise-1", gateset="native")

    @pytest.mark.ionq
    def test_ionq_forte_enterprise_has_qis_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-enterprise-1", gateset="qis")

    @pytest.mark.ionq
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_translate_ionq_qir(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        input_params = backend._get_input_params({})

        payload = backend._translate_input(circuit, input_params)
        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        output_data_format = backend._get_output_data_format()

        self.assertIsInstance(payload, bytes)
        self.assertEqual(input_data_format, "qir.v1")
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT_V2)
        self.assertIn("items", input_params)
        self.assertEqual(len(input_params["items"]), 1)
        item = input_params["items"][0]
        self.assertIn("entryPoint", item)
        self.assertIn("arguments", item)

    @pytest.mark.ionq
    def test_qiskit_get_ionq_qpu_target(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("ionq.qpu.aria-1")
        self.assertEqual(backend.name, "ionq.qpu.aria-1")
        config = backend.configuration()
        self.assertFalse(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(25, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("ionq", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual(
            MICROSOFT_OUTPUT_DATA_FORMAT_V2, config.azure["output_data_format"]
        )

    @pytest.mark.ionq
    def test_ionq_aria_has_default(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-1")

    @pytest.mark.ionq
    def test_ionq_aria_has_qir_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-1", input_data_format="qir.v1")

    @pytest.mark.ionq
    def test_ionq_aria_has_native_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-1", gateset="native")

    @pytest.mark.ionq
    def test_ionq_aria_has_qis_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-1", gateset="qis")

    @pytest.mark.ionq
    def test_ionq_forte1_has_default(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-1")

    @pytest.mark.ionq
    def test_ionq_forte1_has_qir_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-1", input_data_format="qir.v1")

    @pytest.mark.ionq
    def test_ionq_forte1_has_native_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-1", gateset="native")

    @pytest.mark.ionq
    def test_ionq_forte1_has_qis_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.forte-1", gateset="qis")

    # The following test is skipped until we can use a workspace
    # with this target available as part of the E2E tests.
    # @pytest.mark.ionq
    # #@pytest.mark.live_test
    # def test_qiskit_get_ionq_qpu_aria_target(self):
    #     workspace = self.create_workspace()
    #     provider = AzureQuantumProvider(workspace=workspace)

    #     backend = provider.get_backend("ionq.qpu.aria-1")
    #     self.assertEqual(backend.name, "ionq.qpu.aria-1")
    #     config = backend.configuration()
    #     self.assertFalse(config.simulator)
    #     self.assertEqual(1, config.max_experiments)
    #     self.assertEqual(23, config.num_qubits)
    #     self.assertEqual("ionq", config.azure["provider_id"])
    #     self.assertEqual("qir.v1", config.azure["input_data_format"])
    #     self.assertEqual(MICROSOFT_OUTPUT_DATA_FORMAT_V2, config.azure["output_data_format"])

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_qiskit_get_ionq_native_gateset(self):
        # initialize a quantum circuit with native gates (see https://ionq.com/docs/using-native-gates-with-qiskit)
        from _qiskit_ionq import MSGate, GPIGate, GPI2Gate

        native_circuit = QuantumCircuit(2, 2)
        native_circuit.append(MSGate(0, 0), [0, 1])
        native_circuit.append(GPIGate(0), [0])
        native_circuit.append(GPI2Gate(1), [1])

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("ionq.simulator", gateset="native")
        config = backend.configuration()
        self.assertEqual("native", backend.gateset())
        # Trying to translate a regular circuit using the native gateset should fail:
        with pytest.raises(IonQGateError) as exc:
            payload = backend._translate_input(self._3_qubit_ghz())
        # however, translating the native circuit should work fine.
        payload = backend._translate_input(native_circuit)
        payload = json.loads(payload.decode("utf-8"))
        self.assertEqual("ms", payload["circuit"][0]["gate"])
        # Confirm that the payload includes the gateset information.
        self.assertEqual("native", payload["gateset"])
        # We also expect the metadata to be produced correctly for native circuits
        metadata = backend._prepare_job_metadata(native_circuit)
        self.assertEqual(2, len(json.loads(metadata["meas_map"])))

        # should also be available with the qpu target
        backend = provider.get_backend("ionq.qpu.aria-1", gateset="native")
        config = backend.configuration()
        self.assertEqual("native", backend.gateset())
        payload = backend._translate_input(native_circuit)
        payload = json.loads(payload.decode("utf-8"))
        self.assertEqual("ms", payload["circuit"][0]["gate"])
        metadata = backend._prepare_job_metadata(native_circuit)
        self.assertEqual(2, len(json.loads(metadata["meas_map"])))

    @pytest.mark.ionq
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_plugins_retrieve_job(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        self.assertIsInstance(backend, IonQSimulatorQirBackend)
        circuit = self._3_qubit_ghz()
        qiskit_job = backend.run(circuit, shots=100)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            fetched_job = backend.retrieve_job(qiskit_job.id())
            self.assertEqual(fetched_job.id(), qiskit_job.id())
            result = fetched_job.result()
            self.assertEqual(result.data()["probabilities"], {"000": 0.5, "111": 0.5})
            self.assertEqual(sum(result.data()["counts"].values()), 100)
            self.assertAlmostEqual(result.data()["counts"]["000"], 50, delta=20)
            self.assertAlmostEqual(result.data()["counts"]["111"], 50, delta=20)

    def test_plugins_submit_qiskit_noexistent_target(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        with pytest.raises(QiskitBackendNotFoundError):
            provider.get_backend("provider.doesnotexist")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_to_quantinuum(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit, target="quantinuum.sim.h2-1e")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_to_quantinuum_h2_1e(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit, target="quantinuum.sim.h2-1e")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_h2_1sc(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit, target="quantinuum.sim.h2-1sc")

    @pytest.mark.quantinuum
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1")
    @pytest.mark.skip("Target was unavailable at the moment of the recording")
    def test_plugins_submit_qiskit_to_quantinuum_h2_1qpu(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit, target="quantinuum.qpu.h2-1")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_circuit_as_list_to_quantinuum(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum([circuit], target="quantinuum.sim.h2-1e")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_to_quantinuum_passthrough(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum_passthrough(circuit)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_to_quantinuum_h2_1e_passthrough(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum_passthrough(
            circuit, target="quantinuum.sim.h2-1e"
        )

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_h2_1sc_passthrough(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum_passthrough(
            circuit, target="quantinuum.sim.h2-1sc"
        )

    @pytest.mark.quantinuum
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1")
    @pytest.mark.skip("Target was unavailable at the moment of the recording")
    def test_plugins_submit_qiskit_to_quantinuum_h2_1qpu_passthrough(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum_passthrough(
            circuit, target="quantinuum.qpu.h2-1"
        )

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_circuit_as_list_to_quantinuum_passthrough(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum_passthrough(
            [circuit], target="quantinuum.sim.h2-1e"
        )

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_quantinuum(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("quantinuum.sim.h2-1e")
        self.assertIsInstance(backend, QuantinuumQirBackendBase)
        self.assertIn("quantinuum.sim.h2-1e", backend.backend_names)
        self.assertIn(
            backend.backend_names[0],
            [t.name for t in workspace.get_targets(provider_id="quantinuum")],
        )

        with self.assertRaises(NotImplementedError) as context:
            backend.run(circuit=[circuit, circuit], shots=None)
        self.assertEqual(
            str(context.exception),
            "This backend only supports running a single circuit per job.",
        )

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_counts_param(self):
        """
        This test verifies that we can pass a "provider-specific" shots number option.
        Even if the usage of the 'shots' option is encouraged, we should also be able to specify provider's
        native option ('count' in this case).
        """
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h2-1sc")
        self.assertIsInstance(backend, QuantinuumQirBackendBase)

        shots = 10
        with pytest.warns(
            match="Parameter 'count' is subject to change in future versions."
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_explicit_shots_param(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h2-1sc")
        self.assertIsInstance(backend, QuantinuumQirBackendBase)

        shots = 10
        qiskit_job = backend.run(circuit, shots=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_default_shots_param(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h2-1sc")
        self.assertIsInstance(backend, QuantinuumQirBackendBase)

        qiskit_job = backend.run(circuit)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], 500)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_conflicting_shots_and_count_from_options(
        self,
    ):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h2-1sc")
        self.assertIsInstance(backend, QuantinuumQirBackendBase)

        shots = 100
        with pytest.warns(
            match="Parameter 'shots' conflicts with the 'count' parameter."
        ):
            qiskit_job = backend.run(circuit, shots=shots, count=10)

        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_count_from_options(self):
        """
        Check that backend also allows to specify shots by using a provider-specific option,
        but also throws warning with recommndation to use 'shots'
        """
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h2-1sc")
        self.assertIsInstance(backend, QuantinuumQirBackendBase)

        shots = 100

        with pytest.warns(
            match="Parameter 'count' is subject to change in future versions. Please, use 'shots' parameter instead."
        ):
            qiskit_job = backend.run(circuit, count=shots)

        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_quantinuum_passthrough(
        self,
    ):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            "quantinuum.sim.h2-1e", input_data_format="honeywell.openqasm.v1"
        )
        self.assertIn("quantinuum.sim.h2-1e", backend.backend_names)
        self.assertIn(
            backend.backend_names[0],
            [t.name for t in workspace.get_targets(provider_id="quantinuum")],
        )

        with self.assertRaises(NotImplementedError) as context:
            backend.run(circuit=[circuit, circuit], shots=None)
        self.assertEqual(
            str(context.exception), "Multi-experiment jobs are not supported!"
        )

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_counts_param_passthrough(self):
        """
        This test verifies that we can pass a "provider-specific" shots number option.
        Even if the usage of the 'shots' option is encouraged, we should also be able to specify provider's
        native option ('count' in this case).
        """
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            name="quantinuum.sim.h2-1sc", input_data_format="honeywell.openqasm.v1"
        )

        shots = 10
        with pytest.warns(
            match="Parameter 'count' is subject to change in future versions."
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_explicit_shots_param_passthrough(
        self,
    ):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            name="quantinuum.sim.h2-1sc", input_data_format="honeywell.openqasm.v1"
        )

        shots = 10
        qiskit_job = backend.run(circuit, shots=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_default_shots_param_passthrough(
        self,
    ):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            name="quantinuum.sim.h2-1sc", input_data_format="honeywell.openqasm.v1"
        )

        qiskit_job = backend.run(circuit)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], 500)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_conflicting_shots_and_count_from_options_passthrough(
        self,
    ):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            name="quantinuum.sim.h2-1sc", input_data_format="honeywell.openqasm.v1"
        )

        shots = 100
        with pytest.warns(
            match="Parameter 'shots' conflicts with the 'count' parameter."
        ):
            qiskit_job = backend.run(circuit, shots=shots, count=10)

        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_plugins_submit_qiskit_to_quantinuum_with_count_from_options_passthrough(
        self,
    ):
        """
        Check that backend also allows to specify shots by using a provider-specific option,
        but also throws warning with recommndation to use 'shots'
        """
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            name="quantinuum.sim.h2-1sc", input_data_format="honeywell.openqasm.v1"
        )

        shots = 100

        with pytest.warns(
            match="Parameter 'count' is subject to change in future versions. Please, use 'shots' parameter instead."
        ):
            qiskit_job = backend.run(circuit, count=shots)

        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1e")
    def test_qiskit_qir_submit_quantinuum(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = QuantinuumEmulatorQirBackend("quantinuum.sim.h2-1e", provider)

        input_params = backend._get_input_params({})
        payload = backend._translate_input(circuit, input_params)

        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        output_data_format = backend._get_output_data_format()

        self.assertIsInstance(payload, bytes)
        self.assertEqual(input_data_format, "qir.v1")
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT_V2)
        self.assertIn("items", input_params)
        self.assertEqual(len(input_params["items"]), 1)
        item = input_params["items"][0]
        self.assertIn("entryPoint", item)
        self.assertIn("arguments", item)
        shots = 100

        qiskit_job = backend.run(circuit, shots=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "quantinuum")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "qir.v1")
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            MICROSOFT_OUTPUT_DATA_FORMAT_V2,
        )
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)
        self.assertEqual(
            qiskit_job._azure_job.details.input_params["items"][0]["entryPoint"],
            "ENTRYPOINT__main",
        )
        self.assertEqual(
            qiskit_job._azure_job.details.input_params["items"][0]["arguments"], []
        )

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            # verify we can get the counts with the circuit and without
            # These will throw if job metadata is incorrect
            self.assertIsNotNone(result.get_counts(circuit))
            self.assertIsNotNone(result.get_counts())
            self.assertIsNotNone(result.get_counts(0))
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertAlmostEqual(result.data()["counts"]["000"], shots // 2, delta=20)
            self.assertAlmostEqual(result.data()["counts"]["111"], shots // 2, delta=20)
            counts = result.get_counts()
            memory = result.get_memory()

            self.assertEqual(len(memory), shots)
            # shot must consist of 3 bits
            self.assertTrue(
                all([shot.count("0") + shot.count("1") == 3 for shot in memory])
            )
            self.assertEqual(counts, result.data()["counts"])

    def _test_qiskit_submit_quantinuum(
        self, circuit, target="quantinuum.sim.h2-1e", **kwargs
    ):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(target)
        self.assertIsInstance(backend, QuantinuumQirBackendBase)
        expected_data_format = (
            kwargs["input_data_format"] if "input_data_format" in kwargs else "qir.v1"
        )
        self.assertIn(target, backend.backend_names)
        self.assertIn(
            backend.backend_names[0],
            [t.name for t in workspace.get_targets(provider_id="quantinuum")],
        )

        if isinstance(circuit, list):
            num_qubits = circuit[0].num_qubits
            circuit[0].metadata = {"some": "data"}
        else:
            num_qubits = circuit.num_qubits
            circuit.metadata = {"some": "data"}

        qiskit_job = backend.run(circuit, **kwargs)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, target)
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "quantinuum")
        self.assertEqual(
            qiskit_job._azure_job.details.input_data_format, expected_data_format
        )
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            MICROSOFT_OUTPUT_DATA_FORMAT_V2,
        )
        self.assertIn("count", qiskit_job._azure_job.details.input_params)
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        self.assertEqual(JobStatus.DONE, qiskit_job.status())
        result = qiskit_job.result()
        self.assertIn("counts", result.data())
        self.assertIn("probabilities", result.data())
        header = result.results[0].header
        self.assertTrue(_header_has_field(header, "num_qubits"))
        num_qubits_value = _get_header_field(header, "num_qubits")
        self.assertEqual(str(num_qubits_value), str(num_qubits))
        metadata = _get_header_field(header, "metadata", {})
        self.assertEqual(metadata.get("some"), "data")

    def _test_qiskit_submit_quantinuum_passthrough(
        self, circuit, target="quantinuum.sim.h2-1e", **kwargs
    ):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(
            target, input_data_format="honeywell.openqasm.v1"
        )

        expected_data_format = (
            kwargs["input_data_format"] if "input_data_format" in kwargs else "qir.v1"
        )
        self.assertIn(target, backend.backend_names)
        self.assertIn(
            backend.backend_names[0],
            [t.name for t in workspace.get_targets(provider_id="quantinuum")],
        )

        if isinstance(circuit, list):
            num_qubits = circuit[0].num_qubits
            circuit[0].metadata = {"some": "data"}
        else:
            num_qubits = circuit.num_qubits
            circuit.metadata = {"some": "data"}

        qiskit_job = backend.run(circuit, **kwargs)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, target)
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "quantinuum")
        self.assertEqual(
            qiskit_job._azure_job.details.input_data_format, "honeywell.openqasm.v1"
        )
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            "honeywell.quantum-results.v1",
        )
        self.assertIn("count", qiskit_job._azure_job.details.input_params)
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        self.assertEqual(JobStatus.DONE, qiskit_job.status())
        result = qiskit_job.result()
        self.assertIn("counts", result.data())
        self.assertIn("probabilities", result.data())
        header = result.results[0].header
        self.assertTrue(_header_has_field(header, "num_qubits"))
        num_qubits_value = _get_header_field(header, "num_qubits")
        self.assertEqual(str(num_qubits_value), str(num_qubits))
        metadata = _get_header_field(header, "metadata", {})
        self.assertEqual(metadata.get("some"), "data")

    @pytest.mark.quantinuum
    def test_translate_quantinuum_qir(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = QuantinuumEmulatorQirBackend("quantinuum.sim.h2-1e", provider)

        input_params = backend._get_input_params({})
        payload = backend._translate_input(circuit, input_params)

        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        output_data_format = backend._get_output_data_format()

        self.assertIsInstance(payload, bytes)
        self.assertEqual(input_data_format, "qir.v1")
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT_V2)
        self.assertIn("items", input_params)
        self.assertEqual(len(input_params["items"]), 1)
        item = input_params["items"][0]
        self.assertIn("entryPoint", item)
        self.assertIn("arguments", item)

    @pytest.mark.quantinuum
    def test_quantinuum_transpile_supports_native_instructions(self):
        backend = QuantinuumEmulatorBackend(name="quantinuum.sim.h2-1e", provider=None)

        circuit = QuantumCircuit(2)
        circuit.append(Instruction("v", 1, 0, []), [0])
        circuit.append(Instruction("vdg", 1, 0, []), [1])
        circuit.append(Instruction("zz", 2, 0, [0.5]), [0, 1])

        self._assert_transpile_respects_target(
            backend,
            circuit,
            expected_ops={"v", "vdg", "zz"},
        )

    @pytest.mark.quantinuum
    def test_quantinuum_qir_transpile_converts_non_qir_gates(self):
        backend = QuantinuumEmulatorQirBackend(
            name="quantinuum.sim.h2-1e", provider=None
        )

        transpiled_ops = self._assert_qir_transpile_decomposes_non_qir_gates(backend)
        self.assertGreater(
            len(transpiled_ops - {"measure"}),
            0,
            "Expected decomposed operations besides measurement.",
        )

    @pytest.mark.quantinuum
    def test_quantinuum_qir_transpile_decomposes_initialize(self):
        backend = QuantinuumEmulatorQirBackend(
            name="quantinuum.sim.h2-1e", provider=None
        )

        circuit = QuantumCircuit(1)
        circuit.initialize([0, 1], 0)

        # we would get rz, rz, rz, sx, sx, but optimizing should reduce this to just ry
        transpiled = self._assert_transpile_respects_target(
            backend, circuit, expected_ops={"reset", "ry"}, optimization_level=2
        )

        transpiled_ops = [instruction.operation.name for instruction in transpiled.data]

        self.assertNotIn(
            "initialize",
            transpiled_ops,
            "State preparation should be decomposed for Quantinuum QIR backends.",
        )
        self.assertEqual(
            transpiled_ops,
            ["reset", "ry"],
            f"Unexpected decomposition for Quantinuum QIR transpilation: {transpiled_ops}",
        )
        self.assertEqual(
            len(transpiled_ops),
            2,
            "Initialize should decompose into exactly two operations for Quantinuum QIR backends.",
        )
        self.assertAlmostEqual(
            transpiled.data[1].operation.params[0],
            np.pi,
            msg="Initialize([0, 1]) should decompose to an ry(pi) rotation.",
        )

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_configuration_quantinuum_backends(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        # The following backends should have 56 qubits
        for target_name in [
            "quantinuum.qpu.h2-1",
            "quantinuum.sim.h2-1sc",
            "quantinuum.sim.h2-1e",
        ]:
            config = provider.get_backend(target_name).configuration()
            # We check for name so the test log includes it when reporting a failure
            self.assertIsNotNone(target_name)
            self.assertEqual(56, config.num_qubits)

        # The following backends should have 56 qubits
        for target_name in [
            "quantinuum.qpu.h2-1",
            "quantinuum.sim.h2-1sc",
            "quantinuum.sim.h2-1e",
        ]:
            config = provider.get_backend(
                target_name, input_data_format="honeywell.openqasm.v1"
            ).configuration()
            # We check for name so the test log includes it when reporting a failure
            self.assertIsNotNone(target_name)
            self.assertEqual(56, config.num_qubits)

    @pytest.mark.rigetti
    def test_rigetti_qir_transpile_converts_non_qir_gates(self):
        backend = RigettiSimulatorBackend(name=RigettiTarget.QVM.value, provider=None)

        transpiled_ops = self._assert_qir_transpile_decomposes_non_qir_gates(backend)
        self.assertGreater(
            len(transpiled_ops - {"measure"}),
            0,
            "Expected decomposed operations besides measurement.",
        )

    @pytest.mark.rigetti
    def test_rigetti_transpile_supports_standard_gates(self):
        backend = RigettiSimulatorBackend(name=RigettiTarget.QVM.value, provider=None)

        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        self._assert_transpile_respects_target(
            backend,
            circuit,
            expected_ops={"h", "cx", "measure"},
        )

    @pytest.mark.rigetti
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name=RigettiTarget.QVM.value)
    def test_qiskit_submit_to_rigetti(self):

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        self.assertEqual(backend.name, RigettiTarget.QVM.value)
        config = backend.configuration()
        self.assertTrue(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(20, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("rigetti", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual(
            MICROSOFT_OUTPUT_DATA_FORMAT_V2, backend._get_output_data_format()
        )
        shots = 100

        circuit = self._3_qubit_ghz()

        qiskit_job = backend.run(circuit, shots=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, RigettiTarget.QVM.value)
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "rigetti")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "qir.v1")
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            MICROSOFT_OUTPUT_DATA_FORMAT_V2,
        )
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)
        self.assertEqual(
            qiskit_job._azure_job.details.input_params["items"][0]["entryPoint"],
            "ENTRYPOINT__main",
        )
        self.assertEqual(
            qiskit_job._azure_job.details.input_params["items"][0]["arguments"], []
        )

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            # verify we can get the counts with the circuit and without
            # These will throw if job metadata is incorrect
            self.assertIsNotNone(result.get_counts(circuit))
            self.assertIsNotNone(result.get_counts())
            self.assertIsNotNone(result.get_counts(0))
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertAlmostEqual(result.data()["counts"]["000"], shots // 2, delta=20)
            self.assertAlmostEqual(result.data()["counts"]["111"], shots // 2, delta=20)
            counts = result.get_counts()
            memory = result.get_memory()

            self.assertEqual(len(memory), shots)
            self.assertTrue(all([shot == "000" or shot == "111" for shot in memory]))
            self.assertEqual(counts, result.data()["counts"])

    @pytest.mark.rigetti
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name=RigettiTarget.QVM.value)
    def test_qiskit_submit_to_rigetti_with_count_param(self):
        """
        Check that backend also allows to specify shots by using a provider-specific option,
        but also throws warning with recommndation to use 'shots'
        """

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        shots = 100
        circuit = self._3_qubit_ghz()
        with pytest.warns(
            match="Parameter 'count' is subject to change in future versions. Please, use 'shots' parameter instead."
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.rigetti
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name=RigettiTarget.QVM.value)
    def test_qiskit_submit_to_rigetti_with_explicit_shots_param(self):

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        shots = 100
        circuit = self._3_qubit_ghz()
        qiskit_job = backend.run(circuit, shots=shots)

        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.rigetti
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name=RigettiTarget.QVM.value)
    def test_qiskit_submit_to_rigetti_conflicting_shots_and_count_from_options(self):

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        shots = 100
        circuit = self._3_qubit_ghz()

        with pytest.warns(
            match="Parameter 'shots' conflicts with the 'count' parameter. Please, provide only one option for setting shots. "
            "Defaulting to 'shots' parameter."
        ):
            qiskit_job = backend.run(circuit, shots=shots, count=10)

        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.rigetti
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name=RigettiTarget.QVM.value)
    def test_qiskit_submit_to_rigetti_with_count_from_options(self):

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        shots = 100
        circuit = self._3_qubit_ghz()

        with pytest.warns(
            match="Parameter 'count' is subject to change in future versions. Please, use 'shots' parameter instead."
        ):
            qiskit_job = backend.run(circuit, count=shots)

        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.rigetti
    @pytest.mark.live_test
    def test_qiskit_get_rigetti_qpu_targets(self):

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        try:
            backend = provider.get_backend(RigettiTarget.ANKAA_3.value)
        except QiskitBackendNotFoundError as ex:
            msg = f"Target {RigettiTarget.ANKAA_3} is not available for workspace {workspace.name}."
            warnings.warn(
                f"{msg}\nException:\n{QiskitBackendNotFoundError.__name__}\n{ex}"
            )
            pytest.skip(msg)

        self.assertEqual(backend.name, RigettiTarget.ANKAA_3.value)
        config = backend.configuration()
        self.assertFalse(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(84, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("rigetti", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual(
            MICROSOFT_OUTPUT_DATA_FORMAT_V2, backend._get_output_data_format()
        )

    @pytest.mark.qci
    def test_qci_qir_transpile_converts_non_qir_gates(self):
        backend = QCISimulatorBackend(name="qci.simulator", provider=None)

        transpiled_ops = self._assert_qir_transpile_decomposes_non_qir_gates(backend)
        self.assertGreater(
            len(transpiled_ops - {"measure"}),
            0,
            "Expected decomposed operations besides measurement.",
        )

    @pytest.mark.qci
    def test_qci_transpile_supports_barrier(self):
        backend = QCISimulatorBackend(name="qci.simulator", provider=None)

        circuit = QuantumCircuit(1)
        circuit.h(0)
        circuit.barrier()
        circuit.measure_all()

        self._assert_transpile_respects_target(
            backend,
            circuit,
            expected_ops={"h", "barrier", "measure"},
        )

    @pytest.mark.skip("Skipping tests against QCI's unavailable targets")
    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_submit_to_qci(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("qci.simulator")
        self.assertEqual(backend.name, "qci.simulator")
        config = backend.configuration()
        self.assertTrue(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(29, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("qci", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual(
            "microsoft.quantum-results.v2", backend._get_output_data_format()
        )
        shots = 100

        circuit = self._3_qubit_ghz()

        qiskit_job = backend.run(circuit, shots=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "qci.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "qci")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "qir.v1")
        self.assertEqual(
            qiskit_job._azure_job.details.output_data_format,
            MICROSOFT_OUTPUT_DATA_FORMAT_V2,
        )
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)
        self.assertEqual(
            qiskit_job._azure_job.details.input_params["items"][0]["entryPoint"],
            "ENTRYPOINT__main",
        )
        self.assertEqual(
            qiskit_job._azure_job.details.input_params["items"][0]["arguments"], []
        )

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            print(result)
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertAlmostEqual(result.data()["counts"]["000"], shots // 2, delta=20)
            self.assertAlmostEqual(result.data()["counts"]["111"], shots // 2, delta=20)
            counts = result.get_counts()
            self.assertEqual(counts, result.data()["counts"])

    @pytest.mark.skip("Skipping tests against QCI's unavailable targets")
    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_submit_to_qci_with_default_shots(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("qci.simulator")

        circuit = self._3_qubit_ghz()
        qiskit_job = backend.run(circuit)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], 500)

    @pytest.mark.skip("Skipping tests against QCI's unavailable targets")
    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_submit_to_qci_with_deprecated_count_param(self):
        """
        Verify that a warning message is printed when the 'count' option is specified.
        This option was allowed in earlier versions, but now it is accepted only to keep existing
        user codebase compatible.
        """
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("qci.simulator")

        shots = 10
        circuit = self._3_qubit_ghz()
        with pytest.warns(
            DeprecationWarning,
            match="The 'count' parameter will be deprecated. Please, use 'shots' parameter instead.",
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)

    @pytest.mark.skip("Skipping tests against QCI's unavailable targets")
    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_get_qci_qpu_targets(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("qci.machine1")
        self.assertEqual(backend.name, "qci.machine1")
        config = backend.configuration()
        self.assertFalse(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(11, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("qci", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual(
            "microsoft.quantum-results.v2", backend._get_output_data_format()
        )

    @pytest.mark.rigetti
    @pytest.mark.live_test
    @pytest.mark.xdist_group(name=RigettiTarget.QVM.value)
    def test_qiskit_endianness_submit_to_rigetti(self, expectation="000 000 001"):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        shots = 100

        qr = QuantumRegister(3)
        cr = [ClassicalRegister(3) for _ in range(3)]
        circuit = QuantumCircuit(qr, *cr, name="endian0cr3")
        circuit.x(0)
        circuit.measure(qr[0], cr[0][0])
        circuit.measure(qr[1], cr[0][1])
        circuit.measure(qr[1], cr[0][2])
        circuit.measure(qr[1], cr[1][0])
        circuit.measure(qr[1], cr[1][1])
        circuit.measure(qr[1], cr[1][2])
        circuit.measure(qr[2], cr[2][0])
        circuit.measure(qr[2], cr[2][1])
        circuit.measure(qr[2], cr[2][2])
        circuit.metadata = {"some": "data"}

        qiskit_job = backend.run(circuit, shots=shots)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            print(result)
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertEqual(result.data()["counts"][expectation], shots)

    def test_backend_without_azure_config_format_defaults_to_ms_format(self):
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        output_data_format = backend._get_output_data_format()
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT)

    def test_backend_with_azure_config_format_defaults_to_that_format(self):
        expected = "test_format"
        backend = NoopQirBackend(
            None, "AzureQuantumProvider", output_data_format=expected
        )
        actual = backend._get_output_data_format()
        self.assertEqual(expected, actual)

    def test_backend_with_azure_config_format_is_overridden_with_explicit_format(self):
        azure_congfig_value = "test_format"
        backend = NoopQirBackend(
            None, "AzureQuantumProvider", output_data_format=azure_congfig_value
        )
        expected = "test_format_v2"
        options = {"output_data_format": expected}
        actual = backend._get_output_data_format(options)
        self.assertNotIn("output_data_format", options)
        self.assertEqual(expected, actual)

    def test_specifying_targetCapabilities_with_pass_thru_fails(
        self,
    ):
        from azure.quantum.qiskit.backends.quantinuum import QuantinuumEmulatorBackend

        backend = QuantinuumEmulatorBackend(
            "quantinuum.sim.h2-1sc", "AzureQuantumProvider"
        )
        with pytest.raises(ValueError) as exc:
            # mimic the user passing in targetCapabilities as part of the run options
            _ = backend._run("", None, {"targetCapability": "BasicExecution"}, {})
        actual = str(exc.value)
        expected = "The targetCapability parameter has been deprecated"
        self.assertTrue(actual.startswith(expected))
