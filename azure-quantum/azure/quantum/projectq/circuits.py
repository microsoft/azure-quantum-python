##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    from projectq.backends import (
        CircuitDrawer as ProjectQCircuitDrawer,
        CircuitDrawerMatplotlib as ProjectQCircuitDrawerMatplotlib
    )
except ImportError:
    raise ImportError(
        "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
    )

__all__ = ["Circuit"]


class Circuit(ProjectQCircuitDrawer):
    def __init__(
        self, 
        name : str,
        accept_input=False, 
        default_measure=0
    ):
        super().__init__(
            accept_input=accept_input, 
            default_measure=default_measure
        )

        self._name = name

    def name(self):
        return self._name
