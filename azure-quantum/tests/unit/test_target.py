##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
import numpy as np

from azure.quantum._client.models import CostEstimate, UsageEvent
from azure.quantum.target import IonQ, Quantinuum
from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS


class TestIonQ(QuantumTestBase):
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
        self.assertEqual(cost.estimated_total, 0.0)

        target = IonQ(workspace=workspace, name="ionq.qpu")
        cost = target.estimate_cost(circuit, num_shots=100e3)
        self.assertEqual(np.round(cost.estimated_total), 63.0)

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
        workspace = self.create_workspace()
        if circuit is None:
            circuit = self._3_qubit_ghz()
        target = IonQ(workspace=workspace)
        self.assertEqual("ionq.simulator", target.name)
        self.assertEqual("ionq.circuit.v1", target.input_data_format)
        self.assertEqual("ionq.quantum-results.v1", target.output_data_format)
        self.assertEqual("IonQ", target.provider_id)
        self.assertEqual("application/json", target.content_type)
        self.assertEqual("", target.encoding)

        job = target.submit(
            circuit=circuit,
            name="ionq-3ghz-job",
            num_shots=num_shots
        )

        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        # Check if job succeeded
        self.assertEqual(True, job.has_completed())
        self.assertEqual(job.details.status, "Succeeded")
        self.resume_recording()

        job.refresh()

        job = workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        if job.has_completed():
            results = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
            self.assertIn("histogram", results)
            self.assertEqual(results["histogram"]["0"], 0.5)
            self.assertEqual(results["histogram"]["7"], 0.5)

        if num_shots:
            self.assertEqual(job.details.input_params.get("shots"), num_shots)
        else:
            self.assertIsNone(job.details.input_params.get("shots"))

        return job

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_ionq_qpu_target(self):
        workspace = self.create_workspace()
        target = IonQ(workspace=workspace, name="ionq.qpu")
        self.assertEqual("ionq.qpu", target.name)
        self.assertEqual("ionq.circuit.v1", target.input_data_format)
        self.assertEqual("ionq.quantum-results.v1", target.output_data_format)
        self.assertEqual("IonQ", target.provider_id)
        self.assertEqual("application/json", target.content_type)
        self.assertEqual("", target.encoding)


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
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        job = workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        if job.has_completed():
            results = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
            self.assertEqual(results["c0"], ["0"])
            self.assertEqual(results["c1"], ["0"])
