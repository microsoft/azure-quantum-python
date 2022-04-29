#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_solvers.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import pytest
from azure.quantum.aio import Workspace
from azure.quantum.aio.optimization import Problem
from azure.quantum.optimization import OnlineProblem
from azure.quantum.aio.target.solvers import Solver
from asyncmock import AsyncMock, patch


@pytest.fixture
def testsolver():
    mock_ws = AsyncMock(spec=Workspace)
    mock_ws.storage = "mock_storage"
    mock_ws.get_container_uri = AsyncMock(return_value="mock_container_uri/foo/bar")
    testsolver = Solver(
        mock_ws, "Microsoft", "SimulatedAnnealing", "json", "json"
    )
    return testsolver

@pytest.mark.asyncio
async def test_submit_problem(testsolver):
    problem = Problem(name="test", terms = [])
    with patch("azure.quantum.aio.job.base_job.upload_blob") as mock_upload:
        job = await testsolver.submit(problem)
    mock_upload.assert_called_once()
    testsolver.workspace.submit_job.assert_called_once()

@pytest.mark.asyncio
async def test_submit_online_problem(testsolver):
    # Arrange
    o_problem = OnlineProblem(name="test", blob_uri="mock_blob_uri")
    # Act
    _ = await testsolver.submit(o_problem)
    # Assert
    testsolver.workspace.submit_job.assert_called_once()

def test_number_of_solutions_set(testsolver):
    param_name = "number_of_solutions"
    testsolver.set_number_of_solutions(100)
    assert param_name in testsolver.params["params"]
    assert testsolver.params["params"][param_name] == 100
