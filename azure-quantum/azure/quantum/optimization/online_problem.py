import logging
from typing import TYPE_CHECKING, Union, Dict
from azure.quantum.optimization import Problem

logger = logging.getLogger(__name__)

__all__ = ["OnlineProblem"]

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


class OnlineProblem(Problem):
    def __init__(self, name: str, blob_uri: str):
        super().__init__(self)
        self.name = name
        self.uploaded_blob_uri = blob_uri

    def evaluate(
        self, configuration: Union[Dict[int, int], Dict[str, int]]
    ) -> float:
        """
        An OnlineProblem cannot be evaluated on client side.
        Calling this function will raise a user exception
        """
        raise Exception(
            "An Online Problem cannot be evaluated. \
                Please download the problem to do this operation"
        )

    def set_fixed_variables(
        self, fixed_variables: Union[Dict[int, int], Dict[str, int]]
    ) -> Problem:
        """
        An OnlineProblem cannot be evaluated on client side.
        Calling this function will raise a user exception
        """
        raise Exception(
            "An Online Problem cannot set fixed terms. \
                Please download the problem to do this operation"
        )

    def download(self) -> Problem:
        logger.warning("The problem will be downloaded to the client")
        return super().download()
