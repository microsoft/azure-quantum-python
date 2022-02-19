##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING

from azure.quantum.cirq.targets.quantinuum import QuantinuumTarget

if TYPE_CHECKING:
    from azure.quantum import Workspace


class HoneywellTarget(QuantinuumTarget):
    """Base class for interfacing with an Quantinuum (formerly Honeywell) backend in Azure Quantum"""

    def __init__(
        self,
        workspace: "Workspace",
        name: str,
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        provider_id: str = "honeywell",
        content_type: str = "application/qasm",
        encoding: str = "",
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


