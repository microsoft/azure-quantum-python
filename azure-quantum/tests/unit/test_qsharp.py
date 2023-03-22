##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import unittest
import warnings
import pytest
from azure.quantum.job import Job
from common import QuantumTestBase, ZERO_UID

@pytest.mark.qsharp
@pytest.mark.live_test
@pytest.mark.skip(reason="Temporarily disabling these tests as they are failing the QDK build")
class TestQSharpQIRJob(QuantumTestBase):

    @pytest.mark.rigetti
    def test_qsharp_qir_rigetti(self):
        self._run_job("rigetti.sim.qvm")

    @pytest.mark.quantinuum
    def test_qsharp_qir_quantinuum(self):
        self._run_job("quantinuum.sim.h1-1sc")

    @pytest.fixture(autouse=True, scope='class')
    def _qsharp_callable(self):
        import qsharp
        TestQSharpQIRJob.qsharp_callable = qsharp.compile("""
            open Microsoft.Quantum.Intrinsic;
            operation GenerateRandomBit_Inline() : Result {
                use q0 = Qubit();
                H(q0);
                return M(q0);
            }
        """)

    def _run_job(self, target_name):
        with unittest.mock.patch.object(
            Job,
            "create_job_id",
            return_value=ZERO_UID if self.is_playback else Job.create_job_id(),
        ):
            workspace = self.create_workspace()
            target = workspace.get_targets(target_name)
            job = target.submit(input_data=TestQSharpQIRJob.qsharp_callable)

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
