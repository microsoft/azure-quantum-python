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

from azure.quantum.optimization import (
    StreamingProblem,
    Problem,
    ProblemType,
    Term,
)
from common import QuantumTestBase


class TestStreamingProblem(QuantumTestBase):
    
    def __test_upload_problem(
        self,
        count: int,
        terms_thresh: int,
        size_thresh: int,
        compress: bool,
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
        sProblem.compress = compress

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

    def __kwarg_or_value(self, kwarg, name, default):
        if name in kwarg:
            return kwarg[name]

        return default


    def test_streaming_problem_small_chunks(self):
        self.__test_upload_problem(4, 1, 1, False)


    def test_streaming_problem_large_chunks(self):
        self.__test_upload_problem(4, 1000, 10e6, False)


    def test_streaming_problem_small_chunks_compressed(self):
        self.__test_upload_problem(4, 1, 1, True)


    def test_streaming_problem_large_chunks_compressed(self):
        self.__test_upload_problem(4, 1000, 10e6, True)


    def test_streaming_problem_pubo(self):
        self.__test_upload_problem(4, 1, 1, False, ProblemType.pubo)

    def test_streaming_problem_initial_terms(self):
        self.__test_upload_problem(
            4,
            1,
            1,
            False,
            initial_terms=[
                Term(w=10, indices=[0, 1, 2]),
                Term(w=20, indices=[1, 2, 3]),
            ],
            avg_coupling=(4 * 2 + 6) / 6,
            max_coupling=3,
        )

    def check_all(self):
        self.test_streaming_problem_small_chunks()
        self.test_streaming_problem_large_chunks()
        self.test_streaming_problem_small_chunks_compressed()
        self.test_streaming_problem_large_chunks_compressed()
        self.test_streaming_problem_pubo()
        self.test_streaming_problem_initial_terms()


if __name__ == "__main__":
    unittest.main()
