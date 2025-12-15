import unittest
from unittest.mock import Mock

from azure.quantum import Job, JobDetails


def _mock_job(output_data_format: str, results_as_json_str: str) -> Job:
    job_details = JobDetails(
        id="",
        name="",
        provider_id="",
        target="",
        container_uri="",
        input_data_format="",
        output_data_format=output_data_format,
    )
    job_details.status = "Succeeded"
    job = Job(workspace=None, job_details=job_details)

    job.has_completed = Mock(return_value=True)
    job.wait_until_completed = Mock()

    class DowloadDataMock(object):
        def decode():
            str

        pass

    download_data = DowloadDataMock()
    download_data.decode = Mock(return_value=results_as_json_str)
    job.download_data = Mock(return_value=download_data)

    return job


def _get_job_results(output_data_format: str, results_as_json_str: str):
    job = _mock_job(output_data_format, results_as_json_str)
    return job.get_results()


def _get_job_results_histogram(output_data_format: str, results_as_json_str: str):
    job = _mock_job(output_data_format, results_as_json_str)
    return job.get_results_histogram()


def _get_job_results_shots(output_data_format: str, results_as_json_str: str):
    job = _mock_job(output_data_format, results_as_json_str)
    return job.get_results_shots()


class TestJobResultsLocal(unittest.TestCase):
    def test_job_success(self):
        job_results = _get_job_results(
            "test_output_data_format",
            '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
        )
        self.assertTrue(len(job_results["Histogram"]) == 4)

    def test_job_for_microsoft_quantum_results_v1_success(self):
        job_results = _get_job_results(
            "microsoft.quantum-results.v1",
            '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
        )
        self.assertTrue(len(job_results.keys()) == 2)
        self.assertEqual(job_results["[0]"], 0.50)
        self.assertEqual(job_results["[1]"], 0.50)

    def test_job_for_microsoft_quantum_results_v1_no_histogram_returns_raw_result(self):
        job_result_raw = '{"NotHistogramProperty": ["[0]", 0.50, "[1]", 0.50]}'
        job_result = _get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertEqual(job_result, job_result_raw)

    def test_job_for_microsoft_quantum_results_v1_invalid_histogram_returns_raw_result(
        self,
    ):
        job_result_raw = '{"NotHistogramProperty": ["[0]", 0.50, "[1]"]}'
        job_result = _get_job_results("microsoft.quantum-results.v1", job_result_raw)
        self.assertEqual(job_result, job_result_raw)

    def test_job_for_microsoft_quantum_results_v2_success(self):
        job_results = _get_job_results(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
        )
        self.assertTrue(len(job_results.keys()) == 2)
        self.assertEqual(job_results["[0]"], 0.50)
        self.assertEqual(job_results["[1]"], 0.50)

    def test_job_for_microsoft_quantum_results_v2_wrong_type_returns_raw(self):
        job_result_raw = '{"DataFormat": "microsoft.quantum-results.v1", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}'
        job_result = _get_job_results("microsoft.quantum-results.v2", job_result_raw)
        self.assertEqual(job_result, job_result_raw)

    def test_job_for_microsoft_quantum_results_v2_invalid_histogram_returns_raw_result(
        self,
    ):
        job_result_raw = '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]"}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}'
        job_result = _get_job_results("microsoft.quantum-results.v2", job_result_raw)
        self.assertEqual(job_result, job_result_raw)

    def test_job_for_microsoft_quantum_results_histogram_v2_success(self):
        job_results = _get_job_results_histogram(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
        )
        self.assertTrue(len(job_results.keys()) == 2)
        self.assertEqual(job_results["[0]"]["count"], 2)
        self.assertEqual(job_results["[1]"]["count"], 2)
        self.assertEqual(job_results["[0]"]["outcome"], [0])
        self.assertEqual(job_results["[1]"]["outcome"], [1])

    def test_job_for_microsoft_quantum_results_histogram_batch_v2_success(self):
        job_results = _get_job_results_histogram(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
        )
        self.assertTrue(len(job_results) == 3)
        for result in job_results:
            self.assertTrue(len(result.keys()) == 2)
            self.assertEqual(result["[0]"]["count"], 2)
            self.assertEqual(result["[1]"]["count"], 2)
            self.assertEqual(result["[0]"]["outcome"], [0])
            self.assertEqual(result["[1]"]["outcome"], [1])

    def test_job_for_microsoft_quantum_results_histogram_v2_wrong_type_raises_exception(
        self,
    ):
        with self.assertRaises(Exception):
            _get_job_results_histogram(
                "microsoft.quantum-results.v2",
                '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
            )

    def test_job_for_microsoft_quantum_results_shots_v2_success(self):
        job_results = _get_job_results_shots(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
        )
        self.assertTrue(len(job_results) == 4)
        self.assertEqual(job_results[0], [0])
        self.assertEqual(job_results[1], [1])
        self.assertEqual(job_results[2], [1])
        self.assertEqual(job_results[3], [0])

    def test_job_for_microsoft_quantum_results_shots_batch_v2_success(self):
        job_results = _get_job_results_shots(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
        )
        self.assertTrue(len(job_results) == 3)
        for i in range(3):
            self.assertTrue(len(job_results[i]) == 4)
            self.assertEqual(job_results[i][0], [0])
            self.assertEqual(job_results[i][1], [1])
            self.assertEqual(job_results[i][2], [1])
            self.assertEqual(job_results[i][3], [0])

    def test_job_for_microsoft_quantum_results_histogram_v2_tuple_success(self):
        output = """{ 
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
}"""
        job_results = _get_job_results_histogram("microsoft.quantum-results.v2", output)
        self.assertTrue(len(job_results.keys()) == 3)
        self.assertEqual(job_results["[1, 0]"]["count"], 1)
        self.assertEqual(job_results["[1]"]["count"], 1)
        self.assertEqual(
            job_results["([1, 0], (-2.71, 67), [(6, true), (12, false)])"]["count"], 1
        )
        self.assertEqual(
            job_results["([1, 0], (-2.71, 67), [(6, true), (12, false)])"]["outcome"],
            ([1, 0], (-2.71, 67), [(6, True), (12, False)]),
        )
        self.assertEqual(job_results["[1]"]["outcome"], [1])
        self.assertEqual(job_results["[1, 0]"]["outcome"], [1, 0])

    def test_job_for_microsoft_quantum_results_shots_v2_tuple_success(self):
        output = """{
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
            }"""
        job_results = _get_job_results_shots("microsoft.quantum-results.v2", output)
        self.assertTrue(len(job_results) == 3)
        self.assertEqual(job_results[0], ([1, 0], (-2.71, 67)))
        self.assertEqual(job_results[1], [1, 0])
        self.assertEqual(job_results[2], [1])

    def test_job_for_microsoft_quantum_results_shots_v2_wrong_type_raises_exception(
        self,
    ):
        with self.assertRaises(Exception):
            _get_job_results_shots(
                "microsoft.quantum-results.v2",
                '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
            )
