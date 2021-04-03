##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import numpy as np
from typing import List, Dict, Union, Optional

__all__ = ['Term']

class Term:

    def __init__(self, indices: List[int] = None, w: Optional[Union[int, float]] = None, c: Optional[Union[int, float]] = None):
        if(type(w) == None and type(c) == None):
            raise RuntimeError("Cost should be provided for each term.")

        if(w != None):
            if(type(w) != int and type(w) != float):
                raise RuntimeError("w must be a float or int value.")
            else:
                self.c = w
        elif(c != None):
            if(type(c) != int and type(c) != float):
                raise RuntimeError("c must be a float or int value.")
            else:
                self.c = c

        self.ids = indices

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(obj):
        return Term(indices = obj['ids'], c = obj['c'])

    def evaluate(self, configuration: Dict[int, int]) -> float:
        """ Given a variable configuration, evaluate the value of the term.
            :param configuration: The dictionary of variable ids to their assigned value
        """
        try:
            multiplier = np.prod([configuration[i] for i in self.ids])
        except KeyError:
            print("Error - variable id found in term {0}, but not found in the supplied configuration.".format(self.ids))
            raise

        return multiplier*self.c

    def reduce_by_variable_state(self, fixed_variables: Dict[int, int])) -> Term:
        pass

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False