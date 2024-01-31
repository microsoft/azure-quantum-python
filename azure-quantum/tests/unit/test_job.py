##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import unittest
import os
import functools
import pytest
from unittest.mock import Mock
from datetime import date, datetime, timedelta

from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS
from azure.quantum.job.base_job import ContentType
from azure.quantum import Job
from azure.quantum.optimization import Problem, ProblemType, Term
from azure.quantum._client.models import JobDetails
import azure.quantum.target.toshiba as toshiba


SOLVER_TYPES = [
    functools.partial(toshiba.SimulatedBifurcationMachine, loops=10),
]

def get_solver_types():
    toshiba_enabled = os.environ.get("AZURE_QUANTUM_TOSHIBA", "") == "1"
    
    solver_types = []
    for solver_type in SOLVER_TYPES:
        solver_type_name = f'{solver_type.func.__module__}.{solver_type.func.__qualname__}'
        
        if (solver_type_name.__contains__("toshiba") and toshiba_enabled):
            solver_types.append(solver_type)
    return solver_types

"""
Temporarily disabling generation of parametrized test cases due to 
compatibility issues with VCR

def pytest_generate_tests(metafunc):
    if "solver_type" in metafunc.fixturenames:
        solver_types = get_solver_types()
        metafunc.parametrize(
            argnames="solver_type",
            argvalues=(solver_type \
                       for solver_type in solver_types) ,
            ids=(f'{solver_type.func.__module__}.{solver_type.func.__qualname__}' \
                 for solver_type in solver_types) 
        )
"""

class TestJobForSolver:
    """
    Wrapper for TestJob as a workaround to use pytest_generate_tests to 
    dynamically generate test cases for each solver.
    The base classes of TestJob (QuantumTestBase, ReplayableTest) are not
    compatible the pytest_generate_tests as they have a constructor parameter.
    Similar issue here: https://stackoverflow.com/questions/63978287/missing-1-required-positional-argument-error-for-fixture-when-softest-testcase-i
    """

    @pytest.mark.skip(reason="Temporarily disabling generation of parametrized test cases due to \
                              compatibility issues with VCR")
    def test_job_submit(self, solver_type):
        test_job = TestJob("_test_job_submit")
        test_job._test_job_submit(solver_type=solver_type)


