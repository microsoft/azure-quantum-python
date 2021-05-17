import logging
from typing import TYPE_CHECKING, Union, Dict
from azure.quantum.optimization import Problem

logger = logging.getLogger(__name__)

__all__ = ["OnlineProblem"]

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


class OnlineProblem(object):
    def __init__(
        self, name: str,
        blob_uri: str,
        **kw
    ):
        super(OnlineProblem, self).__init__(**kw)
        self.name = name
        self.uploaded_blob_uri = blob_uri

    def download(self, workspace:"Workspace") -> Problem:
        logger.warning("The problem will be downloaded to the client")
        return Problem.download(self, workspace)
