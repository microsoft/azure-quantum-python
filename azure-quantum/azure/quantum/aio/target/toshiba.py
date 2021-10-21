from azure.quantum.aio.target.solvers import Solver
from azure.quantum.target.toshiba import SimulatedBifurcationMachine as SyncSimulatedBifurcationMachine


class SimulatedBifurcationMachine(SyncSimulatedBifurcationMachine, Solver):
    pass