class TestJob(QuantumTestBase):
    """TestJob

    Tests the azure.quantum.job module.
    """

    def test_job_success(self):
        job_results = self._get_job_results("test_output_data_format","{\"Histogram\": [\"[0]\", 0.50, \"[1]\", 0.50]}")
        self.assertTrue(len(job_results["Histogram"]) == 4)
        

    def test_job_for_microsoft_quantum_results_v1_success(self):
        job_results = self._get_job_results("microsoft.quantum-results.v1","{\"Histogram\": [\"[0]\", 0.50, \"[1]\", 0.50]}")
        self.assertTrue(len(job_results.keys()) == 2)
        self.assertTrue(job_results["[0]"], 0.50)
        self.assertTrue(job_results["[1]"], 0.50)

    
    def test_job_for_microsoft_quantum_results_v1_no_histogram_returns_raw_result(self):
        job_result_raw = "{\"NotHistogramProperty\": [\"[0]\", 0.50, \"[1]\", 0.50]}"
        job_result = self._get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertTrue(job_result, job_result_raw)


    def test_job_for_microsoft_quantum_results_v1_invalid_histogram_returns_raw_result(self):
        job_result_raw = "{\"NotHistogramProperty\": [\"[0]\", 0.50, \"[1]\"]}"
        job_result = self._get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertTrue(job_result, job_result_raw)


    def _get_job_results(self, output_data_format, results_as_json_str):
        job_details = JobDetails(
            id= "",
            name= "",
            provider_id="",
            target="",
            container_uri="",
            input_data_format="",
            output_data_format = output_data_format)
        job_details.status = "Succeeded"
        job = Job(
            workspace=None, 
            job_details=job_details)
        
        job.has_completed = Mock(return_value=True)
        job.wait_until_completed = Mock()

        class DowloadDataMock(object):
            def decode(): str
            pass

        download_data = DowloadDataMock()
        download_data.decode = Mock(return_value=results_as_json_str)
        job.download_data = Mock(return_value=download_data)
        
        return job.get_results()

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_TOSHIBA", "") == "1"), reason="Toshiba tests not enabled")
    @pytest.mark.toshiba
    @pytest.mark.live_test
    def test_job_submit_toshiba_simulated_bifurcation_machine(self):
        solver_type = functools.partial(toshiba.SimulatedBifurcationMachine, loops=10)
        solver_name = "SimulatedBifurcationMachine"
        self._test_job_submit(solver_name, solver_type)

    def _test_job_filter(self, solver_type):
        workspace = self.create_workspace()
        solver = solver_type(workspace)
        problem = self.create_problem(name="Test-Job-Filtering")

        job = solver.submit(problem)

        self.assertEqual(True, job.matches_filter()) # test no filters
        self.assertEqual(False, job.matches_filter(name_match="Test1"))
        self.assertEqual(True, job.matches_filter(name_match="Test-"))
        self.assertEqual(True, job.matches_filter(name_match="Test.+"))
        
        # don't run these on playback mode, as the recordings might expire
        # since we're checking against datetime.now()
        if not self.is_playback:
            # Make sure the job creation time is before tomorrow:
            after_time = datetime.now() + timedelta(days=1)
            self.assertEqual(False, job.matches_filter(created_after=after_time))

            # Make sure the job creation time is after yesterday:
            before_time = datetime.now() - timedelta(days=1)
            self.assertEqual(True, job.matches_filter(created_after=before_time))
            before_date = date.today() - timedelta(days=1)
            self.assertEqual(True, job.matches_filter(created_after=before_date))

    def _test_job_submit(
        self,
        solver_name,
        solver_type,
        content_type=ContentType.json,
        solver_kwargs=None
    ):
        """Tests the job submission and its lifecycle for a given solver.

        :param solver_type:
            The class name of the solver, for example "SimulatedBifurcationMachine".
        """

        problem_name = f'Test-{solver_name}-{datetime.now():"%Y%m%d-%H%M%S"}'

        problem = self.create_problem(name=problem_name,content_type=content_type)

        self._test_job_submit_problem(solver_type, problem, solver_kwargs)
    
    def _test_job_submit_problem(self, solver_type, problem, solver_kwargs=None):
        """Tests the job submission and its lifecycle for a given solver.
        :param solver_type:
            The class name of the solver, for example "SimulatedBifurcationMachine".
        :param problem
            The problem to submit
        :param solver_kwargs
            Solver kwargs
        """

        workspace = self.create_workspace()
        solver_kwargs = solver_kwargs or {}
        solver = solver_type(workspace, **solver_kwargs)

        job = solver.submit(problem)
        # TODO: also test solver.optimize(problem)

        self.assertEqual(False, job.has_completed())

        job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)

        job.refresh()
        self.assertEqual(True, job.has_completed())

        job.get_results(timeout_secs=DEFAULT_TIMEOUT_SECS)
        self.assertEqual(True, job.has_completed())

        job = workspace.get_job(job.id)
        self.assertEqual(True, job.has_completed())

        self.assertEqual(job.details.status, "Succeeded")

    def create_problem(
            self,
            name: str,
            init: bool = False,
            problem_type: ProblemType = ProblemType.pubo,
            content_type: ContentType = None ,
        ) -> Problem:
        """Create optimization problem with some default terms

        :param init: Set initial configuration
        :type init: bool
        :return: Optimization problem
        :rtype: Problem
        """
        terms = [
            Term(w=-3, indices=[1, 0]),
            Term(w=5, indices=[2, 0]),
            Term(w=9, indices=[2, 1]),
            Term(w=2, indices=[3, 0]),
            Term(w=-4, indices=[3, 1]),
            Term(w=4, indices=[3, 2]),
        ]

        initial_config = {"1": 0, "0": 1, "2": 0, "3": 1} if init \
                         else None
        return Problem(
            name=name,
            terms=terms,
            init_config=initial_config,
            problem_type=problem_type,
            content_type=content_type or ContentType.json
        )


if __name__ == "__main__":
    unittest.main()
