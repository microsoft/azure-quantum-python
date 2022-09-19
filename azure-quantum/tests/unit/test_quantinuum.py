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
from azure.quantum.target import Quantinuum

from common import QuantumTestBase, ZERO_UID


class TestQuantinuum(QuantumTestBase):
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

    @pytest.mark.quantinuum
    def test_job_estimate_cost_quantinuum(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            circuit = self._teleport()

            target = Quantinuum(workspace=workspace, name="quantinuum.hqs-lt-s1-apival")

            cost = target.estimate_cost(circuit, num_shots=100e3)
            assert cost.estimated_total == 0.0

            target = Quantinuum(workspace=workspace, name="quantinuum.hqs-lt-s1")

            cost = target.estimate_cost(circuit, num_shots=100e3)
            assert cost.estimated_total == 845.0

            target = Quantinuum(workspace=workspace, name="quantinuum.sim.h1-1sc")

            cost = target.estimate_cost(circuit, num_shots=100e3)
            assert cost.estimated_total == 0.0

            target = Quantinuum(workspace=workspace, name="quantinuum.qpu.h1-1")

            cost = target.estimate_cost(circuit, num_shots=100e3)
            assert cost.estimated_total == 845.0

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_job_submit_quantinuum(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            circuit = self._teleport()
            target = Quantinuum(workspace=workspace)
            job = target.submit(circuit)
            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            if not self.is_playback:
                self.pause_recording()
                self.assertEqual(False, job.has_completed())
                try:
                    # Set a timeout for recording
                    job.wait_until_completed(timeout_secs=60)
                except TimeoutError:
                    warnings.warn("Quantinuum execution exceeded timeout. Skipping fetching results.")
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

