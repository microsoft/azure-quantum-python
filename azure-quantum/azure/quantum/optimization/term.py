##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from __future__ import annotations
import numpy as np
from typing import List, Dict, Union, Optional

__all__ = ["Term"]

try:
    import numpy.typing as npt

    WArray = Union[int, float, npt.ArrayLike]

    def _convert_if_numpy_type(param: WArray):
        # Attempt first a conversion to a supported
        # type if parameter is a numpy float/int.
        numpy_integer_types = [
            np.byte,
            np.ubyte,
            np.short,
            np.ushort,
            np.intc,
            np.uintc,
            np.int_,
            np.uint,
            np.longlong,
            np.ulonglong,
            np.int8,
            np.uint8,
            np.int16,
            np.uint16,
            np.int32,
            np.uint32,
            np.int64,
            np.uint64,
        ]

        numpy_float_types = [
            np.float16,
            np.float32,
            np.float64,
            np.float_,
            np.half,
            np.single,
            np.double,
        ]

        if hasattr(param, "__iter__"):
            # Handle scalar-like arrays, if specified.
            param = param[0]

        if (
            hasattr(param, "dtype")
            and param.dtype in numpy_integer_types + numpy_float_types
        ):
            return param.item()
        else:
            return param


except ImportError:
    npt = None
    WArray = Union[int, float]

    def _convert_if_numpy_type(param: WArray):
        return param


class Term:
    def __init__(
        self,
        indices: List[int] = None,
        w: Optional[WArray] = None,
        c: Optional[WArray] = None,
    ):
        if w is not None:
            # Legacy support if 'w' is used to specify
            # term instead of the expected 'c'.
            coeff = w
            parameter_name_used = "w"
        elif c is not None:
            # Current intended specification of term.
            coeff = c
            parameter_name_used = "c"
        else:
            raise RuntimeError("Cost should be provided for each term.")

        coeff = _convert_if_numpy_type(coeff)
        if type(coeff) != int and type(coeff) != float:
            raise RuntimeError(
                f"{parameter_name_used} must be a float or int value, \
                    or a NumPy value that can be converted to those."
            )
        self.c = coeff

        self.ids = indices

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(obj):
        return Term(indices=obj["ids"], c=obj["c"])

    def evaluate(self, configuration: Dict[int, int]) -> float:
        """Given a variable configuration, evaluate the value of the term.
        :param configuration:
            The dictionary of variable ids to their assigned value
        """
        try:
            multiplier = (
                np.prod([configuration[i] for i in self.ids])
                if len(self.ids) > 0
                else 1.0
            )
        except KeyError:
            print(
                "Error - variable id found in term {0}, \
                    but not found in the supplied configuration.".format(
                    self.ids
                )
            )
            raise

        return multiplier * self.c

    def reduce_by_variable_state(
        self, fixed_variables: Dict[int, int]
    ) -> Optional[Term]:
        """Given some fixed variable states,
            transform the existing term into new term.
        Returns None if the new term is effectively 0
        :param fixed_variables:
            The dictionary of variable ids and their fixed state
        """
        new_ids = []
        new_c = self.c

        for i in self.ids:
            if i not in fixed_variables:
                new_ids.append(i)
            else:
                new_c *= fixed_variables[i]
                if new_c == 0:
                    return None

        return Term(indices=new_ids, c=new_c)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
