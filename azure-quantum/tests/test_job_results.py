##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest
from unittest.mock import Mock
from azure.quantum import Job, JobDetails


def _mock_job(output_data_format: str, results_as_json_str: str, status: str = "Succeeded") -> Job:
    job_details = JobDetails(
        id="",
        name="",
        provider_id="",
        target="",
        container_uri="",
        input_data_format="",
        output_data_format=output_data_format,
    )
    job_details.status = status
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


def _get_job_results(output_data_format: str, results_as_json_str: str, status: str = "Succeeded"):
    job = _mock_job(output_data_format, results_as_json_str, status)
    return job.get_results()


def _get_job_results_histogram(output_data_format: str, results_as_json_str: str, status: str = "Succeeded"):
    job = _mock_job(output_data_format, results_as_json_str, status)
    return job.get_results_histogram()


def _get_job_results_shots(output_data_format: str, results_as_json_str: str, status: str = "Succeeded"):
    job = _mock_job(output_data_format, results_as_json_str, status)
    return job.get_results_shots()


def test_job_success():
    job_results = _get_job_results(
        "test_output_data_format",
        '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
    )
    assert len(job_results["Histogram"]) == 4


def test_job_for_microsoft_quantum_results_v1_success():
    job_results = _get_job_results(
        "microsoft.quantum-results.v1",
        '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
    )
    assert len(job_results.keys()) == 2
    assert job_results["[0]"] == 0.50
    assert job_results["[1]"] == 0.50


def test_job_get_results_with_completed_status():
    job_results = _get_job_results(
        "microsoft.quantum-results.v1",
        '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
        "Completed",
    )
    assert len(job_results.keys()) == 2
    assert job_results["[0]"] == 0.50
    assert job_results["[1]"] == 0.50


def test_job_get_results_with_failed_status_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Cannot retrieve results as job execution failed"):
        _get_job_results(
            "microsoft.quantum-results.v1",
            '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
            "Failed",
        )


def test_job_get_results_with_cancelled_status_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Cannot retrieve results as job execution failed"):
        _get_job_results(
            "microsoft.quantum-results.v1",
            '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
            "Cancelled",
        )


def test_job_get_results_histogram_with_completed_status():
    job_results = _get_job_results_histogram(
        "microsoft.quantum-results.v2",
        '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
        "Completed",
    )
    assert len(job_results.keys()) == 2
    assert job_results["[0]"]["count"] == 2
    assert job_results["[1]"]["count"] == 2


def test_job_get_results_histogram_with_failed_status_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Cannot retrieve results as job execution failed"):
        _get_job_results_histogram(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
            "Failed",
        )


def test_job_get_results_histogram_with_cancelled_status_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Cannot retrieve results as job execution failed"):
        _get_job_results_histogram(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
            "Cancelled",
        )


def test_job_get_results_shots_with_completed_status():
    job_results = _get_job_results_shots(
        "microsoft.quantum-results.v2",
        '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
        "Completed",
    )
    assert len(job_results) == 4
    assert job_results[0] == [0]
    assert job_results[1] == [1]
    assert job_results[2] == [1]
    assert job_results[3] == [0]


def test_job_get_results_shots_with_failed_status_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Cannot retrieve results as job execution failed"):
        _get_job_results_shots(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
            "Failed",
        )


def test_job_get_results_shots_with_cancelled_status_raises_runtime_error():
    with pytest.raises(RuntimeError, match="Cannot retrieve results as job execution failed"):
        _get_job_results_shots(
            "microsoft.quantum-results.v2",
            '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
            "Cancelled",
        )


def test_job_for_microsoft_quantum_results_v1_no_histogram_returns_raw_result():
    job_result_raw = '{"NotHistogramProperty": ["[0]", 0.50, "[1]", 0.50]}'
    job_result = _get_job_results("microsoft.quantum-results.v1", job_result_raw)
    assert job_result == job_result_raw


def test_job_for_microsoft_quantum_results_v1_invalid_histogram_returns_raw_result():
    job_result_raw = '{"NotHistogramProperty": ["[0]", 0.50, "[1]"]}'
    job_result = _get_job_results("microsoft.quantum-results.v1", job_result_raw)
    assert job_result == job_result_raw


def test_job_for_microsoft_quantum_results_v2_success():
    job_results = _get_job_results(
        "microsoft.quantum-results.v2",
        '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
    )
    assert len(job_results.keys()) == 2
    assert job_results["[0]"] == 0.50
    assert job_results["[1]"] == 0.50


