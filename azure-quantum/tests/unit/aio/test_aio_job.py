#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_job.py: Checks correctness of azure.quantum.job module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import unittest
import time
import os
import functools
import pytest
from datetime import date, datetime, timedelta, timezone

from typing import List, Type

from common import QuantumTestBase, ZERO_UID
from azure.quantum.aio import Job
from azure.quantum.aio.optimization import Problem, ProblemType
from azure.quantum.aio.target.solvers import Solver
from azure.quantum.optimization import Term
import azure.quantum.aio.target.microsoft as microsoft
import azure.quantum.aio.target.oneqbit as oneqbit
import azure.quantum.aio.target.toshiba as toshiba


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

def get_solver_types() -> List[Type[Solver]]:
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

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Temporarily disabling generation of parametrized test cases due to \
                              compatibility issues with VCR")
    async def test_job_submit(self, solver_type: Type[Solver]):
        test_job = TestJob("_test_job_submit")
        await test_job._test_job_submit(solver_name=str(solver_type), solver_type=solver_type)


class TestJob(QuantumTestBase):
    """TestJob

    Tests the azure.quantum.job module.
    """

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def test_job_submit_microsoft_simulated_annealing(self):
        solver_type = functools.partial(microsoft.SimulatedAnnealing, beta_start=0)
        solver_name = "SimulatedAnnealing"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))
        self.get_async_result(self._test_job_filter(solver_type))

    def test_job_submit_microsoft_parallel_tempering(self):
        solver_type = functools.partial(microsoft.ParallelTempering, sweeps=100)
        solver_name = "ParallelTempering"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    def test_job_submit_microsoft_tabu(self):
        solver_type = functools.partial(microsoft.Tabu, sweeps=100)
        solver_name = "Tabu"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    def test_job_submit_microsoft_quantum_monte_carlo(self):
        solver_type = functools.partial(microsoft.QuantumMonteCarlo, trotter_number=1)
        solver_name = "QuantumMonteCarlo"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    def test_job_submit_microsoft_population_annealing(self):
        solver_type = functools.partial(microsoft.PopulationAnnealing, sweeps=200)
        solver_name = "PopulationAnnealing"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    def test_job_submit_microsoft_substochastic_monte_carlo(self):
        solver_type = functools.partial(microsoft.SubstochasticMonteCarlo, step_limit=280)
        solver_name = "SubstochasticMonteCarlo"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    @pytest.mark.skip()
    def test_job_upload_and_run_solvers(self):
        self.get_async_result(self._test_job_upload_and_run_solvers())

    async def _test_job_upload_and_run_solvers(self):
        problem_name = f'Test-problem-{datetime.now():"%Y%m%d-%H%M%S"}'
        problem = self.create_problem(name=problem_name)
        workspace = self.create_async_workspace()

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_async_workspace()
            # Upload the blob data
            input_data_uri = await problem.upload(
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
                job = await solver.submit(input_data_uri)

                # For recording purposes, we only want to record and
                # and resume recording when the job has completed
                self.pause_recording()
                await job.wait_until_completed()
                await job.get_results()
                self.resume_recording()

                assert job.has_completed()
                assert job.details.status == "Succeeded"

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"), reason="1Qbit tests not enabled")
    def test_job_submit_oneqbit_tabu_search(self):
        solver_type = functools.partial(oneqbit.TabuSearch, improvement_cutoff=10)
        solver_name = "TabuSearch"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"), reason="1Qbit tests not enabled")
    def test_job_submit_oneqbit_pticm_solver(self):
        solver_type = functools.partial(oneqbit.PticmSolver, num_sweeps_per_run=99)
        solver_name = "PticmSolver"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"), reason="1Qbit tests not enabled")
    def test_job_submit_oneqbit_path_relinking_solver(self):
        solver_type = functools.partial(oneqbit.PathRelinkingSolver, distance_scale=0.44)
        solver_name = "PathRelinkingSolver"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    @pytest.mark.skipif(not(os.environ.get("AZURE_QUANTUM_TOSHIBA", "") == "1"), reason="Toshiba tests not enabled")
    def test_job_submit_toshiba_simulated_bifurcation_machine(self):
        solver_type = functools.partial(toshiba.SimulatedBifurcationMachine, loops=10)
        solver_name = "SimulatedBifurcationMachine"
        self.get_async_result(self._test_job_submit(solver_name, solver_type))

    async def _test_job_filter(self, solver_type):
        workspace = self.create_async_workspace()
        solver = solver_type(workspace)
        problem = self.create_problem(name="Test-Job-Filtering")

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id()
        ):
            job = await solver.submit(problem)

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

    async def _test_job_submit(self, solver_name: str, solver_type: Type[Solver]):
        """Tests the job submission and its lifecycle for a given solver.

        :param solver_type:
            The class name of the solver, for example "SimulatedAnnealing".
        """

        problem_name = f'Test-{solver_name}-{datetime.now():"%Y%m%d-%H%M%S"}'

        problem = self.create_problem(name=problem_name)

        await self._test_job_submit_problem(solver_type, problem)
    
    async def _test_job_submit_problem(self, solver_type: Type[Solver], problem: Problem):
        """Tests the job submission and its lifecycle for a given solver.

        :param solver_type:
            The class name of the solver, for example "SimulatedAnnealing".
        :param problem
            The problem to submit
        """

        workspace = self.create_async_workspace()

        solver: Solver = solver_type(workspace)

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):

            job = await solver.submit(problem)
            # TODO: also test solver.optimize(problem)

            # TODO: Fix recording such that playback works with repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if not self.is_playback:
                self.assertEqual(False, job.has_completed())
                if self.in_recording:
                    time.sleep(3)

                await job.refresh()
                await job.get_results()
                self.assertEqual(True, job.has_completed())

                job = await workspace.get_job(job.id)
                self.assertEqual(True, job.has_completed())
            
                assert job.has_completed()
                assert job.details.status == "Succeeded"


    def create_problem(
            self,
            name: str,
            init: bool = False,
            problem_type: ProblemType = ProblemType.pubo,
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
        )
