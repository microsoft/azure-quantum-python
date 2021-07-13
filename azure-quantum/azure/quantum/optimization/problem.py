##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from __future__ import annotations
import logging
import uuid
import io
import gzip
import json
import numpy
import os

from typing import List, Tuple, Union, Dict, Optional, TYPE_CHECKING
from enum import Enum
from azure.quantum.optimization import Term
from azure.quantum.storage import (
    ContainerClient,
    download_blob,
    BlobClient
)
from azure.quantum.job.job import Job

logger = logging.getLogger(__name__)

__all__ = ["Problem", "ProblemType"]

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


class ProblemType(str, Enum):
    pubo = 0
    ising = 1


class Problem:
    """Problem to submit to the service.

    :param name: Problem name
    :type name: str
    :param terms: Problem terms, depending on solver.
        Defaults to None
    :type terms: Optional[List[Term]], optional
    :param init_config: Optional configuration details, depending on solver.
        Defaults to None
    :type init_config: Optional[Dict[str,int]], optional
    :param problem_type: Problem type (ProblemType.pubo or
        ProblemType.ising), defaults to ProblemType.ising
    :type problem_type: ProblemType, optional
    """

    def __init__(
        self,
        name: str,
        terms: Optional[List[Term]] = None,
        init_config: Optional[Dict[str, int]] = None,
        problem_type: ProblemType = ProblemType.ising,
    ):
        self.name = name
        self.terms = terms.copy() if terms is not None else []
        self.problem_type = problem_type
        self.init_config = init_config
        self.uploaded_blob_uri = None
        self.uploaded_blob_params = None

    """
    Constant thresholds used to determine if a problem is "large".
    """
    NUM_VARIABLES_LARGE = 2500
    NUM_TERMS_LARGE = 1e6

    def serialize(self) -> str:
        """Serializes the problem to a JSON string"""
        result = {
            "cost_function": {
                "version": "1.1" if self.init_config else "1.0",
                "type": self.problem_type.name,
                "terms": [term.to_dict() for term in self.terms],
            }
        }

        if self.init_config:
            result["cost_function"]["initial_configuration"] = self.init_config

        return json.dumps(result)

    @classmethod
    def deserialize(cls, problem_as_json: str, name: str):
        """Deserializes the problem from a
            JSON string serialized with Problem.serialize()

        :param problem_as_json:
            The string to be deserialized to a `Problem` instance
        :type problem_as_json: str
        :param name: The name of the problem
        :type name: str
        """
        result = json.loads(problem_as_json)
        problem = Problem(
            name=name,
            terms=[
                Term.from_dict(t) for t in result["cost_function"]["terms"]
            ],
            problem_type=ProblemType[result["cost_function"]["type"]],
        )

        if "initial_configuration" in result["cost_function"]:
            problem.init_config = result["cost_function"][
                "initial_configuration"
            ]

        return problem

    def add_term(self, c: Union[int, float], indices: List[int]):
        """Adds a single term to the `Problem` representation

        :param c: The cost or weight of this term
        :type c: int, float
        :param indices: The variable indices that are in this term
        :type indices: List[int]
        """
        self.terms.append(Term(indices=indices, c=c))
        self.uploaded_blob_uri = None

    def add_terms(self, terms: List[Term]):
        """Adds a list of terms to the `Problem` representation

        :param terms: The list of terms to add to the problem
        """
        self.terms += terms
        self.uploaded_blob_uri = None

    def to_blob(self, compress: bool = False) -> Tuple[bytes, str]:
        """Convert problem data to a binary blob.

        :param compress: Compress the blob using gzip, defaults to None
        :type compress: bool, optional
        :return: Blob data
        :rtype: bytes
        """
        problem_json = self.serialize()
        logger.debug("Problem json: " + problem_json)
        data = io.BytesIO()

        if compress:
            with gzip.GzipFile(fileobj=data, mode="w") as fo:
                fo.write(problem_json.encode())
        else:
            data.write(problem_json.encode())

        return data.getvalue()
    
    def _blob_name(self):
        return "{}-{}".format(self.name, uuid.uuid1())

    def upload(
        self,
        workspace: "Workspace",
        container_name: str = "qio-problems",
        blob_name: str = None,
        compress: bool = True,
        container_uri: str = None
    ):
        """Uploads an optimization problem instance to
        the cloud storage linked with the Workspace.

        :param workspace: interaction terms of the problem.
        :type workspace: Workspace
        :param container_name: Container name, defaults to "qio-problems"
        :type container_name: str, optional
        :param blob_name: Blob name, defaults to None
        :type blob_name: str, optional
        :param compress: Flag to compress the payload, defaults to True
        :type compress: bool, optional
        :param container_uri: Optional container URI
        :type container_uri: str
        :return: uri of the uploaded problem
        :rtype: str
        """
        blob_params = [workspace, container_name, blob_name, compress]
        if self.uploaded_blob_uri and self.uploaded_blob_params == blob_params:
            return self.uploaded_blob_uri

        if blob_name is None:
            blob_name = self._blob_name()

        encoding = "gzip" if compress else ""
        blob = self.to_blob(compress=compress)
        if container_uri is None:
            container_uri = Job.create_container(
                workspace=workspace,
                container_name=container_name
            )
        input_data_uri = Job.upload_input_data(
            input_data=blob,
            blob_name=blob_name,
            container_uri=container_uri,
            encoding=encoding,
            content_type="application/json"
        )
        self.uploaded_blob_params = blob_params
        return input_data_uri

    def set_fixed_variables(
        self, fixed_variables: Union[Dict[int, int], Dict[str, int]]
    ) -> Problem:
        """Transforms the current problem with a set of fixed
        variables and returns the new modified problem.
        The original Problem instance is untouched.

        :param fixed_variables:
            The dictionary of variable ids and their fixed state
        """
        if len(fixed_variables) == 0:
            raise RuntimeError(
                "Error: fixed_variables is empty - \
                please specify at least one fixed variable"
            )

        fixed_transformed = {
            int(k): fixed_variables[k] for k in fixed_variables
        }  # if ids are given in string form, convert them to int
        new_terms = []

        constant = 0
        for term in self.terms:
            reduced_term = term.reduce_by_variable_state(fixed_transformed)
            if reduced_term:
                if len(reduced_term.ids) > 0:
                    new_terms.append(reduced_term)
                else:
                    # reduced to a constant term
                    constant += reduced_term.c

        if constant:
            new_terms.append(Term(c=constant, indices=[]))

        new_init_config = None
        if self.init_config:
            new_init_config = {
                k: self.init_config[k]
                for k in self.init_config
                if int(k) not in fixed_transformed
            }

        return Problem(
            self.name,
            terms=new_terms,
            init_config=new_init_config,
            problem_type=self.problem_type,
        )

    def evaluate(
        self, configuration: Union[Dict[int, int], Dict[str, int]]
    ) -> float:
        """Given a configuration/variable assignment,
        return the cost function value of this problem.

        :param configuration: The dictionary of
         variable ids to their assigned value
        """
        configuration_transformed = {
            int(k): configuration[k] for k in configuration
        }  # if ids are given in string form, convert them to int
        total_cost = 0
        if self.terms:
            for term in self.terms:
                total_cost += term.evaluate(configuration_transformed)

        return total_cost

    def is_large(self) -> bool:
        """Determines if the current problem is large.
        "large" is an arbitrary threshold and can be easily changed.
        Based on usage data, we have defined a
        large problem to be NUM_VARIABLES_LARGE+
        variables AND NUM_TERMS_LARGE+ terms.
        """

        set_vars = set()
        for term in self.terms:
            set_vars.update(term.ids)

        return (
            len(set_vars) >= Problem.NUM_VARIABLES_LARGE
            and len(self.terms) >= Problem.NUM_TERMS_LARGE
        )

    def download(self, workspace:"Workspace"):
        """Downloads the uploaded problem as an instance of `Problem`"""
        if not self.uploaded_blob_uri:
            raise Exception(
                "Problem may not be downloaded before it is uploaded"
            )
        blob_client = BlobClient.from_blob_url(self.uploaded_blob_uri)
        container_client = ContainerClient.from_container_url(
            workspace._get_linked_storage_sas_uri(
                blob_client.container_name
            )
        )
        blob_name = blob_client.blob_name
        blob = container_client.get_blob_client(blob_name)
        contents = download_blob(blob.url)
        return Problem.deserialize(contents, self.name)

    def get_terms(self, id:int) -> List[Term]:
        """ Given an index the function will return
        a list of terms with that index
        """
        terms = []
        if self.terms != []:
            for term in self.terms:
                if id in term.ids:
                    terms.append(term)
            return terms
        else:
            raise Exception("There are currently no terms in this problem. \
                Please download the problem on the client or add terms to the \
                    problem to perform this operation")

    def is_valid_npz(self, 
        files: List[str],
        indices_column_names: List[str] = ["arr_0", "arr_1"],
        c_column_name: str = "arr_2"
        ) -> bool:
        """Determines if the supplied npz has expected column names.
        If none are supplied, checks default naming.
        Otherwise, it checks user-supplied naming.

        :param files: the associated column names of an npz file
        :type: List[str]
        :param indices_column_names: the names of the indices columns
        :type indices_column_names: List[str], optional
        :param c_column_name: the name of the coefficient column
        :type c_column_name: str, optional
        """

        all_columns = indices_column_names + [c_column_name]

        if (len(files) != len(all_columns)):
            return False
        
        if(sorted(files) != sorted(all_columns)):
            return False

        return True

    def terms_from_npz(self,
        file_path = str,
        indices_column_names: List[str] = ["arr_0", "arr_1"],
        c_column_name: str = "arr_2"
        ) -> List[Term]:
        """Reads a user supplied npz file and converts it to a list of `Term`.
        An NPZ file contains several arrays (or columns), which can specify
        the indices of a problem term, along with the coefficient.
        Default naming for these columns is used unless specified by the user.

        :param file_path: file path of the NPZ file to be converted
        :type file_name: str
        :param indices_column_names: the names of the indices columns
        :type indices_column_names: List[str], optional
        :param c_column_name: the name of the coefficient column
        :type c_column_name: str, optional
        """

        terms = []

        if os.path.isfile(file_path):
            problem_file = numpy.load(file_path)

            # Check the default or user-supplied columns are present
            if not(self.is_valid_npz(problem_file.files, indices_column_names, c_column_name)):
                raise Exception("Error in validating NPZ file. \
                    Please check that the names of the arrays match the default \
                        or user-supplied namings.")
            
            # For each of the indices column names, extract the associated indices column data
            problem_ids = [list(problem_file[id]) for id in indices_column_names]

            # Unpack the problem indices and zip with the coefficient column data
            # to produce problem terms
            for term in zip(*problem_ids, problem_file[c_column_name]):
                ids = list(term[:-1])
                indices = list(map(int, ids))

                c = float(term[-1])
                terms.append(Term(c=c, indices=indices))
            return terms
        else:
            raise Exception("Unable to read NPZ file. \
                Please check the file path supplied is correct.")
