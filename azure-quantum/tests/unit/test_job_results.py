##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import re
import unittest
from unittest.mock import Mock
import pytest
from common import QuantumTestBase, RegexScrubbingPatterns
from azure.quantum import Job, JobDetails
from azure.quantum.target import Target


class TestJobResults(QuantumTestBase):
    """TestJob

    Tests the azure.quantum.job module.
    """

    def test_job_success(self):
        job_results = self._get_job_results("test_output_data_format","{\"Histogram\": [\"[0]\", 0.50, \"[1]\", 0.50]}")
        self.assertTrue(len(job_results["Histogram"]) == 4)

    @pytest.mark.live_test
    def test_job_get_results_with_expired_sas_token(self):
        """
        Get existing result blob url and replace its sas token with expired one, 
        so we can test its ability to refresh it.
        """
        target = self.create_echo_target()
        input_data = "{ input: 'data' }"
        job = target.submit(input_data=input_data)
        job.wait_until_completed()

        # mocking SAS-token expiration date to an expired date
        job.details.output_data_uri = re.sub(
            pattern=RegexScrubbingPatterns.URL_QUERY_SAS_KEY_EXPIRATION,
            repl="se=2024-01-01T00%3A00%3A00Z&",
            string=job.details.output_data_uri)

        job_results = job.get_results()
        self.assertEqual(job_results, input_data)


    def test_job_for_microsoft_quantum_results_v1_success(self):
        job_results = self._get_job_results("microsoft.quantum-results.v1","{\"Histogram\": [\"[0]\", 0.50, \"[1]\", 0.50]}")
        self.assertTrue(len(job_results.keys()) == 2)
        self.assertTrue(job_results["[0]"], 0.50)
        self.assertTrue(job_results["[1]"], 0.50)

    
    def test_job_for_microsoft_quantum_results_v1_no_histogram_returns_raw_result(self):
        job_result_raw = "{\"NotHistogramProperty\": [\"[0]\", 0.50, \"[1]\", 0.50]}"
        job_result = self._get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertTrue(job_result, job_result_raw)


    def test_job_for_microsoft_quantum_results_v1_invalid_histogram_returns_raw_result(self):
        job_result_raw = "{\"NotHistogramProperty\": [\"[0]\", 0.50, \"[1]\"]}"
        job_result = self._get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertTrue(job_result, job_result_raw)


    def _get_job_results(self, output_data_format, results_as_json_str):
        job_details = JobDetails(
            id= "",
            name= "",
            provider_id="",
            target="",
            container_uri="",
            input_data_format="",
            output_data_format = output_data_format)
        job_details.status = "Succeeded"
        job = Job(
            workspace=None, 
            job_details=job_details)
        
        job.has_completed = Mock(return_value=True)
        job.wait_until_completed = Mock()

        class DowloadDataMock(object):
            def decode(): str
            pass

        download_data = DowloadDataMock()
        download_data.decode = Mock(return_value=results_as_json_str)
        job.download_data = Mock(return_value=download_data)
        
        return job.get_results()


if __name__ == "__main__":
    unittest.main()
