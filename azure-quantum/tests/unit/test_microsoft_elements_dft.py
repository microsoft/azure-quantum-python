import os
import pytest
from azure.quantum import Job
from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS
from azure.quantum import JobStatus
from azure.quantum.target import DftRuntimeError

@pytest.mark.live_test
class TestMicrosoftElementsDftJob(QuantumTestBase):

    @pytest.mark.microsoft_elements_dft
    def test_dft_success(self):
        dft_input_params = {
            "tasks": [
                {
                    "taskType": "spe",
                    "basisSet": { "name": "def2-svp", "cartesian": False },
                    "xcFunctional": { "name": "m06-2x", "gridLevel": 4 },
                    "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8 }
                }
            ]
        }

        job = self._run_job(dft_input_params)

        self.assertEqual(job.details.status, JobStatus.SUCCEEDED)

        results = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertIsNotNone(results)
        self.assertIsNotNone(results[0]["return_result"])

    @pytest.mark.microsoft_elements_dft
    def test_dft_failure_invalid_input(self):
        dft_input_params = {
            "tasks": [
                {
                    "taskType": "invlidTask",
                    "basisSet": { "name": "def2-svp", "cartesian": False },
                    "xcFunctional": { "name": "m06-2x", "gridLevel": 4 },
                    "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8 }
                }
            ]
        }

        job = self._run_job(dft_input_params)

        self.assertEqual(job.details.status, JobStatus.FAILED)

        with pytest.raises(RuntimeError):
            job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)


    @pytest.mark.microsoft_elements_dft
    def test_dft_failure_algorithm_produces_output(self):
        dft_input_params = {
            "tasks": [
                {
                    "taskType": "spe",
                    "basisSet": { "name": "def2-svp", "cartesian": False },
                    "xcFunctional": { "name": "m06-2x", "gridLevel": 4 },
                    "scf": { "method": "rks", "maxSteps": 1, "convergeThreshold": 1e-8 }
                }
            ]
        }

        job = self._run_job(dft_input_params)

        self.assertEqual(job.details.status, JobStatus.FAILED)

        with pytest.raises(DftRuntimeError) as e:
            job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)

            self.assertIsNotNone(e.value.get_details())            


    def _run_job(self, input_params) -> Job:
        workspace = self.create_workspace()
        target = workspace.get_targets("microsoft.dft")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir_path}/molecule.xyz", "r") as file:
            job = target.submit(input_data=file.read(), input_params=input_params)
            job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
            job.refresh()

            return job
