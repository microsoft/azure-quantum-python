#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_solvers.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import pytest
from unittest.mock import Mock, patch
<<<<<<< HEAD
from azure.quantum import Workspace, storage, problem_pb2
from azure.quantum.optimization import Solver, OnlineProblem, Problem, Term, ProblemType
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
        self.testprotosolver = Solver(
            self.mock_ws, "PopulationAnnealing", "Microsoft" ,"microsoft.qio.v2", "microsoft.qio-results.v2"
        )
=======
from azure.quantum import Workspace
from azure.quantum.optimization import Solver, OnlineProblem, Problem


@pytest.fixture
def testsolver():
    mock_ws = Mock(spec=Workspace)
    mock_ws.storage = "mock_storage"
    mock_ws.get_container_uri = Mock(return_value="mock_container_uri/foo/bar")
    # self.mock_ws.submit_job = Mock(return_value = )
    testsolver = Solver(
        mock_ws, "Microsoft", "SimulatedAnnealing", "json", "json"
    )
    return testsolver
>>>>>>> 463db2faf55e4d490c834035299c69742d34a20e

def test_submit_problem(testsolver):
    problem = Problem(name="test", terms = [])
    with patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
        job = testsolver.submit(problem)
    mock_upload.assert_called_once()
    testsolver.workspace.submit_job.assert_called_once()

def test_submit_online_problem(testsolver):
    # Arrange
    o_problem = OnlineProblem(name="test", blob_uri="mock_blob_uri")
    # Act
    _ = testsolver.submit(o_problem)
    # Assert
    testsolver.workspace.submit_job.assert_called_once()

<<<<<<< HEAD
    def test_number_of_solutions_set(self):
        param_name = "number_of_solutions"
        self.testsolver.set_number_of_solutions(100)
        assert param_name in self.testsolver.params["params"]
        assert self.testsolver.params["params"][param_name] == 100
    
    def test_submit_proto_problem(self):
        problem = Problem(name = "proto_test", serialization_type="application/x-protobuf")
        problem.terms = [
            Term(c=3, indices=[1,0]),
            Term(c=5, indices=[2,0])
        ]
        with patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
            job = self.testprotosolver.submit(problem)
        mock_upload.assert_called_once()
        self.testsolver.workspace.submit_job.assert_called_once()
    
    def test_throw_exception_proto_problem(self):
        self.testprotosolver.name = "SimulatedAnnealing"
        problem = Problem(name = "proto_test", serialization_type="application/x-protobuf")
        problem.terms = [
            Term(c=3, indices=[1,0]),
            Term(c=5, indices=[2,0])
        ]
        with patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
            self.assertRaises( ValueError, self.testprotosolver.submit, problem)
    
=======
def test_number_of_solutions_set(testsolver):
    param_name = "number_of_solutions"
    testsolver.set_number_of_solutions(100)
    assert param_name in testsolver.params["params"]
    assert testsolver.params["params"][param_name] == 100
>>>>>>> 463db2faf55e4d490c834035299c69742d34a20e
