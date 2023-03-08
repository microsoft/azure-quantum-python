#!/bin/env python
# -*- coding: utf-8 -*-
##
# resource_estimator.py: Qiskit result for microsoft.estimator target.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from azure.quantum.target.microsoft.result import MicrosoftEstimatorResult


class ResourceEstimatorResult(MicrosoftEstimatorResult):
    """
    A customized result for a resource estimation job.
    """

    def __init__(
        self,
        data
    ) -> None:
        super().__init__(data)

    @classmethod
    def from_dict(cls, data):
        if not data["success"]:
            error_data = data["error_data"]
            message = "Cannot retrieve results as job execution failed " \
                      f"({error_data['code']}: {error_data['message']})"

            raise RuntimeError(message)

        results = data["results"]
        if len(results) == 1:
            data = results[0]['data']
            return ResourceEstimatorResult(data)
        else:
            raise ValueError("Expected Qiskit results for RE be of length 1")
