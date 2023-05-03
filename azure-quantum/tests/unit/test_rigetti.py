"""Tests the ``azure.quantum.target.rigetti`` module."""
import unittest
import warnings
from typing import Dict, Any, Union, Optional
from unittest.mock import MagicMock

import pytest
from numpy import pi, mean

from azure.quantum.job import Job
from azure.quantum.target import Rigetti
from azure.quantum.target.rigetti import Result, InputParams
from common import QuantumTestBase, ZERO_UID

READOUT = "ro"
BELL_STATE_QUIL = f"""
DECLARE {READOUT} BIT[2]

H 0
CNOT 0 1

MEASURE 0 {READOUT}[0]
MEASURE 1 {READOUT}[1]
"""
SYNTAX_ERROR_QUIL = "a\n" + BELL_STATE_QUIL
PARAMETER_NAME = "theta"
PARAMETRIZED_QUIL = f"""
DECLARE {READOUT} BIT[1]
DECLARE {PARAMETER_NAME} REAL[1]

RX({PARAMETER_NAME}) 0

MEASURE 0 {READOUT}[0]
"""


@pytest.mark.rigetti
@pytest.mark.live_test
class TestRigettiTarget(QuantumTestBase):
    """Tests the azure.quantum.target.Rigetti class."""

    def _run_job(
        self,
        quil: str,
        input_params: Union[InputParams, Dict[str, Any], None],
    ) -> Optional[Result]:
        workspace = self.create_workspace()

        target = Rigetti(workspace=workspace)
        job = target.submit(
            input_data=quil,
            name="qdk-python-test",
            input_params=input_params,
        )

        job.wait_until_completed()
        job.refresh()

        job = workspace.get_job(job.id)
        self.assertTrue(job.has_completed())

        return Result(job)

    def test_job_submit_rigetti_typed_input_params(self) -> None:
        num_shots = 5
        result = self._run_job(BELL_STATE_QUIL, InputParams(count=num_shots))
        self.assertIsNotNone(result)
        readout = result[READOUT]
        self.assertEqual(len(readout), num_shots)
        for shot in readout:
            self.assertEqual(len(shot), 2, "Bell state program should only measure 2 qubits")

    def test_job_submit_rigetti_dict_input_params(self) -> None:
        num_shots = 5
        result = self._run_job(BELL_STATE_QUIL, {"count": num_shots})
        self.assertIsNotNone(result)
        readout = result[READOUT]
        self.assertEqual(len(readout), num_shots)
        for shot in readout:
            self.assertEqual(len(shot), 2, "Bell state program should only measure 2 qubits")

    def test_job_submit_rigetti_default_input_params(self) -> None:
        result = self._run_job(BELL_STATE_QUIL, None)
        self.assertIsNotNone(result)
        readout = result[READOUT]
        self.assertEqual(len(readout), 1)
        for shot in readout:
            self.assertEqual(len(shot), 2, "Bell state program should only measure 2 qubits")

    def test_quil_syntax_error(self) -> None:
        with pytest.raises(RuntimeError) as err:
            self._run_job(SYNTAX_ERROR_QUIL, None)
        self.assertIn("could not be executed because the operator a is not known", str(
            err.value
        ))

    def test_parametrized_quil(self) -> None:
        result = self._run_job(
            PARAMETRIZED_QUIL,
            InputParams(
                count=5, substitutions={PARAMETER_NAME: [[0.0], [pi], [2 * pi]]}
            ),
        )
        self.assertIsNotNone(result)
        readout = result[READOUT]
        self.assertEqual(len(readout), 5 * 3)
        self.assertEqual(mean(readout[0:5]), 0)
        self.assertEqual(mean(readout[5:10]), 1)
        self.assertEqual(mean(readout[10:15]), 0)


class FakeJob:
    def __init__(self, json: bytes, details=None) -> None:
        self.json = json
        if details is None:
            details = MagicMock()
            details.status = "Succeeded"
        self.details = details

    def download_data(self, _) -> bytes:
        return self.json


class TestResult(QuantumTestBase):
    def test_integers(self) -> None:
        result = Result(FakeJob(b'{"ro": [[0, 0], [1, 1]]}'))

        self.assertEqual(result[READOUT], [[0, 0], [1, 1]])

    def test_unsuccessful_job(self) -> None:
        details = MagicMock()
        details.status = "Failed"
        details.error_data = "Some error message"
        with pytest.raises(RuntimeError) as err:
            Result(FakeJob(b'{"ro": [[0, 0], [1, 1]]}', details))
        err_string = str(err.value)
        self.assertIn(details.status, err_string)
        self.assertIn(details.error_data, err_string)
