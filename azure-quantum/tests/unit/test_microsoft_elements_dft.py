import os
import pytest
from azure.quantum import Job
from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS
from azure.quantum import JobStatus
from azure.quantum.job import JobFailedWithResultsError
from azure.quantum.target.microsoft.elements.dft import MicrosoftElementsDft
from pytest_regressions import data_regression
from pathlib import Path


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
        self.assertIsNotNone(results["results"][0]["return_result"])

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

        with pytest.raises(JobFailedWithResultsError) as e:
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

test_file = Path(__file__).parent / "molecule.xyz"

@pytest.mark.parametrize(
        'input_params', [
        {
            "driver": "energy",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
        },
        {
            "driver": "gradient",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
        },
        {
            "driver": "hessian",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
        },
        {
            "driver": "energy",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 }
            },
        },
        {
            "driver": "gradient",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 }
            },
        },
        {
            "driver": "hessian",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 }
            },
        },
    ]
)
@pytest.mark.parametrize(
    'input_data', [
        [ test_file ],
        [ test_file, test_file ],
    ]
)
def test_assemble_true_qcschema_from_files_success(data_regression, input_params, input_data):
    target = MicrosoftElementsDft
    qcschema_data = target._assemble_qcshema_from_files(input_data, input_params)
    data_regression.check(qcschema_data)

@pytest.mark.parametrize(
    'input_params', [
        {
            "driver": "go",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
        },
        {
            "driver": "go",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 },
                "geometryOptimization": {"convergence_grms": 0.001667, "convergence_gmax": 0.0025, "convergence_drms": 0.006667, "convergence_dmax":0.01 }
            },
        },
    ]
)
@pytest.mark.parametrize(
    'input_data', [
        [ test_file ],
        [ test_file, test_file ],
    ]
)
def test_assemble_go_qcschema_from_files_success(data_regression, input_params, input_data):
    target = MicrosoftElementsDft
    qcschema_data = target._assemble_qcshema_from_files(input_data, input_params)
    data_regression.check(qcschema_data)

@pytest.mark.parametrize(
    'input_params', [
        {
            "driver": "bomd",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
        },
        {
            "driver": "bomd",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 },
                "molecularDynamics":{"steps": 5, "temperature": 298, "timeStep": 1, "thermostat": {"type": "berendsen", "timeSmoothingFactor": 0.05 } }
            },
        },
    ]
)
@pytest.mark.parametrize(
    'input_data', [
        [ test_file ],
        [ test_file, test_file ],
    ]
)
def test_assemble_bomd_qcschema_from_files_success(data_regression, input_params, input_data):
    target = MicrosoftElementsDft
    qcschema_data = target._assemble_qcshema_from_files(input_data, input_params)
    data_regression.check(qcschema_data)