#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_online_problem.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from unittest.mock import Mock
from typing import TYPE_CHECKING
from azure.quantum.optimization import Problem, Term, OnlineProblem
import azure.quantum.optimization.problem
from common import expected_terms, QuantumTestBase
import json


class TestOnlineProblemClass(QuantumTestBase):
    def setUp(self):
        self.mock_ws = Mock()
        self.mock_ws._get_linked_storage_sas_uri.return_value = Mock()
        self.o_problem = OnlineProblem(name="test", blob_uri="mock_blob_uri")

    # TODO: instead of using mock, connect to a live service and record the responses
    def test_download(self):
        azure.quantum.optimization.problem.download_blob = Mock(
            return_value=expected_terms()
        )
        azure.quantum.optimization.problem.BlobClient = Mock()
        azure.quantum.optimization.problem.BlobClient.from_blob_url.return_value = Mock()
        azure.quantum.optimization.problem.ContainerClient = Mock()
        azure.quantum.optimization.problem.ContainerClient.from_container_url.return_value = Mock()
        actual_result = self.o_problem.download(self.mock_ws)
        # TODO: add test that user warning was registered in log
        assert actual_result.name == "test"
        azure.quantum.optimization.problem.download_blob.assert_called_once()
        assert isinstance(actual_result, Problem)
