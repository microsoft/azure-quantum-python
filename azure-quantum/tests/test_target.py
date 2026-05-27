##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import copy
from unittest import mock
from azure.quantum.target.target import Target

from mock_client import WorkspaceMock
from common import (
    SUBSCRIPTION_ID,
    RESOURCE_GROUP,
    WORKSPACE,
)

def test_target_submit_does_not_mutate_input_params():
    ws = WorkspaceMock(
        subscription_id=SUBSCRIPTION_ID,
        resource_group=RESOURCE_GROUP,
        name=WORKSPACE,
    )
    target = Target(
        workspace=ws,
        name="fake.target",
        provider_id="fake-provider",
        input_data_format="fake-input-format",
        output_data_format="fake-output-format",
    )
    input_params = {
        "someOption": "someValue",
        "nested": {
            "innerOption": "innerValue",
            "list": [1, 2, 3],
        },
    }
    original = copy.deepcopy(input_params)

    with mock.patch(
        "azure.quantum.job.base_job.BaseJob.upload_input_data",
        return_value="https://example.com/blob",
    ):
        target.submit(
            name="test-job",
            shots=10,
            input_data=b"fake-ir",
            input_params=input_params,
        )

    assert input_params == original
    assert "shots" not in input_params
    assert input_params["nested"]["innerOption"] == "innerValue"
    assert input_params["nested"]["list"] == [1, 2, 3]
