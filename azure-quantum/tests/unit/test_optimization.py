#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_optimization.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import json
import unittest

from azure.quantum.optimization import Problem, ProblemType, Term, GroupType, SlcTerm
from azure.quantum.target.solvers import HardwarePlatform, RangeSchedule
from azure.quantum.target import (
    ParallelTempering,
    PopulationAnnealing,
    SimulatedAnnealing,
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
        for i in range(1,count+1):
            more.append(Term(c=i, indices=[i-1, i]))
        problem.add_terms(more)
        self.assertEqual(2*count, len(problem.terms))
        self.assertEqual(
            Term(c=count, indices=[count-1, count]), problem.terms[-1]
        )

        subterms = [Term(c=1, indices=[i]) for i in range(count)]
        subterms.append(Term(c=-5, indices=[]))
        problem.add_slc_term(terms=[(1, i) for i in range(count)] + [(-5, None)], c=2)
        self.assertEqual(2*count, len(problem.terms))
        self.assertEqual(1, len(problem.terms_slc))
        self.assertEqual(
            SlcTerm(subterms, c=2),
            problem.terms_slc[-1]
        )

        problem.add_terms(subterms, term_type=GroupType.squared_linear_combination, c=2)
        self.assertEqual(2*count, len(problem.terms))
        self.assertEqual(2, len(problem.terms_slc))
        self.assertEqual(
            SlcTerm(subterms, c=2),
            problem.terms_slc[-1]
        )

        problem.add_terms(subterms, term_type=GroupType.combination, c=0.5)
        self.assertEqual(3*count + 1, len(problem.terms))
        self.assertEqual(
            [Term(subterm.ids, c=subterm.c) for subterm in subterms],
            problem.terms[-len(subterms):]
        )

        problem.add_slc_term(subterms, c=3)
        self.assertEqual(3*count + 1, len(problem.terms))
        self.assertEqual(3, len(problem.terms_slc))
        self.assertEqual(
            SlcTerm(subterms, c=3),
            problem.terms_slc[-1]
        )

    def test_provide_cterms(self):
        count = 4
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i + 1]))
        terms.append(SlcTerm(
            [Term(c=i/2, indices=[i+2]) for i in range(count)] + [Term(c=5, indices=[])],
            c=1)
        )
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )

        self.assertEqual(ProblemType.pubo_grouped, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(1, len(problem.terms_slc))
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

    def test_errant_grouped_terms(self):
        with self.assertRaises(ValueError):
            _ = SlcTerm(
                [Term(c=i+2, indices=[i%2]) for i in range(3)], c=1
            )
        with self.assertRaises(ValueError):
            _ = SlcTerm(
                [Term(c=i+1, indices=[i, i+1]) for i in range(2)], c=1
            )
        with self.assertRaises(ValueError):
            _ = SlcTerm(
                [Term(c=i, indices=[]) for i in range(1,3)], c=1
            )
        

    def test_serialization_cterms(self):
        count = 2
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i + 1]))
        terms.append(
            SlcTerm(
                [Term(c=0, indices=[0]), Term(c=1, indices=[1]), Term(c=-5, indices=[])],
                c=1
            )
        )
        problem = Problem(name="test", terms=terms)

        expected = json.dumps(
            {
                "cost_function": {
                    "version": "1.0",
                    "type": "ising_grouped",
                    "terms": [
                        {"c": 0, "ids": [0, 1]},
                        {"c": 1, "ids": [1, 2]}
                    ],
                    "terms_slc":[
                        {"c": 1, "terms": [
                            {"c": 0, "ids": [0]},
                            {"c": 1, "ids": [1]},
                            {"c": -5, "ids": []}
                        ]}
                    ]
                }
            }
        )
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
        subterms = [Term(c=1, indices=[i]) for i in range(3)]
        subterms.append(Term(c=-2, indices=[]))
        terms.append(
            SlcTerm(subterms, c=1)
        )
        problem = Problem(name="test", terms=terms)
        deserialized = Problem.deserialize(problem.serialize(), problem.name)
        self.assertEqual(problem.name, deserialized.name)
        self.assertEqual(problem.problem_type, deserialized.problem_type)
        self.assertEqual(count + 1, len(deserialized.terms))
        self.assertEqual(problem.init_config, deserialized.init_config)
        self.assertEqual(Term(c=0, indices=[0, 1]), problem.terms[0])
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])
        self.assertEqual(
            SlcTerm(subterms, c=1),
            problem.terms_slc[-1]
        )

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

        terms = [
            Term(c=2, indices=[0, 1, 2]),
            SlcTerm(terms=[
                Term(c=1, indices=[0]),
                Term(c=1, indices=[1]),
                Term(c=1, indices=[2]),
                Term(c=-5, indices=[])
            ], c=3)
        ]
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        self.assertEqual(27, problem.evaluate({"0": 0, "1": 1, "2": 1}))
        self.assertEqual(14, problem.evaluate({"0": 1, "1": 1, "2": 1}))


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

        # test grouped terms
        terms = [
            Term(c=1, indices=[]),
            Term(c=2, indices=[0, 1, 2]),
            SlcTerm(terms=[
                Term(c=1, indices=[0]),
                Term(c=1, indices=[1]),
                Term(c=-5, indices=[])
            ], c=3)
        ]
        problem = Problem(
            name="test", terms=terms, problem_type=ProblemType.pubo
        )
        self.assertEqual(
            [Term(c=30, indices=[])],
            problem.set_fixed_variables({"0": 1, "1": 1, "2": 1}).terms,
        )

        self.assertEqual(
            [
                Term(c=2, indices=[1]),
                Term(c=1, indices=[])
            ],
            problem.set_fixed_variables({"0": 1, "2": 1}).terms,
        )

        self.assertEqual(
            [SlcTerm(terms=[
                Term(c=-4, indices=[]),
                Term(c=1, indices=[1])
            ], c=3)],
            problem.set_fixed_variables({"0": 1, "2": 1}).terms_slc,
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

        problem = Problem(name="test", terms=[SlcTerm(
            terms=[Term(indices=[9999], c=1)], c=1
        ) for i in range(int(1e6))], problem_type=ProblemType.pubo)
        self.assertTrue(not problem.is_large())

        problem.add_slc_term([(1.0, i) for i in range(3000)])
        self.assertTrue(problem.is_large())


class TestSolvers(QuantumTestBase):
    def test_available_solvers(self):
        ws = self.create_workspace()

        self.assertIsNotNone(SimulatedAnnealing(ws))
        self.assertIsNotNone(ParallelTempering(ws))

    def test_input_params(self):
        ws = self.create_workspace()

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
        ws = self.create_workspace()

        good = ParallelTempering(ws, timeout=1011)
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.paralleltempering-parameterfree.cpu", good.name
        )
        self.assertEqual({"timeout": 1011}, good.params["params"])

        good = ParallelTempering(ws, seed=20)
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.paralleltempering-parameterfree.cpu", good.name
        )
        self.assertEqual({"seed": 20}, good.params["params"])

        good = ParallelTempering(
            ws, sweeps=20, replicas=3, all_betas=[3, 5, 9]
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering.cpu", good.name)
        self.assertEqual(
            {"sweeps": 20, "replicas": 3, "all_betas": [3, 5, 9]},
            good.params["params"],
        )

        good = ParallelTempering(ws, sweeps=20, all_betas=[3, 9])
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering.cpu", good.name)
        self.assertEqual(
            {"sweeps": 20, "replicas": 2, "all_betas": [3, 9]},
            good.params["params"],
        )

        with self.assertRaises(ValueError):
            _ = ParallelTempering(
                ws, sweeps=20, replicas=3, all_betas=[1, 3, 5, 7, 9]
            )

    def test_SimulatedAnnealing_input_params(self):
        ws = self.create_workspace()

        good = SimulatedAnnealing(ws, timeout=1011, seed=4321)
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.simulatedannealing-parameterfree.cpu", good.name
        )
        self.assertEqual(
            {"timeout": 1011, "seed": 4321}, good.params["params"]
        )

        good = SimulatedAnnealing(
            ws, timeout=1011, seed=4321, platform=HardwarePlatform.FPGA
        )
        self.assertIsNotNone(good)
        self.assertEqual(
            "microsoft.simulatedannealing-parameterfree.fpga", good.name
        )
        self.assertEqual(
            {"timeout": 1011, "seed": 4321}, good.params["params"]
        )

        good = SimulatedAnnealing(ws, beta_start=21)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing.cpu", good.name)
        self.assertEqual({"beta_start": 21}, good.params["params"])

        good = SimulatedAnnealing(
            ws, beta_start=21, platform=HardwarePlatform.FPGA
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing.fpga", good.name)
        self.assertEqual({"beta_start": 21}, good.params["params"])

    def test_QuantumMonteCarlo_input_params(self):
        ws = self.create_workspace()
        good = QuantumMonteCarlo(ws, trotter_number=100, seed=4321)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.qmc.cpu", good.name)
        self.assertEqual(
            {"trotter_number": 100, "seed": 4321}, good.params["params"]
        )

    def test_PopulationAnnealing_input_params(self):
        ws = self.create_workspace()
        beta = RangeSchedule("linear", 0.8, 5.8)
        good = PopulationAnnealing(
            ws,
            alpha=100,
            seed=8888,
            population=300,
            sweeps=1000,
            beta=beta,
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.populationannealing.cpu", good.name)
        self.assertEqual(8888, good.params["params"]["seed"])
        self.assertEqual(100.0, good.params["params"]["alpha"])
        self.assertEqual(300, good.params["params"]["population"])
        self.assertEqual(1000, good.params["params"]["sweeps"])
        self.assertEqual(
            {"type": "linear", "initial": 0.8, "final": 5.8},
            good.params["params"]["beta"],
        )

    def test_SubstochasticMonteCarlo_input_params(self):
        ws = self.create_workspace()
        beta = RangeSchedule("linear", 2.8, 15.8)
        alpha = RangeSchedule("geometric", 2.8, 1.8)
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
        self.assertEqual("microsoft.substochasticmontecarlo.cpu", good.name)
        self.assertEqual(1888, good.params["params"]["seed"])
        self.assertEqual(
            {"type": "geometric", "initial": 2.8, "final": 1.8},
            good.params["params"]["alpha"],
        )
        self.assertEqual(3000, good.params["params"]["target_population"])
        self.assertEqual(1000, good.params["params"]["step_limit"])
        self.assertEqual(5, good.params["params"]["steps_per_walker"])
        self.assertEqual(
            {"type": "linear", "initial": 2.8, "final": 15.8},
            good.params["params"]["beta"],
        )
    
    def test_SubstochasticMonteCarlo_parameter_free(self):
        ws = self.create_workspace()
        good = SubstochasticMonteCarlo(
            ws,
            timeout=10,
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.substochasticmontecarlo-parameterfree.cpu", good.name)
        self.assertEqual(10, good.params["params"]["timeout"])

    def test_SSMC_bad_input_params(self):
        bad_range = None
        with self.assertRaises(ValueError) as context:
            bad_range = RangeSchedule("nothing", 2.8, 15.8)
        self.assertTrue(
            '"schedule_type" must be' in str(context.exception)
        )
        self.assertTrue(bad_range is None)
        beta = 1
        alpha = 2
        ws = self.create_workspace()
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
        print(str(context.exception))
        self.assertTrue(
            ('alpha must be of type RangeSchedule; '
             'found type(alpha)=int') in str(context.exception)
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
        self.assertTrue(
                ("steps_per_walker must be positive; "
                 "found steps_per_walker=-1") in str(context.exception))
        self.assertTrue(bad_solver is None)

        alpha_increasing = RangeSchedule("linear", 1.0, 2.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                alpha=alpha_increasing,
                beta=beta,
            )
        self.assertTrue(
                ("alpha must be decreasing; "
                 "found alpha.initial=1.0 < 2.0=alpha.final.")
                in str(context.exception))
        self.assertTrue(bad_solver is None)

        alpha_negative = RangeSchedule("linear", 1.0, -1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                alpha=alpha_negative,
                beta=beta,
            )
        self.assertTrue(
                ("alpha.final must be greater equal 0; "
                 "found alpha.final=-1.") in str(context.exception))
        self.assertTrue(bad_solver is None)

        alpha_strictly_negative = RangeSchedule("linear", -1.0, -2.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                alpha=alpha_strictly_negative,
                beta=beta,
            )
        self.assertTrue(
                ("alpha.initial must be greater equal 0; "
                 "found alpha.initial=-1.") in str(context.exception))
        self.assertTrue(bad_solver is None)

        alpha = RangeSchedule("linear", 1.0, 0.0)
        beta_decreasing = RangeSchedule("linear", 2.0, 1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                alpha=alpha,
                beta=beta_decreasing,
            )
        self.assertTrue(
                ("beta must be increasing; "
                 "found beta.initial=2.0 > 1.0=beta.final.")
                in str(context.exception))
        self.assertTrue(bad_solver is None)

        beta_zero = RangeSchedule("linear", 0.0, 1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                alpha=alpha,
                beta=beta_zero,
            )
        self.assertTrue(
                ("beta.initial must be greater than 0; "
                 "found beta.initial=0.") in str(context.exception))
        self.assertTrue(bad_solver is None)

        beta_negative = RangeSchedule("linear", -1.0, 1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                alpha=alpha,
                beta=beta_negative,
            )
        self.assertTrue(
                ("beta.initial must be greater than 0; "
                 "found beta.initial=-1.0") in str(context.exception))
        self.assertTrue(bad_solver is None)

        beta_strictly_negative = RangeSchedule("linear", -2.0, -1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = SubstochasticMonteCarlo(
                ws,
                seed=1888,
                target_population=3000,
                step_limit=1000,
                alpha=alpha,
                beta=beta_strictly_negative,
            )
        self.assertTrue(
                ("beta.initial must be greater than 0; "
                 "found beta.initial=-2.0") in str(context.exception))
        self.assertTrue(bad_solver is None)

    def test_PopulationAnnealing_parameter_free(self):
        ws = self.create_workspace()
        good = PopulationAnnealing(
            ws,
            timeout=8,
        )
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.populationannealing-parameterfree.cpu", good.name)
        self.assertEqual(8, good.params["params"]["timeout"])

    def test_PA_bad_input_params(self):
        beta = 1
        ws = self.create_workspace()
        bad_solver = None
        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=300,
                sweeps=1000,
                beta=beta,
            )
        self.assertTrue(
            ("beta must be of type RangeSchedule; "
             "found type(beta)=int.") in str(context.exception)
        )
        self.assertTrue(bad_solver is None)

        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=-300,
                sweeps=1000,
            )
        self.assertTrue("must be positive" in str(context.exception))
        self.assertTrue(bad_solver is None)

        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws, alpha=0.2, seed=8888, sweeps=1000,
            )
        self.assertTrue(
                ("alpha must be greater than 1.0; "
                 "found alpha=0.2.") in str(context.exception))
        self.assertTrue(bad_solver is None)

        beta_decreasing = RangeSchedule("linear", 2.0, 1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=300,
                sweeps=1000,
                beta=beta_decreasing,
            )
        self.assertTrue(
                ("beta must be increasing; "
                 "found beta.initial=2.0 > 1.0=beta.final.")
                in str(context.exception))
        self.assertTrue(bad_solver is None)

        beta_zero = RangeSchedule("linear", 0.0, 1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=300,
                sweeps=1000,
                beta=beta_zero,
            )
        self.assertTrue(
                ("beta.initial must be greater than 0; "
                 "found beta.initial=0.") in str(context.exception))
        self.assertTrue(bad_solver is None)

        beta_negative = RangeSchedule("linear", -1.0, 1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=300,
                sweeps=1000,
                beta=beta_negative,
            )
        self.assertTrue(
                ("beta.initial must be greater than 0; "
                 "found beta.initial=-1.0") in str(context.exception))
        self.assertTrue(bad_solver is None)

        beta_strictly_negative = RangeSchedule("linear", -2.0, -1.0)
        with self.assertRaises(ValueError) as context:
            bad_solver = PopulationAnnealing(
                ws,
                alpha=100,
                seed=8888,
                population=300,
                sweeps=1000,
                beta=beta_strictly_negative,
            )
        self.assertTrue(
                ("beta.initial must be greater than 0; "
                 "found beta.initial=-2.0") in str(context.exception))
        self.assertTrue(bad_solver is None)


if __name__ == "__main__":
    unittest.main()
