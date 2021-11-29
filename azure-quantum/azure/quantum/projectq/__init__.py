"""Azure Quantum ProjectQ Provider"""

from azure.quantum.projectq.engine import AzureQuantumEngine
from azure.quantum import __version__

__all__ = [
    "AzureQuantumEngine",
    "__version__"
]
