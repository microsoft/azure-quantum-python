##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

class Pauli(Enum):
    I = "PauliI"
    X = "PauliX"
    Y = "PauliY"
    Z = "PauliZ"


class Result(Enum):
    Zero = False
    One = True


@dataclass
class Range:
    start: int
    end: int
    step: Optional[int] = None

    @property
    def value(self):
        if self.step is None:
            return {"start": self.start, "end": self.end}
        else:
            return {"start": self.start, "end": self.end, "step": self.step}

@dataclass
class EmptyArray:
    type: Type
