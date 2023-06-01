
##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
from azure.quantum.aio.target import IonQ
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
        self.get_async_result(self._test_job_submit_ionq(num_shots=None))

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_job_submit_ionq_100_shots(self):
        self.get_async_result(self._test_job_submit_ionq(num_shots=100))

    async def _test_job_submit_ionq(self, num_shots):
        workspace = self.create_async_workspace()
        circuit = self._3_qubit_ghz()
        target = IonQ(workspace=workspace)
        job = await target.submit(
            circuit=circuit,
            name="ionq-3ghz-job",
            num_shots=num_shots
        )

        await job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        job = await workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        results = await job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertIn("histogram", results)
        self.assertEqual(results["histogram"]["0"], 0.5)
        self.assertEqual(results["histogram"]["7"], 0.5)

        if num_shots:
            self.assertEqual(job.details.input_params.get("shots"), num_shots)
        else:
            self.assertIsNone(job.details.input_params.get("shots"))
