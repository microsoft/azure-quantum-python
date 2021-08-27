# coding=utf-8
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import warnings
warnings.warn("The azure.quantum.optimization.solvers namespace will be deprecated. \
Please use azure.quantum.target instead.")

from azure.quantum.target.solvers import Solver
from azure.quantum.target.microsoft.qio import (
    ParallelTempering,
    SimulatedAnnealing,
    Tabu,
    QuantumMonteCarlo,
    PopulationAnnealing,
    SubstochasticMonteCarlo,
)
