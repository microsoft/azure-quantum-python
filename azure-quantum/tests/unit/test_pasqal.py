##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import Dict, Any, Union, Optional
from unittest.mock import MagicMock

import pytest
from numpy import pi, mean

from azure.quantum.target import Pasqal
from azure.quantum.target.pasqal import Result, InputParams, PasqalTarget
from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS

TEST_PULSER = """{"sequence_builder": "{\\"version\\": \\"1\\", \\"name\\": \\"pulser-exported\\", \\"register\\": [{\\"name\\": \\"q0\\", \\"x\\": -10.0, \\"y\\": 0.0}, {\\"name\\": \\"q1\\", \\"x\\": -5.0, \\"y\\": -8.660254}, {\\"name\\": \\"q2\\", \\"x\\": -5.0, \\"y\\": 0.0}, {\\"name\\": \\"q3\\", \\"x\\": 0.0, \\"y\\": 0.0}, {\\"name\\": \\"q4\\", \\"x\\": 5.0, \\"y\\": -8.660254}, {\\"name\\": \\"q5\\", \\"x\\": 7.5, \\"y\\": 4.330127}], \\"channels\\": {\\"ch_global\\": \\"rydberg_global\\"}, \\"variables\\": {}, \\"operations\\": [{\\"op\\": \\"pulse\\", \\"channel\\": \\"ch_global\\", \\"protocol\\": \\"min-delay\\", \\"amplitude\\": {\\"kind\\": \\"constant\\", \\"duration\\": 124, \\"value\\": 12.566370614359172}, \\"detuning\\": {\\"kind\\": \\"constant\\", \\"duration\\": 124, \\"value\\": 25.132741228718345}, \\"phase\\": 0.0, \\"post_phase_shift\\": 0.0}, {\\"op\\": \\"pulse\\", \\"channel\\": \\"ch_global\\", \\"protocol\\": \\"min-delay\\", \\"amplitude\\": {\\"kind\\": \\"constant\\", \\"duration\\": 400, \\"value\\": 0.0}, \\"detuning\\": {\\"kind\\": \\"constant\\", \\"duration\\": 400, \\"value\\": -25.132741228718345}, \\"phase\\": 0.0, \\"post_phase_shift\\": 0.0}, {\\"op\\": \\"pulse\\", \\"channel\\": \\"ch_global\\", \\"protocol\\": \\"min-delay\\", \\"amplitude\\": {\\"kind\\": \\"constant\\", \\"duration\\": 100, \\"value\\": 12.566370614359172}, \\"detuning\\": {\\"kind\\": \\"constant\\", \\"duration\\": 100, \\"value\\": 25.132741228718345}, \\"phase\\": 0.0, \\"post_phase_shift\\": 0.0}, {\\"op\\": \\"pulse\\", \\"channel\\": \\"ch_global\\", \\"protocol\\": \\"min-delay\\", \\"amplitude\\": {\\"kind\\": \\"constant\\", \\"duration\\": 400, \\"value\\": 0.0}, \\"detuning\\": {\\"kind\\": \\"constant\\", \\"duration\\": 400, \\"value\\": -25.132741228718345}, \\"phase\\": 0.0, \\"post_phase_shift\\": 0.0}, {\\"op\\": \\"pulse\\", \\"channel\\": \\"ch_global\\", \\"protocol\\": \\"min-delay\\", \\"amplitude\\": {\\"kind\\": \\"constant\\", \\"duration\\": 100, \\"value\\": 12.566370614359172}, \\"detuning\\": {\\"kind\\": \\"constant\\", \\"duration\\": 100, \\"value\\": 25.132741228718345}, \\"phase\\": 0.0, \\"post_phase_shift\\": 0.0}], \\"measurement\\": null, \\"device\\": {\\"version\\": \\"1\\", \\"channels\\": [{\\"id\\": \\"rydberg_global\\", \\"basis\\": \\"ground-rydberg\\", \\"addressing\\": \\"Global\\", \\"max_abs_detuning\\": 31.41592653589793, \\"max_amp\\": 12.566370614359172, \\"min_retarget_interval\\": null, \\"fixed_retarget_t\\": null, \\"max_targets\\": null, \\"clock_period\\": 4, \\"min_duration\\": 16, \\"max_duration\\": 100000000, \\"mod_bandwidth\\": 2, \\"eom_config\\": {\\"limiting_beam\\": \\"RED\\", \\"max_limiting_amp\\": 251.32741228718345, \\"intermediate_detuning\\": 4398.22971502571, \\"controlled_beams\\": [\\"BLUE\\", \\"RED\\"], \\"mod_bandwidth\\": 11}}], \\"name\\": \\"Fresnel\\", \\"dimensions\\": 2, \\"rydberg_level\\": 60, \\"min_atom_distance\\": 5, \\"max_atom_num\\": 20, \\"max_radial_distance\\": 35, \\"interaction_coeff_xy\\": null, \\"supports_slm_mask\\": false, \\"max_layout_filling\\": 0.5, \\"reusable_channels\\": false, \\"pre_calibrated_layouts\\": [], \\"is_virtual\\": false}, \\"layout\\": {\\"coordinates\\": [[-12.5, 4.330127], [-10.0, 0.0], [-7.5, -4.330127], [-7.5, 4.330127], [-5.0, -8.660254], [-5.0, 0.0], [-5.0, 8.660254], [-2.5, -4.330127], [-2.5, 4.330127], [0.0, -8.660254], [0.0, 0.0], [0.0, 8.660254], [2.5, -4.330127], [2.5, 4.330127], [5.0, -8.660254], [5.0, 0.0], [5.0, 8.660254], [7.5, -4.330127], [7.5, 4.330127], [10.0, 0.0]], \\"slug\\": \\"TriangularLatticeLayout(20, 5.0\\\\u00b5m)\\"}}"}"""

@pytest.mark.pasqal
@pytest.mark.live_test
class TestPasqalTarget(QuantumTestBase):
    """Tests the azure.quantum.target.Pasqal class."""

    def _run_job(
        self,
        pulser: str,
        input_params: Union[InputParams, Dict[str, Any], None],
    ) -> Optional[Result]:
        workspace = self.create_workspace()

        target = Pasqal(workspace=workspace, name=PasqalTarget.SIM_EMU_FREE)
        job = target.submit(
            input_data=pulser,
            name="qdk-python-test",
            input_params=input_params,
        )

        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        job.refresh()

        job = workspace.get_job(job.id)
        self.assertTrue(job.has_completed())

        return Result(job)

    def test_job_submit_pasqal_typed_input_params(self) -> None:
        num_runs = 200
        result = self._run_job(TEST_PULSER, InputParams(runs=num_runs))
        self.assertIsNotNone(result)
        self.assertEqual(sum(v for v in result.data.values() if isinstance(v, int)), num_runs)

    def test_job_submit_pasqal_dict_input_params(self) -> None:
        num_runs = 150
        result = self._run_job(TEST_PULSER, input_params={"runs": num_runs})
        self.assertIsNotNone(result)
        self.assertEqual(sum(v for v in result.data.values() if isinstance(v, int)), num_runs)

    def test_job_submit_pasqal_default_input_params(self) -> None:
        default_num_runs = 100
        result = self._run_job(TEST_PULSER, None)
        self.assertIsNotNone(result)
        self.assertEqual(sum(v for v in result.data.values() if isinstance(v, int)), default_num_runs)
