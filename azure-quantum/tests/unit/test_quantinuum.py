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
    @pytest.mark.live_test
    def test_job_submit_quantinuum_with_shots(self):
        self._test_job_submit_quantinuum("quantinuum.sim.h2-1sc", shots=100)


    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_job_submit_quantinuum_with_none_shots(self):
        self._test_job_submit_quantinuum("quantinuum.sim.h2-1sc", shots=None)


    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_job_submit_quantinuum_with_conflictin_shots_and_count_from_input_params(self):
        workspace = self.create_workspace()
        circuit = self._teleport()
        target = workspace.get_targets("quantinuum.sim.h2-1sc")

        shots = 100

        with pytest.warns(
            match="Parameter 'shots' conflicts with the 'count' field of the 'input_params' parameter. "
                  "Please, provide only one option for setting shots. Defaulting to 'shots' parameter.",
        ):
            job = target.submit(
                circuit,
                shots=shots,
                input_params={"count": 20}
            )
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        assert job.details.input_params["count"] == shots

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_job_submit_quantinuum_with_count_from_input_params(self):
        workspace = self.create_workspace()
        circuit = self._teleport()
        target = workspace.get_targets("quantinuum.sim.h2-1sc")

        shots = 100

        with pytest.warns(
             match="Field 'count' from the 'input_params' parameter is subject to change in future versions. "
                   "Please, use 'shots' parameter instead."
        ):
            job = target.submit(
                circuit,
                input_params={"count": shots}
            )
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        assert job.details.input_params["count"] == shots

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_job_submit_quantinuum_h2_1e(self):
        self._test_job_submit_quantinuum("quantinuum.sim.h2-1e")

    @pytest.mark.quantinuum
    @pytest.mark.skip("Target was unavailable at the moment of the recording")
    def test_job_submit_quantinuum_h2_1qpu(self):
        self._test_job_submit_quantinuum("quantinuum.qpu.h2-1")

    def _test_job_submit_quantinuum(
            self, 
            target_name, 
            shots: int = None,
        ):
        workspace = self.create_workspace()
        circuit = self._teleport()
        target = workspace.get_targets(target_name)

        additional_kwargs = {}
        if shots:
            additional_kwargs["shots"] = shots

        job = target.submit(
            circuit,
            **additional_kwargs,
        )
        self.assertEqual(False, job.has_completed())
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        self.assertEqual(True, job.has_completed())
        self.assertEqual(job.details.status, JobStatus.SUCCEEDED)

        job = workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        results = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertAlmostEqual(int(results["c0"][0]), 1, delta=1)
        self.assertAlmostEqual(int(results["c1"][0]), 1, delta=1)
        self.assertAlmostEqual(int(results["c2"][0]), 1, delta=1)
