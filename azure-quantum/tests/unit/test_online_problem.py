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
from azure.quantum.optimization import Problem, Term, OnlineProblem
import azure.quantum.optimization.problem 
from common import expected_terms
import json


class TestOnlineProblemClass(unittest.TestCase):
    
    def setUp(self):
        self.o_problem = OnlineProblem(name = "test", blob_uri = "mock_blob_uri")
    
    
    def test_download(self):
        azure.quantum.optimization.problem.download_blob = Mock(return_value = expected_terms())
        acutal_result = self.o_problem.download()
        #to-do add test that user warning was registered in log
        assert acutal_result.name == 'test'
        azure.quantum.optimization.problem.download_blob.assert_called_once()
        assert isinstance(acutal_result, Problem)

    def test_evaluate(self):
        config_dict = {
            1:1,
            0:1
        }
        with self.assertRaises(Exception):
            self.o_problem.evaluate(config_dict)
    
    def test_set_fixed_variables(self):
        config_dict = {
            1:1,
            0:1
        }
        with self.assertRaises(Exception):
            self.o_problem.set_fixed_variables(config_dict)


