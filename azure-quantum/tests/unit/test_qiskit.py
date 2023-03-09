#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_qiskit.py: Tests for Qiskit plugin
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict, List, Tuple, Union
import unittest
import warnings
import pytest
import json
import random

import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers import JobStatus
from qiskit.providers.models import BackendConfiguration
from qiskit.providers import BackendV1 as Backend
from qiskit.providers.exceptions import QiskitBackendNotFoundError
from qiskit_ionq.exceptions import IonQGateError
from qiskit_ionq import GPIGate, GPI2Gate, MSGate

from azure.quantum.job.job import Job
from azure.quantum.qiskit import AzureQuantumProvider
from azure.quantum.qiskit.job import (
    MICROSOFT_OUTPUT_DATA_FORMAT,
    MICROSOFT_OUTPUT_DATA_FORMAT_V2,
    AzureQuantumJob,
)
from azure.quantum.qiskit.backends.backend import (
    AzureBackend,
    AzureBackendBase,
    AzureQirBackend,
)
from azure.quantum.qiskit.backends.quantinuum import QuantinuumEmulatorQirBackend
from azure.quantum.qiskit.backends.ionq import IonQSimulatorQirBackend

from common import QuantumTestBase, ZERO_UID

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
            if backend.name() == name:
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
            if tup[0] == backend.name()
            and tup[1] == backend.configuration().to_dict()["azure"]["provider_id"]
        )


