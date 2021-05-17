#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_problem.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import unittest
import json
import os
import pytest
from typing import List

from azure.quantum import Workspace
from azure.quantum.optimization import (
    StreamingProblem,
    Problem,
    ProblemType,
    Term,
)
from azure.quantum.storage import download_blob
from integration_test_util import create_workspace


class TestStreamingProblem(unittest.TestCase):
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
        ws = create_workspace()
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

    @pytest.mark.skip(reason="No live-test infra available yet")
    def test_small_chunks(self):
        self.__test_upload_problem(4, 1, 1, False)

    @pytest.mark.skip(reason="No live-test infra available yet")
    def test_large_chunks(self):
        self.__test_upload_problem(4, 1000, 10e6, False)

    @pytest.mark.skip(reason="No live-test infra available yet")
    def test_small_chunks_compressed(self):
        self.__test_upload_problem(4, 1, 1, True)

    @pytest.mark.skip(reason="No live-test infra available yet")
    def test_large_chunks_compressed(self):
        self.__test_upload_problem(4, 1000, 10e6, True)

    @pytest.mark.skip(reason="No live-test infra available yet")
    def test_pubo(self):
        self.__test_upload_problem(4, 1, 1, False, ProblemType.pubo)

    @pytest.mark.skip(reason="No live-test infra available yet")
    def test_initial_terms(self):
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
        self.test_small_chunks()
        self.test_large_chunks()
        self.test_small_chunks_compressed()
        self.test_large_chunks_compressed()
        self.test_pubo()
        self.test_initial_terms()


if __name__ == "__main__":
    # Our test infra is not quite ready to run tests against a live service
    # To run these tests follow the README.md from the integration tests folder
    # unittest.main()

    tests = TestStreamingProblem()
    tests.check_all()
