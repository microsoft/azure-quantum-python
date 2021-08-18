##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from azure.quantum.target import Target

def get_all_targets() -> Dict[str, "Target"]:
    """Get all target classes by provider ID"""
    from azure.quantum.target import IonQ, Honeywell
    from azure.quantum.target.microsoft import MicrosoftOptimization

    return {
        "ionq": IonQ,
        "honeywell": Honeywell,
        "Microsoft": MicrosoftOptimization
    }
