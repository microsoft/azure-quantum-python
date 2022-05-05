#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_job.py: Checks correctness of azure.quantum.job module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import unittest
import os
import functools
import pytest
from datetime import date, datetime, timedelta

from common import QuantumTestBase, ZERO_UID
from azure.quantum.job.base_job import ContentType
from azure.quantum import Job
from azure.quantum.optimization import Problem, ProblemType, Term, SlcTerm
import azure.quantum.optimization as microsoft
import azure.quantum.target.oneqbit as oneqbit
import azure.quantum.target.toshiba as toshiba


SOLVER_TYPES = [
    functools.partial(microsoft.SimulatedAnnealing, beta_start=0),
    functools.partial(microsoft.ParallelTempering, sweeps=100),
    functools.partial(microsoft.Tabu, sweeps=100),
    functools.partial(microsoft.QuantumMonteCarlo, trotter_number=1),
    functools.partial(microsoft.PopulationAnnealing, sweeps=200),
    functools.partial(microsoft.SubstochasticMonteCarlo, step_limit=280),
    functools.partial(oneqbit.TabuSearch, improvement_cutoff=10),
    functools.partial(oneqbit.PticmSolver, num_sweeps_per_run=99),
    functools.partial(oneqbit.PathRelinkingSolver, distance_scale=0.44),
    functools.partial(toshiba.SimulatedBifurcationMachine, loops=10),
]

