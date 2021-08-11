##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from azure.quantum import Workspace
from azure.quantum.target import IonQ


# Enter your workspace details here
# Find your resource ID via portal.azure.com
workspace = Workspace(
    resource_id="",
    location=""
)

# Create raw JSON circuit.
circuit = {
    "qubits": 3,
    "circuit": [
        {
        "gate": "h",
        "target": 0
        },
        {
        "gate": "cnot",
        "control": 0,
        "target": 1
        },
        {
        "gate": "cnot",
        "control": 0,
        "target": 2
        },
    ]
}

# Create the IonQ target and submit the circuit.
# We need the resulting Job object to get retrieve results.
target = IonQ(workspace=workspace, target="ionq.simulator")
job = target.submit(circuit)

# Print job ID.
print(f"Job ID: {job.id}")

# Get results. This method queries the service periodically
# to get the job status and waits until the job is done.
results = job.get_results()

# Plot the results (this requires matplotlib)
import pylab as pl
pl.rcParams["font.size"] = 16
hist = {format(n, "03b"): 0 for n in range(8)}
hist.update({format(int(k), "03b"): v for k, v in results["histogram"].items()})
pl.bar(hist.keys(), hist.values())
pl.ylabel("Probabilities")
