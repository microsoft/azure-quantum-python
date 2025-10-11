##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
import numpy as np

from azure.quantum._client.models import CostEstimate, UsageEvent
from azure.quantum.target import IonQ
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
    @pytest.mark.live_test
    def test_job_submit_ionq(self):
        self._test_job_submit_ionq(shots=None)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq_100_shots(self):
        self._test_job_submit_ionq(shots=100)

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq_with_shots_from_input_params(self):
        workspace = self.create_workspace()
        circuit = self._3_qubit_ghz()
        target = IonQ(workspace=workspace)

        shots = 100

        job = target.submit(
            circuit=circuit,
            input_params={"shots": shots},
        )

        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)   
        assert job.details.input_params["shots"] == shots
        
    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq_with_conflicting_shots_from_input_params(self):
        workspace = self.create_workspace()
        circuit = self._3_qubit_ghz()
        target = IonQ(workspace=workspace)

        shots = 100

        with pytest.warns( 
             match="Parameter 'shots' conflicts with the 'shots' field of the 'input_params' parameter. "
                  "Please, provide only one option for setting shots. Defaulting to 'shots' parameter.",
        ):
            job = target.submit(
                circuit=circuit,
                shots=shots,
                input_params={"shots": 20},
            )

        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)   
        assert job.details.input_params["shots"] == shots

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq_cost_estimate(self):
        job = self._test_job_submit_ionq(shots=None)
        self.assertIsNotNone(job.details)
        cost_estimate: CostEstimate = job.details.cost_estimate
        self.assertIsNotNone(cost_estimate)
        self.assertEqual(cost_estimate.currency_code, "USD")
        events: list[UsageEvent] = cost_estimate.events
        self.assertGreater(len(events), 0)
        self.assertGreaterEqual(cost_estimate.estimated_total, 0)

    def _test_job_submit_ionq(
            self, 
            shots: int = None,
            circuit=None
        ):
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
        
        additional_kwargs = {}

        if shots is not None:
            additional_kwargs["shots"] = shots


        job = target.submit(
            circuit=circuit,
            name="ionq-3ghz-job",
            **additional_kwargs,
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

        if shots is not None:
            self.assertEqual(job.details.input_params.get("shots"), shots)
        else:
            self.assertIsNone(job.details.input_params.get("shots"))

        return job

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_ionq_qpu_target(self):
        workspace = self.create_workspace()
        target = IonQ(workspace=workspace, name="ionq.qpu.aria-1")
        self.assertEqual("ionq.qpu.aria-1", target.name)
        self.assertEqual("ionq.circuit.v1", target.input_data_format)
        self.assertEqual("ionq.quantum-results.v1", target.output_data_format)
        self.assertEqual("IonQ", target.provider_id)
        self.assertEqual("application/json", target.content_type)
        self.assertEqual("", target.encoding)
