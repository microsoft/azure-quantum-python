##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

# Physical resource estimation for RSA using a pre-compiled QIR code

import argparse
import os
from azure.quantum import Workspace
from azure.quantum.target.microsoft import MicrosoftEstimator, QubitParams, \
    QECScheme

# Configure program arguments
parser = argparse.ArgumentParser(
    prog="rsa",
    description="Physical resource estimation for RSA using a pre-compiled "
                "QIR code")

parser.add_argument(
    "-r",
    "--resource-id",
    default=os.environ.get("AZURE_QUANTUM_RESOURCE_ID"),
    help="Resource ID of Azure Quantum workspace (must be set, unless set via "
         "environment variable AZURE_QUANTUM_RESOURCE_ID)")

parser.add_argument(
    "-l",
    "--location",
    default=os.environ.get("AZURE_QUANTUM_LOCATION"),
    help="Location of Azure Quantum workspace (must be set, unless set via "
         "environment AZURE_QUANTUM_LOCATION)")

# Parse and validate arguments
args = parser.parse_args()

if not args.resource_id:
    parser.error("the following arguments are required: -r/--resource-id")
if not args.location:
    parser.error("the following arguments are required: -l/--location")

# download QIR bitcode

import urllib.request
bitcode = urllib.request.urlopen("https://aka.ms/RE/eh_factoring").read()

# connect to Azure Quantum workspace (you can find the information for your
# resource_id and location on the Overview page of your Quantum workspace)
workspace = Workspace(resource_id=args.resource_id, location=args.location)
estimator = MicrosoftEstimator(workspace)

params = estimator.make_params(num_items=4)

params.arguments["product"] = "25195908475657893494027183240048398571429282126204032027777137836043662020707595556264018525880784406918290641249515082189298559149176184502808489120072844992687392807287776735971418347270261896375014971824691165077613379859095700097330459748808428401797429100642458691817195118746121515172654632282216869987549182422433637259085141865462043576798423387184774447920739934236584823824281198163815010674810451660377306056201619676256133844143603833904414952634432190114657544454178424020924616515723350778707749817125772467962926386356373289912154831438167899885040445364023527381951378636564391212010397122822120720357"
params.arguments["generator"] = 7
params.arguments["exp_window_len"] = 5
params.arguments["mul_window_len"] = 5

# Error budget
params.error_budget = 0.333

# Gate-based (reasonable)
params.items[0].qubit_params.name = QubitParams.GATE_NS_E3
# Gate-based (optimistic)
params.items[1].qubit_params.name = QubitParams.GATE_NS_E4
# Majorana (reasonable)
params.items[2].qubit_params.name = QubitParams.MAJ_NS_E4
params.items[2].qec_scheme.name = QECScheme.FLOQUET_CODE
# Majorana (optimistic)
params.items[3].qubit_params.name = QubitParams.MAJ_NS_E6
params.items[3].qec_scheme.name = QECScheme.FLOQUET_CODE

job = estimator.submit(bitcode, input_params=params)
results = job.get_results()

table = results.summary_data_frame(labels=[
    "Gate-based (reasonable)",
    "Gate-based (optimistic)",
    "Majorana (reasonable)",
    "Majorana (optimistic)"
])

print()
print(table[["Physical qubits", "Physical runtime"]])

## Access non-formatted values, e.g.,
# print(results[0]["physicalCounts"]["physicalQubits"])
# print(results[0]["physicalCounts"]["runtime"])