def test_job_for_microsoft_quantum_results_v2_wrong_type_returns_raw():
    job_result_raw = '{"DataFormat": "microsoft.quantum-results.v1", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}'
    job_result = _get_job_results("microsoft.quantum-results.v2", job_result_raw)
    assert job_result == job_result_raw


def test_job_for_microsoft_quantum_results_v2_invalid_histogram_returns_raw_result():
    job_result_raw = '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]"}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}'
    job_result = _get_job_results("microsoft.quantum-results.v2", job_result_raw)
    assert job_result == job_result_raw


def test_job_for_microsoft_quantum_results_histogram_v2_success():
    job_results = _get_job_results_histogram(
        "microsoft.quantum-results.v2",
        '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
    )
    assert len(job_results.keys()) == 2
    assert job_results["[0]"]["count"] == 2
    assert job_results["[1]"]["count"] == 2
    assert job_results["[0]"]["outcome"] == [0]
    assert job_results["[1]"]["outcome"] == [1]


def test_job_for_microsoft_quantum_results_histogram_batch_v2_success():
    job_results = _get_job_results_histogram(
        "microsoft.quantum-results.v2",
        '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
    )
    assert len(job_results) == 3
    for result in job_results:
        assert len(result.keys()) == 2
        assert result["[0]"]["count"] == 2
        assert result["[1]"]["count"] == 2
        assert result["[0]"]["outcome"] == [0]
        assert result["[1]"]["outcome"] == [1]


def test_job_for_microsoft_quantum_results_histogram_v2_wrong_type_raises_exception():
    try:
        _get_job_results_histogram(
            "microsoft.quantum-results.v2",
            '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
        )
        assert False
    except Exception:
        assert True


def test_job_for_microsoft_quantum_results_shots_v2_success():
    job_results = _get_job_results_shots(
        "microsoft.quantum-results.v2",
        '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
    )
    assert len(job_results) == 4
    assert job_results[0] == [0]
    assert job_results[1] == [1]
    assert job_results[2] == [1]
    assert job_results[3] == [0]


def test_job_for_microsoft_quantum_results_shots_batch_v2_success():
    job_results = _get_job_results_shots(
        "microsoft.quantum-results.v2",
        '{"DataFormat": "microsoft.quantum-results.v2", "Results": [{"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}, {"Histogram": [{"Outcome": [0], "Display": "[0]", "Count": 2}, {"Outcome": [1], "Display": "[1]", "Count": 2}], "Shots": [[0], [1], [1], [0]]}]}',
    )
    assert len(job_results) == 3
    for i in range(3):
        assert len(job_results[i]) == 4
        assert job_results[i][0] == [0]
        assert job_results[i][1] == [1]
        assert job_results[i][2] == [1]
        assert job_results[i][3] == [0]


def test_job_for_microsoft_quantum_results_histogram_v2_tuple_success():
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
    assert len(job_results.keys()) == 3
    assert job_results["[1, 0]"]["count"] == 1
    assert job_results["[1]"]["count"] == 1
    assert job_results["([1, 0], (-2.71, 67), [(6, true), (12, false)])"]["count"] == 1
    assert job_results["([1, 0], (-2.71, 67), [(6, true), (12, false)])"][
        "outcome"
    ] == ([1, 0], (-2.71, 67), [(6, True), (12, False)])
    assert job_results["[1]"]["outcome"] == [1]
    assert job_results["[1, 0]"]["outcome"] == [1, 0]


def test_job_for_microsoft_quantum_results_shots_v2_tuple_success():
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
    assert len(job_results) == 3
    assert job_results[0] == ([1, 0], (-2.71, 67))
    assert job_results[1] == [1, 0]
    assert job_results[2] == [1]


def test_job_for_microsoft_quantum_results_v2_with_dash():
    output = """
    {
        "DataFormat": "microsoft.quantum-results.v2",
        "Results": [
            {
            "Histogram": [
                {
                "Outcome": [ 0, 1, "-" ],
                "Display": "[0, 1, -]",
                "Count": 1
                }
            ],
            "Shots": [ [ 0, 1, "-" ] ]
            }
        ]
    }
    """
    job_results = _get_job_results("microsoft.quantum-results.v2", output)
    assert len(job_results.keys()) == 1
    assert job_results["[0, 1, -]"] == 1.0

    job_results = _get_job_results_histogram("microsoft.quantum-results.v2", output)
    # expecting dict with key: [0, 1, -] and value: {'outcome': [0, 1, '-'], 'count': 1}
    assert len(job_results.keys()) == 1
    assert job_results["[0, 1, -]"]["count"] == 1
    assert job_results["[0, 1, -]"]["outcome"] == [0, 1, '-']

    job_results = _get_job_results_shots("microsoft.quantum-results.v2", output)
    assert len(job_results) == 1
    assert job_results[0] == [0, 1, '-']


