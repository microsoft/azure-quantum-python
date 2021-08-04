#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_solvers.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import unittest
from unittest.mock import Mock, patch
from azure.quantum import Workspace, storage
from azure.quantum.optimization import Solver, OnlineProblem, Problem
import azure.quantum.storage


class TestSolvers(unittest.TestCase):
    def setUp(self):
        self.mock_ws = Mock(spec=Workspace)
        self.mock_ws.storage = "mock_storage"
        self.mock_ws.get_container_uri = Mock(return_value="mock_container_uri/foo/bar")
        # self.mock_ws.submit_job = Mock(return_value = )
        self.testsolver = Solver(
            self.mock_ws, "Microsoft", "SimulatedAnnealing", "json", "json"
        )

    def test_submit_problem(self):
        problem = Problem(name="test", terms = [])
        with patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
            job = self.testsolver.submit(problem)
        mock_upload.assert_called_once()
        self.testsolver.workspace.submit_job.assert_called_once()

    def test_submit_online_problem(self):
        # Arrange
        o_problem = OnlineProblem(name="test", blob_uri="mock_blob_uri")
        # Act
        _ = self.testsolver.submit(o_problem)
        # Assert
        self.testsolver.workspace.submit_job.assert_called_once()

    def test_number_of_solutions_set(self):
        param_name = "number_of_solutions"
        self.testsolver.set_number_of_solutions(100)
        assert param_name in self.testsolver.params["params"]
        assert self.testsolver.params["params"][param_name] == 100
