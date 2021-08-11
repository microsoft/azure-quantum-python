##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from azure.quantum import Workspace
from azure.quantum.target import Honeywell


# Enter your workspace details here
# Find your resource ID via portal.azure.com
workspace = Workspace(
    resource_id="",
    location=""
)

# Create raw OpenQASM circuit. 
circuit = """OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c0[1];
creg c1[3];

h q[0];
cx q[0], q[1];
x q[2];
h q[2];
cx q[2], q[0];
h q[2];
measure q[0] -> c1[0];
c0[0] = c1[0];
if (c0==1) x q[1];
c0[0] = 0;
measure q[2] -> c1[1];
c0[0] = c1[1];
if (c0==1) z q[1];
c0[0] = 0;
h q[1];
measure q[1] -> c1[2];
"""

# Create the Honeywell target and submit the circuit.
# We need the resulting Job object to retrieve results.
target = Honeywell(workspace=workspace, target="honeywell.hqs-lt-s1-sim")
job = target.submit(circuit)

# Print job ID.
print(f"Job ID: {job.id}")

# Get results. This method queries the service periodically
# to get the job status and waits until the job is done.
results = job.get_results()
