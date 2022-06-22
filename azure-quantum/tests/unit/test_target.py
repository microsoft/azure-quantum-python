#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_qiskit.py: Tests for Qiskit plugin
##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import unittest
import warnings
import pytest

import numpy as np

from azure.core.exceptions import HttpResponseError
from azure.quantum.job.job import Job
from azure.quantum._client.models import CostEstimate, UsageEvent
from azure.quantum.target import IonQ, Honeywell, Quantinuum

from common import QuantumTestBase, ZERO_UID


class TestIonQ(QuantumTestBase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def _3_qubit_ghz(self):
        return {
            "qubits": 3,
            "circuit": [
                {
                "gate": "h",
                "target": 0
                },
                {
                "gate": "cnot",
                "control": 0,
                "target": 1
                },
                {
                "gate": "cnot",
                "control": 0,
                "target": 2
                },
            ]
        }

    @pytest.mark.ionq
    def test_estimate_cost_ionq(self):
        workspace = self.create_workspace()
        circuit = self._3_qubit_ghz()
        target = IonQ(workspace=workspace, name="ionq.simulator")
        cost = target.estimate_cost(circuit, num_shots=100e3)
        assert cost.estimated_total == 0.0

        target = IonQ(workspace=workspace, name="ionq.qpu")
        cost = target.estimate_cost(circuit, num_shots=100e3)
        assert np.round(cost.estimated_total) == 63.0


    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq(self):
        self._test_job_submit_ionq(num_shots=None)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq_100_shots(self):
        self._test_job_submit_ionq(num_shots=100)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq_cost_estimate(self):
        job = self._test_job_submit_ionq(num_shots=None)
        self.assertIsNotNone(job.details)
        cost_estimate: CostEstimate = job.details.cost_estimate
        self.assertIsNotNone(cost_estimate)
        self.assertEqual(cost_estimate.currency_code, "USD")
        events: list[UsageEvent] = cost_estimate.events
        self.assertGreater(len(events), 0)
        self.assertGreaterEqual(cost_estimate.estimated_total, 0)

    def _test_job_submit_ionq(self, num_shots, circuit=None):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            if circuit is None:
                circuit = self._3_qubit_ghz()
            target = IonQ(workspace=workspace)
            assert "ionq.simulator" == target.name
            assert "ionq.circuit.v1" == target.input_data_format
            assert "ionq.quantum-results.v1" == target.output_data_format
            assert "IonQ" == target.provider_id
            assert "application/json" == target.content_type
            assert "" == target.encoding

            job = target.submit(
                circuit=circuit,
                name="ionq-3ghz-job",
                num_shots=num_shots
            )

            # If in recording mode, we don't want to record the pooling of job
            # status as the current testing infrastructure does not support
            # multiple identical requests.
            # So we pause the recording until the job has actually completed.
            # See: https://github.com/microsoft/qdk-python/issues/118
            self.pause_recording()
            try:
                # Set a timeout for IonQ recording
                job.wait_until_completed(timeout_secs=60)
            except TimeoutError:
                warnings.warn("IonQ execution exceeded timeout. Skipping fetching results.")

            # Check if job succeeded
            self.assertEqual(True, job.has_completed())
            assert job.details.status == "Succeeded"
            self.resume_recording()

            # Record a single GET request such that job.wait_until_completed
            # doesn't fail when running recorded tests
            # See: https://github.com/microsoft/qdk-python/issues/118
            job.refresh()

            job = workspace.get_job(job.id)
            self.assertEqual(True, job.has_completed())

            if job.has_completed():
                results = job.get_results()
                assert "histogram" in results
                assert results["histogram"]["0"] == 0.5
                assert results["histogram"]["7"] == 0.5

            if num_shots:
                assert job.details.input_params.get("shots") == num_shots
            else:
                assert job.details.input_params.get("shots") is None

            return job

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_ionq_qpu_target(self):
        workspace = self.create_workspace()
        target = IonQ(workspace=workspace, name="ionq.qpu")
        assert "ionq.qpu" == target.name
        assert "ionq.circuit.v1" == target.input_data_format
        assert "ionq.quantum-results.v1" == target.output_data_format
        assert "IonQ" == target.provider_id
        assert "application/json" == target.content_type
        assert "" == target.encoding



class TestHoneywell(QuantumTestBase):
    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def _teleport(self):
        return """OPENQASM 2.0;
        include "qelib1.inc";

        qreg q[3];
        creg c0[1];
        creg c1[1];
        creg c2[1];

        h q[0];
        cx q[0], q[1];
        x q[2];
        h q[2];
        cx q[2], q[0];
        h q[2];
        measure q[0] -> c0[0];
        if (c0==1) x q[1];
        measure q[2] -> c1[0];
        if (c1==1) z q[1];
        h q[1];
        measure q[1] -> c2[0];
        """

    @pytest.mark.honeywell
    def test_job_estimate_cost_honeywell(self, provider_id="honeywell"):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            circuit = self._teleport()

            target = Honeywell(workspace=workspace, name="honeywell.hqs-lt-s1-apival") if provider_id == "honeywell" \
                     else Quantinuum(workspace=workspace, name="quantinuum.hqs-lt-s1-apival")

            cost = target.estimate_cost(circuit, num_shots=100e3)
            assert cost.estimated_total == 0.0

            target = Honeywell(workspace=workspace, name="honeywell.hqs-lt-s1") if provider_id == "honeywell" \
                     else Quantinuum(workspace=workspace, name="quantinuum.hqs-lt-s1")

            cost = target.estimate_cost(circuit, num_shots=100e3)
            assert cost.estimated_total == 845.0

    @pytest.mark.honeywell
    @pytest.mark.live_test
    def test_job_submit_honeywell(self, provider_id="honeywell"):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            circuit = self._teleport()
            target = Honeywell(workspace=workspace) if provider_id == "honeywell" \
                     else Quantinuum(workspace=workspace)
            try:
                job = target.submit(circuit)
            except HttpResponseError as e:
                if "InvalidJobDefinition" not in e.message \
                and "The provider specified does not exist" not in e.message:
                    raise(e)
                warnings.warn(e.message)
            else:
                # Make sure the job is completed before fetching the results
                # playback currently does not work for repeated calls
                if not self.is_playback:
                    self.pause_recording()
                    self.assertEqual(False, job.has_completed())
                    try:
                        # Set a timeout for Honeywell recording
                        job.wait_until_completed(timeout_secs=60)
                    except TimeoutError:
                        warnings.warn("Quantinuum (formerly Honeywell) execution exceeded timeout. Skipping fetching results.")
                    else:
                        # Check if job succeeded
                        self.assertEqual(True, job.has_completed())
                        assert job.details.status == "Succeeded"
                    self.resume_recording()

                job = workspace.get_job(job.id)
                self.assertEqual(True, job.has_completed())

                if job.has_completed():
                    results = job.get_results()
                    assert results["c0"] == ["0"]
                    assert results["c1"] == ["0"]

