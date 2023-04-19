#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_microsoft_qc.py: Tests for microsoft-qc provider.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest
from pytest import raises
from unittest.mock import patch

from os import path
import re

from common import QuantumTestBase, ZERO_UID

from azure.quantum.job.job import Job
from azure.quantum.target.microsoft import MicrosoftEstimator, \
    MicrosoftEstimatorJob, MicrosoftEstimatorResult, \
    MicrosoftEstimatorParams, QubitParams


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

    def setUp(self):
        """
        Sets up some mock patches for job IDs and wait_until_completed.
        """
        super().setUp()
        self.patch_job_id = patch.object(
            MicrosoftEstimatorJob,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id())
        # Modify the Job.wait_until_completed method such that it only records
        # once, see: https://github.com/microsoft/qdk-python/issues/118
        self.patch_wait = patch.object(
            Job,
            "wait_until_completed",
            self.mock_wait(Job.wait_until_completed)
        )
        self.patch_job_id.start()
        self.patch_wait.start()

    def tearDown(self):
        """
        Stops mock patches.
        """
        self.patch_wait.stop()
        self.patch_job_id.stop()
        super().tearDown()

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_estimator_non_batching_job(self):
        """
        Submits a job with default job parameters.

        Checks whether job and results have expected type.
        """
        ws = self.create_workspace()
        estimator = MicrosoftEstimator(ws)

        ccnot = self._ccnot_bitcode()
        job = estimator.submit(ccnot)
        assert type(job) == MicrosoftEstimatorJob
        job.wait_until_completed()
        if job.details.status != "Succeeded":
            raise Exception(f"Job {job.id} not succeeded in "
                            "test_estimator_non_batching_job")
        result = job.get_results()
        assert type(result) == MicrosoftEstimatorResult

        # Retrieve job by ID
        job2 = ws.get_job(job.id)
        assert type(job2) == type(job)
        result2 = job2.get_results()
        assert type(result2) == type(result)


    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_estimator_failing_job(self):
        """
        Submits a job with wrong parameters.

        Checks whether error handling is correct.
        """
        ws = self.create_workspace()
        estimator = MicrosoftEstimator(ws)

        ccnot = self._ccnot_bitcode()
        job = estimator.submit(ccnot, input_params={"errorBudget": 2})
        assert type(job) == MicrosoftEstimatorJob
        job.wait_until_completed()
        assert job.details.status == "Failed"

        expected = "Cannot retrieve results as job execution failed " \
                   "(InvalidInputError: The error budget must be " \
                   "between 0.0 and 1.0, provided input was `2`)"
        with raises(RuntimeError, match=re.escape(expected)):
            _ = job.get_results()

    @pytest.mark.microsoft_qc
    def test_estimator_failing_job_client_validation(self):
        """
        Submits a job with wrong parameters.

        Checks whether error handling is correct.
        """

        # This test will not send any request (not even authentication),
        # because the error is caught before submit can send a request.
        ws = self.create_workspace()
        estimator = MicrosoftEstimator(ws)

        ccnot = self._ccnot_bitcode()
        params = estimator.make_params()
        params.error_budget = 2
        expected = "error_budget must be value between 0 and 1"
        with raises(ValueError, match=expected):
            estimator.submit(ccnot, input_params=params)

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_estimator_qiskit_job(self):
        """
        Submits a job from a Qiskit QuantumCircuit.

        Checks whether error handling is correct.
        """
        ws = self.create_workspace()
        estimator = MicrosoftEstimator(ws)

        from qiskit import QuantumCircuit
        circ = QuantumCircuit(3)
        circ.ccx(0, 1, 2)

        job = estimator.submit(circ)
        assert type(job) == MicrosoftEstimatorJob
        job.wait_until_completed()
        if job.details.status != "Succeeded":
            raise Exception(f"Job {job.id} not succeeded in "
                            "test_estimator_qiskit_job")
        result = job.get_results()
        assert type(result) == MicrosoftEstimatorResult

    def test_estimator_params_validation_valid_cases(self):
        """
        Checks validation cases for resource estimation parameters for valid
        cases.
        """
        params = MicrosoftEstimatorParams()

        params.error_budget = 0.1
        params.qubit_params.name = QubitParams.GATE_NS_E3
        params.qubit_params.instruction_set = "gate_based"
        params.qubit_params.t_gate_error_rate = 0.03
        params.qubit_params.t_gate_time = "10 ns"

        # If validation would be wrong, the call to as_dict will raise an
        # exception.
        params.as_dict()

    def test_estimator_params_validation_large_error_budget(self):
        params = MicrosoftEstimatorParams()
        params.error_budget = 2
        expected = "error_budget must be value between 0 and 1"
        with raises(ValueError, match=expected):
            params.as_dict()

    def test_estimator_params_validation_small_error_budget(self):
        params = MicrosoftEstimatorParams()
        params.error_budget = 0
        expected = "error_budget must be value between 0 and 1"
        with raises(ValueError, match=expected):
            params.as_dict()

    def test_estimator_params_validation_invalid_instruction_set(self):
        params = MicrosoftEstimatorParams()
        params.qubit_params.instruction_set = "invalid"
        with raises(ValueError, match="instruction_set must be GateBased or "
                                      "Majorana"):
            params.as_dict()

    def test_estimator_params_validation_invalid_error_rate(self):
        params = MicrosoftEstimatorParams()
        params.qubit_params.t_gate_error_rate = 0
        with raises(ValueError, match="t_gate_error_rate must be between 0 "
                                      "and 1"):
            params.as_dict()

    def test_estimator_params_validation_invalid_gate_time_type(self):
        params = MicrosoftEstimatorParams()
        params.qubit_params.t_gate_time = 20
        with raises(TypeError, match="expected string or bytes-like object"):
            params.as_dict()

    def test_estimator_params_validation_invalid_gate_time_value(self):
        params = MicrosoftEstimatorParams()
        params.qubit_params.t_gate_time = "20"
        with raises(ValueError, match="t_gate_time is not a valid time "
                                      "string; use a suffix s, ms, us, or ns"):
            params.as_dict()

    def test_estimator_params_validation_missing_instruction_set(self):
        params = MicrosoftEstimatorParams()
        params.qubit_params.t_gate_time = "1 ns"
        with raises(LookupError, match="instruction_set must be set for "
                                       "custom qubit parameters"):
            params.as_dict()

    def test_estimator_params_validation_missing_fields(self):
        params = MicrosoftEstimatorParams()
        params.qubit_params.instruction_set = "gateBased"
        params.qubit_params.t_gate_time = "1 ns"
        with raises(LookupError, match="one_qubit_measurement_time must be "
                                       "set"):
            params.as_dict()
