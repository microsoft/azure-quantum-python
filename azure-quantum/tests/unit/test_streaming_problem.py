#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_streaming_problem.py: Checks correctness of azure.quantum.StreamingProblem.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import unittest
import json
from typing import List
import pytest

from azure.quantum.optimization import (
    StreamingProblem,
    Problem,
    ProblemType,
    Term,
)
from azure.quantum.storage import download_blob
from common import QuantumTestBase


class TestStreamingProblem(QuantumTestBase):
    
    def __test_upload_problem(
        self,
        count: int,
        terms_thresh: int,
        size_thresh: int,
        problem_type: ProblemType = ProblemType.ising,
        initial_terms: List[Term] = [],
        **kwargs
    ):
        if not (self.in_recording or self.is_live):
            # Temporarily disabling this test in playback mode 
            # due to multiple calls to the storage API
            # that need to have a request id to distinguish
            # them while playing back
            print("Skipping this test in playback mode")
            return

        ws = self.create_workspace()

        sProblem = StreamingProblem(
            ws, name="test", problem_type=problem_type, terms=initial_terms
        )
        rProblem = Problem(
            "test", problem_type=problem_type, terms=initial_terms
        )
        sProblem.upload_terms_threshold = terms_thresh
        sProblem.upload_size_threshold = size_thresh 

        for i in range(count):
            sProblem.add_term(c=i, indices=[i, i + 1])
            rProblem.add_term(c=i, indices=[i, i + 1])

        self.assertEqual(problem_type, sProblem.problem_type)
        self.assertEqual(problem_type.name, sProblem.stats["type"])
        self.assertEqual(
            count + len(initial_terms), sProblem.stats["num_terms"]
        )
        self.assertEqual(
            self.__kwarg_or_value(kwargs, "avg_coupling", 2),
            sProblem.stats["avg_coupling"],
        )
        self.assertEqual(
            self.__kwarg_or_value(kwargs, "max_coupling", 2),
            sProblem.stats["max_coupling"],
        )
        self.assertEqual(
            self.__kwarg_or_value(kwargs, "min_coupling", 2),
            sProblem.stats["min_coupling"],
        )

        uri = sProblem.upload(ws)
        uploaded = json.loads(sProblem.download().serialize())
        local = json.loads(rProblem.serialize())
        self.assertEqual(uploaded, local)

    def __test_upload_problem_with_init_config(
        self,
        problem_type: ProblemType = ProblemType.ising,
        initial_terms: List[Term] = [],
        initial_config: Dict[str, int] = None,
        **kwargs
    ):
        if not (self.in_recording or self.is_live):
            # Temporarily disabling this test in playback mode 
            # due to multiple calls to the storage API
            # that need to have a request id to distinguish
            # them while playing back
            print("Skipping this test in playback mode")
            return

        ws = self.create_workspace()

        sProblem = StreamingProblem(
            ws, name="test", problem_type=problem_type, terms=initial_terms
        )
        cProblem = StreamingProblem(
            "test", problem_type=problem_type, terms=initial_terms, init_config=initial_config
        )

        self.assertEqual(problem_type, sProblem.problem_type)
        self.assertEqual(problem_type, cProblem.problem_type)
        self.assertEqual(problem_type.name, sProblem.stats["type"])
        self.assertEqual(problem_type.name, cProblem.stats["type"])
        self.assertEqual(len(initial_terms), sProblem.stats["num_terms"])
        self.assertEqual(len(initial_terms), cProblem.stats["num_terms"])

        uri = cProblem.upload(ws)
        uploaded = json.loads(cProblem.download().serialize())
        local = json.loads(cProblem.serialize())
        self.assertEqual(uploaded, local)

    def __kwarg_or_value(self, kwarg, name, default):
        if name in kwarg:
            return kwarg[name]

        return default


    @pytest.mark.live_test
    def test_streaming_problem_small_chunks(self):
        self.__test_upload_problem(4, 1, 1)


    @pytest.mark.live_test
    def test_streaming_problem_large_chunks(self):
        self.__test_upload_problem(4, 1000, 10e6)


    @pytest.mark.live_test
    def test_streaming_problem_small_chunks_compressed(self):
        self.__test_upload_problem(4, 1, 1)


    @pytest.mark.live_test
    def test_streaming_problem_large_chunks_compressed(self):
        self.__test_upload_problem(4, 1000, 10e6)


    @pytest.mark.live_test
    def test_streaming_problem_pubo(self):
        self.__test_upload_problem(4, 1, 1, ProblemType.pubo)

    @pytest.mark.live_test
    def test_streaming_problem_initial_terms(self):
        self.__test_upload_problem(
            4,
            1,
            1,
            initial_terms=[
                Term(w=10, indices=[0, 1, 2]),
                Term(w=20, indices=[1, 2, 3]),
            ],
            avg_coupling=(4 * 2 + 6) / 6,
            max_coupling=3,
        )

    @pytest.mark.live_test
    def test_upload_streaming_problem_with_initial_config(self):
        self.__test_upload_problem_with_init_config(
            initial_terms=[
                Term(c=-9, indices=[0]),
                Term(c=-3, indices=[1,0]),
                Term(c=5, indices=[2,0])
            ],
            initial_config={'0': -1, '1': 1, '2': 1}
        )

    @pytest.mark.live_test
    def test_upload_streaming_problem_with_initial_config_pubo(self):
        self.__test_upload_problem_with_init_config(
            problem_type=ProblemType.pubo,
            initial_terms=[
                Term(c=-9, indices=[0]),
                Term(c=-3, indices=[1,0]),
                Term(c=5, indices=[2,0])
            ],
            initial_config={'0': 1, '1': 1, '2': 0}
        )

    def check_all(self):
        self.test_streaming_problem_small_chunks()
        self.test_streaming_problem_large_chunks()
        self.test_streaming_problem_small_chunks_compressed()
        self.test_streaming_problem_large_chunks_compressed()
        self.test_streaming_problem_pubo()
        self.test_streaming_problem_initial_terms()
        self.test_upload_streaming_problem_with_initial_config()
        self.test_upload_streaming_problem_with_initial_config_pubo()


if __name__ == "__main__":
    unittest.main()
