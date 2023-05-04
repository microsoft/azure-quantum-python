
##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
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
    def test_job_submit_quantinuum(self):
        self.get_async_result(self._test_job_submit_quantinuum())

    async def _test_job_submit_quantinuum(self, **kwargs):
        workspace = self.create_async_workspace()
        circuit = self._teleport()
        target = await workspace.get_targets("quantinuum.sim.h1-1e")
        job = await target.submit(circuit)

        await job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        job = await workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        results = await job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertEqual(results["c0"], results["c2"])
