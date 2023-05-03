import unittest
import warnings

from azure.core.exceptions import HttpResponseError
from azure.quantum.aio.job.job import Job
from azure.quantum.aio.target import IonQ
from azure.quantum.aio.target.quantinuum import Quantinuum

from common import QuantumTestBase, ZERO_UID


class TestIonQ(QuantumTestBase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """

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

    def test_job_submit_ionq(self):
        self.get_async_result(self._test_job_submit_ionq(num_shots=None))

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

        await job.wait_until_completed()

        job = await workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        results = await job.get_results()
        self.assertIn("histogram", results)
        self.assertEqual(results["histogram"]["0"], 0.5)
        self.assertEqual(results["histogram"]["7"], 0.5)

        if num_shots:
            self.assertEqual(job.details.input_params.get("shots"), num_shots)
        else:
            self.assertIsNone(job.details.input_params.get("shots"))


class TestQuantinuum(QuantumTestBase):
    def _teleport(self):
        return """OPENQASM 2.0;
        include "qelib1.inc";

        qreg q[3];
        creg c0[1];
        creg c1[3];

        h q[0];
        cx q[0], q[1];
        x q[2];
        h q[2];
        cx q[2], q[0];
        h q[2];
        measure q[0] -> c1[0];
        c0[0] = c1[0];
        if (c0==1) x q[1];
        c0[0] = 0;
        measure q[2] -> c1[1];
        c0[0] = c1[1];
        if (c0==1) z q[1];
        c0[0] = 0;
        h q[1];
        measure q[1] -> c1[2];
        """

    def test_job_submit_quantinuum(self):
        self.get_async_result(self._test_job_submit_quantinuum())

    async def _test_job_submit_quantinuum(self, **kwargs):
        workspace = self.create_async_workspace()
        circuit = self._teleport()
        target = Quantinuum(workspace=workspace)
        job = await target.submit(circuit)

        await job.wait_until_completed()

        job = await workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        results = await job.get_results()
        self.assertEqual(results["c0"], ["0"])
        self.assertEqual(results["c1"], ["000"])
