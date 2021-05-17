#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_problem.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import json
import unittest
from azure.quantum import Workspace
from azure.quantum.optimization import Problem, ProblemType, Term
from azure.quantum.optimization.solvers import (
    ParallelTempering,
    PopulationAnnealing,
    RangeSchedule,
    SimulatedAnnealing,
    HardwarePlatform,
    QuantumMonteCarlo,
    SubstochasticMonteCarlo,
)
from common import QuantumTestBase


class TestProblem(QuantumTestBase):
    def test_add_terms(self):
        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i + 1])
        self.assertEqual(ProblemType.ising, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(w=1, indices=[1, 2]), problem.terms[1])

        more = []
        for i in range(count + 1):
            more.append(Term(w=i, indices=[i, i - 1]))
        problem.add_terms(more)
        self.assertEqual((count * 2) + 1, len(problem.terms))
        self.assertEqual(
            Term(w=count, indices=[count, count - 1]), problem.terms[count * 2]
        )

    def test_provide_terms(self):
        count = 4
        terms = []
        for i in range(count):
            terms.append(Term(w=i, indices=[i, i + 1]))
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )

        self.assertEqual(ProblemType.pubo, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

    def test_add_terms_cterms(self):
        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i + 1])
        self.assertEqual(ProblemType.ising, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

        more = []
        for i in range(count + 1):
            more.append(Term(c=i, indices=[i, i - 1]))
        problem.add_terms(more)
        self.assertEqual((count * 2) + 1, len(problem.terms))
        self.assertEqual(
            Term(c=count, indices=[count, count - 1]), problem.terms[count * 2]
        )

    def test_provide_cterms(self):
        count = 4
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i + 1]))
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )

        self.assertEqual(ProblemType.pubo, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

    def test_serialization_cterms(self):
        count = 2
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i + 1]))
        problem = Problem(name="test", terms=terms)

        expected = json.dumps(
            {
                "cost_function": {
                    "version": "1.0",
                    "type": "ising",
                    "terms": [
                        {"c": 0, "ids": [0, 1]},
                        {"c": 1, "ids": [1, 2]},
                    ],
                }
            }
        )
        print(problem.serialize())
        actual = problem.serialize()
        self.assertEqual(expected, actual)

    def test_serialization_init_config(self):
        count = 2
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i + 1]))
        init_config = {"0": -1, "1": 1, "2": -1}
        problem = Problem(name="test", terms=terms, init_config=init_config)

        expected = json.dumps(
            {
                "cost_function": {
                    "version": "1.1",
                    "type": "ising",
                    "terms": [
                        {"c": 0, "ids": [0, 1]},
                        {"c": 1, "ids": [1, 2]},
                    ],
                    "initial_configuration": {"0": -1, "1": 1, "2": -1},
                }
            }
        )
        actual = problem.serialize()
        self.assertEqual(expected, actual)

    def test_deserialize(self):
        count = 2
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i + 1]))
        problem = Problem(name="test", terms=terms)
        deserialized = Problem.deserialize(problem.serialize(), problem.name)
        self.assertEqual(problem.name, deserialized.name)
        self.assertEqual(problem.problem_type, deserialized.problem_type)
        self.assertEqual(count, len(deserialized.terms))
        self.assertEqual(problem.init_config, deserialized.init_config)
        self.assertEqual(Term(c=0, indices=[0, 1]), problem.terms[0])
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

    def test_deserialize_init_config(self):
        count = 2
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i + 1]))
        init_config = {"0": -1, "1": 1, "2": -1}
        problem = Problem(name="test", terms=terms, init_config=init_config)
        deserialized = Problem.deserialize(problem.serialize(), problem.name)
        self.assertEqual(problem.name, deserialized.name)
        self.assertEqual(problem.problem_type, deserialized.problem_type)
        self.assertEqual(count, len(deserialized.terms))
        self.assertEqual(problem.init_config, deserialized.init_config)
        self.assertEqual(Term(c=0, indices=[0, 1]), problem.terms[0])
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

    def test_problem_evaluate(self):
        terms = []
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        self.assertEqual(0, problem.evaluate({}))
        self.assertEqual(0, problem.evaluate({"0": 1}))

        terms = [Term(c=10, indices=[0, 1, 2])]
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        self.assertEqual(0, problem.evaluate({"0": 0, "1": 1, "2": 1}))
        self.assertEqual(10, problem.evaluate({"0": 1, "1": 1, "2": 1}))

        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.ising
        )
        self.assertEqual(-10, problem.evaluate({"0": -1, "1": 1, "2": 1}))
        self.assertEqual(10, problem.evaluate({"0": -1, "1": -1, "2": 1}))

        terms = [Term(c=10, indices=[0, 1, 2]), Term(c=-5, indices=[1, 2])]
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        self.assertEqual(-5, problem.evaluate({"0": 0, "1": 1, "2": 1}))
        self.assertEqual(5, problem.evaluate({"0": 1, "1": 1, "2": 1}))

        terms = [Term(c=10, indices=[])]  # constant term
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        self.assertEqual(10, problem.evaluate({}))

    def test_problem_fixed_variables(self):
        terms = []
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        problem_new = problem.set_fixed_variables({"0": 1})
        self.assertEqual([], problem_new.terms)

        # test small cases
        terms = [Term(c=10, indices=[0, 1, 2]), Term(c=-5, indices=[1, 2])]
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        self.assertEqual([], problem.set_fixed_variables({"1": 0}).terms)
        self.assertEqual(
            [Term(c=10, indices=[0]), Term(c=-5, indices=[])],
            problem.set_fixed_variables({"1": 1, "2": 1}).terms,
        )

        # test all const terms get merged
        self.assertEqual(
            [Term(c=5, indices=[])],
            problem.set_fixed_variables({"0": 1, "1": 1, "2": 1}).terms,
        )

        # test init_config gets transferred
        problem = Problem(
            "My Problem", terms=terms, init_config={"0": 1, "1": 1, "2": 1}
        )
        problem2 = problem.set_fixed_variables({"0": 0})
        self.assertEqual({"1": 1, "2": 1}, problem2.init_config)

    def test_problem_large(self):
        problem = Problem(name="test", terms=[], problem_type=ProblemType.pubo)
        self.assertTrue(not problem.is_large())

        problem.add_term(5.0, [])
        self.assertTrue(not problem.is_large())

        problem.add_term(6.0, list(range(3000)))
        self.assertTrue(not problem.is_large())

        problem.add_terms(
            [Term(indices=[9999], c=1.0)] * int(1e6)
        )  # create 1mil dummy terms
        self.assertTrue(problem.is_large())


