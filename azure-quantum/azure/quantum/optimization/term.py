##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from __future__ import annotations
import numpy as np
from typing import List, Dict, Union, Optional
from enum import Enum
from abc import ABC

__all__ = ["TermBase", "Term", "GroupType", "GroupedTerm"]

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
        TermBase.__init__(self, w=w, c=c)
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

class GroupedTerm(TermBase):
    """
    Grouped term class featuring a particular combination type of monomial terms.
    """
    def __init__(
        self,
        term_type: GroupType,
        terms: List[Term],
        c: Optional[WArray] = 1.0,
    ):
        TermBase.__init__(self, c=c)
        self.term_type = term_type
        self.terms = terms
        self.validate()
    
    @staticmethod
    def is_grouped_term(term_dict: dict):
        return "type" in term_dict
    
    def validate(self):
        """
        Check for and raise errors in GroupedTerm formulation.
        """
        if self.term_type is GroupType.combination:
            # Disabled GroupType
            raise ValueError(
                "Error - type {} GroupedTerm is not enabled;"
                + "formulate list of Term objects instead.".format(self.term_type)
            )
        elif self.term_type is GroupType.squared_linear_combination:
            # Check linearity of terms and that like terms are combined
            seen = set()
            for term in self.terms:
                if len(term.ids) > 1:
                    # Nonlinear term
                    raise ValueError(
                        "Error - terms must be linear in type {} GroupedTerm".format(self.term_type)
                    )
                elif len(term.ids) == 1:
                    # Linear term
                    id = term.ids[0]
                else:
                    # Constant term
                    id = -1
                if id in seen:
                    raise ValueError(
                        "Error - like terms must be combined in type {} GroupedTerm".format(self.term_type)
                    )
                else:
                    seen.add(id)
        else:
            pass

    def to_dict(self):
        """
        Return dictionary format of GroupedTerm for solver input
        """
        return {
            'type': self.term_type,
            'c': self.c,
            'terms': [monomial_term.to_dict() for monomial_term in self.terms],
        }
    
    @classmethod
    def from_dict(cls, obj: dict):
        """
        Create GroupedTerm from dictionary with keys "type", "terms" and "c"
        """
        if obj["type"] == "na":
            term_type = GroupType.combination
        elif obj["type"] == "slc":
            term_type = GroupType.squared_linear_combination
        else:
            print(
                "Error - unknown grouped term type {0}".format(
                    obj["type"]
                )
            )
            raise
        
        try:
            terms = [Term.from_dict(term_dict) for term_dict in obj["terms"]]
        except:
            print(
                "Error - grouped list of terms missing or errant."
            )
            raise
        return cls(term_type=term_type, terms=terms, c=obj["c"])
    
    def evaluate(self, configuration: Dict[int, int]) -> float:
        """Given a variable configuration, evaluate the value of the grouped term.
        :param configuration:
            Dictionary in which each key is a variable id;
            each value is the variable assignment (usually -1, 0, or 1)
        """
        if self.term_type is GroupType.combination:
            combination_eval = 0.0
            for term in self.terms:
                combination_eval += term.evaluate(configuration)
            eval = combination_eval
        elif self.term_type is GroupType.squared_linear_combination:
            combination_eval = 0.0
            for term in self.terms:
                combination_eval += term.evaluate(configuration)
            eval = self.c * combination_eval**2
        else:
            print(
                "Error - evaluate not handled for GroupType {0}".format(
                    self.term_type
                )
            )
            raise
        
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

        # GroupType simplifications when new_terms has a single element
        # Further simplifications require knowledge of binary vs. spin setting,
        # such as simplifying an SLC term consisting of a single variable
        if len(new_terms) == 1:
            term = new_terms[0]
            if self.term_type is GroupType.combination:
                return Term(indices=term.ids, c=self.c * term.c)
            elif self.term_type is GroupType.squared_linear_combination:
                if len(term.ids) == 0:
                    # Simplify SLC term consisting of a single constant
                    # For example, C(k)^2 as a GroupedTerm to Ck^2 as a Term
                    return Term(indices=[], c=self.c * term.c**2)
            else:
                pass
        
        return GroupedTerm(term_type=self.term_type, terms=new_terms, c=self.c)
