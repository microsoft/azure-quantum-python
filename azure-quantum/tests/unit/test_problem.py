#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_solvers.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import unittest
from unittest.mock import Mock
from typing import TYPE_CHECKING
from azure.quantum.optimization import Problem, Term
import azure.quantum.optimization.problem
from common import expected_terms
import json

class TestProblemClass(unittest.TestCase):
    def setUp(self):
        self.mock_ws = Mock()
        self.mock_ws._get_linked_storage_sas_uri.return_value = Mock()
        self.problem = Problem(name="test")
        self.problem.terms = [
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
        ]
        self.problem.uploaded_blob_uri = "mock_blob_uri"

    def test_download(self):
        azure.quantum.optimization.problem.download_blob = Mock(
            return_value=expected_terms()
        )
        azure.quantum.optimization.problem.BlobClient = Mock()
        azure.quantum.optimization.problem.BlobClient.from_blob_url.return_value = Mock()
        azure.quantum.optimization.problem.ContainerClient = Mock()
        azure.quantum.optimization.problem.ContainerClient.from_container_url.return_value = Mock()
        acutal_result = self.problem.download(self.mock_ws)
        assert acutal_result.name == "test"
        azure.quantum.optimization.problem.download_blob.assert_called_once()

    def test_get_term(self):
        terms = self.problem.get_terms(0)
        assert len(terms) == 2

    def test_get_term_raise_exception(self):
        test_prob = Problem(name="random")
        with self.assertRaises(Exception):
            test_prob.get_terms(id=0)
