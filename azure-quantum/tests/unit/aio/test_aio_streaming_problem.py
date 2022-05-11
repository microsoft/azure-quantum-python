#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_streaming_problem.py: Checks correctness of azure.quantum.StreamingProblem.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import json
from typing import List

from azure.quantum.aio.optimization import (
    Problem,
    ProblemType,
    StreamingProblem
)
from azure.quantum.optimization import Term
from common import QuantumTestBase


class TestStreamingProblem(QuantumTestBase):
    
    async def __test_upload_problem(
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

        ws = self.create_async_workspace()

        sProblem = await StreamingProblem.create(
            ws, name="test", problem_type=problem_type, terms=initial_terms
        )
        rProblem = Problem(
            "test", problem_type=problem_type, terms=initial_terms
        )
        sProblem.upload_terms_threshold = terms_thresh
        sProblem.upload_size_threshold = size_thresh

        for i in range(count):
            await sProblem.add_term(c=i, indices=[i, i + 1])
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

        uri = await sProblem.upload(ws)
        data = await sProblem.download()
        uploaded = json.loads(data.serialize())
        local = json.loads(rProblem.serialize())
        self.assertEqual(uploaded, local)

    def __kwarg_or_value(self, kwarg, name, default):
        if name in kwarg:
            return kwarg[name]

        return default

    def test_streaming_problem_small_chunks(self):
        self.get_async_result(self.__test_upload_problem(4, 1, 1))

    def test_streaming_problem_large_chunks(self):
        self.get_async_result(self.__test_upload_problem(4, 1000, 10e6))

    def test_streaming_problem_pubo(self):
        self.get_async_result(self.__test_upload_problem(4, 1, 1, ProblemType.pubo))

    def test_streaming_problem_initial_terms(self):
        self.get_async_result( self.__test_upload_problem(
            4,
            1,
            1,
            initial_terms=[
                Term(w=10, indices=[0, 1, 2]),
                Term(w=20, indices=[1, 2, 3]),
            ],
            avg_coupling=(4 * 2 + 6) / 6,
            max_coupling=3,
        ) )

    def check_all(self):
        self.test_streaming_problem_small_chunks()
        self.test_streaming_problem_large_chunks()
        self.test_streaming_problem_pubo()
        self.test_streaming_problem_initial_terms()
