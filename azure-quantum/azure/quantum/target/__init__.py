##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
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
from .rigetti import Rigetti

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "honeywell": Honeywell,
    "quantinuum": Quantinuum,
    "rigetti": Rigetti,
    "Microsoft": Solver,
    "toshiba": Solver,
    "1qbit": Solver,
}
