#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_solvers.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from logging import raiseExceptions
import pytest
from unittest.mock import Mock, patch
from azure.quantum import Workspace
from azure.quantum.optimization import Solver, OnlineProblem, Problem, Term, ProblemType
from azure.quantum.serialization import ProtoProblem

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

@pytest.fixture
def testprotosolver():
    mock_ws = Mock(spec=Workspace)
    mock_ws.storage = "mock_storage"
    mock_ws.get_container_uri = Mock(return_value="mock_container_uri/foo/bar")
    # self.mock_ws.submit_job = Mock(return_value = )
    testsolver = Solver(
        mock_ws, "PopulationAnnealing"
    )
    return testsolver

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

def test_number_of_solutions_set(testsolver):
    param_name = "number_of_solutions"
    testsolver.set_number_of_solutions(100)
    assert param_name in testsolver.params["params"]
    assert testsolver.params["params"][param_name] == 100

def test_submit_proto_problem(testprotosolver):
        print(testprotosolver.name)
        problem = Problem(name = "proto_test", content_type="application/x-protobuf")
        problem.terms = [
            Term(c=3, indices=[1,0]),
            Term(c=5, indices=[2,0])
        ]
        with patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
            job = testprotosolver.submit(problem)
        mock_upload.assert_called_once()
        testprotosolver.workspace.submit_job.assert_called_once()
 
def test_throw_exception_proto_problem(testprotosolver):
    testprotosolver.name = "SimulatedAnnealing"
    problem = Problem(name = "proto_test_exception", content_type="application/x-protobuf")
    problem.terms = [
        Term(c=3, indices=[1,0]),
        Term(c=5, indices=[2,0])
    ]
    with patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
        pytest.raises( ValueError, testprotosolver.submit, problem)
