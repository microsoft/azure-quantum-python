##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from dataclasses import dataclass, field
from re import sub
from typing import Any, Dict, List, Optional, Tuple, Type, Callable
from ..argument_types import EmptyArray, Pauli, Range, Result


__all__ = ["InputParams"]


class EntryPointArguments:
    """
    Wrapper class to set QIR entry point arguments.

    This class is used to set QIR entry point arguments inside the
    InputParamsItem class.  It overrides the __setitem__ method to
    automatically detect the entry point's argument from the passed value.
    """

    # Maps supported Python types to QIR entry point type names and a callable
    # that extracts the serialized value from the original value. (list (=
    # Array) is handled as a special case.)
    type_map: Dict[type, Tuple[str, Callable]] = {
        int: ("Int", lambda v: v),
        float: ("Double", lambda v: v),
        bool: ("Boolean", lambda v: v),
        str: ("String", lambda v: v),
        Pauli: ("Pauli", lambda v: v.value),
        Result: ("Result", lambda v: v.value),
        Range: ("Range", lambda v: v.value)
    }

    def __init__(self):
        self.entries = []

    def __setitem__(self, name: str, value: Any):
        """
        Creates entry point argument entry and automatically determines the
        type from value.
        """
        if type(value) == list:
            if len(value) == 0:
                raise ValueError("Use EmptyArray(type) to assign an empty "
                                 "error")
            else:
                first = value[0]
                first_value, first_type = self._extract_value_and_type(first)
                values = [first_value]
                for next in value[1:]:
                    next_value, next_type = self._extract_value_and_type(next)
                    if next_type != first_type:
                        raise TypeError("All elements in a list must have "
                                        "the same type")
                    values.append(next_value)
                self.entries.append(
                    {"name": name,
                     "value": values,
                     "type": "Array",
                     "elementType": first_type})
        elif type(value) == EmptyArray:
            element_type = self._extract_type(value.element_type)
            self.entries.append(
                {"name": name,
                 "value": [],
                 "type": "Array",
                 "elementType": element_type})
        else:
            entry_value, entry_type = self._extract_value_and_type(value)
            self.entries.append(
                {"name": name, "value": entry_value, "type": entry_type})

    def _extract_type(self, type: Type) -> str:
        """
        Convert Python type to QIR entry point argument type name.
        """
        if type in self.type_map:
            return self.type_map[type][0]
        elif type == list:
            raise TypeError(f"Nested lists are not supported")
        else:
            type_name = type.__name__
            raise TypeError(f"Unsupported type {type_name}")

    def _extract_value_and_type(self, value: Any) -> Tuple[Any, str]:
        """
        Convert Python value to QIR entry point argument type name and
        serialized value.
        """
        if type(value) in self.type_map:
            entry_type, entry_value_func = self.type_map[type(value)]
            return entry_value_func(value), entry_type
        elif type(value) == list:
            raise TypeError(f"Nested lists are not supported")
        else:
            type_name = type(value).__name__
            raise TypeError(f"Unsupported type {type_name} for {value}")


@dataclass
class AutoValidatingParams:
    """
    A helper class for target parameters.

    It has a function as_dict that automatically extracts a dictionary from
    the class' fields.  They are added to the result dictionary if their value
    is not None, the key is automatically transformed from Python snake case
    to camel case, and if validate is True and if the field has a validation
    function, the field is validated beforehand.
    """
    def as_dict(self, validate=True):
        result = {}

        for name, field in self.__dataclass_fields__.items():
            field_value = self.__getattribute__(name)
            if field_value is not None:
                # validate field?
                if validate and "validate" in field.metadata:
                    func = field.metadata["validate"]
                    # check for indirect call (like in @staticmethod)
                    if hasattr(func, "__func__"):
                        func = func.__func__
                    func(name, field_value)

                # translate field name to camel case
                s = sub(r"(_|-)+", " ", name).title().replace(" ", "")
                attribute = ''.join([s[0].lower(), s[1:]])
                result[attribute] = field_value

        if validate:
            self.post_validation(result)

        return result

    def post_validation(self, result):
        """
        A function that is called after all individual fields have been
        validated, but before the result is returned.

        Here result is the current dictionary.
        """
        pass


def validating_field(validation_func, default=None):
    """
    A helper method to declare field for an AutoValidatingParams data class.
    """
    return field(default=default, metadata={"validate": validation_func})


class InputParamsItem:
    """
    Base class for input parameters.

    This class serves both as the base class for InputParams as well as for the
    items in the InputParams.
    """
    def __init__(self):
        # all input param items may have an entry point name and a list of
        # arguments
        self.entry_point: Optional[str] = None
        self.arguments = EntryPointArguments()

    def as_dict(self, validate=True) -> Dict[str, Any]:
        """
        Returns input params as a dictionary.
        """
        result = {}

        if self.entry_point is not None:
            result['entryPoint'] = self.entry_point

        if len(self.arguments.entries) > 0:
            result['arguments'] = self.arguments.entries

        return result


class InputParams(InputParamsItem):
    """
    Class to define input parameters.

    This class allows to define input parameters for non-batching and batching
    jobs.  The instance represents a batching job, if and only if num_items is
    set to some positive number less or equal to MAX_NUM_ITEMS.

    Both this class and the items in this class are based on InputParamsItem as
    a template, which can be overriden for specializations created by a target.
    This class should never be constructed directly but only through the
    InputParams.make_params method.
    """

    MAX_NUM_ITEMS: int = 1000

    def __init__(
            self,
            num_items: Optional[int] = None,
            item_type: Type[InputParamsItem] = InputParamsItem):
        """
        Constructs a InputParams instance.

        The item_type argument should be set by targets that override
        InputParams and have a specialized InputParamsItem class.
        """
        item_type.__init__(self)

        # fileURIs
        self.file_uris = {}

        if num_items is not None:
            self.has_items = True
            if num_items <= 0 or num_items > self.MAX_NUM_ITEMS:
                raise ValueError(
                    "num_items must be a positive value less or equal to "
                    f"{self.MAX_NUM_ITEMS}")
            self._items = [item_type() for _ in range(num_items)]
        else:
            self.has_items = False

        self.item_type = item_type

    @property
    def items(self) -> List:
        if self.has_items:
            return self._items
        else:
            raise Exception("Cannot access items in a non-batching job, call "
                            "make_params with num_items parameter")

    def as_dict(self, validate=True) -> Dict[str, Any]:
        """
        Constructs a dictionary from the input params.

        For batching jobs, top-level entries are merged into item entries.
        Item entries have priority in case they are specified.
        """

        # initialize result and set type hint
        result: Dict[str, Any] = self.item_type.as_dict(self, validate)

        if self.has_items:
            result["items"] = [item.as_dict(validate) for item in self._items]
            # In case of batching, no need to stop if failing an item
            result["resumeAfterFailedItem"] = True

        # add fileUris if existing
        if len(self.file_uris) > 0:
            result["fileUris"] = self.file_uris

        return result