##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

"""Azure Quantum Qiskit Provider"""

from azure.quantum import __version__
from azure.quantum.qiskit.provider import AzureQuantumProvider

__all__ = [
    "AzureQuantumProvider",
    "__version__"
]
