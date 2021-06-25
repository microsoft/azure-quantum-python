import io
import json
from typing import Any, Dict, Tuple

from azure.quantum import Job
from azure.quantum._client.models import JobDetails
from azure.quantum.storage import upload_blob, ContainerClient
from azure.quantum.workspace import Workspace

IonQJson = Dict[str, Any]
IONQ_INPUT_DATA_FORMAT = "ionq.circuit.v1"
IONQ_OUTPUT_DATA_FORMAT = "ionq.quantum-results.v1"
IONQ_PROVIDER_ID = "IonQ"
DEFAULT_TIMEOUT = 100


class IonQ:
    def __init__(self, workspace: Workspace, target: str = "ionq.simulator"):
        self.workspace = workspace
        self.target = target
    
    def submit(
        self,
        circuit: IonQJson,
        name: str = None,
        timeout: int = DEFAULT_TIMEOUT
    ) -> Job:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format
        :type circuit: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        if name is None:
            n_qubits = circuit["qubits"]
            n_gates = len(circuit["circuit"])
            name = f"ionq_{n_qubits}_qubits_{n_gates}_gates"
        job_id = Job.create_job_id()
        data = self.encode_data(circuit)
        container_uri, uploaded_blob_uri = self.upload_blob(data)
        details = JobDetails(
            id=job_id,
            name=name,
            container_uri=container_uri,
            input_data_format=IONQ_INPUT_DATA_FORMAT,
            output_data_format=IONQ_OUTPUT_DATA_FORMAT,
            input_data_uri=uploaded_blob_uri,
            provider_id=IONQ_PROVIDER_ID,
            target=self.target,
            input_params={'params': {'timeout': timeout}},
        )
        job = Job(self.workspace, details)
        job = self.workspace.submit_job(job)
        return job

    def encode_data(circuit: IonQJson) -> bytes:
        data = io.BytesIO()
        circuit = json.dumps(circuit)
        data.write(circuit.encode())
        return data.getvalue()

    def upload_blob(
        self,
        data: bytes,
        job_id: str,
        blob_name = "inputData",
        content_type = "application/json",
        encoding = ""
    ) -> Tuple[str, str]:
        container_name = f"job-{job_id}"
        container_uri = self.workspace._get_linked_storage_sas_uri(container_name)
        container_client = ContainerClient.from_container_url(container_uri)
        uploaded_blob_uri = upload_blob(container_client, blob_name, content_type, encoding, data, return_sas_token=False)
        return container_uri, uploaded_blob_uri
