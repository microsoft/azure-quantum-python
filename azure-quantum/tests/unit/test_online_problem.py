#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_solvers.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
'''
import unittest
from unittest.mock import Mock
from typing import TYPE_CHECKING
from azure.quantum.optimization import Problem, Term, OnlineProblem
import azure.quantum.optimization.problem
from common import expected_terms
import json


class TestOnlineProblemClass(unittest.TestCase):
    def setUp(self):
        self.mock_ws = Mock()
        self.mock_ws._get_linked_storage_sas_uri.return_value = Mock()
        self.o_problem = OnlineProblem(name="test", blob_uri="mock_blob_uri")

    @pytest.skip(reason= "OnlineProblem not available in SDK yet")
    def test_download(self):
        azure.quantum.optimization.problem.download_blob = Mock(
            return_value=expected_terms()
        )
        azure.quantum.optimization.problem.BlobClient = Mock()
        azure.quantum.optimization.problem.BlobClient.from_blob_url.return_value = Mock()
        azure.quantum.optimization.problem.ContainerClient = Mock()
        azure.quantum.optimization.problem.ContainerClient.from_container_url.return_value = Mock()
        acutal_result = self.o_problem.download(self.mock_ws)
        # to-do add test that user warning was registered in log
        assert acutal_result.name == "test"
        azure.quantum.optimization.problem.download_blob.assert_called_once()
        assert isinstance(acutal_result, Problem)
'''