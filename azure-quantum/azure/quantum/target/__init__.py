from .target import Target
from .quantum_computing.ionq import IonQ
from .quantum_computing.honeywell import Honeywell
from .optimization import Solver
from .optimization.microsoft import (
    ParallelTempering,
    SimulatedAnnealing,
    Tabu,
    QuantumMonteCarlo,
    PopulationAnnealing,
    SubstochasticMonteCarlo,
)
from .optimization.oneqbit import (
    TabuSearch,
    PticmSolver,
    PathRelinkingSolver,
)
from .optimization.toshiba import (
    SimulatedBifurcationMachine
)

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "honeywell": Honeywell,
    "Microsoft": Solver
}