def test_job_for_microsoft_quantum_results_shots_v2_error_in_shots():
    output = """
    {
        "DataFormat": "microsoft.quantum-results.v2",
        "Results": [
            {
            "Histogram": [
                {
                "Outcome": [10],
                "Display": "[10]",
                "Count": 3
                },
                {
                "Outcome": {
                    "Error": {
                    "Code": "0x20",
                    "Name": "TestErrorThirtyTwo"
                    }
                },
                "Display": "Error 0x20: TestErrorThirtyTwo",
                "Count": 1
                },
                {
                "Outcome": {
                    "Error": {
                    "Code": "0x40",
                    "Name": "TestErrorSixtyFour"
                    }
                },
                "Display": "Error 0x40: TestErrorSixtyFour",
                "Count": 1
                }
            ],
            "Shots": [
                [10],
                {
                "Error": {
                    "Code": "0x20",
                    "Name": "TestErrorThirtyTwo",
                    "Foo": "42",
                    "Bar": "baz"
                }
                },
                [10],
                {
                "Error": {
                    "Code": "0x40",
                    "Name": "TestErrorSixtyFour",
                    "Arg0": "99",
                    "Arg1": "33"
                }
                },
                [10]
            ]
            }
        ]
    }
    """
    
    job_results = _get_job_results_shots("microsoft.quantum-results.v2", output)
    assert len(job_results) == 5
    assert job_results[0] == [10]
    assert job_results[1] == {"Error": {"Code": "0x20", "Name": "TestErrorThirtyTwo", "Foo": "42", "Bar": "baz"}}
    assert job_results[2] == [10]
    assert job_results[3] == {"Error": {"Code": "0x40", "Name": "TestErrorSixtyFour", "Arg0": "99", "Arg1": "33"}}
    assert job_results[4] == [10]


def test_job_for_microsoft_quantum_results_histogram_v2_error_in_histogram():
    output = """
    {
        "DataFormat": "microsoft.quantum-results.v2",
        "Results": [
            {
            "Histogram": [
                {
                "Outcome": [10],
                "Display": "[10]",
                "Count": 3
                },
                {
                "Outcome": {
                    "Error": {
                    "Code": "0x20",
                    "Name": "TestErrorThirtyTwo"
                    }
                },
                "Display": "Error 0x20: TestErrorThirtyTwo",
                "Count": 1
                },
                {
                "Outcome": {
                    "Error": {
                    "Code": "0x40",
                    "Name": "TestErrorSixtyFour"
                    }
                },
                "Display": "Error 0x40: TestErrorSixtyFour",
                "Count": 1
                }
            ],
            "Shots": [
                [10],
                {
                "Error": {
                    "Code": "0x20",
                    "Name": "TestErrorThirtyTwo",
                    "Foo": "42",
                    "Bar": "baz"
                }
                },
                [10],
                {
                "Error": {
                    "Code": "0x40",
                    "Name": "TestErrorSixtyFour",
                    "Arg0": "99",
                    "Arg1": "33"
                }
                },
                [10]
            ]
            }
        ]
    }
    """
    
    job_results = _get_job_results_histogram("microsoft.quantum-results.v2", output)
    assert len(job_results.keys()) == 3
    assert job_results["[10]"]["count"] == 3
    assert job_results["Error 0x20: TestErrorThirtyTwo"]["count"] == 1
    assert job_results["Error 0x40: TestErrorSixtyFour"]["count"] == 1
    assert job_results["[10]"]["outcome"] == [10]
    assert job_results["Error 0x20: TestErrorThirtyTwo"]["outcome"] == {"Error": {"Code": "0x20", "Name": "TestErrorThirtyTwo"}}
    assert job_results["Error 0x40: TestErrorSixtyFour"]["outcome"] == {"Error": {"Code": "0x40", "Name": "TestErrorSixtyFour"}}


def test_job_for_microsoft_quantum_results_shots_v2_wrong_type_raises_exception():
    try:
        _get_job_results_shots(
            "microsoft.quantum-results.v2",
            '{"Histogram": ["[0]", 0.50, "[1]", 0.50]}',
        )
        assert False
    except Exception:
        assert True
