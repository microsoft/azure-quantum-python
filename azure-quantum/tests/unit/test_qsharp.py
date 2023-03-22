##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import unittest
import warnings
import pytest
from azure.quantum.job import Job
from common import QuantumTestBase, ZERO_UID
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

    def _run_job(self, target_name, inline):
        with unittest.mock.patch.object(
            Job,
            "create_job_id",
            return_value=ZERO_UID if self.is_playback else Job.create_job_id(),
        ):
            workspace = self.create_workspace()
            target = workspace.get_targets(target_name)
            input_data = (JobPayloadFactory.get_qsharp_inline_callable_bell_state()[0] if inline
                          else JobPayloadFactory.get_qsharp_file_callable_bell_state()[0])
            job = target.submit(input_data=input_data)

            self.pause_recording()
            try:
                job.wait_until_completed(timeout_secs=60)
            except TimeoutError:
                warnings.warn(
                    "Wait_until_completed exceeded timeout. Skipping fetching results."
                )
                return None
            self.resume_recording()

            job.refresh()
            assert job.details.status == "Succeeded"

            results = job.get_results()
            assert results is not None
