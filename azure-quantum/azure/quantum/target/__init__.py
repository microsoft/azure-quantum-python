##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from azure.quantum.target.quantinuum import Quantinuum
from .target import Target
from .solvers import Solver
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
from .honeywell import Honeywell
from .quantinuum import Quantinuum

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "honeywell": Honeywell,
    "quantinuum": Quantinuum,
    "Microsoft": Solver,
    "toshiba": Solver,
    "1qbit": Solver,
}
