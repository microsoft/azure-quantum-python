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
import re

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

from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS

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
        self.assertLess(pos, 3)
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

        self.assertEqual(AzureQuantumJob._qir_to_qiskit_bitstring(azure_register), bitstring)
        self.assertEqual(AzureQuantumJob._qir_to_qiskit_bitstring(azure_registers), " ".join(
            f"{bit}10" for bit in reversed(bits)
        ))
        self.assertEqual(AzureQuantumJob._qir_to_qiskit_bitstring(bitstring), bitstring)

    def test_qiskit_submit_ionq_5_qubit_superposition(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("ionq.simulator")
        num_shots = 1000

        circuit = self._5_qubit_superposition()
        circuit.metadata = {"some": "data"}

        qiskit_job = backend.run(circuit, shots=num_shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "ionq.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "ionq")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "ionq.circuit.v1")
        self.assertEqual(qiskit_job._azure_job.details.output_data_format, "ionq.quantum-results.v1")
        self.assertIn("qiskit", qiskit_job._azure_job.details.metadata)
        self.assertIn("name", qiskit_job._azure_job.details.metadata)
        self.assertIn("meas_map", qiskit_job._azure_job.details.metadata)
        self.assertIn("metadata", qiskit_job._azure_job.details.metadata)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertEqual(sum(result.data()["counts"].values()), num_shots)
            self.assertAlmostEqual(result.data()["counts"]["0"], num_shots // 2, delta=50)
            self.assertAlmostEqual(result.data()["counts"]["1"], num_shots // 2, delta=50)
            self.assertEqual(result.data()["probabilities"], {"0": 0.5, "1": 0.5})
            counts = result.get_counts()
            self.assertEqual(counts, result.data()["counts"])
            self.assertEqual(result.results[0].header.num_qubits, "5")
            self.assertEqual(result.results[0].header.metadata["some"], "data")

    @pytest.mark.ionq
    def test_plugins_estimate_cost_qiskit_ionq(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("ionq.simulator")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(cost.estimated_total, 0.0)

        backend = provider.get_backend("ionq.qpu")
        cost = backend.estimate_cost(circuit, shots=1024)
        self.assertEqual(np.round(cost.estimated_total), 1.0)

        backend = provider.get_backend("ionq.qpu")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(np.round(cost.estimated_total), 66.0)

        ## The following two tests are skipped until we can use a workspace
        ## with this target available as part of the E2E tests.
        # backend = provider.get_backend("ionq.qpu.aria-1")
        # cost = backend.estimate_cost(circuit, shots=1024)
        # self.assertEqual(np.round(cost.estimated_total), 1.0)

        # backend = provider.get_backend("ionq.qpu.aria-1")
        # cost = backend.estimate_cost(circuit, shots=100e3)
        # self.assertEqual(np.round(cost.estimated_total), 240.0)

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
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("ionq.simulator")

        with pytest.raises(NotImplementedError) as exc:
            backend.run(circuit=[circuit, circuit], shots=500)
        self.assertEqual(str(exc.value), "Multi-experiment jobs are not supported!")

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_qobj_to_ionq(self):
        from qiskit import assemble

        circuit = self._3_qubit_ghz()
        qobj = assemble(circuit)
        self._test_qiskit_submit_ionq(circuit=qobj, shots=1024)

    def _qiskit_wait_to_complete(
            self,
            qiskit_job,
            provider,
            expected_status=JobStatus.DONE):
        job = qiskit_job._azure_job
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertEqual(expected_status, qiskit_job.status())
        qiskit_job = provider.get_job(job.id)
        self.assertEqual(expected_status, qiskit_job.status())

    def test_plugins_submit_qiskit_to_ionq_with_shots_param(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        
        shots = 10
        qiskit_job = backend.run(circuit, shots=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)
    
    def test_plugins_submit_qiskit_to_ionq_with_default_shots(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        
        qiskit_job = backend.run(circuit)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], 500)

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
        
        shots = 10

        with pytest.warns(
            DeprecationWarning, 
            match="The 'count' parameter will be deprecated. Please, use 'shots' parameter instead."
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)

    def _test_qiskit_submit_ionq(self, circuit, **kwargs):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("ionq.simulator")
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
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, expected_data_format)
        self.assertEqual(qiskit_job._azure_job.details.output_data_format, "ionq.quantum-results.v1")
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
            self.assertTrue(hasattr(result.results[0].header, "num_qubits"))
            self.assertTrue(hasattr(result.results[0].header, "metadata"))

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
    def test_ionq_simulator_default_target_has_qis_gateset(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.simulator")
        config = backend.configuration()
        self.assertEqual(config.gateset, "qis")

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
        self.assertEqual(input_data_format, "qir.v1")

    @pytest.mark.ionq
    def test_ionq_qpu_has_native_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu", gateset="native")
        config = backend.configuration()
        self.assertEqual(config.gateset, "native")

    @pytest.mark.ionq
    def test_ionq_qpu_has_qis_gateset_target(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu", gateset="qis")
        config = backend.configuration()
        self.assertEqual(config.gateset, "qis")

    @pytest.mark.ionq
    def test_ionq_qpu_default_target_has_qis_gateset(self):
        provider = DummyProvider()
        backend = provider.get_backend("ionq.qpu")
        config = backend.configuration()
        self.assertEqual(config.gateset, "qis")

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

        self.assertIsInstance(payload, bytes)
        self.assertEqual(input_data_format, "qir.v1")
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT)
        self.assertIn("items", input_params)
        self.assertEqual(len(input_params["items"]), 1)
        item = input_params["items"][0]
        self.assertIn("entryPoint", item)
        self.assertIn("arguments", item)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_qiskit_get_ionq_qpu_target(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("ionq.qpu")
        self.assertEqual(backend.name(), "ionq.qpu")
        config = backend.configuration()
        self.assertFalse(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(11, config.num_qubits)
        self.assertEqual("application/json", config.azure["content_type"])
        self.assertEqual("ionq", config.azure["provider_id"])
        self.assertEqual("ionq.circuit.v1", config.azure["input_data_format"])
        self.assertEqual("ionq.quantum-results.v1", config.azure["output_data_format"])
        self.assertEqual("qis", backend.gateset())

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
    def test_ionq_aria2_has_default(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-2")

    @pytest.mark.ionq
    def test_ionq_aria2_has_qir_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-2", input_data_format="qir.v1")

    @pytest.mark.ionq
    def test_ionq_aria2_has_native_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-2", gateset="native")

    @pytest.mark.ionq
    def test_ionq_aria2_has_qis_gateset_target(self):
        provider = DummyProvider()
        provider.get_backend("ionq.qpu.aria-2", gateset="qis")

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
    #     self.assertEqual(backend.name(), "ionq.qpu.aria-1")
    #     config = backend.configuration()
    #     self.assertFalse(config.simulator)
    #     self.assertEqual(1, config.max_experiments)
    #     self.assertEqual(23, config.num_qubits)
    #     self.assertEqual("ionq", config.azure["provider_id"])
    #     self.assertEqual("ionq.circuit.v1", config.azure["input_data_format"])
    #     self.assertEqual("ionq.quantum-results.v1", config.azure["output_data_format"])

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
        self.assertEqual(2, len(metadata["meas_map"]))

        # should also be available with the qpu target
        backend = provider.get_backend("ionq.qpu", gateset="native")
        config = backend.configuration()
        self.assertEqual("native", backend.gateset())
        payload = backend._translate_input(native_circuit)
        payload = json.loads(payload.decode("utf-8"))
        self.assertEqual("ms", payload["circuit"][0]["gate"])
        metadata = backend._prepare_job_metadata(native_circuit)
        self.assertEqual(2, len(metadata["meas_map"]))

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_retrieve_job(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
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

    @pytest.mark.quantinuum
    def test_plugins_estimate_cost_qiskit_quantinuum(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)

        backend = provider.get_backend("quantinuum.sim.h1-1sc")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(cost.estimated_total, 0.0)

        backend = provider.get_backend("quantinuum.sim.h1-1e")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(cost.estimated_total, 745.0)

        backend = provider.get_backend("quantinuum.qpu.h1-1")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(cost.estimated_total, 745.0)

        backend = provider.get_backend("quantinuum.sim.h2-1sc")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(cost.estimated_total, 0.0)

        backend = provider.get_backend("quantinuum.sim.h2-1e")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(cost.estimated_total, 745.0)

        backend = provider.get_backend("quantinuum.qpu.h2-1")
        cost = backend.estimate_cost(circuit, shots=100e3)
        self.assertEqual(cost.estimated_total, 745.0)

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
    def test_plugins_submit_qiskit_to_quantinuum_h2_1e(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit,
                                            target="quantinuum.sim.h2-1e")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_quantinuum_h2_1sc(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit,
                                            target="quantinuum.sim.h2-1sc")

    @pytest.mark.quantinuum
    @pytest.mark.skip("Target was unavailable at the moment of the recording")
    def test_plugins_submit_qiskit_to_quantinuum_h2_1qpu(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_quantinuum(circuit,
                                            target="quantinuum.qpu.h2-1")

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
        backend = provider.get_backend("quantinuum.sim.h1-2e")
        self.assertIn("quantinuum.sim.h1-2e", backend.backend_names)
        self.assertIn(backend.backend_names[0], [
            t.name for t in workspace.get_targets(provider_id="quantinuum")
        ])

        with self.assertRaises(NotImplementedError) as context:
            backend.run(circuit=[circuit, circuit], shots=None)
        self.assertEqual(str(context.exception), "Multi-experiment jobs are not supported!")
    
    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_quantinuum_with_counts_param(self):
        """
        This test verifies that we can pass a "provider-specific" shots number option.
        Even if the usage of the 'shots' option is encouraged, we should also be able to specify provider's 
        native option ('count' in this case).
        """
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h1-1e")
        
        shots = 10
        qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)
    
    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_quantinuum_with_explicit_shots_param(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h1-1e")
        
        shots = 10
        qiskit_job = backend.run(circuit, shots=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_quantinuum_with_default_shots_param(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(name="quantinuum.sim.h1-1e")
        
        qiskit_job = backend.run(circuit)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], 500)

    def _test_qiskit_submit_quantinuum(self, circuit, target="quantinuum.sim.h1-1e", **kwargs):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(target)
        expected_data_format = (
            kwargs["input_data_format"]
            if "input_data_format" in kwargs
            else "honeywell.openqasm.v1"
        )
        self.assertIn(target, backend.backend_names)
        self.assertIn(backend.backend_names[0], [
            t.name for t in workspace.get_targets(provider_id="quantinuum")
        ])

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
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, expected_data_format)
        self.assertEqual(qiskit_job._azure_job.details.output_data_format, "honeywell.quantum-results.v1")
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
        self.assertTrue(hasattr(result.results[0].header, "num_qubits"))
        self.assertEqual(result.results[0].header.num_qubits, str(num_qubits))
        self.assertEqual(result.results[0].header.metadata["some"], "data")

    @pytest.mark.quantinuum
    def test_translate_quantinuum_qir(self):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = QuantinuumEmulatorQirBackend(
            "quantinuum.sim.h1-2e", provider
        )

        input_params = backend._get_input_params({})
        payload = backend._translate_input(circuit, input_params)

        config = backend.configuration()
        input_data_format = config.azure["input_data_format"]
        output_data_format = backend._get_output_data_format()

        self.assertIsInstance(payload, bytes)
        self.assertEqual(input_data_format, "qir.v1")
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT)
        self.assertIn("items", input_params)
        self.assertEqual(len(input_params["items"]), 1)
        item = input_params["items"][0]
        self.assertIn("entryPoint", item)
        self.assertIn("arguments", item)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_configuration_quantinuum_backends(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        # The following backends should have 20 qubits
        for target_name in [
            "quantinuum.qpu.h1-1",
            "quantinuum.sim.h1-1sc",
            "quantinuum.sim.h1-1e",
            "quantinuum.qpu.h1-2",
            "quantinuum.sim.h1-2sc",
            "quantinuum.sim.h1-2e",
        ]:
            config = provider.get_backend(target_name).configuration()
            # We check for name so the test log includes it when reporting a failure
            self.assertIsNotNone(target_name)
            self.assertEqual(20, config.num_qubits)

        # The following backends should have 32 qubits
        for target_name in [
            "quantinuum.qpu.h2-1",
            "quantinuum.sim.h2-1sc",
            "quantinuum.sim.h2-1e",
        ]:
            config = provider.get_backend(target_name).configuration()
            # We check for name so the test log includes it when reporting a failure
            self.assertIsNotNone(target_name)
            self.assertEqual(32, config.num_qubits)

    @pytest.mark.rigetti
    @pytest.mark.live_test
    def test_qiskit_submit_to_rigetti(self):
        from azure.quantum.target.rigetti import RigettiTarget

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        self.assertEqual(backend.name(), RigettiTarget.QVM.value)
        config = backend.configuration()
        self.assertTrue(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(20, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("rigetti", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual("microsoft.quantum-results.v1", backend._get_output_data_format())
        shots = 100

        circuit = self._3_qubit_ghz()

        qiskit_job = backend.run(circuit, count=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, RigettiTarget.QVM.value)
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "rigetti")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "qir.v1")
        self.assertEqual(qiskit_job._azure_job.details.output_data_format, "microsoft.quantum-results.v1")
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)
        self.assertEqual(qiskit_job._azure_job.details.input_params["items"][0]["entryPoint"], circuit.name)
        self.assertEqual(qiskit_job._azure_job.details.input_params["items"][0]["arguments"], [])

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
            self.assertEqual(counts, result.data()["counts"])  
    
    @pytest.mark.rigetti
    @pytest.mark.live_test
    def test_qiskit_submit_to_rigetti_with_count_param(self):
        """
        This test verifies that we can pass a "provider-specific" shots number option.
        Even if the usage of the 'shots' option is encouraged, we should also be able to specify provider's 
        native option ('count' in this case).
        """
        from azure.quantum.target.rigetti import RigettiTarget

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(RigettiTarget.QVM.value)
        shots = 100
        circuit = self._3_qubit_ghz()

        qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)
        
    @pytest.mark.rigetti
    @pytest.mark.live_test
    def test_qiskit_submit_to_rigetti_with_explicit_shots_param(self):
        from azure.quantum.target.rigetti import RigettiTarget

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
    def test_qiskit_get_rigetti_qpu_targets(self):
        from azure.quantum.target.rigetti import RigettiTarget

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend(RigettiTarget.ASPEN_M_3.value)
        self.assertEqual(backend.name(), RigettiTarget.ASPEN_M_3.value)
        config = backend.configuration()
        self.assertFalse(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(80, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("rigetti", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual("microsoft.quantum-results.v1", backend._get_output_data_format())

    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_submit_to_qci(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        self.assertIn("azure-quantum-qiskit", provider._workspace.user_agent)
        backend = provider.get_backend("qci.simulator")
        self.assertEqual(backend.name(), "qci.simulator")
        config = backend.configuration()
        self.assertTrue(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(29, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("qci", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual("microsoft.quantum-results.v1", backend._get_output_data_format())
        shots = 100

        circuit = self._3_qubit_ghz()

        qiskit_job = backend.run(circuit, shots=shots)

        # Check job metadata:
        self.assertEqual(qiskit_job._azure_job.details.target, "qci.simulator")
        self.assertEqual(qiskit_job._azure_job.details.provider_id, "qci")
        self.assertEqual(qiskit_job._azure_job.details.input_data_format, "qir.v1")
        self.assertEqual(qiskit_job._azure_job.details.output_data_format, "microsoft.quantum-results.v1")
        self.assertEqual(qiskit_job._azure_job.details.input_params["count"], shots)
        self.assertEqual(qiskit_job._azure_job.details.input_params["items"][0]["entryPoint"], circuit.name)
        self.assertEqual(qiskit_job._azure_job.details.input_params["items"][0]["arguments"], [])

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

        shots=10
        circuit = self._3_qubit_ghz()
        with pytest.warns(
            DeprecationWarning, 
            match="The 'count' parameter will be deprecated. Please, use 'shots' parameter instead."
        ):
            qiskit_job = backend.run(circuit, count=shots)
        self._qiskit_wait_to_complete(qiskit_job, provider)
        self.assertEqual(qiskit_job._azure_job.details.input_params["shots"], shots)

    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_get_qci_qpu_targets(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)

        backend = provider.get_backend("qci.machine1")
        self.assertEqual(backend.name(), "qci.machine1")
        config = backend.configuration()
        self.assertFalse(config.simulator)
        self.assertEqual(1, config.max_experiments)
        self.assertEqual(11, config.num_qubits)
        self.assertEqual("qir.v1", config.azure["content_type"])
        self.assertEqual("qci", config.azure["provider_id"])
        self.assertEqual("qir.v1", config.azure["input_data_format"])
        self.assertEqual("microsoft.quantum-results.v1", backend._get_output_data_format())

    # @pytest.mark.parametrize("endian_pos, expectation",
    #     [(0,"000 000 001"), (1,"000 010 000"), (2,"100 000 000")]
    # )
    @pytest.mark.qci
    @pytest.mark.live_test
    def test_qiskit_endianness_submit_to_qci(
        self, endian_pos=0, expectation="000 000 001"
    ):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("qci.simulator")
        shots = 100

        circuit = self._endianness(pos=endian_pos)
        circuit.metadata = {"some": "data"}

        qiskit_job = backend.run(circuit, shots=shots)

        # Make sure the job is completed before fetching the results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            print(result)
            self.assertEqual(sum(result.data()["counts"].values()), shots)
            self.assertEqual(result.data()["counts"][expectation], shots)

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_qiskit_controlled_s_to_resource_estimator(self):
        from pyqir import rt

        patcher = unittest.mock.patch.object(rt, "initialize")
        patcher.start()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("microsoft.estimator")

        circuit = self._controlled_s()

        qiskit_job = backend.run(circuit)

        # Make sure the job is completed before fetching results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        patcher.stop()

        self.assertEqual(qiskit_job.status(), JobStatus.DONE)
        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertEqual(result.data()["logicalCounts"]["numQubits"], 2)
            self.assertEqual(result.data()["jobParams"]["qubitParams"]["name"], "qubit_gate_ns_e3")
            self.assertEqual(result.data()["jobParams"]["qecScheme"]["name"], "surface_code")
            self.assertEqual(result.data()["jobParams"]["errorBudget"], 0.001)

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_qiskit_controlled_s_to_resource_estimator_with_high_error_rate(self):
        from pyqir import rt

        patcher = unittest.mock.patch.object(rt, "initialize")
        patcher.start()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("microsoft.estimator")

        circuit = self._controlled_s()

        qiskit_job = backend.run(
            circuit, qubitParams={"name": "qubit_gate_ns_e4"}, errorBudget=0.0001
        )

        # Make sure the job is completed before fetching results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        patcher.stop()

        self.assertEqual(qiskit_job.status(), JobStatus.DONE)
        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()
            self.assertEqual(result.data()["logicalCounts"]["numQubits"], 2)
            self.assertEqual(result.data()["jobParams"]["qubitParams"]["name"], "qubit_gate_ns_e4")
            self.assertEqual(result.data()["jobParams"]["qecScheme"]["name"], "surface_code")
            self.assertEqual(result.data()["jobParams"]["errorBudget"], 0.0001)

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_qiskit_controlled_s_to_resource_estimator_with_items(self):
        from pyqir import rt

        patcher = unittest.mock.patch.object(rt, "initialize")
        patcher.start()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("microsoft.estimator")

        circuit = self._controlled_s()

        item1 = {"qubitParams": {"name": "qubit_gate_ns_e3"}, "errorBudget": 1e-4}
        item2 = {"qubitParams": {"name": "qubit_gate_ns_e4"}, "errorBudget": 1e-4}
        qiskit_job = backend.run(circuit, items=[item1, item2])

        # Make sure the job is completed before fetching results
        self._qiskit_wait_to_complete(qiskit_job, provider)

        patcher.stop()

        self.assertEqual(qiskit_job.status(), JobStatus.DONE)
        if JobStatus.DONE == qiskit_job.status():
            result = qiskit_job.result()

            self.assertEqual(result.data(0)["logicalCounts"]["numQubits"], 2)
            self.assertEqual(result.data(0)["jobParams"]["qubitParams"]["name"], "qubit_gate_ns_e3")
            self.assertEqual(result.data(0)["jobParams"]["qecScheme"]["name"], "surface_code")
            self.assertEqual(result.data(0)["jobParams"]["errorBudget"], 0.0001)

            self.assertEqual(result.data(1)["logicalCounts"]["numQubits"], 2)
            self.assertEqual(result.data(1)["jobParams"]["qubitParams"]["name"], "qubit_gate_ns_e4")
            self.assertEqual(result.data(1)["jobParams"]["qecScheme"]["name"], "surface_code")
            self.assertEqual(result.data(1)["jobParams"]["errorBudget"], 0.0001)

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

    def test_backend_without_azure_config_format_and_multiple_experiment_support_defaults_to_ms_format_v2(
        self,
    ):
        backend = NoopQirBackend(None, "AzureQuantumProvider", **{"max_experiments": 2})
        output_data_format = backend._get_output_data_format()
        self.assertEqual(output_data_format, MICROSOFT_OUTPUT_DATA_FORMAT_V2)

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
            "quantinuum.sim.h1-1sc", "AzureQuantumProvider"
        )
        with pytest.raises(ValueError) as exc:
            # mimic the user passing in targetCapabilities as part of the run options
            _ = backend._run("", None, {"targetCapability": "BasicExecution"}, {})
        actual = str(exc.value)
        expected = "The targetCapability parameter has been deprecated"
        self.assertTrue(actual.startswith(expected))
