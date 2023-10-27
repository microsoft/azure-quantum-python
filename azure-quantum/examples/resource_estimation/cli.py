##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

# A resource estimation CLI that can execute resource estimation jobs from
# various input formats and generate JSON output.

import argparse
import json
import os
import sys
from azure.quantum import Workspace
from azure.quantum.target.microsoft import MicrosoftEstimator

# Configure program arguments
parser = argparse.ArgumentParser(
    prog="estimate",
    description="Estimate physical resources using Azure Quantum")

parser.add_argument(
    "filename",
    help="Quantum program (.ll, .qir, .bc, .qs, .qasm)")

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

parser.add_argument(
    "-p",
    "--job-params",
    help="JSON file with job parameters")

parser.add_argument(
    "-o",
    "--output",
    help="Output file (default: stdout)"
)

# Parse and validate arguments
args = parser.parse_args()

if not args.resource_id:
    parser.error("the following arguments are required: -r/--resource-id")
if not args.location:
    parser.error("the following arguments are required: -l/--location")

# Set up Azure Quantum workspace
workspace = Workspace(resource_id=args.resource_id, location=args.location)
estimator = MicrosoftEstimator(workspace)

# Prepare program input based on file extension
extension = os.path.splitext(args.filename)[1]
if extension == ".ll":
    # LLVM IR
    try:
        import pyqir
        ir_code = open(args.filename, "r").read()
        context = pyqir.Context()
        module = pyqir.Module.from_ir(context, ir_code)
        input_data = module.bitcode
    except ImportError:
        raise ImportError("PyQIR is not installed. Please install the pyqir "
                          "package to use this feature.")
elif extension == ".qir" or extension == ".bc":
    # QIR or LLVM bitcode
    input_data = open(args.filename, "rb").read()
elif extension == ".qs":
    # Q#
    try:
        import qsharp
        qsharp.packages.add("Microsoft.Quantum.Numerics")
        qsharp_code = open(args.filename, "r").read()
        input_data = qsharp.compile(qsharp_code)
    except ImportError:
        raise ImportError("Q# is not installed. Please install the qsharp "
                          "package to use this feature.")
elif extension == ".qasm":
    # OpenQASM
    try:
        from qiskit import QuantumCircuit
        qasm_code = open(args.filename, "r").read()
        input_data = QuantumCircuit.from_qasm_str(qasm_code)
    except ImportError:
        raise ImportError("Qiskit is not installed. Please install the qiskit "
                          "package to use this feature.")

else:
    raise ValueError(f"Unknown file extension {extension}")

# Parse job arguments
input_params = {}
if args.job_params:
    with open(args.job_params, 'r') as f:
        input_params = json.load(f)

# Submit job
job = estimator.submit(input_data, input_params=input_params)

# Get results
try:
    results = job.get_results()
except RuntimeError as e:
    print()
    print(e, file=sys.stderr)
    exit(1)

# Write results to output file
if args.output:
    with open(args.output, 'w') as f:
        f.write(results.json)
else:
    print(results.json)
