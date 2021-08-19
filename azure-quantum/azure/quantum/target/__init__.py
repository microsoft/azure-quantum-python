from azure.quantum.target.target import Target
from azure.quantum.target.ionq import IonQ
from azure.quantum.target.honeywell import Honeywell
from azure.quantum.target.optimization import (
    Solver,
    ParallelTempering,
    SimulatedAnnealing,
    Tabu,
    QuantumMonteCarlo,
    PopulationAnnealing,
    SubstochasticMonteCarlo,
)
from azure.quantum.target.optimization.oneqbit import (
    TabuSearch,
    PticmSolver,
    PathRelinkingSolver,
)
from azure.quantum.target.optimization.toshiba import (
    SimulatedBifurcationMachine
)

# Default targets to use when there is no associated target class
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "honeywell": Honeywell,
    "Microsoft": Solver
}
