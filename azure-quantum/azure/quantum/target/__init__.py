##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from .target import Target
from .solvers import Solver
from .toshiba import (
    SimulatedBifurcationMachine
)
from .ionq import IonQ
from .quantinuum import Quantinuum
from .rigetti import Rigetti
from .pasqal import Pasqal

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "quantinuum": Quantinuum,
    "rigetti": Rigetti,
    "toshiba": Solver,
    "pasqal": Pasqal
}


__all__ = [
    "Target",
    "IonQ",
    "Quantinuum",
    "Rigetti",
    "Pasqal",
    "DEFAULT_TARGETS"
    ]