import unittest
from unittest.mock import Mock, patch
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

    def test_evaluate(self):
        config_dict = {
            1:1,
            0:1
        }
        with self.assertRaises(Exception):
            self.o_problem.evaluate(config_dict)


