#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_problem.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

## IMPORTS ##

import unittest
import json

from azure.quantum import Workspace
from azure.quantum.optimization import Problem, ProblemType, Term
from azure.quantum.optimization.solvers import ParallelTempering, SimulatedAnnealing, HardwarePlatform, QuantumMonteCarlo
from azure_devtools.scenario_tests.base import ReplayableTest

from workspace_init import create_workspace

class TestJob(ReplayableTest):
    def test_job_refresh(self):
        ws = create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        solver = SimulatedAnnealing(ws)
        job = solver.submit(problem)
        job.refresh()

    def test_job_get_results(self):
        ws = create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        solver = SimulatedAnnealing(ws)
        job = solver.submit(problem)
        actual = job.get_results()
        expected = {
            'version': '1.0',
            'configuration': {'0': 1, '1': 1, '2': -1, '3': 1, '4': -1},
            'cost': -6.0,
            'parameters': {'beta_start': 0.2, 'beta_stop': 1.9307236000000003, 'restarts': 360, 'sweeps': 50}}

        self.assertEqual(expected, actual)
        

if __name__ == "__main__":
    unittest.main()
