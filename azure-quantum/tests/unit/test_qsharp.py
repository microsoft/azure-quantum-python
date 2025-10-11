##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
from azure.quantum import JobStatus
from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS
from import_qsharp import skip_if_no_qsharp
from test_job_payload_factory import JobPayloadFactory


@pytest.mark.qsharp
@pytest.mark.live_test
@skip_if_no_qsharp
class TestQSharpQIRJob(QuantumTestBase):

    @pytest.mark.rigetti
    def test_qsharp_qir_inline_rigetti(self):
        self._run_job("rigetti.sim.qvm", inline=True)

    @pytest.mark.rigetti
    def test_qsharp_qir_file_rigetti(self):
        self._run_job("rigetti.sim.qvm", inline=False)

    @pytest.mark.quantinuum
    def test_qsharp_qir_inline_quantinuum_h2(self):
        self._run_job("quantinuum.sim.h2-1e", inline=True)

    @pytest.mark.quantinuum
    def test_qsharp_qir_file_quantinuum(self):
        self._run_job("quantinuum.sim.h2-1e", inline=False)

    def _run_job(self, target_name, inline):
        workspace = self.create_workspace()
        target = workspace.get_targets(target_name)
        input_data = (JobPayloadFactory.get_qsharp_inline_callable_bell_state() if inline
                      else JobPayloadFactory.get_qsharp_file_callable_bell_state())
        job = target.submit(input_data=input_data)

        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        job.refresh()
        self.assertEqual(job.details.status, JobStatus.SUCCEEDED)

        results = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)

        # We assert that the test job outcomes are as expected (with one shot, one of the two outcomes should occur)
        self.assertTrue("(0, 0)" in results or "(1, 1)" in results)
        self.assertTrue(len(results.keys()) == 1)

        results_histogram = job.get_results_histogram()
        histogram_key = "(0, 0)"  if "(0, 0)" in results_histogram else "(1, 1)"

        self.assertIsNotNone(results_histogram[histogram_key])
        self.assertEqual(results_histogram[histogram_key]["outcome"], eval(histogram_key))
        self.assertEqual(results_histogram[histogram_key]["count"], 1)
        self.assertTrue(len(results_histogram.keys()) == 1)

        results_shots = job.get_results_shots()

        self.assertEqual(len(results_shots), 1)
        self.assertEqual(results_shots[0], results_histogram[histogram_key]["outcome"])