class NoopQirBackend(AzureQirBackend):
    def __init__(
        self,
        configuration: BackendConfiguration,
        provider: "AzureQuantumProvider",
        **fields,
    ):
        default_config = BackendConfiguration.from_dict(
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
                "azure": self._azure_config(fields.pop("output_data_format", None)),
            }
        )

        configuration: BackendConfiguration = fields.pop(
            "configuration", default_config
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
        return None

    def _translate_input(
        self, circuits: List[QuantumCircuit], input_params: Dict[str, Any]
    ) -> bytes:
        return None


class NoopPassThruBackend(AzureBackend):
    def __init__(
        self,
        configuration: BackendConfiguration,
        provider: "AzureQuantumProvider",
        **fields,
    ):
        default_config = BackendConfiguration.from_dict(
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

        configuration: BackendConfiguration = fields.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **fields)

    def run(self, run_input=None, **kwargs):
        return self._normalize_run_input_params(run_input, **kwargs)

    def _azure_config(self, fields) -> Dict[str, str]:
        return fields

    def _default_options(cls):
        return None

    def _translate_input(self, circuit):
        return None


class TestQiskit(QuantumTestBase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback else Job.create_job_id()

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

    def _endianness(self, pos=0):
        assert pos < 3
        qr = QuantumRegister(3)
        cr = [ClassicalRegister(3) for _ in range(3)]
        circuit = QuantumCircuit(qr, *cr, name=f"endian{pos}cr3")
        circuit.x(pos)
        circuit.measure(qr[pos], cr[pos][pos])
        return circuit

    def _controlled_s(self):
        circuit = QuantumCircuit(3)
        circuit.t(0)
        circuit.t(1)
        circuit.cx(0, 1)
        circuit.tdg(1)
        circuit.cx(0, 1)
        return circuit

    def test_unnamed_run_input_passes_through(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        assert backend.run("default") == "default"
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        assert backend.run("default") == "default"

    def test_named_run_input_passes_through(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        assert backend.run(run_input="default") == "default"
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        assert backend.run(run_input="default") == "default"

    def test_named_circuit_passes_through(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        assert backend.run(circuit="default") == "default"
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        assert backend.run(circuit="default") == "default"

    def test_both_named_circuit_and_run_input_chooses_run_input(self):
        backend = NoopPassThruBackend(None, "AzureQuantumProvider")
        assert backend.run(run_input="a", circuit="b") == "a"
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        assert backend.run(run_input="a", circuit="b") == "a"

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

        assert AzureQuantumJob._qir_to_qiskit_bitstring(azure_register) == bitstring
        assert AzureQuantumJob._qir_to_qiskit_bitstring(azure_registers) == " ".join(
            f"{bit}10" for bit in reversed(bits)
        )
        assert AzureQuantumJob._qir_to_qiskit_bitstring(bitstring) == bitstring

    def test_qiskit_submit_ionq_5_qubit_superposition(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            assert "azure-quantum-qiskit" in provider._workspace.user_agent
            backend = provider.get_backend("ionq.simulator")
            num_shots = 1000

            circuit = self._5_qubit_superposition()
            circuit.metadata = {"some": "data"}

            qiskit_job = backend.run(circuit, shots=num_shots)

            # Check job metadata:
            assert qiskit_job._azure_job.details.target == "ionq.simulator"
            assert qiskit_job._azure_job.details.provider_id == "ionq"
            assert qiskit_job._azure_job.details.input_data_format == "ionq.circuit.v1"
            assert (
                qiskit_job._azure_job.details.output_data_format
                == "ionq.quantum-results.v1"
            )
            assert "qiskit" in qiskit_job._azure_job.details.metadata
            assert "name" in qiskit_job._azure_job.details.metadata
            assert "meas_map" in qiskit_job._azure_job.details.metadata
            assert "metadata" in qiskit_job._azure_job.details.metadata

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert sum(result.data()["counts"].values()) == num_shots
                assert np.isclose(result.data()["counts"]["0"], num_shots // 2, 20)
                assert np.isclose(result.data()["counts"]["1"], num_shots // 2, 20)
                assert result.data()["probabilities"] == {"0": 0.5, "1": 0.5}
                counts = result.get_counts()
                assert counts == result.data()["counts"]
                assert result.results[0].header.num_qubits == "5"
                assert result.results[0].header.metadata["some"] == "data"

    @pytest.mark.ionq
    def test_plugins_estimate_cost_qiskit_ionq(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        assert "azure-quantum-qiskit" in provider._workspace.user_agent
        backend = provider.get_backend("ionq.simulator")
        cost = backend.estimate_cost(circuit, shots=100e3)
        assert cost.estimated_total == 0.0

        backend = provider.get_backend("ionq.qpu")
        cost = backend.estimate_cost(circuit, shots=1024)
        assert np.round(cost.estimated_total) == 1.0

        backend = provider.get_backend("ionq.qpu")
        cost = backend.estimate_cost(circuit, shots=100e3)
        assert np.round(cost.estimated_total) == 66.0

        ## The following two tests are skipped until we can use a workspace
        ## with this target available as part of the E2E tests.
        # backend = provider.get_backend("ionq.qpu.aria-1")
        # cost = backend.estimate_cost(circuit, shots=1024)
        # assert np.round(cost.estimated_total) == 1.0

        # backend = provider.get_backend("ionq.qpu.aria-1")
        # cost = backend.estimate_cost(circuit, shots=100e3)
        # assert np.round(cost.estimated_total) == 240.0

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq(circuit)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_circuit_as_list_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq([circuit])

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_ionq(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        assert "azure-quantum-qiskit" in provider._workspace.user_agent
        backend = provider.get_backend("ionq.simulator")

        with pytest.raises(NotImplementedError) as exc:
            backend.run(circuit=[circuit, circuit], shots=500)
        assert str(exc.value) == "Multi-experiment jobs are not supported!"

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_qobj_to_ionq(self):
        from qiskit import assemble

        circuit = self._3_qubit_ghz()
        qobj = assemble(circuit)
        self._test_qiskit_submit_ionq(circuit=qobj, shots=1024)

    def _qiskit_wait_to_complete(self, qiskit_job, provider):
        job = qiskit_job._azure_job
        self.pause_recording()
        try:
            job.wait_until_completed(timeout_secs=60)
        except TimeoutError:
            self.resume_recording()
            warnings.warn(
                f"Qiskit Job {job.id} exceeded timeout. Skipping fetching results."
            )
        else:
            self.resume_recording()

            # Record a single GET request such that job.wait_until_completed
            # doesn't fail when running recorded tests
            # See: https://github.com/microsoft/qdk-python/issues/118
            job.refresh()

            self.assertEqual(JobStatus.DONE, qiskit_job.status())
            qiskit_job = provider.get_job(job.id)
            self.assertEqual(JobStatus.DONE, qiskit_job.status())

    def _test_qiskit_submit_ionq(self, circuit, **kwargs):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            assert "azure-quantum-qiskit" in provider._workspace.user_agent
            backend = provider.get_backend("ionq.simulator")
            expected_data_format = (
                kwargs["input_data_format"]
                if "input_data_format" in kwargs
                else "ionq.circuit.v1"
            )

            shots = kwargs.get("shots", backend.options.shots)

            qiskit_job = backend.run(circuit, **kwargs)

            # Check job metadata:
            assert qiskit_job._azure_job.details.target == "ionq.simulator"
            assert qiskit_job._azure_job.details.provider_id == "ionq"
            assert (
                qiskit_job._azure_job.details.input_data_format == expected_data_format
            )
            assert (
                qiskit_job._azure_job.details.output_data_format
                == "ionq.quantum-results.v1"
            )
            assert qiskit_job._azure_job.details.input_params["shots"] == shots
            assert "qiskit" in qiskit_job._azure_job.details.metadata
            assert "name" in qiskit_job._azure_job.details.metadata
            assert "metadata" in qiskit_job._azure_job.details.metadata
            assert "meas_map" in qiskit_job._azure_job.details.metadata

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert sum(result.data()["counts"].values()) == shots
                assert np.isclose(result.data()["counts"]["000"], shots // 2, 20)
                assert np.isclose(result.data()["counts"]["111"], shots // 2, 20)
                assert result.data()["probabilities"] == {"000": 0.5, "111": 0.5}
                counts = result.get_counts()
                assert counts == result.data()["counts"]
                assert hasattr(result.results[0].header, "num_qubits")
                assert hasattr(result.results[0].header, "metadata")

    @pytest.mark.ionq
    def test_ionq_simulator_has_default(self):
        workspace = self.create_workspace()
        provider = DummyProvider(workspace=workspace)
        provider.get_backend("ionq.simulator")

    @pytest.mark.ionq
    def test_ionq_simulator_has_qir_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator", input_data_format="qir.v1")
        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        assert input_data_format == "qir.v1"

    @pytest.mark.ionq
    def test_ionq_simulator_has_native_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator", gateset="native")
        config = backend.configuration()
        assert config.gateset == "native"

    @pytest.mark.ionq
    def test_ionq_simulator_has_qis_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator", gateset="qis")
        config = backend.configuration()
        assert config.gateset == "qis"

    @pytest.mark.ionq
    def test_ionq_simulator_default_target_has_qis_gateset(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator")
        config = backend.configuration()
        assert config.gateset == "qis"

    @pytest.mark.ionq
    def test_ionq_qpu_has_default(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu")

    @pytest.mark.ionq
    def test_ionq_qpu_has_qir_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu", input_data_format="qir.v1")
        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        assert input_data_format == "qir.v1"

    @pytest.mark.ionq
    def test_ionq_qpu_has_native_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu", gateset="native")
        config = backend.configuration()
        assert config.gateset == "native"

    @pytest.mark.ionq
    def test_ionq_qpu_has_qis_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu", gateset="qis")
        config = backend.configuration()
        assert config.gateset == "qis"

    @pytest.mark.ionq
    def test_ionq_qpu_default_target_has_qis_gateset(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu")
        config = backend.configuration()
        assert config.gateset == "qis"

    @pytest.mark.ionq
    def test_translate_ionq_qir(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = IonQSimulatorQirBackend("ionq.simulator", provider)
        input_params = backend._get_input_params({})

        payload = backend._translate_input(circuit, input_params)
        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        output_data_format = backend._get_output_data_format()

        assert isinstance(payload, bytes)
        assert input_data_format == "qir.v1"
        assert output_data_format == MICROSOFT_OUTPUT_DATA_FORMAT
        assert "items" in input_params and len(input_params["items"]) == 1
        item = input_params["items"][0]
        assert "entryPoint" in item
        assert "arguments" in item

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_qiskit_get_ionq_qpu_target(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("ionq.qpu")
        assert backend.name() == "ionq.qpu"
        config = backend.configuration()
        assert False == config.simulator
        assert 1 == config.max_experiments
        assert 11 == config.num_qubits
        assert "application/json" == config.azure["content_type"]
        assert "ionq" == config.azure["provider_id"]
        assert "ionq.circuit.v1" == config.azure["input_data_format"]
        assert "ionq.quantum-results.v1" == config.azure["output_data_format"]
        assert "qis" == backend.gateset()

    # The following test is skipped until we can use a workspace
    # with this target available as part of the E2E tests.
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

    # @pytest.mark.ionq
    # #@pytest.mark.live_test
    # def test_qiskit_get_ionq_qpu_aria_target(self):
    #     workspace = self.create_workspace()
    #     provider = AzureQuantumProvider(workspace=workspace)

    #     backend = provider.get_backend("ionq.qpu.aria-1")
    #     assert backend.name() == "ionq.qpu.aria-1"
    #     config = backend.configuration()
    #     assert False == config.simulator
    #     assert 1 == config.max_experiments
    #     assert 23 == config.num_qubits
    #     assert "ionq" == config.azure["provider_id"]
    #     assert "ionq.circuit.v1" == config.azure["input_data_format"]
    #     assert "ionq.quantum-results.v1" == config.azure["output_data_format"]

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_qiskit_get_ionq_native_gateset(self):
        # initialize a quantum circuit with native gates (see https://ionq.com/docs/using-native-gates-with-qiskit)
        native_circuit = QuantumCircuit(2, 2)
        native_circuit.append(MSGate(0, 0), [0, 1])
        native_circuit.append(GPIGate(0), [0])
        native_circuit.append(GPI2Gate(1), [1])

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("ionq.simulator", gateset="native")
        config = backend.configuration()
        assert "native" == backend.gateset()
        # Trying to translate a regular circuit using the native gateset should fail:
        with pytest.raises(IonQGateError) as exc:
            payload = backend._translate_input(self._3_qubit_ghz())
        # however, translating the native circuit should work fine.
        payload = backend._translate_input(native_circuit)
        payload = json.loads(payload.decode("utf-8"))
        assert "ms" == payload["circuit"][0]["gate"]
        # Confirm that the payload includes the gateset information.
        assert "native" == payload["gateset"]
        # We also expect the metadata to be produced correctly for native circuits
        metadata = backend._prepare_job_metadata(native_circuit)
        assert 2 == len(metadata["meas_map"])

        # should also be available with the qpu target
        backend = provider.get_backend("ionq.qpu", gateset="native")
        config = backend.configuration()
        assert "native" == backend.gateset()
        payload = backend._translate_input(native_circuit)
        payload = json.loads(payload.decode("utf-8"))
        assert "ms" == payload["circuit"][0]["gate"]
        metadata = backend._prepare_job_metadata(native_circuit)
        assert 2 == len(metadata["meas_map"])

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_retrieve_job(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("ionq.simulator")
            circuit = self._3_qubit_ghz()
            qiskit_job = backend.run(circuit, shots=100)

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                fetched_job = backend.retrieve_job(qiskit_job.id())
                assert fetched_job.id() == qiskit_job.id()
                result = fetched_job.result()
                assert result.data()["probabilities"] == {"000": 0.5, "111": 0.5}
                assert sum(result.data()["counts"].values()) == 100
                assert np.isclose(result.data()["counts"]["000"], 50, atol=20)
                assert np.isclose(result.data()["counts"]["111"], 50, atol=20)

    @pytest.mark.quantinuum
    def test_plugins_estimate_cost_qiskit_quantinuum(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        assert "azure-quantum-qiskit" in provider._workspace.user_agent
        backend = provider.get_backend("quantinuum.hqs-lt-s1-apival")
        cost = backend.estimate_cost(circuit, shots=100e3)
        assert cost.estimated_total == 0.0

        backend = provider.get_backend("quantinuum.hqs-lt-s1")
        cost = backend.estimate_cost(circuit, shots=100e3)
        assert cost.estimated_total == 745.0

    @pytest.mark.live_test
    def test_plugins_submit_qiskit_noexistent_target(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        with pytest.raises(QiskitBackendNotFoundError):
            provider.get_backend("provider.doesnotexist")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_quantinuum(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_circuit_as_list_to_quantinuum(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum([circuit])

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_quantinuum(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("quantinuum.hqs-lt-s1-apival")
        assert "quantinuum.hqs-lt-s1-apival" in backend.backend_names
        assert backend.backend_names[0] in [
            t.name for t in workspace.get_targets(provider_id="quantinuum")
        ]

        with pytest.raises(NotImplementedError) as exc:
            backend.run(circuit=[circuit, circuit], shots=None)
        assert str(exc.value) == "Multi-experiment jobs are not supported!"

    def _test_qiskit_submit_quantinuum(self, circuit, **kwargs):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("quantinuum.hqs-lt-s1-apival")
            expected_data_format = (
                kwargs["input_data_format"]
                if "input_data_format" in kwargs
                else "honeywell.openqasm.v1"
            )
            assert "quantinuum.hqs-lt-s1-apival" in backend.backend_names
            assert backend.backend_names[0] in [
                t.name for t in workspace.get_targets(provider_id="quantinuum")
            ]

            if isinstance(circuit, list):
                num_qubits = circuit[0].num_qubits
                circuit[0].metadata = {"some": "data"}
            else:
                num_qubits = circuit.num_qubits
                circuit.metadata = {"some": "data"}

            qiskit_job = backend.run(circuit, **kwargs)

            # Check job metadata:
            assert qiskit_job._azure_job.details.target == "quantinuum.hqs-lt-s1-apival"
            assert qiskit_job._azure_job.details.provider_id == "quantinuum"
            assert (
                qiskit_job._azure_job.details.input_data_format == expected_data_format
            )
            assert (
                qiskit_job._azure_job.details.output_data_format
                == "honeywell.quantum-results.v1"
            )
            assert "count" in qiskit_job._azure_job.details.input_params
            assert "qiskit" in qiskit_job._azure_job.details.metadata
            assert "name" in qiskit_job._azure_job.details.metadata
            assert "metadata" in qiskit_job._azure_job.details.metadata

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert result.data()["counts"] == {"000": 500}
                assert result.data()["probabilities"] == {"000": 1.0}
                assert hasattr(result.results[0].header, "num_qubits")
                assert result.results[0].header.num_qubits == str(num_qubits)
                assert result.results[0].header.metadata["some"] == "data"

    @pytest.mark.quantinuum
    def test_translate_quantinuum_qir(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = QuantinuumEmulatorQirBackend(
            "quantinuum.sim.h1-2sc-preview", provider
        )

        input_params = backend._get_input_params()
        payload = backend._translate_input(circuit, input_params)

        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        output_data_format = backend._get_output_data_format()

        assert isinstance(payload, bytes)
        assert input_data_format == "qir.v1"
        assert output_data_format == MICROSOFT_OUTPUT_DATA_FORMAT
        assert "items" in input_params and len(input_params["items"]) == 1
        item = input_params["items"][0]
        assert "entryPoint" in item
        assert "arguments" in item

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_configuration_quantinuum_backends(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        # The following backends should have 20 qubits
        for target_name in [
            "quantinuum.hqs-lt-s1",
            "quantinuum.qpu.h1-1",
            "quantinuum.hqs-lt-s1-apival",
            "quantinuum.sim.h1-1sc",
            "quantinuum.hqs-lt-s1-sim",
            "quantinuum.sim.h1-1e",
        ]:
            config = provider.get_backend(target_name).configuration()
            # We check for name so the test log includes it when reporting a failure
            assert target_name is not None and 20 == config.num_qubits

        # The following backends should have 12 qubits
        for target_name in [
            "quantinuum.hqs-lt-s2",
            "quantinuum.qpu.h1-2",
            "quantinuum.hqs-lt-s2-apival",
            "quantinuum.sim.h1-2sc",
            "quantinuum.hqs-lt-s2-sim",
            "quantinuum.sim.h1-2e",
        ]:
            config = provider.get_backend(target_name).configuration()
            # We check for name so the test log includes it when reporting a failure
            assert target_name is not None and 12 == config.num_qubits

    @pytest.mark.rigetti
    @pytest.mark.live_test
    def test_qiskit_submit_to_rigetti(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            from azure.quantum.target.rigetti import RigettiTarget

            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            assert "azure-quantum-qiskit" in provider._workspace.user_agent
            backend = provider.get_backend(RigettiTarget.QVM.value)
            assert backend.name() == RigettiTarget.QVM.value
            config = backend.configuration()
            assert True == config.simulator
            assert 1 == config.max_experiments
            assert 20 == config.num_qubits
            assert "qir.v1" == config.azure["content_type"]
            assert "rigetti" == config.azure["provider_id"]
            assert "qir.v1" == config.azure["input_data_format"]
            assert "microsoft.quantum-results.v1" == backend._get_output_data_format()
            shots = 100

            circuit = self._3_qubit_ghz()
            circuit.metadata = {"some": "data"}

            qiskit_job = backend.run(circuit, count=shots)

            # Check job metadata:
            assert qiskit_job._azure_job.details.target == RigettiTarget.QVM.value
            assert qiskit_job._azure_job.details.provider_id == "rigetti"
            assert qiskit_job._azure_job.details.input_data_format == "qir.v1"
            assert (
                qiskit_job._azure_job.details.output_data_format
                == "microsoft.quantum-results.v1"
            )
            assert "qiskit" in qiskit_job._azure_job.details.metadata
            assert "name" in qiskit_job._azure_job.details.metadata
            assert "num_qubits" in qiskit_job._azure_job.details.metadata
            assert "metadata" in qiskit_job._azure_job.details.metadata
            assert qiskit_job._azure_job.details.metadata["num_qubits"] == "4"
            assert qiskit_job._azure_job.details.input_params["count"] == shots
            assert qiskit_job._azure_job.details.input_params["entryPoint"] == "main"
            assert qiskit_job._azure_job.details.input_params["arguments"] == []

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                print(result)
                assert sum(result.data()["counts"].values()) == shots
                assert np.isclose(result.data()["counts"]["000"], shots // 2, 20)
                assert np.isclose(result.data()["counts"]["111"], shots // 2, 20)
                counts = result.get_counts()
                assert counts == result.data()["counts"]
                assert hasattr(result.results[0].header, "num_qubits")
                assert hasattr(result.results[0].header, "metadata")
                assert result.results[0].header.num_qubits == "4"
                assert result.results[0].header.metadata["some"] == "data"

    @pytest.mark.rigetti
    @pytest.mark.live_test
    def test_qiskit_get_rigetti_qpu_targets(self):
        from azure.quantum.target.rigetti import RigettiTarget

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend(RigettiTarget.ASPEN_M_2.value)
        assert backend.name() == RigettiTarget.ASPEN_M_2.value
        config = backend.configuration()
        assert False == config.simulator
        assert 1 == config.max_experiments
        assert 80 == config.num_qubits
        assert "qir.v1" == config.azure["content_type"]
        assert "rigetti" == config.azure["provider_id"]
        assert "qir.v1" == config.azure["input_data_format"]
        assert "microsoft.quantum-results.v1" == backend._get_output_data_format()

    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_submit_to_qci(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            assert "azure-quantum-qiskit" in provider._workspace.user_agent
            backend = provider.get_backend("qci.simulator")
            assert backend.name() == "qci.simulator"
            config = backend.configuration()
            assert True == config.simulator
            assert 1 == config.max_experiments
            assert 29 == config.num_qubits
            assert "qir.v1" == config.azure["content_type"]
            assert "qci" == config.azure["provider_id"]
            assert "qir.v1" == config.azure["input_data_format"]
            assert "microsoft.quantum-results.v1" == backend._get_output_data_format()
            shots = 100

            circuit = self._3_qubit_ghz()
            circuit.metadata = {"some": "data"}

            qiskit_job = backend.run(circuit, shots=shots)

            # Check job metadata:
            assert qiskit_job._azure_job.details.target == "qci.simulator"
            assert qiskit_job._azure_job.details.provider_id == "qci"
            assert qiskit_job._azure_job.details.input_data_format == "qir.v1"
            assert (
                qiskit_job._azure_job.details.output_data_format
                == "microsoft.quantum-results.v1"
            )
            assert "qiskit" in qiskit_job._azure_job.details.metadata
            assert "name" in qiskit_job._azure_job.details.metadata
            assert "num_qubits" in qiskit_job._azure_job.details.metadata
            assert "metadata" in qiskit_job._azure_job.details.metadata
            assert qiskit_job._azure_job.details.metadata["num_qubits"] == "4"
            assert qiskit_job._azure_job.details.input_params["count"] == shots
            assert qiskit_job._azure_job.details.input_params["entryPoint"] == "main"
            assert qiskit_job._azure_job.details.input_params["arguments"] == []

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                print(result)
                assert sum(result.data()["counts"].values()) == shots
                assert np.isclose(result.data()["counts"]["000"], shots // 2, 20)
                assert np.isclose(result.data()["counts"]["111"], shots // 2, 20)
                counts = result.get_counts()
                assert counts == result.data()["counts"]
                assert hasattr(result.results[0].header, "num_qubits")
                assert hasattr(result.results[0].header, "metadata")
                assert result.results[0].header.num_qubits == "4"
                assert result.results[0].header.metadata["some"] == "data"

    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_get_qci_qpu_targets(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("qci.machine1")
        assert backend.name() == "qci.machine1"
        config = backend.configuration()
        assert False == config.simulator
        assert 1 == config.max_experiments
        assert 11 == config.num_qubits
        assert "qir.v1" == config.azure["content_type"]
        assert "qci" == config.azure["provider_id"]
        assert "qir.v1" == config.azure["input_data_format"]
        assert "microsoft.quantum-results.v1" == backend._get_output_data_format()

    # @pytest.mark.parametrize("endian_pos, expectation",
    #     [(0,"000 000 001"), (1,"000 010 000"), (2,"100 000 000")]
    # )
    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_endianness_submit_to_qci(
        self, endian_pos=0, expectation="000 000 001"
    ):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("qci.simulator")
            shots = 100

            circuit = self._endianness(pos=endian_pos)
            circuit.metadata = {"some": "data"}

            qiskit_job = backend.run(circuit, shots=shots)
            assert qiskit_job._azure_job.details.metadata["num_qubits"] == "3"

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                print(result)
                assert sum(result.data()["counts"].values()) == shots
                assert result.data()["counts"][expectation] == shots

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_qiskit_controlled_s_to_resource_estimator(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("microsoft.estimator")

            circuit = self._controlled_s()

            qiskit_job = backend.run(circuit)

            # Make sure the job is completed before fetching results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert result.data()["logicalCounts"]["numQubits"] == 2
                assert (
                    result.data()["jobParams"]["qubitParams"]["name"]
                    == "qubit_gate_ns_e3"
                )
                assert result.data()["jobParams"]["qecScheme"]["name"] == "surface_code"
                assert result.data()["jobParams"]["errorBudget"] == 0.001

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_qiskit_controlled_s_to_resource_estimator_with_high_error_rate(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("microsoft.estimator")

            circuit = self._controlled_s()

            qiskit_job = backend.run(
                circuit, qubitParams={"name": "qubit_gate_ns_e4"}, errorBudget=0.0001
            )

            # Make sure the job is completed before fetching results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert result.data()["logicalCounts"]["numQubits"] == 2
                assert (
                    result.data()["jobParams"]["qubitParams"]["name"]
                    == "qubit_gate_ns_e4"
                )
                assert result.data()["jobParams"]["qecScheme"]["name"] == "surface_code"
                assert result.data()["jobParams"]["errorBudget"] == 0.0001

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_qiskit_controlled_s_to_resource_estimator_with_items(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("microsoft.estimator")

            circuit = self._controlled_s()

            # TODO: explicit entryPoint specification can be removed after
            #       change in microsoft.estimator target.
            item1 = {"entryPoint": "circuit-0", "qubitParams": {"name": "qubit_gate_ns_e3"}, "errorBudget": 1e-4}
            item2 = {"entryPoint": "circuit-0", "qubitParams": {"name": "qubit_gate_ns_e4"}, "errorBudget": 1e-4}
            qiskit_job = backend.run(circuit, items=[item1, item2])

            # Make sure the job is completed before fetching results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            print(qiskit_job)
            print(dir(qiskit_job))

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()

                assert result.data(0)["logicalCounts"]["numQubits"] == 2
                assert (
                    result.data(0)["jobParams"]["qubitParams"]["name"]
                    == "qubit_gate_ns_e3"
                )
                assert (
                    result.data(0)["jobParams"]["qecScheme"]["name"] == "surface_code"
                )
                assert result.data(0)["jobParams"]["errorBudget"] == 0.0001

                assert result.data(1)["logicalCounts"]["numQubits"] == 2
                assert (
                    result.data(1)["jobParams"]["qubitParams"]["name"]
                    == "qubit_gate_ns_e4"
                )
                assert (
                    result.data(1)["jobParams"]["qecScheme"]["name"] == "surface_code"
                )
                assert result.data(1)["jobParams"]["errorBudget"] == 0.0001

    def test_backend_without_azure_config_format_defaults_to_ms_format(self):
        backend = NoopQirBackend(None, "AzureQuantumProvider")
        output_data_format = backend._get_output_data_format()
        assert output_data_format == MICROSOFT_OUTPUT_DATA_FORMAT

    def test_backend_with_azure_config_format_defaults_to_that_format(self):
        expected = "test_format"
        backend = NoopQirBackend(
            None, "AzureQuantumProvider", output_data_format=expected
        )
        actual = backend._get_output_data_format()
        assert expected == actual

    def test_backend_without_azure_config_format_and_multiple_experiment_support_defaults_to_ms_format_v2(
        self,
    ):
        backend = NoopQirBackend(None, "AzureQuantumProvider", **{"max_experiments": 2})
        output_data_format = backend._get_output_data_format()
        assert output_data_format == MICROSOFT_OUTPUT_DATA_FORMAT_V2

    def test_backend_with_azure_config_format_is_overridden_with_explicit_format(self):
        azure_congfig_value = "test_format"
        backend = NoopQirBackend(
            None, "AzureQuantumProvider", output_data_format=azure_congfig_value
        )
        expected = "test_format_v2"
        options = {"output_data_format": expected}
        actual = backend._get_output_data_format(options)
        assert "output_data_format" not in options
        assert expected == actual
