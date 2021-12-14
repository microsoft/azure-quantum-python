##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from __future__ import annotations
import numpy as np
from typing import List, Dict, Union, Optional
from enum import Enum
from abc import ABC

__all__ = ["TermBase", "Term", "GroupType", "SlcTerm"]

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


class TermBase(ABC):
    """
    Term base class; this class is not directly initialized
    """
    def __init__(
        self,
        c: Optional[WArray] = None,
    ):
        if c is not None:
            # Current intended specification of term.
            coeff = c
        else:
            raise RuntimeError("Cost should be provided for each term.")

        coeff = _convert_if_numpy_type(coeff)
        if type(coeff) != int and type(coeff) != float:
            raise RuntimeError(
                "c must be a float or int value, \
                    or a NumPy value that can be converted to those."
            )
        self.c = coeff

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, obj):
        return cls(c=obj.get("c"))

    def evaluate(self, *args, **kwargs) -> float:
        """Given a variable configuration, evaluate the value of the term.
        :param configuration:
            The dictionary of variable ids to their assigned value
        """
        return self.c

    def reduce_by_variable_state(self, *args, **kwargs) -> Optional[TermBase]:
        """Given some fixed variable states,
            transform the existing term into new term.
        Returns None if the new term is effectively 0
        :param fixed_variables:
            The dictionary of variable ids and their fixed state
        """
        return TermBase(c=self.c) if self.c != 0 else None

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

class Term(TermBase):
    """
    Class describing a single (monomial) term.
    """
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
        TermBase.__init__(self, c=coeff)
        self.ids = indices
    
    @classmethod
    def from_dict(cls, obj: dict):
        return cls(indices=obj.get("ids"), c=obj.get("c"))
    
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


class GroupType(str, Enum):
    combination = "na"
    squared_linear_combination = "slc"

class SlcTerm(TermBase):
    """
    Squared Linear Combination term class.
    """
    def __init__(
        self,
        terms: List[Term],
        c: Optional[WArray] = 1.0,
    ):
        TermBase.__init__(self, c=c)
        self.terms = terms
        self.validate()
    
    def validate(self):
        """
        Check for and raise errors in Squared Linear Combination formulation.
        """
        # Check linearity of terms and that like terms are combined
        seen = set()
        for term in self.terms:
            if len(term.ids) > 1:
                # Nonlinear term
                raise ValueError("Error - terms must be linear in type SlcTerm")
            elif len(term.ids) == 1:
                # Linear term
                id = term.ids[0]
            else:
                # Constant term
                id = -1
            if id in seen:
                raise ValueError("Error - like terms must be combined in type SlcTerm")
            else:
                seen.add(id)


    def to_dict(self):
        """
        Return dictionary format of SlcTerm for solver input
        """
        return {
            'c': self.c,
            'terms': [monomial_term.to_dict() for monomial_term in self.terms],
        }
    
    @classmethod
    def from_dict(cls, obj: dict):
        """
        Create SlcTerm from dictionary with keys "terms" and "c"
        """
        try:
            terms = [Term.from_dict(term_dict) for term_dict in obj["terms"]]
        except:
            print(
                "Error - grouped list of terms missing or errant for squared linear combination type."
            )
            raise
        return cls(terms=terms, c=obj["c"])
    
    def evaluate(self, configuration: Dict[int, int]) -> float:
        """Given a variable configuration, evaluate the value of the slc term.
        :param configuration:
            Dictionary in which each key is a variable id;
            each value is the variable assignment (usually -1, 0, or 1)
        """
        combination_eval = 0.0
        for term in self.terms:
            combination_eval += term.evaluate(configuration)
        eval = self.c * combination_eval**2
        
        return eval
    
    def reduce_by_variable_state(
        self,
        fixed_variables: Dict[int, int]
    ) -> Optional[TermBase]:
        """Given some fixed variable states,
            transform the existing grouped term into new term.
        Returns None if the new term is effectively 0
        :param fixed_variables:
            The dictionary of variable ids and their fixed state
        """
        new_terms_dict = dict()
        for monomial in self.terms:
            new_monomial = monomial.reduce_by_variable_state(fixed_variables)
            if new_monomial:
                ids = tuple(sorted(new_monomial.ids))
                try:
                    new_terms_dict[ids] += new_monomial.c
                except:
                    new_terms_dict[ids] = new_monomial.c
        new_terms = [Term(indices=list(ids), c=c) for ids,c in new_terms_dict.items()]
        if len(new_terms) == 0:
            return None

        # Slc simplifications when new_terms has a single constant element
        # such as simplifying an SLC term consisting of a single variable
        if len(new_terms) == 1:
            term = new_terms[0]
            if len(term.ids) == 0:
                # Simplify SLC term consisting of a single constant
                # For example, C(k)^2 as a GroupedTerm to Ck^2 as a Term
                return Term(indices=[], c=self.c * term.c**2)

        return SlcTerm(terms=new_terms, c=self.c)
