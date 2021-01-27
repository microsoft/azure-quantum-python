#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_job.py: Checks correctness of azure.quantum.job module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

## IMPORTS ##

import unittest
import json
import uuid
import os

from azure.quantum import Workspace
from azure.quantum.optimization import Problem
from azure.quantum.optimization.solvers import SimulatedAnnealing
from azure.quantum import Job
from azure_devtools.scenario_tests.base import ReplayableTest

from workspace_init import create_workspace, create_workspace_mock_login
from recording_updater import RecordingUpdater

class TestJob(ReplayableTest):
    """TestJob

    Tests the azure.quantum.job module.

    The 'recordings' directory is used to replay network connections.
    To manully create new recordings, remove the 'recordings' subdirectory and run the tests twice.
        Once to generate the recordings using valid credentials.
        A second time to update the recordings with dummy values and validate the updated recordings work.

    Additionally, a temporary 'config.ini' file will be required in the 'azure-quantum' directory for the first run of the tests.
    Create the 'config.ini' with the following contents using valid values:
    [azure.quantum]
    subscription_id=<id>
    resource_group=<rg>
    workspace_name=<ws>
    1qbit_enabled=false
    """
    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_dummy_job_id(self):
        if self.in_recording:
            # This is live, so return a real job id.
            return TestJob.create_job_id()
        # This is a replay, so return the dummy job id that will be in the updated recordings.
        return RecordingUpdater.dummy_uid
        
    def create_workspace(self):
        if self.in_recording:
            ws = create_workspace()
        else:
            ws = create_workspace_mock_login(
                subscription_id=RecordingUpdater.dummy_uid,
                resource_group=RecordingUpdater.dummy_rg,
                name=RecordingUpdater.dummy_ws)
        return ws

    def test_job_refresh(self):
        ws = self.create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        with unittest.mock.patch.object(Job, self.mock_create_job_id_name, return_value=self.get_dummy_job_id()):
            solver = SimulatedAnnealing(ws)
            job = solver.submit(problem)
            job.refresh()

    def test_job_get_results(self):
        ws = self.create_workspace()

        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])

        with unittest.mock.patch.object(Job, self.mock_create_job_id_name, return_value=self.get_dummy_job_id()):
            solver = SimulatedAnnealing(ws)
            job = solver.submit(problem)
            actual = job.get_results()

        expected = {
            'version': '1.0',
            'configuration': {'0': 1, '1': 1, '2': -1, '3': 1, '4': -1},
            'cost': -6.0,
            'parameters': {'beta_start': 0.2, 'beta_stop': 1.9307236000000003, 'restarts': 360, 'sweeps': 50}}

        self.assertEqual(expected, actual)
        

def update_recordings_with_dummy_values():
    """Replace all secrets in the recorded .yaml files with dummy values as defined in RecordingUpdater. This only needs to be run once."""
    recording_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "recordings"))
    recording_glob = "*.yaml"
    if os.path.exists(recording_directory):    
        recording_updater = RecordingUpdater(recording_directory, recording_glob)
        recording_updater.update_recordings_with_dummy_values()


if __name__ == "__main__":
    update_recordings_with_dummy_values()
    unittest.main()
