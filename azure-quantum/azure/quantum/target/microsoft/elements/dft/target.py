import warnings

from azure.quantum.job.base_job import ContentType
from azure.quantum.job.job import Job
from azure.quantum.target.target import Target
from azure.quantum.workspace import Workspace
from azure.quantum.target.params import InputParams
from typing import Any, Dict, Type, Union, List
from .job import MicrosoftElementsDftJob
from pathlib import Path
import copy
import json


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
        
        if isinstance(input_data, list):

            qcschema_data = self._assemble_qcshema_from_files(input_data, input_params)

            qcschema_blobs = {}
            for i in range(len(qcschema_data)):
                qcschema_blobs[f"inputData_{i}"] = self._encode_input_data(qcschema_data[i])

            toc_str = self._create_table_of_contents(input_data, list(qcschema_blobs.keys()))
            toc = self._encode_input_data(toc_str)

            return self._get_job_class().from_input_data_container(
                workspace=self.workspace,
                name=name,
                target=self.name,
                input_data=toc,
                batch_input_blobs=qcschema_blobs,
                input_params={ 'numberOfFiles': len(qcschema_data), "inputFiles": list(qcschema_blobs.keys()), **input_params },
                content_type=kwargs.pop('content_type', self.content_type),
                encoding=kwargs.pop('encoding', self.encoding),
                provider_id=self.provider_id,
                input_data_format=kwargs.pop('input_data_format', 'microsoft.qc-schema.v1'),
                output_data_format=kwargs.pop('output_data_format', self.output_data_format),
                session_id=self.get_latest_session_id(),
                **kwargs
            )
        else:
            return super().submit(
                input_data=input_data,
                name=name, 
                shots=shots, 
                input_params=input_params,
                **kwargs
            )


    
    @classmethod
    def _assemble_qcshema_from_files(self, input_data: List[str], input_params: Dict) -> str:
        """
        Convert a list of files to a list of qcshema objects serialized in json.
        """

        qcshema_objects = []
        for file in input_data:
            file_path = Path(file)
            if not file_path.exists():
                raise FileNotFoundError(f"File {file} does not exist.")
            
            file_data = file_path.read_text()
            if file_path.suffix == '.xyz':
                mol = self._xyz_to_qcschema_mol(file_data)
                new_qcschema = self._new_qcshema( input_params, mol )
                qcshema_objects.append(new_qcschema)
            elif file_path.suffix == '.json':
                if input_params is not None and len(input_params.keys()) > 0:
                    warnings.warn('Input parameters were given along with a QcSchema file which contains parameters, using QcSchema parameters as is.')
                with open(file_path, 'r') as f:
                    qcshema_objects.append( json.load(f) )
            else:
                raise ValueError(f"File type '{file_path.suffix}' for file '{file_path}' is not supported. Please use xyz or QcSchema file formats.")

        return qcshema_objects

    @classmethod
    def _new_qcshema( self, input_params: Dict[str,Any], mol: Dict[str,Any],  ) -> Dict[str, Any]:
        """
        Create a new default qcshema object.
        """

        if input_params.get("driver") == "go":
            copy_input_params = copy.deepcopy(input_params)
            copy_input_params["driver"] = "gradient"
            new_object = {
                "schema_name": "qcschema_optimization_input",
                "schema_version": 1,
                "initial_molecule": mol,
            }
            if copy_input_params.get("keywords") and copy_input_params["keywords"].get("geometryOptimization"):
                new_object["keywords"] = copy_input_params["keywords"].pop("geometryOptimization")
            new_object["input_specification"] = copy_input_params
            return new_object
        elif input_params.get("driver") == "bomd":
            copy_input_params = copy.deepcopy(input_params)
            copy_input_params["driver"] = "gradient"
            new_object = {
                "schema_name": "madft_molecular_dynamics_input",
                "schema_version": 1,
                "initial_molecule": mol,
            }
            if copy_input_params.get("keywords") and copy_input_params["keywords"].get("molecularDynamics"):
                new_object["keywords"] = copy_input_params["keywords"].pop("molecularDynamics")
            new_object["input_specification"] = copy_input_params
            return new_object
        else:
            new_object = copy.deepcopy(input_params)
            new_object.update({
                "schema_name": "qcschema_input",
                "schema_version": 1,
                "molecule": mol,
            })
            return new_object
            

    @classmethod
    def _xyz_to_qcschema_mol(self, file_data: str ) -> Dict[str, Any]:
        """
        Convert xyz format to qcschema molecule.
        """

        lines = file_data.split("\n")
        if len(lines) < 3:
            raise ValueError("Invalid xyz format.")
        n_atoms = int(lines.pop(0))
        comment = lines.pop(0)
        mol = {
            "geometry": [],
            "symbols": [],
        }
        for line in lines:
            if line:
                elements = line.split()
                if len(elements) < 4:
                    raise ValueError("Invalid xyz format.")
                symbol, x, y, z = elements
                mol["symbols"].append(symbol)
                mol["geometry"] += [float(x), float(y), float(z)]
            else:
                break
        
        if len(mol["symbols"]) != n_atoms:
            raise ValueError("Number of inputs does not match the number of atoms in xyz file.")

        return mol

    @classmethod
    def _get_job_class(cls) -> Type[Job]:
        return MicrosoftElementsDftJob

    @classmethod
    def _create_table_of_contents(cls, input_files: List[str], input_blobs: List[str]) -> Dict[str,Any]:
        """Create the table of contents for a batched job that contains a description of file and the mapping between the file names and the blob names"""

        assert len(input_files) == len(input_blobs), "Internal error: number of blobs is not that same as the number of files."

        toc = []
        for i in range(len(input_files)):
            toc.append( 
                {
                    "inputFileName": input_files[i],
                    "qcschemaBlobName": input_blobs[i],
                }
            )

        return {
            "description": "This files contains the mapping between the xyz file name that were submitted and the qcschema blobs that are used for the calculation.",
            "tableOfContents": toc,
        }