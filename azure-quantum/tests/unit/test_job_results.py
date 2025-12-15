##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import re
import unittest
import pytest
from common import QuantumTestBase, RegexScrubbingPatterns


class TestJobResults(QuantumTestBase):
    """TestJob

    Tests the azure.quantum.job module.
    """

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
            string=job.details.output_data_uri,
        )

        job_results = job.get_results()
        self.assertEqual(job_results, input_data)


if __name__ == "__main__":
    unittest.main()
