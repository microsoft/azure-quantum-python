
from azure.quantum import Workspace, Job
from azure.quantum.target import Target

import io
import gzip

class PassThroughTarget(Target):
    """
    Basic target that submits a raw byte-array to an Azure Quantum target.
    All job parameters, including input_data_format, target_id, provider, etc
    Need to be explicitly specified during init...
    """
    @staticmethod
    def _encode_input_data(data: io.BytesIO) -> bytes:
        # Bug #: For now, it is required that content is in gzip.
        compressed = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed, mode="w") as fo:
            fo.write(data.readall())
        return compressed.getvalue()

    def submit(self, stream: io.BytesIO, name: str, **kwargs) -> Job:
        return super().submit(
            input_data=stream,
            name=name,
            encoding="gzip",
            **kwargs
        )

workspace = Workspace(
    resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo-sim",
    location="westus2"
)

print("Using workspace", workspace.name)

# Bug #2: simulator is not listed in get_targets()...
# Verify simulator is a valid target in this workspace:
# targets =  [e.name for e in workspace.get_targets()]
# print(targets)
# if not "microsoft.simulator.fullstate" in targets:
#     print("Workspace is missing full-state simulator")
#     exit(1)

# Create pass-through target:
target = PassThroughTarget(
    workspace= workspace,
    name= "microsoft.simulator.fullstate",
    input_data_format = "qir.v1/full-profile",
    # For now, the output format returned by the simulator is "microsoft.qio-results.v2"
    output_data_format = "microsoft.qio-results.v2",
    provider_id = "Microsoft.Simulator",
    content_type = "qir.v1/full-profile",
    encoding = ""
)

# Open the QIR file and submit it. The only thing required is the entryPoint.
f = open("qir/union.ll", "rb", buffering=0)
job = target.submit(f, "union__HelloQ.ll", input_params={ "entryPoint": "union__HelloQ" })

# Print job, wait for results:
print(job.id)
job.wait_until_completed()

# Download and print results:
results = job.download_data(job.details.output_data_uri).decode()
print("-------------------------------------------------------------------------")
print(results)

