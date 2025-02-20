##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import re
import warnings
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Type, Union, List

from ...job import Job
from ...job.base_job import ContentType
from ...workspace import Workspace
from ..params import InputParams, InputParamsItem, AutoValidatingParams, \
    validating_field
from ..target import Target

def _check_error_rate(name, value):
    if value <= 0.0 or value >= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")

def _check_error_rate_or_process_and_readout(name, value):
    if value is None:
        return

    if isinstance(value, float):
        _check_error_rate(name, value)
        return

    if not isinstance(value, MeasurementErrorRate):
        raise ValueError(f"{name} must be either a float or "
                         "MeasurementErrorRate with two fields: 'process' and 'readout'")

def check_time(name, value):
    pat = r"^(\+?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(s|ms|μs|µs|us|ns)$"
    if re.match(pat, value) is None:
        raise ValueError(f"{name} is not a valid time string; use a "
                         "suffix s, ms, us, or ns")

@dataclass
class MeasurementErrorRate(AutoValidatingParams):
    process: float = field(metadata={"validate": _check_error_rate})
    readout: float = field(metadata={"validate": _check_error_rate})

@dataclass
class ProtocolSpecificDistillationUnitSpecification(AutoValidatingParams):
    num_unit_qubits: Optional[int] = None
    duration_in_qubit_cycle_time: Optional[int] = None

    def post_validation(self, result):
        if self.num_unit_qubits is None:
            raise LookupError("num_unit_qubits must be set")

        if self.duration_in_qubit_cycle_time is None:
            raise LookupError("duration_in_qubit_cycle_time must be set")


@dataclass
class DistillationUnitSpecification(AutoValidatingParams):
    name: Optional[str] = None
    display_name: Optional[str] = None
    num_input_ts: Optional[int] = None
    num_output_ts: Optional[int] = None
    failure_probability_formula:  Optional[str] = None
    output_error_rate_formula:  Optional[str] = None
    physical_qubit_specification: Optional[ProtocolSpecificDistillationUnitSpecification] = None
    logical_qubit_specification: Optional[ProtocolSpecificDistillationUnitSpecification] = None
    logical_qubit_specification_first_round_override: \
        Optional[ProtocolSpecificDistillationUnitSpecification] = None

    def has_custom_specification(self):
        return \
        self.display_name is not None \
        or self.num_input_ts is not None \
        or self.num_output_ts is not None \
        or self.failure_probability_formula is not None \
        or self.output_error_rate_formula is not None \
        or self.physical_qubit_specification is not None \
        or self.logical_qubit_specification is not None \
        or self.logical_qubit_specification_first_round_override is not None

    def has_predefined_name(self):
        return self.name is not None

    def post_validation(self, result):
        if not self.has_custom_specification() and not self.has_predefined_name():
            raise LookupError("name must be set or custom specification must be provided")

        if self.has_custom_specification() and self.has_predefined_name():
            raise LookupError("If predefined name is provided, "
                            "custom specification is not allowed. "
                            "Either remove name or remove all other "
                            "specification of the distillation unit")

        if self.has_predefined_name():
            return # all other validation is on the server side

        if self.num_input_ts is None:
            raise LookupError("num_input_ts must be set")

        if self.num_output_ts is None:
            raise LookupError("num_output_ts must be set")

        if self.failure_probability_formula is None:
            raise LookupError("failure_probability_formula must be set")

        if self.output_error_rate_formula is None:
            raise LookupError("output_error_rate_formula must be set")

        if self.physical_qubit_specification is not None:
            self.physical_qubit_specification.post_validation(result)

        if self.logical_qubit_specification is not None:
            self.logical_qubit_specification.post_validation(result)

        if self.logical_qubit_specification_first_round_override is not None:
            self.logical_qubit_specification_first_round_override.post_validation(result)

    def as_dict(self, validate=True) -> Dict[str, Any]:
        specification_dict = super().as_dict(validate)
        if len(specification_dict) != 0:
            if self.physical_qubit_specification is not None:
                physical_qubit_specification_dict = \
                self.physical_qubit_specification.as_dict(validate)
                if len(physical_qubit_specification_dict) != 0:
                    specification_dict["physicalQubitSpecification"] = \
                        physical_qubit_specification_dict

            if self.logical_qubit_specification is not None:
                logical_qubit_specification_dict = \
                self.logical_qubit_specification.as_dict(validate)
                if len(logical_qubit_specification_dict) != 0:
                    specification_dict["logicalQubitSpecification"] = \
                        logical_qubit_specification_dict

            if self.logical_qubit_specification_first_round_override is not None:
                logical_qubit_specification_first_round_override_dict = \
                self.logical_qubit_specification_first_round_override.as_dict(validate)
                if len(logical_qubit_specification_first_round_override_dict) != 0:
                    specification_dict["logicalQubitSpecificationFirstRoundOverride"] = \
                        logical_qubit_specification_first_round_override_dict

        return specification_dict
