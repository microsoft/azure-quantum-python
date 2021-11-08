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
import numpy
import os
import re
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING
from azure.quantum.serialization import ProtoProblem
from azure.quantum.optimization import Problem, ProblemType, Term, SlcTerm
import azure.quantum.optimization.problem
from common import expected_terms
import numpy
import os


class TestProblemClass(unittest.TestCase):
    
    def setUp(self):
        self.mock_ws = Mock()
        self.mock_ws.get_container_uri = Mock(return_value = "mock_container_uri/foo/bar")

        ## QUBO problem
        self.problem = Problem(name="test")
        self.problem.terms = [
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
        ]
        self.problem.uploaded_blob_uri = "mock_blob_uri"

        # Create equivalent NPZ file for translation
        self.problem.row = numpy.array([1, 2])
        self.problem.col = numpy.array([0, 0])
        self.problem.data = numpy.array([3, 5])
        
        # If arguments are passed to savez with no keywords
        # then default names are used (e.g. "arr_0", "arr_1", etc)
        # otherwise it uses those supplied by user (e.g. "row", "col", etc)
        self.default_qubo_filename = "default_qubo.npz"
        numpy.savez(self.default_qubo_filename, 
            self.problem.row,
            self.problem.col,
            self.problem.data
        )

        self.with_keywords_qubo_filename = "with_keywords_qubo.npz"
        numpy.savez(self.with_keywords_qubo_filename,
            row=self.problem.row,
            col=self.problem.col,
            data=self.problem.data
        )

        ## PUBO problem
        self.pubo_problem = Problem(name="test")
        self.pubo_problem.terms = [
            Term(c=3, indices=[1, 0, 1]),
            Term(c=5, indices=[2, 0, 0]),
            Term(c=-1, indices=[1, 0, 0]),
            Term(c=4, indices=[0, 2, 1])
        ]

        # Create equivalent NPZ file for translation
        self.pubo_problem.i = numpy.array([1, 2, 1, 0])
        self.pubo_problem.j = numpy.array([0, 0, 0, 2])
        self.pubo_problem.k = numpy.array([1, 0, 0, 1])
        self.pubo_problem.c = numpy.array([3, 5, -1, 4])
        
        self.default_pubo_filename = "default_pubo.npz"
        numpy.savez(self.default_pubo_filename, 
            self.pubo_problem.i,
            self.pubo_problem.j,
            self.pubo_problem.k,
            self.pubo_problem.c
        )

        self.with_keywords_pubo_filename = "with_keywords_pubo.npz"
        numpy.savez(self.with_keywords_pubo_filename,
            i=self.pubo_problem.i,
            j=self.pubo_problem.j,
            k=self.pubo_problem.k,
            c=self.pubo_problem.c
        )
    
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
            assert re.search(f'"name"\\s*:\\s*"{problem_name}"',
                             serialized_problem,
                             flags=re.RegexFlag.MULTILINE)

            # name is in the correct place in the json structure
            problem_json = json.loads(serialized_problem)
            assert problem_json["metadata"]["name"] == problem_name

            # deserializes name
            deserialized_problem = Problem.deserialize(problem_as_json=serialized_problem)
            assert problem_name == deserialized_problem.name

            new_problem_name = "new_problem_name"
            # use the name passed in the parameter
            deserialized_problem = Problem.deserialize(problem_as_json=serialized_problem,
                                                       name=new_problem_name)
            assert new_problem_name == deserialized_problem.name

        # test deserializing a problem that does not have a name in the json
        # and leaving the name as None
        serialized_problem_without_name = '{"cost_function": {"version": "1.0", "type": "ising", "terms": [{"c": 3, "ids": [1, 0]}, {"c": 5, "ids": [2, 0]}]}}'        
        deserialized_problem = Problem.deserialize(problem_as_json=serialized_problem_without_name)
        assert deserialized_problem.name == "Optimization problem"

        # test deserializing a problem that does not have a name in the json
        # and using the name parameter
        new_problem_name = "new_problem_name"
        deserialized_problem = Problem.deserialize(problem_as_json=serialized_problem_without_name,
                                                   name=new_problem_name)
        assert new_problem_name == deserialized_problem.name

        # test deserializing a problem that does not have a name but have a metadata in the json
        # and leaving the name as None
        serialized_problem_without_name = '{"metadata":{"somemetadata":123}, "cost_function": {"version": "1.0", "type": "ising", "terms": [{"c": 3, "ids": [1, 0]}, {"c": 5, "ids": [2, 0]}]}}'        
        deserialized_problem = Problem.deserialize(problem_as_json=serialized_problem_without_name)
        assert deserialized_problem.name == "Optimization problem"

    def test_upload(self):
        with patch("azure.quantum.optimization.problem.BlobClient") as mock_blob_client, \
            patch("azure.quantum.optimization.problem.ContainerClient") as mock_container_client, \
            patch("azure.quantum.job.base_job.upload_blob") as mock_upload:
            mock_blob_client.from_blob_url.return_value = Mock()
            mock_container_client.from_container_url.return_value = Mock()
            assert(self.pubo_problem.uploaded_blob_uri == None)
            actual_result = self.pubo_problem.upload(self.mock_ws)
            mock_upload.get_blob_uri_with_sas_token = Mock()
            azure.quantum.job.base_job.upload_blob.assert_called_once()


    def test_download(self):
        with patch("azure.quantum.optimization.problem.download_blob") as mock_download_blob,\
            patch("azure.quantum.optimization.problem.BlobClient") as mock_blob_client,\
            patch("azure.quantum.optimization.problem.ContainerClient") as mock_container_client:
            mock_download_blob.return_value=expected_terms()
            mock_blob_client.from_blob_url.return_value = Mock()
            mock_container_client.from_container_url.return_value = Mock()
            actual_result = self.problem.download(self.mock_ws)
            assert actual_result.name == "test"
            azure.quantum.optimization.problem.download_blob.assert_called_once()

    def test_get_term(self):
        terms = self.problem.get_terms(0)
        assert len(terms) == 2

    def test_get_term_raise_exception(self):
        test_prob = Problem(name="random")
        with self.assertRaises(Exception):
            test_prob.get_terms(id=0)
    
    def test_grouped_type(self):
        problem = Problem(name="test_pubo_grouped", problem_type=ProblemType.pubo)
        problem.terms = [
            Term(c=3, indices=[1, 0, 1]),
            Term(c=5, indices=[2, 0, 0]),
            Term(c=-1, indices=[1, 0, 0]),
            Term(c=4, indices=[0, 2, 1])
        ]
        assert problem.problem_type is ProblemType.pubo
        problem.add_slc_term([(3,0), (2,1), (-1,None)])
        assert problem.problem_type is ProblemType.pubo_grouped

    def test_create_npz_file_default(self):
        # When no keywords are supplied, columns have default names
        # e.g. "arr_0", "arr_1" etc
        
        # QUBO
        npz_file = numpy.load(self.default_qubo_filename)
        num_columns = 3

        self.assertEqual(len(npz_file.files), num_columns)
        for i in range(num_columns):
            self.assertEqual(npz_file.files[i], "arr_%s" % i)

        # PUBO
        npz_file = numpy.load(self.default_pubo_filename)
        num_columns = 4

        self.assertEqual(len(npz_file.files), num_columns)
        for i in range(num_columns):
            self.assertEqual(npz_file.files[i], "arr_%s" % i)

    def test_create_npz_file_with_keywords(self):
        # When keywords are supplied, columns use these names

        # QUBO
        npz_file = numpy.load(self.with_keywords_qubo_filename)
        keywords = ["row", "col", "data"]

        self.assertEqual(len(npz_file.files), len(keywords))
        for i in range(len(keywords)):
            self.assertEqual(npz_file.files[i], keywords[i])

        # PUBO
        npz_file = numpy.load(self.with_keywords_pubo_filename)
        keywords = ["i", "j", "k", "c"]

        self.assertEqual(len(npz_file.files), len(keywords))
        for i in range(len(keywords)):
            self.assertEqual(npz_file.files[i], keywords[i])

    def test_valid_npz(self):
        default_qubo = numpy.load(self.default_qubo_filename)
        with_keywords_qubo = numpy.load(self.with_keywords_qubo_filename)

        default_pubo = numpy.load(self.default_pubo_filename)
        with_keywords_pubo = numpy.load(self.with_keywords_pubo_filename)

        ## Valid files
        self.assertTrue(self.problem.is_valid_npz(default_qubo.files))
        self.assertTrue(self.problem.is_valid_npz(
            default_qubo.files,
            ["arr_0", "arr_1"],
            "arr_2")
        )

        self.assertTrue(self.problem.is_valid_npz(
            with_keywords_qubo.files,
            ["col", "row"],
            "data")
        )

        self.assertTrue(self.pubo_problem.is_valid_npz(
            default_pubo.files,
            ["arr_0", "arr_1", "arr_2"],
            "arr_3")
        )
        self.assertTrue(self.pubo_problem.is_valid_npz(
            with_keywords_pubo.files,
            ["i", "j", "k"],
            "c")
        )

        ## Invalid files
        # Too many columns
        self.assertFalse(self.problem.is_valid_npz(
            default_qubo.files,
            ["arr_0", "arr_1", "arr_2"],
            "arr_3")
        )

        self.assertFalse(self.pubo_problem.is_valid_npz(
            default_pubo.files,
            ["arr_0", "arr_1", "arr_2", "arr_3"],
            "arr_4")
        )

        # Wrong column names
        self.assertFalse(self.problem.is_valid_npz(
            with_keywords_qubo.files,
            ["i", "j"],
            "k")
        )

        self.assertFalse(self.pubo_problem.is_valid_npz(
            with_keywords_pubo.files,
            ["x", "y", "z"],
            "c")
        )

        # No indices column names
        self.assertFalse(self.problem.is_valid_npz(
            with_keywords_qubo.files,
            [],
            "data")
        )

        # Wrong coefficient column name
        self.assertFalse(self.problem.is_valid_npz(
           with_keywords_qubo.files,
           ["row", "col"], 
           "")
        )

    def test_terms_from_npz_qubo(self):
        # Exceptions are raised for invalid file paths or files with incorrect naming
        self.assertRaises(Exception, self.problem.terms_from_npz, "invalid_file_path.npz")
        self.assertRaises(
            Exception,
            self.problem.terms_from_npz,
            self.default_qubo_filename,
            ["arr_0", "arr_1", "arr_2"],
            "arr_3"
        )

        # Terms are produced for valid files
        self.assertEqual(
            self.problem.terms_from_npz(self.default_qubo_filename),
            self.problem.terms
        )

        self.assertEqual(
            self.problem.terms_from_npz(
                self.with_keywords_qubo_filename,
                ["row", "col"],
                "data"
            ),
            self.problem.terms
        )

    def test_terms_from_npz_pubo(self):
        # Exceptions are raised for invalid file paths or files with incorrect naming
        self.assertRaises(Exception, self.pubo_problem.terms_from_npz, "invalid_file_path.npz")
        self.assertRaises(
            Exception,
            self.pubo_problem.terms_from_npz,
            self.default_pubo_filename,
            ["arr_0", "arr_1", "arr_2", "arr_3"],
            "arr_4"
        )

        # Terms are produced for valid files
        self.assertEqual(
            self.pubo_problem.terms_from_npz(
                self.default_pubo_filename,
                ["arr_0", "arr_1", "arr_2"],
                "arr_3"
            ),
            self.pubo_problem.terms
        )

        self.assertEqual(
            self.pubo_problem.terms_from_npz(
                self.with_keywords_pubo_filename,
                ["i", "j", "k"],
                "c"
            ),
            self.pubo_problem.terms
        )
    
    def test_serialzie_proto_problem(self):
        problem = Problem(name = "test_proto", problem_type = ProblemType.ising, content_type="application/x-protobuf")
        problem.terms = [
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
        ]
        problem_msgs = problem.serialize()
        self.assertEqual(
            len(problem_msgs), 1
        )
        proto_problem = ProtoProblem()
        proto_problem.ParseFromString(problem_msgs[0])
        self.assertEqual(
            proto_problem.cost_function.type, 
            ProtoProblem.ProblemType.ISING
        )
        self.assertEqual(
            len(proto_problem.cost_function.terms),
            12
        )
    
    def test_deserialize_proto_problem(self):
        problem = Problem(name = "test_proto", problem_type = ProblemType.pubo, content_type="application/x-protobuf")
        problem.terms = [
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
            Term(c=3, indices=[1, 0]),
            Term(c=5, indices=[2, 0]),
        ]
        problem_msgs = problem.serialize()
        deserialized_problem = Problem.deserialize(problem_msgs)
        self.assertEqual( len(deserialized_problem.terms), 12 )
        self.assertEqual(deserialized_problem.problem_type, ProblemType.pubo)
        self.assertEqual(deserialized_problem.name, problem.name)
    
    def tearDown(self):
        test_files = [
            self.default_qubo_filename,
            self.with_keywords_qubo_filename,
            self.default_pubo_filename,
            self.with_keywords_pubo_filename
        ]

        for test_file in test_files:
            if os.path.isfile(test_file):
                os.remove(test_file)
      