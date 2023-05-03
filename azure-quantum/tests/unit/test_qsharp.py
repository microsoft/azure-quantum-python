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
    def test_qsharp_qir_inline_quantinuum(self):
        self._run_job("quantinuum.sim.h1-1sc", inline=True)

    @pytest.mark.quantinuum
    def test_qsharp_qir_file_quantinuum(self):
        self._run_job("quantinuum.sim.h1-1sc", inline=False)

    @pytest.mark.microsoft_qc
    def test_qsharp_qir_inline_microsoft_qc(self):
        self._run_job("microsoft.estimator", inline=True)

    @pytest.mark.microsoft_qc
    def test_qsharp_qir_file_microsoft_qc(self):
        self._run_job("microsoft.estimator", inline=False)

    def _run_job(self, target_name, inline):
        workspace = self.create_workspace()
        target = workspace.get_targets(target_name)
        input_data = (JobPayloadFactory.get_qsharp_inline_callable_bell_state()[0] if inline
                      else JobPayloadFactory.get_qsharp_file_callable_bell_state()[0])
        job = target.submit(input_data=input_data)

        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        job.refresh()
        self.assertEqual(job.details.status, JobStatus.SUCCEEDED)

        results = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertIsNotNone(results)
