#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_microsoft_qc.py: Tests for microsoft-qc provider.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest
from os import path

from common import QuantumTestBase

from azure.quantum.target.microsoft import MicrosoftEstimatorJob

class TestMicrosoftQC(QuantumTestBase):
    """TestMicrosoftQC
    
    Tests the azure.quantum.target.microsoft module.
    """

    def _ccnot_bitcode(self) -> bytes:
        """
        QIR sample file for CCNOT gate applied to 3 qubits.
        """
        bitcode_filename = path.join(path.dirname(__file__), "qir", "ccnot.bc")
        with open(bitcode_filename, "rb") as f:
            return f.read()

    @pytest.mark.microsoft_qc
    @pytest.mark.live_test
    def test_estimator_non_batching_job(self):
        """
        Submits a job default job parameters.

        Checks whether job and results have expected type.
        """
        ws = self.create_workspace()
        estimator = ws.get_targets("microsoft.estimator")

        ccnot = self._ccnot_bitcode()
        job = estimator.submit(ccnot)
        assert type(job) == MicrosoftEstimatorJob

        job.wait_until_completed()
        result = job.get_results()

        assert type(result) == dict
