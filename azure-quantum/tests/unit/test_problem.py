import unittest
from unittest.mock import Mock, patch
from azure.quantum.optimization import Problem, Term
import azure.quantum.optimization.problem 
from common import expected_terms
import json


class TestProblemClass(unittest.TestCase):
    
    def setUp(self):
        self.problem = Problem(name = "test")
        self.problem.terms = [
            Term(c = 3, indices=[1,0]),
            Term(c = 5, indices=[2,0])
        ]
        self.problem.uploaded_blob_uri = "mock_blob_uri"
    
    def test_download(self):
        azure.quantum.optimization.problem.download_blob = Mock(return_value = expected_terms())
        acutal_result = self.problem.download()
        assert acutal_result.name == 'test'
        azure.quantum.optimization.problem.download_blob.assert_called_once()



