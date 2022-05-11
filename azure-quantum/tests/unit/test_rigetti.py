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
        with unittest.mock.patch.object(
            Job,
            "create_job_id",
            return_value=ZERO_UID if self.is_playback else Job.create_job_id(),
        ):

            workspace = self.create_workspace()

            target = Rigetti(workspace=workspace)
            job = target.submit(
                input_data=quil,
                name="qdk-python-test",
                input_params=input_params,
            )

            # If in recording mode, we don't want to record the pooling of job
            # status as the current testing infrastructure does not support
            # multiple identical requests.
            # So we pause the recording until the job has actually completed.
            # See: https://github.com/microsoft/qdk-python/issues/118
            self.pause_recording()
            try:
                # Set a timeout for IonQ recording
                job.wait_until_completed(timeout_secs=60)
            except TimeoutError:
                warnings.warn(
                    "Rigetti execution exceeded timeout. Skipping fetching results."
                )
                return None

            self.resume_recording()

            # Record a single GET request such that job.wait_until_completed
            # doesn't fail when running recorded tests
            # See: https://github.com/microsoft/qdk-python/issues/118
            job.refresh()

            job = workspace.get_job(job.id)
            assert job.has_completed()

            return Result(job)

    def test_job_submit_rigetti_typed_input_params(self) -> None:
        num_shots = 5
        result = self._run_job(BELL_STATE_QUIL, InputParams(count=num_shots))
        assert result is not None
        readout = result[READOUT]
        assert len(readout) == num_shots
        for shot in readout:
            assert len(shot) == 2, "Bell state program should only measure 2 qubits"

    def test_job_submit_rigetti_dict_input_params(self) -> None:
        num_shots = 5
        result = self._run_job(BELL_STATE_QUIL, {"count": num_shots})
        assert result is not None
        readout = result[READOUT]
        assert len(readout) == num_shots
        for shot in readout:
            assert len(shot) == 2, "Bell state program should only measure 2 qubits"

    def test_job_submit_rigetti_default_input_params(self) -> None:
        result = self._run_job(BELL_STATE_QUIL, None)
        assert result is not None
        readout = result[READOUT]
        assert len(readout) == 1
        for shot in readout:
            assert len(shot) == 2, "Bell state program should only measure 2 qubits"

    def test_quil_syntax_error(self) -> None:
        with pytest.raises(RuntimeError) as err:
            self._run_job(SYNTAX_ERROR_QUIL, None)
        assert "could not be executed because the operator a is not known" in str(
            err.value
        )

    def test_parametrized_quil(self) -> None:
        result = self._run_job(
            PARAMETRIZED_QUIL,
            InputParams(
                count=5, substitutions={PARAMETER_NAME: [[0.0], [pi], [2 * pi]]}
            ),
        )
        assert result is not None
        readout = result[READOUT]
        assert len(readout) == 5 * 3
        assert mean(readout[0:5]) == 0
        assert mean(readout[5:10]) == 1
        assert mean(readout[10:15]) == 0


class FakeJob:
    def __init__(self, json: bytes, details=None) -> None:
        self.json = json
        if details is None:
            details = MagicMock()
            details.status = "Succeeded"
        self.details = details

    def download_data(self, _) -> bytes:
        return self.json


class TestResult:
    def test_integers(self) -> None:
        result = Result(FakeJob(b'{"ro": [[0, 0], [1, 1]]}'))

        assert result[READOUT] == [[0, 0], [1, 1]]

    def test_unsuccessful_job(self) -> None:
        details = MagicMock()
        details.status = "Failed"
        details.error_data = "Some error message"
        with pytest.raises(RuntimeError) as err:
            Result(FakeJob(b'{"ro": [[0, 0], [1, 1]]}', details))
        err_string = str(err.value)
        assert details.status in err_string
        assert details.error_data in err_string
