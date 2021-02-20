#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_job.py: Checks correctness of azure.quantum.job module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

## IMPORTS ##

import unittest
import json
import uuid
import os

from azure.quantum import Workspace
from azure.quantum.optimization import Problem
from azure.quantum.optimization.solvers import SimulatedAnnealing
from azure.quantum import Job
from tests.quantum_test_base import QuantumTestBase 

class TestJob(QuantumTestBase):
    """TestJob

    Tests the azure.quantum.job module.
    """
    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_dummy_job_id(self):
        return self.create_random_name("job-", 20)
        if self.in_recording:
            # This is live, so return a real job id.
            return TestJob.create_job_id()
        # This is a replay, so return the dummy job id that will be in the updated recordings.
        return self.dummy_uid

    def test_job_refresh(self):
        ws = self.create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        with unittest.mock.patch.object(Job, self.mock_create_job_id_name, return_value=self.get_dummy_job_id()):
            solver = SimulatedAnnealing(ws)
            job = solver.submit(problem)
            job.refresh()

    def test_job_has_completed(self):
        ws = self.create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        with unittest.mock.patch.object(Job, self.mock_create_job_id_name, return_value=self.get_dummy_job_id()):
            solver = SimulatedAnnealing(ws)
            job = solver.submit(problem)
            self.assertEqual(False, job.has_completed())
            job.get_results()
            self.assertEqual(True, job.has_completed())

    def test_job_wait_unit_completed(self):
        ws = self.create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        with unittest.mock.patch.object(Job, self.mock_create_job_id_name, return_value=self.get_dummy_job_id()):
            solver = SimulatedAnnealing(ws)
            job = solver.submit(problem)
            job.wait_until_completed()
            self.assertEqual(True, job.has_completed())

    def test_job_get_results(self):
        ws = self.create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        with unittest.mock.patch.object(Job, self.mock_create_job_id_name, return_value=self.get_dummy_job_id()):
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
