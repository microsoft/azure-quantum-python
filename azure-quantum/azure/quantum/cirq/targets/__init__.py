##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from azure.quantum.cirq.targets.target import Target
from azure.quantum.cirq.targets.honeywell import HoneywellTarget
from azure.quantum.cirq.targets.ionq import IonQTarget

__all__ = ["Target", "HoneywellTarget", "IonQTarget"]

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQTarget,
    "honeywell": HoneywellTarget,
}
