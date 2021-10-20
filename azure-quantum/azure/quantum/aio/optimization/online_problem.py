import logging
from typing import TYPE_CHECKING
from azure.quantum.aio.optimization import Problem
from azure.quantum.optimization import OnlineProblem as SyncOnlineProblem

logger = logging.getLogger(__name__)

__all__ = ["OnlineProblem"]

if TYPE_CHECKING:
    from azure.quantum.aio.workspace import Workspace


class OnlineProblem(SyncOnlineProblem):
    async def download(self, workspace: "Workspace") -> Problem:
        logger.warning("The problem will be downloaded to the client")
        return await Problem.download(self, workspace)