def get_solver_types():
    one_qbit_enabled = os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"
    toshiba_enabled = os.environ.get("AZURE_QUANTUM_TOSHIBA", "") == "1"
    
    solver_types = []
    for solver_type in SOLVER_TYPES:
        solver_type_name = f'{solver_type.func.__module__}.{solver_type.func.__qualname__}'
        
        if (solver_type_name.startswith("azure.quantum.target.solvers.") # Microsoft solvers
            or (solver_type_name.__contains__("toshiba") and toshiba_enabled)
            or (solver_type_name.__contains__("oneqbit") and one_qbit_enabled)):
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

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_submit_microsoft_simulated_annealing(self):
        solver_type = functools.partial(microsoft.SimulatedAnnealing, beta_start=0)
        solver_name = "SimulatedAnnealing"
        self._test_job_submit(solver_name, solver_type)
        self._test_job_filter(solver_type)
        with self.assertRaises(ValueError):
            self._test_job_submit(solver_name, solver_type, test_grouped=True)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_submit_microsoft_parallel_tempering(self):
        solver_type = functools.partial(microsoft.ParallelTempering, sweeps=100)
        solver_name = "ParallelTempering"
        self._test_job_submit(solver_name, solver_type)
        with self.assertRaises(ValueError):
            self._test_job_submit(solver_name, solver_type, test_grouped=True)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_submit_microsoft_tabu(self):
        solver_type = functools.partial(microsoft.Tabu, sweeps=100)
        solver_name = "Tabu"
        self._test_job_submit(solver_name, solver_type)
        with self.assertRaises(ValueError):
            self._test_job_submit(solver_name, solver_type, test_grouped=True)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_submit_microsoft_quantum_monte_carlo(self):
        solver_type = functools.partial(microsoft.QuantumMonteCarlo, trotter_number=1)
        solver_name = "QuantumMonteCarlo"
        self._test_job_submit(solver_name, solver_type)
        with self.assertRaises(ValueError):
            self._test_job_submit(solver_name, solver_type, test_grouped=True)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_submit_microsoft_population_annealing(self):
        solver_type = functools.partial(microsoft.PopulationAnnealing, sweeps=200)
        solver_name = "PopulationAnnealing"
        self._test_job_submit(solver_name, solver_type)
        # renable after schema change is deployed
        # self._test_job_submit(solver_name, solver_type, test_grouped=True)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_submit_microsoft_substochastic_monte_carlo(self):
        solver_type = functools.partial(microsoft.SubstochasticMonteCarlo, step_limit=280)
        solver_name = "SubstochasticMonteCarlo"
        self._test_job_submit(solver_name, solver_type)
        # renable after schema change is deployed
        # self._test_job_submit(solver_name, solver_type, test_grouped=True)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_submit_microsoft_population_annealing_proto(self):
        solver_type = functools.partial(microsoft.PopulationAnnealing, sweeps=200, content_type = ContentType.protobuf)
        solver_name = "PopulationAnnealing"
        self._test_job_submit(solver_name, solver_type, content_type=ContentType.protobuf)

    @pytest.mark.qio
    def test_job_submit_microsoft_substochastic_monte_carlo_proto(self):
        solver_type = functools.partial(microsoft.SubstochasticMonteCarlo, step_limit=280, content_type = ContentType.protobuf)
        solver_name = "SubstochasticMonteCarlo"
        self._test_job_submit(solver_name, solver_type, content_type=ContentType.protobuf)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_upload_and_run_solvers(self):
        problem_name = f'Test-problem-{datetime.now():"%Y%m%d-%H%M%S"}'
        problem = self.create_problem(name=problem_name)
        workspace = self.create_workspace()

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            # Upload the blob data
            input_data_uri = problem.upload(
                workspace=workspace,
                blob_name="inputData",
                container_name=f"qc-test-{self.get_test_job_id()}"
            )

        for solver_type in get_solver_types():
            solver = solver_type(workspace)

            with unittest.mock.patch.object(
                Job,
                self.mock_create_job_id_name,
                return_value=self.get_test_job_id(),
            ):
                # Submit the blob data URI and run job
                job = solver.submit(input_data_uri)

                # For recording purposes, we only want to record and
                # and resume recording when the job has completed
                self.pause_recording()
                job.wait_until_completed()
                self.resume_recording()

                job.refresh()
                job.get_results()
                assert job.has_completed()
                assert job.details.status == "Succeeded"

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"), reason="1Qbit tests not enabled")
    @pytest.mark.oneqbit
    @pytest.mark.live_test
    def test_job_submit_oneqbit_tabu_search(self):
        solver_type = functools.partial(oneqbit.TabuSearch, improvement_cutoff=10)
        solver_name = "TabuSearch"
        solver_kwargs = {
            "improvement_cutoff": 2,
            "improvement_tolerance": 1e-9,
            "seed": 123,
            "tabu_tenure": 2,
            "tabu_tenure_rand_max": 2,
            "timeout": 2,
        }
        self._test_job_submit(solver_name, solver_type, solver_kwargs=solver_kwargs)

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"), reason="1Qbit tests not enabled")
    @pytest.mark.oneqbit
    @pytest.mark.live_test
    def test_job_submit_oneqbit_pticm_solver(self):
        solver_type = functools.partial(oneqbit.PticmSolver, num_sweeps_per_run=99)
        solver_name = "PticmSolver"
        solver_kwargs = {
            "auto_set_temperatures": False,
            "elite_threshold": 0.3,
            "frac_icm_thermal_layers": 0.5,
            "frac_sweeps_fixing": 0.15,
            "frac_sweeps_idle": 1.0,
            "frac_sweeps_stagnation": 1.0,
            "goal": "OPTIMIZE",
            "high_temp": 2,
            "low_temp": 0.2,
            "max_samples_per_layer": 10,
            "max_total_sweeps": 1000,
            "num_elite_temps": 4,
            "num_replicas": 2,
            "num_sweeps_per_run": 100,
            "num_temps": 30,
            "perform_icm": True,
            "scaling_type": "MEDIAN",
            "seed": 42,
            "var_fixing_type": "NO_FIXING"
        }

        with pytest.deprecated_call():
            self._test_job_submit(solver_name, solver_type, solver_kwargs=solver_kwargs.copy())
        
        solver_kwargs.pop("perform_icm")
        self._test_job_submit(solver_name, solver_type, solver_kwargs=solver_kwargs)

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"), reason="1Qbit tests not enabled")
    @pytest.mark.oneqbit
    @pytest.mark.live_test
    def test_job_submit_oneqbit_path_relinking_solver(self):
        solver_type = functools.partial(oneqbit.PathRelinkingSolver, distance_scale=0.44)
        solver_name = "PathRelinkingSolver"
        solver_kwargs = {
            "distance_scale": 0.33,
            "greedy_path_relinking": False,
            "ref_set_count": 10,
            "seed": 123,
            "timeout": 0,
        }
        self._test_job_submit(solver_name, solver_type, solver_kwargs=solver_kwargs)

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

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id()
        ):
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
        test_grouped=False,
        content_type=ContentType.json,
        solver_kwargs=None
    ):
        """Tests the job submission and its lifecycle for a given solver.

        :param solver_type:
            The class name of the solver, for example "SimulatedAnnealing".
        """

        problem_name = f'Test-{solver_name}-{datetime.now():"%Y%m%d-%H%M%S"}'

        problem = self.create_problem(name=problem_name, test_grouped=test_grouped,content_type=content_type)

        self._test_job_submit_problem(solver_type, problem, solver_kwargs)
    
    def _test_job_submit_problem(self, solver_type, problem, solver_kwargs=None):
        """Tests the job submission and its lifecycle for a given solver.
        :param solver_type:
            The class name of the solver, for example "SimulatedAnnealing".
        :param problem
            The problem to submit
        :param solver_kwargs
            Solver kwargs
        """

        workspace = self.create_workspace()
        solver_kwargs = solver_kwargs or {}
        solver = solver_type(workspace, **solver_kwargs)

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):

            job = solver.submit(problem)
            # TODO: also test solver.optimize(problem)

            self.assertEqual(False, job.has_completed())

            # For recording purposes, we only want to record and
            # and resume recording when the job has completed
            self.pause_recording()
            job.wait_until_completed()
            self.resume_recording()

            job.refresh()
            self.assertEqual(True, job.has_completed())

            job.get_results()
            self.assertEqual(True, job.has_completed())

            job = workspace.get_job(job.id)
            self.assertEqual(True, job.has_completed())

            assert job.details.status == "Succeeded"


    @pytest.mark.live_test
    @pytest.mark.qio
    def test_problem_upload_download(self):
        solver_type = functools.partial(microsoft.SimulatedAnnealing, beta_start=0)
        solver_name = "SimulatedAnnealing"
        workspace = self.create_workspace()
        solver = solver_type(workspace)
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            problem_name = f'Test-{solver_name}-{datetime.now():"%Y%m%d-%H%M%S"}'
            if self.is_playback:
                problem_name = f'Test-{solver_name}-"20210101-000000"'
            problem = self.create_problem(name=problem_name)
            job = solver.submit(problem)
            # Check if problem can be successfully downloaded and deserialized
            problem_as_json = job.download_data(job.details.input_data_uri)
            downloaded_problem = Problem.deserialize(input_problem=problem_as_json)

            actual = downloaded_problem.serialize()
            expected = problem.serialize()
            self.assertEqual(expected, actual)

    @pytest.mark.live_test
    @pytest.mark.qio
    def test_job_attachments(self):
        workspace = self.create_workspace()
        solver = microsoft.SimulatedAnnealing(workspace)

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            expected_1 = "Some data 1".encode('utf-8')
            expected_2 = "Some other random data 2".encode('utf-8')
            problem = self.create_problem(name="test_job_attachments")

            job = solver.submit(problem)

            url1 = job.upload_attachment("test-1", expected_1)
            self.assertTrue(job.id in url1)
            self.assertTrue("test-1" in url1)

            url2 = job.upload_attachment("test-2", expected_2)
            self.assertTrue(job.id in url2)
            self.assertTrue("test-2" in url2)

            actual_1 = job.download_attachment("test-1")
            self.assertEqual(expected_1, actual_1)

            actual_2 = job.download_attachment("test-2")
            self.assertEqual(expected_2, actual_2)

            # Check if download_attachment can successfully download other blobs 
            # automatically created
            problem_as_json = job.download_attachment("inputData")
            downloaded_problem = Problem.deserialize(input_problem=problem_as_json)
            actual = downloaded_problem.serialize()
            expected = problem.serialize()
            self.assertEqual(expected, actual)


    def create_problem(
            self,
            name: str,
            init: bool = False,
            problem_type: ProblemType = ProblemType.pubo,
            test_grouped: bool = False,
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
        if test_grouped:
            terms.append(SlcTerm(
                c=1,
                terms=[Term(c=i+2, indices=[i]) for i in range(3)]
            ))

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
