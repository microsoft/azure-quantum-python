from azure.quantum import Workspace
from azure.quantum.job import JobFailedWithResultsError
from pathlib import Path
import json

workspace = Workspace(
    resource_id = "/subscriptions/677fc922-91d0-4bf6-9b06-4274d319a0fa/resourceGroups/AzureQuantum/providers/Microsoft.Quantum/Workspaces/Ashwin-Dft-Demo-Canary-2",
    location = "eastus2euap")

# For example-
# workspace = Workspace(
#     resource_id = "/subscriptions/677fc922-91d0-4bf6-9b06-4274d319a0fa/resourceGroups/ashwinm-dft-rg/providers/Microsoft.Quantum/Workspaces/ashwinm-dft-canary-01",
#     location = "eastus2euap")

print("Verifying access to DFT target.")

# To submit DFT jobs, we will be using the microsoft.dft target in the workspace.
target = workspace.get_targets("microsoft.dft")

# Next, we create a dictionary variable to specify the parameters for the DFT calculation. 
dft_input_params = {"tasks":[{"taskType":"spe","basisSet":{"name":"def2-svp","cartesian":False},"xcFunctional":{"name":"m06-2x","gridLevel":4},"scf":{"method":"rks","maxSteps":100,"convergeThreshold":1e-8}}]}

# We are now ready to submit the Job using the target.submit call. It takes three parameters-
# 1. The input molecule in xyz format.
# 2. The DFT parameters that we declared above.
# 3. A friendly name to help identify the job in the Azure Portal later.

print("Submitting DFT job.")
results = None
try:
    job = target.submit(
        input_data=Path('/workspaces/azure-quantum-python/samples/dft/molecules/water2.xyz').read_text(),
        input_params=dft_input_params,
        name="water2-spe")    
    print(f"Submitted job with id {job.id}.")
    job.wait_until_completed()
    results = job.get_results()
except JobFailedWithResultsError as e:
    results = e.get_failure_results()

print("\nDFT job has completed.")

# Let's dump the results to the dftOutput.json file
outputFile = open("dftOutput.json", "w")
outputFile.write(json.dumps(results, indent=4))
outputFile.close()

# We could also just print the final energy.
print(results["results"][0]["return_result"])

# Let's dump the logs to the dftLog.txt file
logFile = open("dftLog.txt", "wb")
logFile.write(job.download_attachment("log.txt"))
logFile.close()