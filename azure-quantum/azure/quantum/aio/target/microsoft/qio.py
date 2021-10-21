##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from azure.quantum.aio.target.solvers import Solver
from azure.quantum.target.microsoft.qio import ParallelTempering as SyncParallelTempering
from azure.quantum.target.microsoft.qio import SimulatedAnnealing as SyncSimulatedAnnealing
from azure.quantum.target.microsoft.qio import Tabu as SyncTabu
from azure.quantum.target.microsoft.qio import QuantumMonteCarlo as SyncQuantumMonteCarlo
from azure.quantum.target.microsoft.qio import PopulationAnnealing as SyncPopulationAnnealing
from azure.quantum.target.microsoft.qio import SubstochasticMonteCarlo as SyncSubstochasticMonteCarlo


class ParallelTempering(Solver, SyncParallelTempering):
    pass


class SimulatedAnnealing(Solver, SyncSimulatedAnnealing):
    pass


class Tabu(Solver, SyncTabu):
    pass


class QuantumMonteCarlo(Solver, SyncQuantumMonteCarlo):
    pass


class PopulationAnnealing(Solver, SyncPopulationAnnealing):
    pass


class SubstochasticMonteCarlo(Solver, SyncSubstochasticMonteCarlo):
    pass
