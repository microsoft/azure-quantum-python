#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_problem.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import unittest
import json
from azure.quantum.job.base_job import ContentType
import numpy
import os
import re
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING
from azure.quantum.optimization import Problem, ProblemType, Term
import azure.quantum.optimization.problem
from common import expected_terms
import numpy
import os


class TestProblemClass(unittest.TestCase):
    
    def setUp(self):
        self.mock_ws = Mock()
        self.mock_ws.get_container_uri = Mock(return_value = "mock_container_uri/foo/bar")
        self.mock_ws._get_linked_storage_sas_uri = Mock(return_value = "mock_linked_storage_sas_uri/foo/bar")
        ## QUBO problem
        self.problem = Problem(name="test")
        self.problem.terms = [
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
        ]
        self.problem.uploaded_blob_uri = "mock_blob_uri"

        ## PUBO problem
        self.pubo_problem = Problem(name="test")
        self.pubo_problem.terms = [
            Term(c=3, indices=[1, 0, 1]),
            Term(c=5, indices=[2, 0, 0]),
            Term(c=-1, indices=[1, 0, 0]),
            Term(c=4, indices=[0, 2, 1])
        ]
    
    def test_problem_name_serialization(self):
        problem_names = ["test",
                         "my_problem"]
        for problem_name in problem_names:
            problem = Problem(name=problem_name)
            problem.terms = [
                Term(c=3, indices=[1, 0]),
                Term(c=5, indices=[2, 0]),
            ]
            serialized_problem = problem.serialize()

            # name is in the serialized string
            self.assertTrue(re.search(f'"name"\\s*:\\s*"{problem_name}"',
                                      serialized_problem,
                                      flags=re.RegexFlag.MULTILINE))

            # name is in the correct place in the json structure
            problem_json = json.loads(serialized_problem)
            self.assertEqual(problem_json["metadata"]["name"], problem_name)

            # deserializes name
            deserialized_problem = Problem.deserialize(input_problem=serialized_problem)
            self.assertEqual(problem_name, deserialized_problem.name)

            new_problem_name = "new_problem_name"
            # use the name passed in the parameter
            deserialized_problem = Problem.deserialize(input_problem=serialized_problem,
                                                       name=new_problem_name)
            self.assertEqual(new_problem_name, deserialized_problem.name)

        # test deserializing a problem that does not have a name in the json
        # and leaving the name as None
        serialized_problem_without_name = '{"cost_function": {"version": "1.0", "type": "ising", "terms": [{"c": 3, "ids": [1, 0]}, {"c": 5, "ids": [2, 0]}]}}'        
        deserialized_problem = Problem.deserialize(input_problem=serialized_problem_without_name)
        self.assertEqual(deserialized_problem.name, "Optimization problem")

        # test deserializing a problem that does not have a name in the json
        # and using the name parameter
        new_problem_name = "new_problem_name"
        deserialized_problem = Problem.deserialize(input_problem=serialized_problem_without_name,
                                                   name=new_problem_name)
        self.assertEqual(new_problem_name, deserialized_problem.name)

        # test deserializing a problem that does not have a name but have a metadata in the json
        # and leaving the name as None
        serialized_problem_without_name = '{"metadata":{"somemetadata":123}, "cost_function": {"version": "1.0", "type": "ising", "terms": [{"c": 3, "ids": [1, 0]}, {"c": 5, "ids": [2, 0]}]}}'        
        deserialized_problem = Problem.deserialize(input_problem=serialized_problem_without_name)
        self.assertEqual(deserialized_problem.name, "Optimization problem")

    def test_upload(self):
        with patch("azure.quantum.optimization.problem.BlobClient") as mock_blob_client, \
            patch("azure.quantum.optimization.problem.ContainerClient") as mock_container_client, \
            patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
            mock_blob_client.from_blob_url.return_value = Mock()
            mock_container_client.from_container_url.return_value = Mock()
            self.assertIsNone(self.pubo_problem.uploaded_blob_uri)
            actual_result = self.pubo_problem.upload(self.mock_ws)
            mock_upload.get_blob_uri_with_sas_token = Mock()
            azure.quantum.job.base_job.upload_blob.assert_called_once()


    def test_download(self):
        with patch("azure.quantum.optimization.problem.download_blob") as mock_download_blob,\
            patch("azure.quantum.optimization.problem.BlobClient") as mock_blob_client,\
            patch("azure.storage.blob.BlobClient.from_blob_url") as mock_blob_url,\
            patch("azure.quantum.optimization.problem.ContainerClient") as mock_container_client:
            mock_download_blob.return_value=expected_terms()
            mock_blob_client.from_blob_url.return_value = Mock()
            mock_container_client.from_container_url.return_value = Mock()
            mock_blob_url = Mock()
            actual_result = self.problem.download(self.mock_ws)
            self.assertEqual(actual_result.name, "test")
            azure.quantum.optimization.problem.download_blob.assert_called_once()

    def test_get_term(self):
        terms = self.problem.get_terms(0)
        self.assertEqual(len(terms), 2)

    def test_get_term_raise_exception(self):
        test_prob = Problem(name="random")
        with self.assertRaises(Exception):
            test_prob.get_terms(id=0)
    
    def tearDown(self):
        test_files = [
            self.default_qubo_filename,
            self.default_pubo_filename
        ]

        for test_file in test_files:
            if os.path.isfile(test_file):
                os.remove(test_file)
      