##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import warnings
warnings.warn("Please note that Microsoft QIO solvers will be deprecated and \
no longer available in Azure Quantum after June 30th 2023.")

from .parallel_tempering import ParallelTempering
from .population_annealing import PopulationAnnealing
from .quantum_monte_carlo import QuantumMonteCarlo
from .simulated_annealing import SimulatedAnnealing
from .substochastic_montecarlo import SubstochasticMonteCarlo
from .tabu import Tabu
