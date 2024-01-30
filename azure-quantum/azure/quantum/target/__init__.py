##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from .target import Target
from .ionq import IonQ
from .quantinuum import Quantinuum
from .rigetti import Rigetti
from .pasqal import Pasqal
from .microsoft.elements.dft import MicrosoftElementsDft, MicrosoftElementsDftJob

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQ,
    "quantinuum": Quantinuum,
    "rigetti": Rigetti,
    "pasqal": Pasqal
}
