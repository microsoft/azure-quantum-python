import os
import pytest
from tempfile import TemporaryFile, NamedTemporaryFile
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
    qcschema_data = target.assemble_qcschema_from_files(input_data, input_params)
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
            },
        },
        {
            "driver": "go",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 },
            },
            "go_keywords": {
                "gdiis": True,
            }
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
    qcschema_data = target.assemble_qcschema_from_files(input_data, input_params)
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
            },
        },
        {
            "driver": "bomd",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 },
            },
            "bomd_keywords": {
                "steps": 1000,
            }
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
    qcschema_data = target.assemble_qcschema_from_files(input_data, input_params)
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
        """6
water dimer
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
-O   0.00   0.00   2.00  -0.6
-H   1.00   0.00   2.00   0.3
-H  -1.00   1.00   3.00   0.3
""",
        """6
water dimer
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
-O   0.00   0.00   2.00  -0.6
-H   1.00   0.00   2.00   0.3
-H  -1.00   1.00   3.00   0.3

""",
        """12
water dimer
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
-O   0.00   0.00   2.00  -0.6
-H   1.00   0.00   2.00   0.3
-H  -1.00   1.00   3.00   0.3
O   0.00   0.00   3.00
H   1.00   0.00   3.00
H  -1.00   1.00   4.00
-O   0.00   0.00   4.00  -0.6
-H   1.00   0.00   4.00   0.3
-H  -1.00   1.00   5.00   0.3

""",
    ],
    ids=[
        'minimal',
        'minimal_with_line_at_end',
        'qmmm_minimal',
        'qmmm_minimal_with_line_at_end',
        'qmmm_discontinuous_qm_mm'
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
        """3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
H  -1.00   1.00   1.00  -0.6
""",
        """
3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
""",
    ],
    ids=[
        'atom_missing',
        'atom_on_previous_line',
        'empty_line_in_middle',
        'duplicated_line',
        'mm_atom_without_dash',
        'empty_line_at_beginning'
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
    qcschema_data = target.assemble_qcschema_from_files(input_data, {})
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
            qcschema_data = target.assemble_qcschema_from_files([file_name], {})

    os.remove(file_name) 

@pytest.mark.parametrize(
    'input_data', [
        [test_xyz_file, test_qcschema_file]
    ]
)
def test_mixed_extensions_raise_value_error(input_data):
    target = MicrosoftElementsDft
    with pytest.raises(ValueError):
        qcschema_data = target.assemble_qcschema_from_files(input_data, {})

@pytest.mark.parametrize(
    'input_params', [
        {},
        {'driver': 'bomd'},
        {'model': {'method': 'b3lyp', 'basis': 'def2-svp'}},
        {'driver': 'bomd', 'model': { 'method': 'b3lyp'}},
        {'driver': 'bomd', 'model': { 'basis': 'def2-svp'}},
    ]
)
def test_raise_value_error_when_not_having_required_parameters(input_params):
    target = MicrosoftElementsDft
    with pytest.raises(ValueError):
        qcschema_data = target.assemble_qcschema_from_files([test_xyz_file], input_params)

@pytest.mark.parametrize(
    "xyz",[
        """3
water
O   0.00   0.00   0.00
H   1.00   0.00   0.00
H  -1.00   1.00   1.00
H  -1.00   1.00   1.00  -0.6
""",
    ],
    ids=[
        'qmmm',
    ],
)
@pytest.mark.parametrize(
    'input_params', [
        {
            "driver": "hessian",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
        },
        {
            "driver": "go",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
        },
        {
            "driver": "bomd",
            "model": { "method": "m06-2x", "basis": "def2-svp" },
            "keywords": {
                "scf": { "method": "rks", "maxSteps": 100, "convergeThreshold": 1e-8, "requireWaveFunction": True},
                "xcFunctional": { "gridLevel": 3 },
            },
            "bomd_keywords": {
                "steps": 1000,
            }
        },
    ],
    ids=[
        'hessian',
        'go',
        'bomd'
    ]
)
def test_raise_value_error_for_unsupported_tasks(xyz, input_params):
    with NamedTemporaryFile(suffix=".xyz", delete=False) as fp:
        fp.write(xyz.encode())
        fp.flush()
        temp_xyz_file = fp.name

    target = MicrosoftElementsDft
    with pytest.raises(ValueError):
        qcschema_data = target.assemble_qcschema_from_files([temp_xyz_file], input_params)

    os.remove(temp_xyz_file)


@pytest.mark.parametrize(
    'input_params', [
        {'method': 'm062x'},
    ]
)
def test_assemble_qcschema_issues_warning_for_params_with_qcschema(input_params):
    target = MicrosoftElementsDft
    with pytest.warns(UserWarning):
        qcschema_data = target.assemble_qcschema_from_files([ test_qcschema_file ], input_params)

def test_issue_warning_for_large_number_of_tasks():
    input_data = [test_xyz_file]*1001
    target = MicrosoftElementsDft
    with pytest.warns(UserWarning):
        target._check_file_paths(input_data)


@pytest.mark.parametrize(
    'input_params', [
        {},
        None,
    ]
)
def test_assemble_qcschema_issues_no_warnings_for_empty_params_with_qcschema(recwarn, input_params):
    target = MicrosoftElementsDft
    qcschema_data = target.assemble_qcschema_from_files([ test_qcschema_file ], input_params)
    assert len(recwarn) == 0

def test_pass_none_as_params_for_qcschema_input(data_regression):
    target = MicrosoftElementsDft
    qcschema_data = target.assemble_qcschema_from_files([ test_qcschema_file ], None)
    data_regression.check(qcschema_data)
    