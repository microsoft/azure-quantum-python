import logging
from typing import TYPE_CHECKING
from azure.quantum.aio.optimization import Problem

logger = logging.getLogger(__name__)

__all__ = ["OnlineProblem"]

if TYPE_CHECKING:
    from azure.quantum.aio.workspace import Workspace


class OnlineProblem(object):
    def __init__(
        self, name: str,
        blob_uri: str,
        **kw
    ):
        super(OnlineProblem, self).__init__(**kw)
        self.name = name
        self.uploaded_blob_uri = blob_uri

    async def download(self, workspace:"Workspace") -> Problem:
        logger.warning("The problem will be downloaded to the client")
        return await Problem.download(self, workspace)
