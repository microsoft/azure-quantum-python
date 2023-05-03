##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest

from azure.quantum import  JobStatus
from azure.quantum.target import Quantinuum

from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS

class TestQuantinuum(QuantumTestBase):
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
        workspace = self.create_workspace()
        circuit = self._teleport()

        target = Quantinuum(workspace=workspace, name="quantinuum.hqs-lt-s1-apival")

        cost = target.estimate_cost(circuit, num_shots=100e3)
        self.assertEqual(cost.estimated_total, 0.0)

        target = Quantinuum(workspace=workspace, name="quantinuum.hqs-lt-s1")

        cost = target.estimate_cost(circuit, num_shots=100e3)
        self.assertEqual(cost.estimated_total, 845.0)

        target = Quantinuum(workspace=workspace, name="quantinuum.sim.h1-1sc")

        cost = target.estimate_cost(circuit, num_shots=100e3)
        self.assertEqual(cost.estimated_total, 0.0)

        target = Quantinuum(workspace=workspace, name="quantinuum.qpu.h1-1")

        cost = target.estimate_cost(circuit, num_shots=100e3)
        self.assertEqual(cost.estimated_total, 845.0)

        target = Quantinuum(workspace=workspace, name="quantinuum.sim.h1-2sc")

        cost = target.estimate_cost(circuit, num_shots=100e3)
        self.assertEqual(cost.estimated_total, 0.0)

        target = Quantinuum(workspace=workspace, name="quantinuum.qpu.h1-2")

        cost = target.estimate_cost(circuit, num_shots=100e3)
        self.assertEqual(cost.estimated_total, 845.0)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_job_submit_quantinuum(self):
        workspace = self.create_workspace()
        circuit = self._teleport()
        target = Quantinuum(workspace=workspace)
        job = target.submit(circuit)
        self.assertEqual(False, job.has_completed())
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        self.assertEqual(True, job.has_completed())
        self.assertEqual(job.details.status, JobStatus.SUCCEEDED)

        job = workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        results = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertEqual(results["c0"], ["0"])
        self.assertEqual(results["c1"], ["0"])
