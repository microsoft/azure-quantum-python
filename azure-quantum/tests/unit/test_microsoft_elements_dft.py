import os
import pytest
from tempfile import TemporaryFile
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

test_xyz_file = Path(__file__).parent / "molecule.xyz"

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
        [ test_xyz_file ],
        [ test_xyz_file, test_xyz_file ],
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
        [ test_xyz_file ],
        [ test_xyz_file, test_xyz_file ],
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
        [ test_xyz_file ],
        [ test_xyz_file, test_xyz_file ],
    ]
)
def test_assemble_bomd_qcschema_from_files_success(data_regression, input_params, input_data):
    target = MicrosoftElementsDft
    qcschema_data = target._assemble_qcshema_from_files(input_data, input_params)
    data_regression.check(qcschema_data)


@pytest.mark.parametrize(
    'inputs', [
        {
            'input_files': ["molecule_1.xyz"],
            'input_blobs': ["inputData0"],
        },
        {
            'input_files': ["molecule_1.xyz","molecule_2.xyz"],
            'input_blobs': ["inputData0","inputData1"],
        },
    ]
)
def test_create_toc_data(data_regression, inputs):
    target = MicrosoftElementsDft
    toc_data = target._create_table_of_contents(inputs["input_files"], inputs["input_blobs"])
    data_regression.check(toc_data)

@pytest.mark.parametrize(
    "xyz_str", [
        """3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
""",
        """3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00

""",
        """3
water
O   0.00   0.00   0.00  
H   1.00   0.00   0.00  
H  -1.00   1.00   1.00  

""",
    ]
)
def test_xyz_parsing_correct_xyz_files(data_regression, xyz_str):
    target = MicrosoftElementsDft
    mol = target._xyz_to_qcschema_mol(xyz_str)
    data_regression.check(mol)

@pytest.mark.parametrize(
    "xyz_str", [
        """3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00
""",
        """3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00 H -1.00   1.00   1.00
""",
        """3
water
O   0.00   0.00   0.00

H   1.00   0.00   0.00
H  -1.00   1.00   1.00
""",
        """3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
H  -1.00   1.00   1.00
""",
    ]
)
def test_xyz_raises_for_bad_input(xyz_str):
    target = MicrosoftElementsDft
    with pytest.raises(ValueError):
        mol_data = target._xyz_to_qcschema_mol(xyz_str)



test_qcschema_file = Path(__file__).parent / "molecule.json"

@pytest.mark.parametrize(
    'input_data', [
        [ test_qcschema_file ],
        [ test_qcschema_file, test_qcschema_file ],
    ]
)
def test_assemble_qcschema_from_qcschema_files_success(data_regression, input_data):
    target = MicrosoftElementsDft
    qcschema_data = target._assemble_qcshema_from_files(input_data, {})
    data_regression.check(qcschema_data)


@pytest.mark.parametrize(
    'unsupported_extension',[
        '',
        '.cif',
        '.pdb',
    ]
)
def test_assemble_qcschema_raise_value_error_for_unsupported_file_types(unsupported_extension):
    target = MicrosoftElementsDft
    with TemporaryFile(suffix=unsupported_extension, delete=False) as fp:
        file_name = fp.name
        fp.write("Hello World!".encode())
        fp.close()

        with pytest.raises(ValueError):
            qcschema_data = target._assemble_qcshema_from_files([file_name], {})

    os.remove(file_name) 

@pytest.mark.parametrize(
    'input_params', [
        {'method': 'm062x'},
    ]
)
def test_assemble_qcschema_issues_warning_for_params_with_qcschema(input_params):
    target = MicrosoftElementsDft
    with pytest.warns(UserWarning):
        qcschema_data = target._assemble_qcshema_from_files([ test_qcschema_file ], input_params)

@pytest.mark.parametrize(
    'input_params', [
        {},
        None,
    ]
)
def test_assemble_qcschema_issues_no_warnings_for_empty_params_with_qcschema(recwarn, input_params):
    target = MicrosoftElementsDft
    qcschema_data = target._assemble_qcshema_from_files([ test_qcschema_file ], input_params)
    assert len(recwarn) == 0