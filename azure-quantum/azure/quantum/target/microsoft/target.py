##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Type
from ...job import Job
from ...job.base_job import ContentType
from ...workspace import Workspace
from ..target import Target
from . import MicrosoftEstimatorJob


class MicrosoftEstimator(Target):
    """
    Resource estimator target from the microsoft-qc provider.
    """

    target_names = [
        "microsoft.estimator"
    ]

    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.estimator",
        **kwargs
    ):
        # There is only a single target name for this target
        assert name == self.target_names[0]

        # make sure to not pass argument twice
        kwargs.pop("provider_id", None)

        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format="qir.v1",
            output_data_format="microsoft.resource-estimates.v1",
            provider_id="microsoft-qc",
            content_type=ContentType.json,
            **kwargs
        )

    @classmethod
    def _get_job_class(cls) -> Type[Job]:
        return MicrosoftEstimatorJob