from json import JSONDecodeError
import unittest
import os
import pytest
from azure.quantum.target.microsoft.simulator.fullstate import FullStateTarget
from azure.quantum.job.job import Job

from common import QuantumTestBase, ZERO_UID


class TestFullStateSimulator(QuantumTestBase):
    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def _test_qir_file(self):
        return os.path.join(os.path.split(__file__)[0], "qir", "Sample.ll")

    def _test_qir_qiskit_file(self):
        return os.path.join(os.path.split(__file__)[0], "qir", "QiskitSample.ll")

    def test_job_submit_microsoft_full_state(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            target: FullStateTarget = workspace.get_targets("microsoft.simulator.fullstate")
            job = target.submit_qir_file(self._test_qir_file(), "QIR test", "Sample__HelloQ")
            result: str = job.get_results()
            assert result.startswith("Hello quantum world!")

    def test_job_submit_microsoft_full_state_qiskit(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            target: FullStateTarget = workspace.get_targets("microsoft.simulator.fullstate")
            job = target.submit_qir_file(self._test_qir_qiskit_file(), "Qiskit GHZ program", "QuantumApplication__Run")
            results = job.get_results()
            assert results
