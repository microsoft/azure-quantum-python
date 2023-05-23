##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest
from pytest import raises
from os import path
import re

from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS

from azure.quantum import JobStatus
from azure.quantum.target.microsoft import MicrosoftEstimator, \
    MicrosoftEstimatorJob, MicrosoftEstimatorResult, \
    MicrosoftEstimatorParams, QubitParams, ErrorBudgetPartition


class TestMicrosoftQC(QuantumTestBase):
    """TestMicrosoftQC

    Tests the azure.quantum.target.microsoft module.
    """

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
        Submits a job with default job parameters.

        Checks whether job and results have expected type.
        """
        ws = self.create_workspace()
        estimator = MicrosoftEstimator(ws)

        ccnot = self._ccnot_bitcode()
        job = estimator.submit(ccnot)
        self.assertIsInstance(job, MicrosoftEstimatorJob)
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        result = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertIsInstance(result, MicrosoftEstimatorResult)

        # Retrieve job by ID
        job2 = ws.get_job(job.id)
        self.assertEqual(type(job2), type(job))
        result2 = job2.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertEqual(type(result2), type(result))

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_estimator_batching_job(self):
        """
        Submits a job with default job parameters.

        Checks whether job and results have expected type.
        """
        ws = self.create_workspace()
        estimator = MicrosoftEstimator(ws)

        ccnot = self._ccnot_bitcode()
        params = estimator.make_params(num_items=2)
        params.items[0].error_budget = 0.001
        params.items[1].error_budget = 0.002
        job = estimator.submit(ccnot, input_params=params)
        self.assertIsInstance(job, MicrosoftEstimatorJob)
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        if job.details.status != "Succeeded":
            raise Exception(f"Job {job.id} not succeeded in "
                            "test_estimator_batching_job")
        result = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        errors = []
        if type(result) != MicrosoftEstimatorResult:
            errors.append("Unexpected type for result")

        if 'summary_data_frame' not in dir(result):
            errors.append("summary_data_frame not method of result")

        from pandas import DataFrame
        df = result.summary_data_frame()
        if type(df) != DataFrame:
            errors.append("Unexpected type for summary data frame")

        self.assertEqual(errors, [])

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
        self.assertIsInstance(job, MicrosoftEstimatorJob)
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertEqual(job.details.status, "Failed")

        expected = "Cannot retrieve results as job execution failed " \
                   "(InvalidInputError: The error budget must be " \
                   "between 0.0 and 1.0, provided input was `2`)"
        with raises(RuntimeError, match=re.escape(expected)):
            _ = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)

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

        self.assertIsInstance(job, MicrosoftEstimatorJob)
        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        self.assertEqual(job.details.status, JobStatus.SUCCEEDED)

        result = job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertIsInstance(result, MicrosoftEstimatorResult)

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

    def test_estimator_error_budget_float(self):
        params = MicrosoftEstimatorParams()
        params.error_budget = 0.001
        assert params.as_dict() == {"errorBudget": 0.001}

    def test_estimator_error_budget_partition(self):
        params = MicrosoftEstimatorParams()
        params.error_budget = ErrorBudgetPartition(0.01, 0.02, 0.03)
        assert params.as_dict() == {
            "errorBudget": {
                "logical": 0.01,
                "rotations": 0.03,
                "tStates": 0.02
            }
        }