def _init_ws_():
    return Workspace(
        subscription_id="subs_id", resource_group="rg", name="n", storage=None
    )


class TestSolvers(QuantumTestBase):
    def test_available_solvers(self):
        ws = _init_ws_()

        self.assertIsNotNone(SimulatedAnnealing(ws))
        self.assertIsNotNone(ParallelTempering(ws))

    def test_input_params(self):
        ws = _init_ws_()

        s2_params = SimulatedAnnealing(ws).params
        self.assertEqual({}, s2_params["params"])

        s2_params = SimulatedAnnealing(ws, timeout=1010).params
        self.assertEqual({"timeout": 1010}, s2_params["params"])

        p3_params = ParallelTempering(
            ws, sweeps=2024, all_betas=[3, 4, 5]
        ).params
        self.assertEqual(
            {"all_betas": [3, 4, 5], "replicas": 3, "sweeps": 2024},
            p3_params["params"],
        )

        s3_params = SimulatedAnnealing(ws, beta_start=3.2, sweeps=12).params
        self.assertEqual(
            {"beta_start": 3.2, "sweeps": 12}, s3_params["params"]
        )

    def test_ParallelTempering_input_params(self):
        ws = _init_ws_()

        good = ParallelTempering(ws, timeout=1011)
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.paralleltempering-parameterfree.cpu", good.target
        )
        self.assertEqual({"timeout": 1011}, good.params["params"])

        good = ParallelTempering(ws, seed=20)
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.paralleltempering-parameterfree.cpu", good.target
        )
        self.assertEqual({"seed": 20}, good.params["params"])

        good = ParallelTempering(
            ws, sweeps=20, replicas=3, all_betas=[3, 5, 9]
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering.cpu", good.target)
        self.assertEqual(
            {"sweeps": 20, "replicas": 3, "all_betas": [3, 5, 9]},
            good.params["params"],
        )

        good = ParallelTempering(ws, sweeps=20, all_betas=[3, 9])
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering.cpu", good.target)
        self.assertEqual(
            {"sweeps": 20, "replicas": 2, "all_betas": [3, 9]},
            good.params["params"],
        )

        with self.assertRaises(ValueError):
            _ = ParallelTempering(
                ws, sweeps=20, replicas=3, all_betas=[1, 3, 5, 7, 9]
            )

    def test_SimulatedAnnealing_input_params(self):
        ws = _init_ws_()

        good = SimulatedAnnealing(ws, timeout=1011, seed=4321)
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.simulatedannealing-parameterfree.cpu", good.target
        )
        self.assertEqual(
            {"timeout": 1011, "seed": 4321}, good.params["params"]
        )

        good = SimulatedAnnealing(
            ws, timeout=1011, seed=4321, platform=HardwarePlatform.FPGA
        )
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.simulatedannealing-parameterfree.fpga", good.target
        )
        self.assertEqual(
            {"timeout": 1011, "seed": 4321}, good.params["params"]
        )

        good = SimulatedAnnealing(ws, beta_start=21)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing.cpu", good.target)
        self.assertEqual({"beta_start": 21}, good.params["params"])

        good = SimulatedAnnealing(
            ws, beta_start=21, platform=HardwarePlatform.FPGA
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing.fpga", good.target)
        self.assertEqual({"beta_start": 21}, good.params["params"])

    def test_QuantumMonteCarlo_input_params(self):
        ws = _init_ws_()
        good = QuantumMonteCarlo(ws, trotter_number=100, seed=4321)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.qmc.cpu", good.target)
        self.assertEqual(
            {"trotter_number": 100, "seed": 4321}, good.params["params"]
        )

    def test_PopulationAnnealing_input_params(self):
        ws = _init_ws_()
        beta = RangeSchedule("linear", 0.8, 5.8)
        good = PopulationAnnealing(
            ws,
            alpha=100,
            seed=8888,
            population=300,
            sweeps=1000,
            culling_fraction=0.5,
            beta=beta,
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.populationannealing.cpu", good.target)
        self.assertEqual(8888, good.params["params"]["seed"])
        self.assertEqual(100.0, good.params["params"]["alpha"])
        self.assertEqual(300, good.params["params"]["population"])
        self.assertEqual(1000, good.params["params"]["sweeps"])
        self.assertEqual(0.5, good.params["params"]["culling_fraction"])
        self.assertEqual(
            {"type": "linear", "initial": 0.8, "final": 5.8},
            good.params["params"]["beta"],
        )

    def test_SubstochasticMonteCarlo_input_params(self):
        ws = _init_ws_()
        beta = RangeSchedule("linear", 2.8, 15.8)
        alpha = RangeSchedule("geometric", 1.8, 2.8)
        good = SubstochasticMonteCarlo(
            ws,
            alpha=alpha,
            seed=1888,
            target_population=3000,
            step_limit=1000,
            steps_per_walker=5,
            beta=beta,
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.substochasticmontecarlo.cpu", good.target)
        self.assertEqual(1888, good.params["params"]["seed"])
        self.assertEqual(
            {"type": "geometric", "initial": 1.8, "final": 2.8},
            good.params["params"]["alpha"],
        )
        self.assertEqual(3000, good.params["params"]["target_population"])
        self.assertEqual(1000, good.params["params"]["step_limit"])
        self.assertEqual(5, good.params["params"]["steps_per_walker"])
        self.assertEqual(
            {"type": "linear", "initial": 2.8, "final": 15.8},
            good.params["params"]["beta"],
        )

    def test_SSMC_bad_input_params(self):
        bad_range = None
        with self.assertRaises(ValueError) as context:
            bad_range = RangeSchedule("nothing", 2.8, 15.8)
        self.assertTrue(
            '"schedule_type" can only be' in str(context.exception)
        )
        self.assertTrue(bad_range is None)
        beta = 1
        alpha = 2
        ws = _init_ws_()
        bad_solver = None
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                alpha=alpha,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                steps_per_walker=5,
                beta=beta,
            )
        self.assertTrue(
            'can only be from class "RangeSchedule"!' in str(context.exception)
        )
        self.assertTrue(bad_solver is None)

        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                steps_per_walker=-1,
            )
        self.assertTrue("must be positive" in str(context.exception))
        self.assertTrue(bad_solver is None)

    def test_PA_bad_input_params(self):
        beta = 1
        ws = _init_ws_()
        bad_solver = None
        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=300,
                sweeps=1000,
                culling_fraction=0.5,
                beta=beta,
            )
        self.assertTrue(
            'can only be from class "RangeSchedule"!' in str(context.exception)
        )
        self.assertTrue(bad_solver is None)

        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=-300,
                sweeps=1000,
                culling_fraction=0.5,
            )
        self.assertTrue("must be positive" in str(context.exception))
        self.assertTrue(bad_solver is None)

        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws, alpha=0.2, seed=8888, sweeps=1000, culling_fraction=0.5
            )
        self.assertTrue("can not be smaller than" in str(context.exception))
        self.assertTrue(bad_solver is None)


# TODO AB#11076: Add tests for:
#  * [ ] Problem upload
#  * [ ] Solvers.optimize
#  * [ ] Job
#  * [ ] Workspace

if __name__ == "__main__":
    unittest.main()
