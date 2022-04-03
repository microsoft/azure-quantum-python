#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_qiskit.py: Tests for Qiskit plugin
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import unittest
import warnings
import pytest

import numpy as np

from qiskit import QuantumCircuit
from qiskit.providers import JobStatus
from qiskit.providers.exceptions import QiskitBackendNotFoundError

from azure.quantum.job.job import Job
from azure.quantum.qiskit import AzureQuantumProvider
from azure.quantum.qiskit.backends.honeywell import HONEYWELL_PROVIDER_ID

from common import QuantumTestBase, ZERO_UID

class TestQiskit(QuantumTestBase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def _3_qubit_ghz(self):
        circuit = QuantumCircuit(4, 3)
        circuit.name = "Qiskit Sample - 3-qubit GHZ circuit"
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.cx(1, 2)
        circuit.h(3) # Helper qubit that is not measured
        circuit.measure([0, 1, 2], [0, 1, 2])
        return circuit

    def _5_qubit_superposition(self):
        circuit = QuantumCircuit(5, 1)
        for q in range(5):
            circuit.h(q)
        circuit.measure([0], [0])
        return circuit

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

            qiskit_job = backend.run(
                circuit=self._5_qubit_superposition(),
                shots=num_shots
            )

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert sum(result.data()["counts"].values()) == num_shots
                assert np.isclose(result.data()["counts"]["0"], num_shots//2, 20)
                assert np.isclose(result.data()["counts"]["1"], num_shots//2, 20)
                assert result.data()["probabilities"] == {'0': 0.5, '1': 0.5}
                counts = result.get_counts()
                assert counts == result.data()["counts"]

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

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq(circuit=circuit, num_shots=500, num_shots_actual=500)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_circuit_as_list_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq(circuit=[circuit], num_shots=500, num_shots_actual=500)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_ionq(self):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        assert "azure-quantum-qiskit" in provider._workspace.user_agent
        backend = provider.get_backend("ionq.simulator")

        with pytest.raises(NotImplementedError) as exc:
            backend.run(
                circuit=[circuit, circuit],
                shots=500
            )
        assert str(exc.value) == "Multi-experiment jobs are not supported!"

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_qobj_to_ionq(self):
        from qiskit import assemble
        circuit = self._3_qubit_ghz()
        qobj = assemble(circuit)
        self._test_qiskit_submit_ionq(circuit=qobj, num_shots=1024, num_shots_actual=1024)

    def _qiskit_wait_to_complete(self, qiskit_job, provider):
        job = qiskit_job._azure_job
        self.pause_recording()
        try:
            job.wait_until_completed(timeout_secs=60)
        except TimeoutError:
            self.resume_recording()
            warnings.warn(f"Qiskit Job {job.id} exceeded timeout. Skipping fetching results.")
        else:
            self.resume_recording()

            # Record a single GET request such that job.wait_until_completed
            # doesn't fail when running recorded tests
            # See: https://github.com/microsoft/qdk-python/issues/118
            job.refresh()

            self.assertEqual(JobStatus.DONE, qiskit_job.status())
            qiskit_job = provider.get_job(job.id)
            self.assertEqual(JobStatus.DONE, qiskit_job.status())

    def _test_qiskit_submit_ionq(self, circuit, num_shots, num_shots_actual):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            assert "azure-quantum-qiskit" in provider._workspace.user_agent
            backend = provider.get_backend("ionq.simulator")

            qiskit_job = backend.run(
                circuit=circuit,
                shots=num_shots
            )

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert sum(result.data()["counts"].values()) == num_shots_actual
                assert np.isclose(result.data()["counts"]["000"], num_shots_actual//2, 20)
                assert np.isclose(result.data()["counts"]["111"], num_shots_actual//2, 20)
                assert result.data()["probabilities"] == {'000': 0.5, '111': 0.5}
                counts = result.get_counts()
                assert counts == result.data()["counts"]

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
            qiskit_job = backend.run(
                circuit=circuit,
                shots=100
            )

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                fetched_job = backend.retrieve_job(qiskit_job.id())
                assert fetched_job.id() == qiskit_job.id()
                result = fetched_job.result()
                assert result.data()["probabilities"] == {
                    '000': 0.5,
                    '111': 0.5
                }
                assert sum(result.data()["counts"].values()) == 100
                assert np.isclose(result.data()["counts"]["000"], 50, atol=20)
                assert np.isclose(result.data()["counts"]["111"], 50, atol=20)

    @pytest.mark.honeywell
    def test_plugins_estimate_cost_qiskit_honeywell(self, provider_id="honeywell"):
        circuit = self._3_qubit_ghz()
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        assert "azure-quantum-qiskit" in provider._workspace.user_agent
        backend = provider.get_backend(f"{provider_id}.hqs-lt-s1-apival")
        cost = backend.estimate_cost(circuit, shots=100e3)
        assert cost.estimated_total == 0.0

        backend = provider.get_backend(f"{provider_id}.hqs-lt-s1")
        cost = backend.estimate_cost(circuit, shots=100e3)
        assert cost.estimated_total == 745.0

    @pytest.mark.live_test
    def test_plugins_submit_qiskit_noexistent_target(self):
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        with pytest.raises(QiskitBackendNotFoundError):
            provider.get_backend("provider.doesnotexist")

    @pytest.mark.honeywell
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_honeywell(self, provider_id="honeywell"):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_honeywell(circuit=circuit, shots=None, provider_id=provider_id)

    @pytest.mark.honeywell
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_circuit_as_list_to_honeywell(self, provider_id="honeywell"):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_honeywell(circuit=[circuit], shots=None, provider_id=provider_id)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_honeywell(self, provider_id="honeywell"):
        circuit = self._3_qubit_ghz()

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(f"{provider_id}.hqs-lt-s1-apival")
        assert f"{provider_id}.hqs-lt-s1-apival" in backend.backend_names
        assert backend.backend_names[0] in [t.name for t in workspace.get_targets(provider_id=provider_id)]

        with pytest.raises(NotImplementedError) as exc:
            backend.run(
                circuit=[circuit, circuit],
                shots=None
            )
        assert str(exc.value) == "Multi-experiment jobs are not supported!"

    def _test_qiskit_submit_honeywell(self, circuit, shots, provider_id="honeywell"):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend(f"{provider_id}.hqs-lt-s1-apival")
            assert f"{provider_id}.hqs-lt-s1-apival" in backend.backend_names
            assert backend.backend_names[0] in [t.name for t in workspace.get_targets(provider_id=provider_id)]

            if shots is None:
                qiskit_job = backend.run(
                    circuit=circuit
                )

            else:
                qiskit_job = backend.run(
                    circuit=circuit,
                    shots=shots
                )

            # Make sure the job is completed before fetching the results
            self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert result.data()["counts"] == {'000': 500}
                assert result.data()["probabilities"] == {'000': 1.0}

    @pytest.mark.quantinuum
    def test_plugins_estimate_cost_qiskit_quantinuum(self):
        self.test_plugins_estimate_cost_qiskit_honeywell(provider_id="quantinuum")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_quantinuum(self):
        self.test_plugins_submit_qiskit_to_honeywell(provider_id="quantinuum")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_circuit_as_list_to_quantinuum(self):
        self.test_plugins_submit_qiskit_circuit_as_list_to_honeywell(provider_id="quantinuum")

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_multi_circuit_experiment_to_quantinuum(self):
        self.test_plugins_submit_qiskit_multi_circuit_experiment_to_honeywell(provider_id="quantinuum")
