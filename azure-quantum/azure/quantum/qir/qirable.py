##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import Optional, Dict, Protocol
from abc import abstractmethod

__all__ = ["Qirable"]

class Qirable(Protocol):
    @abstractmethod
    def _repr_qir_(self, metadata: Optional[Dict[str, str]] = None) -> bytes:
        raise NotImplementedError
