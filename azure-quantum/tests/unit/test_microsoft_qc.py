#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_microsoft_qc.py: Tests for microsoft-qc provider.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest
import unittest
import unittest.mock
from os import path

from common import QuantumTestBase, ZERO_UID

from azure.quantum.job.job import Job
from azure.quantum.target.microsoft import MicrosoftEstimatorJob


class TestMicrosoftQC(QuantumTestBase):
    """TestMicrosoftQC

    Tests the azure.quantum.target.microsoft module.
    """

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def _ccnot_bitcode(self) -> bytes:
        """
        QIR sample file for CCNOT gate applied to 3 qubits.
        """
        bitcode_filename = path.join(path.dirname(__file__), "qir", "ccnot.bc")
        with open(bitcode_filename, "rb") as f:
            return f.read()

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_estimator_non_batching_job(self):
        """
        Submits a job default job parameters.

        Checks whether job and results have expected type.
        """
        with unittest.mock.patch.object(
            MicrosoftEstimatorJob,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            # Modify the Job.wait_until_completed method
            # such that it only records once
            # See: https://github.com/microsoft/qdk-python/issues/118
            with unittest.mock.patch.object(
                Job,
                "wait_until_completed",
                self.mock_wait(Job.wait_until_completed)
            ):
                ws = self.create_workspace()
                estimator = ws.get_targets("microsoft.estimator")

                ccnot = self._ccnot_bitcode()
                job = estimator.submit(ccnot)
                assert type(job) == MicrosoftEstimatorJob
                job.wait_until_completed()
                if job.details.status != "Succeeded":
                    raise Exception(f"Job {job.id} not succeeded in "
                                    "test_estimator_non_batching_job")
                result = job.get_results()

                assert type(result) == dict
