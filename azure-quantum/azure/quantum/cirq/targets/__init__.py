##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

"""Defines set of Cirq targets for interacting with Azure Quantum"""

from azure.quantum.cirq.targets.target import Target
from azure.quantum.cirq.targets.quantinuum import QuantinuumTarget
from azure.quantum.cirq.targets.ionq import IonQTarget
from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

__all__ = [
    "Target",
    "QuantinuumTarget",
    "IonQTarget",
    "AzureGenericQirCirqTarget",
]

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {
    "ionq": IonQTarget,
    "quantinuum": QuantinuumTarget,
}
