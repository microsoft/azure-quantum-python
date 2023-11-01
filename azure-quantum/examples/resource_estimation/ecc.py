##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

# Physical resource estimation for Elliptic Curve Cryptography starting from
# logical resource estimates

import argparse
import os
from azure.quantum import Workspace
from azure.quantum.target.microsoft import MicrosoftEstimator, QubitParams, \
    QECScheme
import qsharp

# Configure program arguments
parser = argparse.ArgumentParser(
    prog="rsa",
    description="Physical resource estimation for Elliptic Curve Cryptography "
                "starting from logical resource estimates")

parser.add_argument(
    "-k",
    "--keysize",
    default=256,
    help="Key size (256, 384, 521)")

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

# define and compile Q# operation
ECCEstimates = qsharp.compile('''
open Microsoft.Quantum.ResourceEstimation;

operation ECCEstimates(keysize: Int) : Unit {
  if keysize == 256 {
    use qubits = Qubit[2124];
    AccountForEstimates([
      TCount(7387343750),          // 1.72 * 2.0^32
      MeasurementCount(118111601)  // 1.76 * 2.0^26
    ], PSSPCLayout(), qubits);
  } elif keysize == 384 {
    use qubits = Qubit[3151];
    AccountForEstimates([
      TCount(25941602468),         // 1.51 * 2.0^34
      MeasurementCount(660351222)  // 1.23 * 2.0^29
    ], PSSPCLayout(), qubits);
  } elif keysize == 521 {
    use qubits = Qubit[4258];
    AccountForEstimates([
      TCount(62534723830),         // 1.82 * 2.0^35
      MeasurementCount(1707249501) // 1.59 * 2.0^30
    ], PSSPCLayout(), qubits);
  } else {
    fail $"keysize {keysize} is not supported";
  }
}
''')

# connect to Azure Quantum workspace (you can find the information for your
# resource_id and location on the Overview page of your Quantum workspace)
workspace = Workspace(resource_id=args.resource_id, location=args.location)
estimator = MicrosoftEstimator(workspace)

params = estimator.make_params(num_items=4)

params.arguments["keysize"] = int(args.keysize)

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

job = estimator.submit(ECCEstimates, input_params=params)
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
