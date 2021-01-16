##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from typing import List, Union, Optional

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

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
