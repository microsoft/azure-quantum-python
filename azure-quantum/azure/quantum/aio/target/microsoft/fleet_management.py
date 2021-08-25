##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from azure.quantum.aio.target.solvers import Solver
from azure.quantum.target.microsoft.fleet_management import FleetManagement as SyncFleetManagement


class FleetManagement(Solver, SyncFleetManagement):
    pass
