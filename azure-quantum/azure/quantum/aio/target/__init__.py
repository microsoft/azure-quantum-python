##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from azure.quantum.aio.target.target import Target
from azure.quantum.aio.target.solvers import Solver
from .microsoft.qio import (
    ParallelTempering,
    SimulatedAnnealing,
    Tabu,
    QuantumMonteCarlo,
    PopulationAnnealing,
    SubstochasticMonteCarlo,
)
from .oneqbit import (
    TabuSearch,
    PticmSolver,
    PathRelinkingSolver,
)
from .toshiba import (
    SimulatedBifurcationMachine
)
from .ionq import IonQ
from .quantinuum import Quantinuum

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "quantinuum": Quantinuum,
    "Microsoft": Solver,
    "toshiba": Solver,
    "1qbit": Solver,
}
