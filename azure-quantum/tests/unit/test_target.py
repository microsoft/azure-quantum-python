import unittest

from azure.quantum.job.job import Job
from azure.quantum.target import IonQ

from common import QuantumTestBase, ZERO_UID


class TestIonQ(QuantumTestBase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()
    
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

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            circuit = self._3_qubit_ghz()
            target = IonQ(workspace=workspace)
            job = target.submit(circuit)
            results = job.get_results()
            assert "histogram" in results
            assert results["histogram"]["0"] == 0.5
            assert results["histogram"]["7"] == 0.5
