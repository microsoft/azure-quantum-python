import unittest
import warnings
from azure.quantum.target.microsoft.simulator.fullstate import FullStateTarget
from azure.quantum.workspace import Workspace
import pytest

import numpy as np

from azure.core.exceptions import HttpResponseError
from azure.quantum.job.job import Job
from azure.quantum._client.models import CostEstimate, UsageEvent
from azure.quantum.target import IonQ, Honeywell

from common import QuantumTestBase, ZERO_UID


class TestFullStateSimulator(QuantumTestBase):
    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def get_test_qir_file(self):
        return "Sample.ll"

    def test_job_submit_ms_full_state(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            target: FullStateTarget = workspace.get_targets("microsoft.simulator.fullstate")
            job = target.submit_qir_file("Sample.ll", "QIR test", "Sample__HelloQ")
            result = job.get_results()
            assert result
