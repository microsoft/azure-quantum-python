import warnings

from azure.quantum.job.base_job import ContentType
from azure.quantum.job.job import Job
from azure.quantum.target.target import Target
from azure.quantum.workspace import Workspace
from azure.quantum.target.params import InputParams
from typing import Any, Dict, Type, Union
from .job import MicrosoftElementsDftJob


class MicrosoftElementsDft(Target):
    """
    Microsoft Elements Dft target from the microsoft-elements provider.
    """

    target_names = [
        "microsoft.dft"
    ]


    def __init__(
        self,
        workspace: "Workspace",
        name: str = "microsoft.dft",
        **kwargs
    ):
        """
        Initializes a new DFT target.

        :param workspace: Associated workspace
        :type workspace: Workspace
        :param name: Target name
        """
        # There is only a single target name for this target
        assert name == self.target_names[0]

        # make sure to not pass argument twice
        kwargs.pop("provider_id", None)

        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format="microsoft.xyz.v1",
            output_data_format="microsoft.dft-results.v1",
            provider_id="microsoft-elements",
            content_type=ContentType.text_plain,
            **kwargs
        )


    def submit(self,
               input_data: Any,
               name: str = "azure-quantum-dft-job",
               shots: int = None,
               input_params: Union[Dict[str, Any], InputParams, None] = None,
               **kwargs) -> MicrosoftElementsDftJob:
        """
        Submit DFT job to Azure Quantum Services.
        
        :param input_data: Input data
        :type input_data: Any
        :param name: Job name
        :type name: str
        :param shots: Number of shots. Ignored in DFT job. Defaults to None
        :type shots: int
        :param input_params: Input parameters
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """

        if shots is not None:
            warnings.warn("The 'shots' parameter is ignored in Microsoft Elements Dft job.")
        
        return super().submit(
            input_data=input_data,
            name=name, 
            shots=shots, 
            input_params=input_params,
            **kwargs
        )


    @classmethod
    def _get_job_class(cls) -> Type[Job]:
        return MicrosoftElementsDftJob
