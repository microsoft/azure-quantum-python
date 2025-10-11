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
    @pytest.mark.xdist_group(name="echo-output")
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
        self.assertEqual(job_results["[0]"], 0.50)
        self.assertEqual(job_results["[1]"], 0.50)

    
    def test_job_for_microsoft_quantum_results_v1_no_histogram_returns_raw_result(self):
        job_result_raw = "{\"NotHistogramProperty\": [\"[0]\", 0.50, \"[1]\", 0.50]}"
        job_result = self._get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertEqual(job_result, job_result_raw)


    def test_job_for_microsoft_quantum_results_v1_invalid_histogram_returns_raw_result(self):
        job_result_raw = "{\"NotHistogramProperty\": [\"[0]\", 0.50, \"[1]\"]}"
        job_result = self._get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertEqual(job_result, job_result_raw)

    def test_job_for_microsoft_quantum_results_v2_success(self):
        job_results = self._get_job_results("microsoft.quantum-results.v2","{\"DataFormat\": \"microsoft.quantum-results.v2\", \"Results\": [{\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}]}")
        self.assertTrue(len(job_results.keys()) == 2)
        self.assertEqual(job_results["[0]"], 0.50)
        self.assertEqual(job_results["[1]"], 0.50)

    def test_job_for_microsoft_quantum_results_v2_wrong_type_raises_exception(self):
        job_result_raw = "{\"DataFormat\": \"microsoft.quantum-results.v1\", \"Results\": [{\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}]}"
        job_result = self._get_job_results("microsoft.quantum-results.v2", job_result_raw)
        self.assertEqual(job_result, job_result_raw)


    def test_job_for_microsoft_quantum_results_v2_invalid_histogram_returns_raw_result(self):
        job_result_raw = "{\"DataFormat\": \"microsoft.quantum-results.v2\", \"Results\": [{\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\"}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}]}"
        job_result = self._get_job_results("microsoft.quantum-results.v2", job_result_raw)
        self.assertEqual(job_result, job_result_raw)

    def test_job_for_microsoft_quantum_results_histogram_v2_success(self):
        job_results = self._get_job_results_histogram("microsoft.quantum-results.v2","{\"DataFormat\": \"microsoft.quantum-results.v2\", \"Results\": [{\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}]}")
        self.assertTrue(len(job_results.keys()) == 2)
        self.assertEqual(job_results["[0]"]["count"], 2)
        self.assertEqual(job_results["[1]"]["count"], 2)
        self.assertEqual(job_results["[0]"]["outcome"], [0])
        self.assertEqual(job_results["[1]"]["outcome"], [1])

    def test_job_for_microsoft_quantum_results_histogram_batch_v2_success(self):
        job_results = self._get_job_results_histogram("microsoft.quantum-results.v2","{\"DataFormat\": \"microsoft.quantum-results.v2\", \"Results\": [{\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}, {\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}, {\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}]}")
        self.assertTrue(len(job_results) == 3)
        for result in job_results:
            self.assertTrue(len(result.keys()) == 2)
            self.assertEqual(result["[0]"]["count"], 2)
            self.assertEqual(result["[1]"]["count"], 2)
            self.assertEqual(result["[0]"]["outcome"], [0])
            self.assertEqual(result["[1]"]["outcome"], [1])

    def test_job_for_microsoft_quantum_results_histogram_v2_wrong_type_raises_exception(self):
        try:
            job_results = self._get_job_results_histogram("microsoft.quantum-results.v2","{\"Histogram\": [\"[0]\", 0.50, \"[1]\", 0.50]}")
            # Fail test because we didn't get the error
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_job_for_microsoft_quantum_results_shots_v2_success(self):
        job_results = self._get_job_results_shots("microsoft.quantum-results.v2","{\"DataFormat\": \"microsoft.quantum-results.v2\", \"Results\": [{\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}]}")
        self.assertTrue(len(job_results) == 4)
        self.assertEqual(job_results[0], [0])
        self.assertEqual(job_results[1], [1])
        self.assertEqual(job_results[2], [1])
        self.assertEqual(job_results[3], [0])
    
    def test_job_for_microsoft_quantum_results_shots_batch_v2_success(self):
        job_results = self._get_job_results_shots("microsoft.quantum-results.v2","{\"DataFormat\": \"microsoft.quantum-results.v2\", \"Results\": [{\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}, {\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}, {\"Histogram\": [{\"Outcome\": [0], \"Display\": \"[0]\", \"Count\": 2}, {\"Outcome\": [1], \"Display\": \"[1]\", \"Count\": 2}], \"Shots\": [[0], [1], [1], [0]]}]}")
        self.assertTrue(len(job_results) == 3)
        for i in range(3):
            self.assertTrue(len(job_results[i]) == 4)
            self.assertEqual(job_results[i][0], [0])
            self.assertEqual(job_results[i][1], [1])
            self.assertEqual(job_results[i][2], [1])
            self.assertEqual(job_results[i][3], [0])

    def test_job_for_microsoft_quantum_results_histogram_v2_tuple_success(self):
        output = '''{ 
    \"DataFormat\": \"microsoft.quantum-results.v2\", 
    \"Results\": [ 
        { 
            \"Histogram\": [ 
                { 
                    \"Outcome\": { 
                        \"Item1\": [1, 0], 
                        \"Item2\": { 
                            \"Item1\": -2.71, 
                            \"Item2\": 67 
                        }, 
                        \"Item3\": [ 
                            { 
                                \"Item1\": 6, 
                                \"Item2\": true 
                            }, 
                            { 
                                \"Item1\": 12, 
                                \"Item2\": false 
                            } 
                        ] 
                    }, 
                    \"Display\": \"([1, 0], (-2.71, 67), [(6, true), (12, false)])\", 
                    \"Count\": 1 
                }, 
                { 
                    \"Outcome\": [1, 0], 
                    \"Display\": \"[1, 0]\", 
                    \"Count\": 1 
                }, 
                { 
                    \"Outcome\": [1], 
                    \"Display\": \"[1]\", 
                    \"Count\": 1 
                } 
            ], 
            \"Shots\": [ 
                { 
                    \"Item1\": [1, 0], 
                    \"Item2\": { 
                        \"Item1\": -2.71, 
                        \"Item2\": 67 
                    }, 
                    \"Item3\": [ 
                        { 
                            \"Item1\": 6, 
                            \"Item2\": true 
                        }, 
                        { 
                            \"Item1\": 12, 
                            \"Item2\": false 
                        } 
                    ] 
                }, 
                [1, 0], 
                [1] 
            ] 
        } 
    ] 
}'''
        job_results = self._get_job_results_histogram("microsoft.quantum-results.v2", output)
    
        self.assertTrue(len(job_results.keys()) == 3)
        self.assertEqual(job_results["[1, 0]"]["count"], 1)
        self.assertEqual(job_results["[1]"]["count"], 1)
        self.assertEqual(job_results["([1, 0], (-2.71, 67), [(6, true), (12, false)])"]["count"], 1)
        self.assertEqual(job_results["([1, 0], (-2.71, 67), [(6, true), (12, false)])"]["outcome"], ([1, 0], (-2.71, 67), [(6, True), (12, False)]))
        self.assertEqual(job_results["[1]"]["outcome"], [1])
        self.assertEqual(job_results["[1, 0]"]["outcome"], [1, 0])

    def test_job_for_microsoft_quantum_results_shots_v2_tuple_success(self):
        output = '''{
            \"DataFormat\": \"microsoft.quantum-results.v2\",
            \"Results\": [
                {
                \"Histogram\": [
                    {
                    \"Outcome\": {
                        \"Item1\": [
                        1,
                        0
                        ],
                        \"Item2\": {
                        \"Item1\": -2.71,
                        \"Item2\": 67
                        }
                    },
                    \"Display\": \"([1, 0], (-2.71, 67))\",
                    \"Count\": 1
                    },
                    {
                    \"Outcome\": [1, 0],
                    \"Display\": \"[1, 0]\",
                    \"Count\": 1
                    },
                    {
                    \"Outcome\": [1],
                    \"Display\": \"[1]\",
                    \"Count\": 1
                    }
                ],
                \"Shots\": [
                    {
                    \"Item1\": [
                        1,
                        0
                    ],
                    \"Item2\": {
                        \"Item1\": -2.71,
                        \"Item2\": 67
                    }
                    },
                    [1, 0],
                    [1]
                ]
                }
            ]
            }'''
        job_results = self._get_job_results_shots("microsoft.quantum-results.v2", output)

        self.assertTrue(len(job_results) == 3)
        self.assertEqual(job_results[0], ([1, 0], (-2.71, 67)))
        self.assertEqual(job_results[1], [1, 0])
        self.assertEqual(job_results[2], [1])

    def test_job_for_microsoft_quantum_results_shots_v2_wrong_type_raises_exception(self):
        try:
            job_results = self._get_job_results_shots("microsoft.quantum-results.v2","{\"Histogram\": [\"[0]\", 0.50, \"[1]\", 0.50]}")
            # Fail test because we didn't get the error
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def _get_job_results(self, output_data_format, results_as_json_str):
        job = self._mock_job(output_data_format, results_as_json_str)
        
        return job.get_results()
    
    def _get_job_results_histogram(self, output_data_format, results_as_json_str):
        job = self._mock_job(output_data_format, results_as_json_str)

        return job.get_results_histogram()
    
    def _get_job_results_shots(self, output_data_format, results_as_json_str):
        job = self._mock_job(output_data_format, results_as_json_str)
        
        return job.get_results_shots()
    
    def _mock_job(self, output_data_format, results_as_json_str):
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

        return job


if __name__ == "__main__":
    unittest.main()
