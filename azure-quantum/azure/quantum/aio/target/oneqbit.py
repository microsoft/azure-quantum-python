from azure.quantum.target.oneqbit import (
    TabuSearch as SyncTabuSearch,
    PticmSolver as SyncPticmSolver,
    PathRelinkingSolver as SyncPathRelinkingSolver,
)
from azure.quantum.target.solvers import Solver


class TabuSearch(SyncTabuSearch, Solver):
    pass


class PticmSolver(SyncPticmSolver, Solver):
    pass


class PathRelinkingSolver(SyncPathRelinkingSolver, Solver):
    pass
