from azure.quantum.target.ionq import IonQ
from azure.quantum.target.honeywell import Honeywell
from azure.quantum.target.target import Target
from azure.quantum.optimization import MicrosoftOptimization

ALL_TARGETS = {
    "ionq": IonQ,
    "honeywell": Honeywell,
    "Microsoft": MicrosoftOptimization
}
