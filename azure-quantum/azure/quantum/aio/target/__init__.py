from azure.quantum.aio.target.ionq import IonQ
from azure.quantum.aio.target.honeywell import Honeywell
from azure.quantum.aio.target.target import Target
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
from .microsoft import FleetManagement
from .ionq import IonQ
from .honeywell import Honeywell

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "honeywell": Honeywell,
    "Microsoft": Solver,
    "toshiba": Solver,
    "1qbit": Solver,
}
