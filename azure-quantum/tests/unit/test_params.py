#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_params.py: Tests for input parameters
##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from re import escape
from common import QuantumTestBase
from pytest import raises
from azure.quantum.argument_types import EmptyArray, Pauli, Range, Result
from azure.quantum.target.params import InputParams
from azure.quantum.target.microsoft import MicrosoftEstimatorParams


class TestWorkspace(QuantumTestBase):
    def test_params_empty(self):
        params = InputParams()
        assert params.as_dict() == {}

    def test_params_entry_point(self):
        params = InputParams()
        params.entry_point = "run_program"
        assert params.as_dict() == {"entryPoint": "run_program"}

    def test_params_arguments(self):
        params = InputParams()
        params.arguments["number"] = 12
        assert params.as_dict() == {"arguments": [
            {"name": "number", "value": 12, "type": "Int"}]}

    def test_params_shared_entry_point(self):
        params = InputParams(num_items=2)
        params.entry_point = "run_program"
        params.items[0].arguments["number"] = 8
        params.items[1].arguments["number"] = 16
        assert params.as_dict() == {
            'entryPoint': 'run_program',
            'items': [
                {'arguments': [{'name': 'number', 'value': 8, 'type': 'Int'}]},
                {'arguments': [{'name': 'number', 'value': 16, 'type': 'Int'}]}
            ]}

    def test_params_override_argument(self):
        params = InputParams(num_items=2)
        params.entry_point = "run_program"
        params.arguments["number"] = 8
        params.items[1].arguments["number"] = 16
        assert params.as_dict() == {
            'entryPoint': 'run_program',
            'arguments': [{'name': 'number', 'value': 8, 'type': 'Int'}],
            'items': [{},
                      {'arguments':
                       [{'name': 'number', 'value': 16, 'type': 'Int'}]}]}

    def test_params_file_uris(self):
        params = InputParams(num_items=2)
        params.entry_point = "run_program"
        params.items[0].entry_point = "other_program"
        params.file_uris["base"] = "https://some_link"
        assert params.as_dict() == {
            'entryPoint': 'run_program',
            'items': [{'entryPoint': 'other_program'}, {}],
            'fileUris': {'base': 'https://some_link'}}

    def test_params_for_estimator(self):
        params = MicrosoftEstimatorParams(num_items=2)
        params.entry_point = "run_program"
        params.items[0].entry_point = "other_program"
        params.file_uris["base"] = "https://some_link"
        params.error_budget = 0.23
        assert params.as_dict() == {
            'entryPoint': 'run_program',
            'errorBudget': 0.23,
            'items': [{'entryPoint': 'other_program'}, {}],
            'fileUris': {'base': 'https://some_link'}}

    def test_input_argument_simple_types(self):
        params = InputParams()
        params.arguments["bitwidth"] = 42
        params.arguments["alpha"] = 0.123
        params.arguments["depthOptimal"] = True
        params.arguments["method"] = "qft"
        params.arguments["basis"] = Pauli.X
        params.arguments["expected"] = Result.Zero

        expected = {
            "arguments": [
                {"name": "bitwidth", "type": "Int", "value": 42},
                {"name": "alpha", "type": "Double", "value": 0.123},
                {"name": "depthOptimal", "type": "Boolean", "value": True},
                {"name": "method", "type": "String", "value": "qft"},
                {"name": "basis", "type": "Pauli", "value": "PauliX"},
                {"name": "expected", "type": "Result", "value": False},
            ]
        }

        assert params.as_dict() == expected

    def test_input_argument_complex_types(self):
        params = InputParams()
        params.arguments["range"] = Range(0, 10, step=2)
        params.arguments["loop"] = Range(-10, 10)
        params.arguments["numbers"] = [1, 2, 3]
        params.arguments["bases"] = [Pauli.I, Pauli.X, Pauli.Y, Pauli.Z]
        params.arguments["results"] = [Result.Zero, Result.One]
        params.arguments["empty"] = EmptyArray(int)

        expected = {
            "arguments": [
                {"name": "range", "type": "Range",
                 "value": {"start": 0, "end": 10, "step": 2}},
                {"name": "loop", "type": "Range",
                 "value": {"start": -10, "end": 10}},
                {"name": "numbers", "type": "Array", "elementType": "Int",
                 "value": [1, 2, 3]},
                {"name": "bases", "type": "Array", "elementType": "Pauli",
                 "value": ["PauliI", "PauliX", "PauliY", "PauliZ"]},
                {"name": "results", "type": "Array", "elementType": "Result",
                 "value": [False, True]},
                {"name": "empty", "type": "Array", "elementType": "Int",
                 "value": []}
            ]
        }

        assert params.as_dict() == expected

    def test_input_params_wrong_input(self):
        params = InputParams()

        with raises(TypeError, match="Unsupported type complex for 1j"):
            params.arguments["complex"] = 1j

        message = "Use EmptyArray(type) to assign an empty error"
        with raises(ValueError, match=escape(message)):
            params.arguments["numbers"] = []

        with raises(TypeError, match="All elements in a list must have the "
                                     "same type"):
            params.arguments["mixed"] = [1, True]

        with raises(TypeError, match="Nested lists are not supported"):
            params.arguments["nested"] = [[1, 2, 3], [4, 5, 6]]
