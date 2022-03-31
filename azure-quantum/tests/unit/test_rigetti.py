"""Tests the ``azure.quantum.target.rigetti`` module."""
import unittest
import warnings
from typing import Dict, Any, Union
from unittest.mock import MagicMock

import pytest

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


@pytest.mark.rigetti
@pytest.mark.live_test
class TestRigettiTarget(QuantumTestBase):
    """Tests the azure.quantum.target.Rigetti class."""

    def _run_job(self, input_params: Union[InputParams, Dict[str, Any], None]) -> Result:
        with unittest.mock.patch.object(
            Job,
            "create_job_id",
            return_value=ZERO_UID if self.is_playback else Job.create_job_id(),
        ):

            workspace = self.create_workspace()

            target = Rigetti(workspace=workspace)
            job = target.submit(
                input_data=BELL_STATE_QUIL,
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
                warnings.warn("Rigetti execution exceeded timeout. Skipping fetching results.")

            # Check if job succeeded
            assert job.has_completed()
            assert job.details.status == "Succeeded"
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
        result = self._run_job(InputParams(count=num_shots))
        readout = result[READOUT]
        assert len(readout) == num_shots
        for shot in readout:
            assert len(shot) == 2, "Bell state program should only measure 2 qubits"

    def test_job_submit_rigetti_dict_input_params(self) -> None:
        num_shots = 5
        result = self._run_job({"count": num_shots})
        readout = result[READOUT]
        assert len(readout) == num_shots
        for shot in readout:
            assert len(shot) == 2, "Bell state program should only measure 2 qubits"

    def test_job_submit_rigetti_default_input_params(self) -> None:
        result = self._run_job(None)
        readout = result[READOUT]
        assert len(readout) == 1
        for shot in readout:
            assert len(shot) == 2, "Bell state program should only measure 2 qubits"


class FakeJob:
    def __init__(self, json: bytes) -> None:
        self.json = json
        self.details = MagicMock()

    def download_data(self, _) -> bytes:
        return self.json


class TestResult:
    def test_integers(self) -> None:
        result = Result(FakeJob(b'{"ro": [[0, 0], [1, 1]]}'))

        assert result[READOUT] == [[0, 0], [1, 1]]
