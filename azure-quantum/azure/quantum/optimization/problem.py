##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from __future__ import annotations
import logging
import io
import gzip
import json
import numpy
import os
import tarfile


from typing import List, Tuple, Union, Dict, Optional, TYPE_CHECKING
from enum import Enum
from azure.quantum.optimization import TermBase, Term
from azure.quantum.storage import (
    ContainerClient,
    download_blob,
    BlobClient,
    download_blob_metadata,
    download_blob_properties
)
from azure.quantum.job.base_job import ContentType
from azure.quantum.job.job import Job
from azure.quantum.target.target import Target

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
        When passing None, it will default to "Optimization problem"
    :param terms: Problem terms, depending on solver.
        Defaults to None
    :type terms: Optional[List[TermBase]], optional
    :param init_config: Optional configuration details, depending on solver.
        Defaults to None
    :type init_config: Optional[Dict[str,int]], optional
    :param problem_type: Problem type (ProblemType.pubo or
        ProblemType.ising), defaults to ProblemType.ising
    :type problem_type: ProblemType, optional
    :param content_type: Content type, eg: application/json. Default is application/json
    :type content_type: ContentType, optional
    """

    def __init__(
        self,
        name: str,
        terms: Optional[List[TermBase]] = None,
        init_config: Optional[Dict[str, int]] = None,
        problem_type: ProblemType = ProblemType.ising,
        content_type: Optional[ContentType] = ContentType.json 
    ):
        self.name = name or "Optimization problem"
        self.problem_type = problem_type
        self.init_config = init_config
        self.uploaded_blob_uri = None
        self.uploaded_blob_params = None
        self.content_type = content_type

        # each type of term has its own section for quicker serialization
        self.terms = []

        # set the terms
        if terms:
            for term in terms:
                self.terms.append(term)

    """
    Constant thresholds used to determine if a problem is "large".
    """
    NUM_VARIABLES_LARGE = 2500
    NUM_TERMS_LARGE = 1e6


    def serialize(self) -> Union[str, list]:
        """Wrapper function for serializing to json
        """ 
        return self.to_json()

    def to_json(self) -> str:
        """Serializes the problem to a JSON string"""
        result = {
            "metadata": {
                "name": self.name,
            },
            "cost_function": {
                "version": "1.1" if self.init_config else "1.0",
                "type": self.problem_type.name,
                "terms": [term.to_dict() for term in self.terms]
            }
        }

        if self.init_config:
            result["cost_function"]["initial_configuration"] = self.init_config

        return json.dumps(result)

    
    @classmethod
    def from_json(
            cls, 
            input_problem: str, 
            name: Optional[str] = None
        ) -> Problem:
        """Deserializes the problem from a
        json serialized with Problem.serialize()

        :param input_problem:
            the json string to be deserialized to a `Problem` instance
        :type problem_msgs: str
        :param
        :param name: 
            The name of the problem is optional, since it will try 
            to read the serialized name from the json payload.
            If this parameter is not empty, it will use it as the
            problem name ignoring the serialized value.
        :type name: Optional[str]
        """
        result = json.loads(input_problem)

        if name is None:
            metadata = result.get("metadata")
            if metadata is not None:
                name = metadata.get("name")

        terms = [Term.from_dict(t) for t in result["cost_function"]["terms"]] if "terms" in result["cost_function"] else []

        problem = cls(
            name=name,
            terms=terms,
            problem_type=ProblemType[result["cost_function"]["type"]],
        )

        if "initial_configuration" in result["cost_function"]:
            problem.init_config = result["cost_function"]["initial_configuration"]

        return problem

    @classmethod
    def deserialize(
        cls, 
        input_problem: Union[str, list],
        name: Optional[str] = None, 
        content_type: Optional[ContentType] = None) -> Problem:
        """Deserializes the problem from a
        JSON string serialized with Problem.serialize()
        Also used to deserialize the messages downloaded from the blob

        :param input_problem:
            The json string
        :type input_problem: Union[str,list]
        :param
        :param name: 
            The name of the problem is optional, since it will try 
            to read the serialized name from the json payload.
            If this parameter is not empty, it will use it as the
            problem name ignoring the serialized value.
        :type name: Optional[str]
        :param content_type: The content type of the input problem data
        :type: Optional, ContentType
        """
        return cls.from_json(input_problem, name)

    def add_term(self, c: Union[int, float], indices: List[int]):
        """Adds a single monomial term to the `Problem` representation

        :param c: The cost or weight of this term
        :type c: int, float
        :param indices: The variable indices that are in this term
        :type indices: List[int]
        """
        self.terms.append(Term(indices=indices, c=c))
        self.uploaded_blob_uri = None

    def add_terms(
        self, 
        terms: List[Term]
    ):
        """Adds a list of monomial terms to the `Problem` representation

        :param terms: The list of terms to add to the problem
        """
        self.terms += terms
        self.uploaded_blob_uri = None
    
            
    def to_blob(self) -> bytes:
        """Convert problem data to a binary blob.

        :return: Blob data
        :rtype: bytes
        """
        input_problem = self.serialize()
        debug_input_string = input_problem if type(input_problem) is str else b''.join( input_problem).decode('latin-1')
        logger.debug("Input Problem: " + debug_input_string)
        data = io.BytesIO()
        with gzip.GzipFile(fileobj=data, mode="w") as fo:
            fo.write(input_problem.encode())

        return data.getvalue()
    
    def _blob_name(self):
        import uuid
        return "{}-{}".format(self.name, uuid.uuid1())

    def upload(
        self,
        workspace: "Workspace",
        container_name: str = "optimization-problems",
        blob_name: str = "inputData",
        container_uri: str = None,
    ):
        """Uploads an optimization problem instance to
        the cloud storage linked with the Workspace.

        :param workspace: interaction terms of the problem.
        :type workspace: Workspace
        :param container_name: Container name, defaults to "optimization-problems"
        :type container_name: str, optional
        :param blob_name: Blob name, defaults to None
        :type blob_name: str, optional
        :param container_uri: Optional container URI
        :type container_uri: str
        :return: uri of the uploaded problem
        :rtype: str
        """
        blob_params = [workspace, container_name, blob_name]
        if self.uploaded_blob_uri and self.uploaded_blob_params == blob_params:
            return self.uploaded_blob_uri

        if blob_name is None:
            blob_name = self._blob_name()

        encoding = "gzip"
        content_type = self.content_type

        blob = self.to_blob()
        if container_uri is None:
            container_uri = workspace.get_container_uri(
                container_name=container_name
            )
        input_data_uri = Job.upload_input_data(
            input_data=blob,
            blob_name=blob_name,
            container_uri=container_uri,
            encoding=encoding,
            content_type= content_type
        )
        self.uploaded_blob_params = blob_params
        self.uploaded_blob_uri = input_data_uri
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
                if not isinstance(reduced_term, Term) or len(reduced_term.ids) > 0:
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

    def _evaluate(self, configuration, term_list):
        total = 0
        if term_list:
            for term in term_list:
                total += term.evaluate(configuration)
        return total

    def evaluate(self, configuration: Union[Dict[int, int], Dict[str, int]]) -> float:
        """Given a configuration/variable assignment,
        return the cost function value of this problem.

        :param configuration: The dictionary of
         variable ids to their assigned value
        """
        configuration_transformed = {
            int(k): configuration[k] for k in configuration
        }  # if ids are given in string form, convert them to int

        total_cost = 0
        for terms in self.terms:
            total_cost += self._evaluate(configuration_transformed, terms)

        return total_cost

    def is_large(self) -> bool:
        """Determines if the current problem is large.
        "large" is an arbitrary threshold and can be easily changed.
        Based on usage data, we have defined a
        large problem to be NUM_VARIABLES_LARGE+
        variables AND NUM_TERMS_LARGE+ terms.
        """

        set_vars = set()
        total_term_count = 0
        for term in self.terms:
            if isinstance(term, Term):
                set_vars.update(term.ids)
                total_term_count += 1
        
        return (
            len(set_vars) >= Problem.NUM_VARIABLES_LARGE
            and total_term_count >= Problem.NUM_TERMS_LARGE
        )

    def download(self, workspace: "Workspace"):
        """Downloads the uploaded problem as an instance of `Problem`"""
        if not self.uploaded_blob_uri:
            raise Exception("Problem may not be downloaded before it is uploaded")
        blob_client = BlobClient.from_blob_url(self.uploaded_blob_uri)
        container_client = ContainerClient.from_container_url(
            workspace._get_linked_storage_sas_uri(blob_client.container_name)
        )
        blob_name = blob_client.blob_name
        blob = container_client.get_blob_client(blob_name)
        contents = download_blob(blob.url)
        blob_properties = download_blob_properties(blob.url)        
        content_type = blob_properties.content_type
        return Problem.deserialize(contents, self.name, content_type)

    def get_terms(self, id: int) -> List[TermBase]:
        """Given an index the function will return
        a list of terms with that index
        """
        terms = []
        if self.terms != []:
            for term in self.terms:
                if isinstance(term, Term):
                    if id in term.ids:
                        terms.append(term)
            return terms
        else:
            raise Exception(
                "There are currently no terms in this problem. \
                Please download the problem on the client or add terms to the \
                    problem to perform this operation"
            )