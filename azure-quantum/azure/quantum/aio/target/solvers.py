##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import TYPE_CHECKING, Union
from azure.quantum.aio import Workspace, Job
from azure.quantum.aio.target.target import Target
from azure.quantum.target.solvers import Solver as SyncSolver
from azure.quantum.aio.job.base_job import DEFAULT_TIMEOUT

if TYPE_CHECKING:
    from azure.quantum.aio.optimization.problem import Problem

logger = logging.getLogger(__name__)

__all__ = [
    "HardwarePlatform",
    "RangeSchedule",
    "Solver",
]


class Solver(Target, SyncSolver):

    workspace: Workspace

    async def submit(
        self, problem: Union[str, "Problem"], compress: bool = True
    ) -> Job:
        """Submits a job to execution to the associated
        Azure Quantum Workspace.

        :param problem:
            The Problem to solve. It can be an instance of a Problem,
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        :param compress:
            Whether or not to compress the problem when uploading it
            the Blob Storage.
        """
        from azure.quantum.aio.optimization.problem import Problem
        if isinstance(problem, Problem):
            # Create job from input data
            name = problem.name
            blob = problem.to_blob(compress=compress)
            job = await Job.from_input_data(
                workspace=self.workspace,
                name=name,
                target=self.name,
                input_data=blob,
                blob_name="inputData",
                content_type="application/json",
                provider_id=self.provider_id,
                input_data_format=self.input_data_format,
                output_data_format=self.output_data_format,
                input_params=self.params,
            )
        
        else:
            if hasattr(problem, "uploaded_blob_uri"):
                name = problem.name
                problem_uri = problem.uploaded_blob_uri

            elif isinstance(problem, str):
                name = "Optimization problem"
                problem_uri = problem
            
            else:
                raise ValueError("Cannot submit problem: should be of type str, Problem or have uploaded_blob_uri attribute.")

            # Create job from storage URI
            job = await Job.from_storage_uri(
                workspace=self.workspace,
                name=name,
                target=self.name,
                input_data_uri=problem_uri,
                provider_id=self.provider_id,
                input_data_format=self.input_data_format,
                output_data_format=self.output_data_format,
                input_params=self.params
            )

        return job

    async def optimize(self, problem: Union[str, "Problem"], timeout_secs: int=DEFAULT_TIMEOUT):
        """[Submits the Problem to the associated
            Azure Quantum Workspace and get the results.

        :param problem:
            The Problem to solve. It can be an instance of a Problem,
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        :type problem: Union[str, Problem]
        :param timeout_secs: Timeout in seconds, defaults to 300
        :type timeout_secs: int
        :return: Job results
        :rtype: dict
        """
        if not isinstance(problem, str):
            self.check_submission_warnings(problem)

        job = await self.submit(problem)
        logger.info(f"Submitted job: '{job.id}'")

        return await job.get_results(timeout_secs=timeout_secs)
