##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import gzip
import io

from typing import Dict, Any, TYPE_CHECKING
from azure.quantum.target.target import Target

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace
    from azure.quantum.job import Job


class FullStateTarget(Target):
    """
    Submit a QIR program to the full state simulator target.

    Known bugs:
    
    # Bug https://ms-quantum.visualstudio.com/Quantum%20Program/_workitems/edit/37094:
    # For now, the output format returned by the simulator is "microsoft.qio-results.v2"

    # Bug https://ms-quantum.visualstudio.com/Quantum%20Program/_workitems/edit/37095:
    # Job fails with Exception if output format doesn't match job's output format.

    # Bug https://ms-quantum.visualstudio.com/Quantum%20Program/_workitems/edit/37096:
    # Controller/QIR errors are not getting propagated and all we get is "InternalError"
    """
    target_names = (
        "microsoft.simulator.fullstate",
    )
    def __init__(
        self,
        workspace: "Workspace",
        name= "microsoft.simulator.fullstate",
        input_data_format = "qir.v1/full-profile",
        output_data_format = "microsoft.qio-results.v2",
        provider_id = "Microsoft.Simulator",
        content_type = "qir.v1/full-profile",
        encoding = "gzip",
        **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding,
            **kwargs
        )

    @staticmethod
    def _encode_input_data(data: bytes) -> bytes:
        # Bug https://ms-quantum.visualstudio.com/Quantum%20Program/_workitems/edit/37092:
        # For now, it is required that content is in gzip.
        compressed = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed, mode="w") as fo:
            fo.write(data)
        return compressed.getvalue()

    def submit_qir_file(
        self,
        file_path: str,
        name: str,
        entrypoint: str,
        **kwargs
    ) -> "Job":
        """Submit QIR from file and return Job.

        Provide input_data_format, output_data_format and content_type
        keyword arguments to override default values.

        :param file_path: QIR input file
        :type file_path: str
        :param name: Job name
        :type name: str
        :param entrypoint: Entrypoint name
        :type entrypoint: str
        :return: Azure Quantum job
        :rtype: Job
        """
        with open(file_path, "rb", buffering=0) as f:
            return super().submit(
                input_data=f.readall(),
                name=name,
                input_params={ "entryPoint": entrypoint },
                **kwargs
            )
