import os
from azure.quantum import Workspace
from azure.quantum.target.microsoft.simulator.fullstate import FullStateSimulator


workspace = Workspace(
    subscription_id=os.environ["AZURE_QUANTUM_SUBSCRIPTION_ID"],
    resource_group=os.environ["AZURE_QUANTUM_WORKSPACE_RG"],
    name=os.environ["AZURE_QUANTUM_WORKSPACE_NAME"],
    location=os.environ["AZURE_QUANTUM_WORKSPACE_LOCATION"]
)

print("Using workspace", workspace.name)

target: FullStateSimulator = workspace.get_targets("microsoft.simulator.fullstate")
job = target.submit_qir_file("qir/Sample.ll", "HelloQ", entrypoint="Sample__HelloQ")

# Print job, wait for results:
print(job.id)
job.wait_until_completed()

# Download and print results:
results = job.download_data(job.details.output_data_uri).decode()
print("-------------------------------------------------------------------------")
print(results)
