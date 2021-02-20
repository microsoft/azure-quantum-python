
#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_problem.py: Checks correctness of azure.quantum.optimization module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

## IMPORTS ##

import json

from azure.quantum import Workspace
from azure.quantum.optimization import Problem, ProblemType, Term
from azure.quantum.optimization.solvers import ParallelTempering, SimulatedAnnealing, HardwarePlatform, QuantumMonteCarlo
from tests.quantum_test_base import QuantumTestBase 

class TestProblem(QuantumTestBase):
    def test_add_terms(self):
        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])
        self.assertEqual(ProblemType.ising, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(w=1, indices=[1, 2]), problem.terms[1])

        more = []
        for i in range(count + 1):
            more.append(Term(w=i, indices=[i, i-1]))
        problem.add_terms(more)
        self.assertEqual((count * 2) + 1, len(problem.terms))
        self.assertEqual(Term(w=count, indices=[count, count - 1]), problem.terms[count * 2])


    def test_provide_terms(self):
        count = 4
        terms = []
        for i in range(count):
            terms.append(Term(w=i, indices=[i, i+1]))
        problem = Problem(name="test", terms=terms, problem_type=ProblemType.pubo)

        self.assertEqual(ProblemType.pubo, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])


    def test_add_terms_cterms(self):
        problem = Problem(name="test")
        count = 4

        for i in range(count):
            problem.add_term(c=i, indices=[i, i+1])
        self.assertEqual(ProblemType.ising, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

        more = []
        for i in range(count + 1):
            more.append(Term(c=i, indices=[i, i-1]))
        problem.add_terms(more)
        self.assertEqual((count * 2) + 1, len(problem.terms))
        self.assertEqual(Term(c=count, indices=[count, count - 1]), problem.terms[count * 2])


    def test_provide_cterms(self):
        count = 4
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i+1]))
        problem = Problem(name="test", terms=terms, problem_type=ProblemType.pubo)

        self.assertEqual(ProblemType.pubo, problem.problem_type)
        self.assertEqual(count, len(problem.terms))
        self.assertEqual(Term(c=1, indices=[1, 2]), problem.terms[1])

        
    def test_serialization_cterms(self):
        count = 2
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i+1]))
        problem = Problem(name="test", terms=terms)

        expected = json.dumps({
            "cost_function": {
                "version": "1.0",
                "type":  "ising",
                "terms": [ { 'c':0, 'ids':[0, 1] }, {'c':1, 'ids':[1, 2]} ],
            }
        })
        print(problem.serialize())
        actual = problem.serialize()
        self.assertEqual(expected, actual)
    
    def test_serialization_init_config(self):
        count = 2
        terms = []
        for i in range(count):
            terms.append(Term(c=i, indices=[i, i+1]))
        init_config = {"0":-1 , "1": 1, "2": -1}
        problem = Problem(name="test", terms=terms, init_config=init_config)

        expected = json.dumps({
            "cost_function": {
                "version": "1.1",
                "type":  "ising",
                "terms": [ { 'c':0, 'ids':[0, 1] }, {'c':1, 'ids':[1, 2]} ],
                "initial_configuration": {"0":-1 , "1": 1, "2": -1},
            }
        })
        actual = problem.serialize()
        self.assertEqual(expected, actual)


def _init_ws_():
    return Workspace(
        subscription_id="subs_id", 
        resource_group="rg",
        name="n",
        storage=None
    )

class TestSolvers(QuantumTestBase):

    def test_available_solvers(self):
        ws = _init_ws_()

        self.assertIsNotNone(SimulatedAnnealing(ws))
        self.assertIsNotNone(ParallelTempering(ws))


    def test_input_params(self):
        ws = _init_ws_()

        s2_params = SimulatedAnnealing(ws).params
        self.assertEqual({ }, s2_params["params"])

        s2_params = SimulatedAnnealing(ws, timeout=1010).params
        self.assertEqual({ "timeout": 1010 }, s2_params["params"])

        p3_params = ParallelTempering(ws, sweeps=2024, all_betas=[3, 4, 5]).params
        self.assertEqual({ "all_betas": [3, 4, 5], "replicas": 3, "sweeps": 2024 }, p3_params["params"])
        
        s3_params = SimulatedAnnealing(ws, beta_start=3.2, sweeps=12).params
        self.assertEqual({ "beta_start": 3.2, "sweeps": 12 }, s3_params["params"])


    def test_ParallelTempering_input_params(self):
        ws = _init_ws_()

        good = ParallelTempering(ws, timeout=1011)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering-parameterfree.cpu", good.target)
        self.assertEqual({ "timeout": 1011 }, good.params["params"])

        good = ParallelTempering(ws, seed=20)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering-parameterfree.cpu", good.target)
        self.assertEqual({ "seed": 20 }, good.params["params"])

        good = ParallelTempering(ws, sweeps=20, replicas=3, all_betas=[3,5,9])
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering.cpu", good.target)
        self.assertEqual({ "sweeps": 20, "replicas": 3, "all_betas":[3,5,9] }, good.params["params"])

        good = ParallelTempering(ws, sweeps=20, all_betas=[3,9])
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.paralleltempering.cpu", good.target)
        self.assertEqual({ "sweeps": 20, "replicas": 2, "all_betas":[3,9] }, good.params["params"])
        
        with self.assertRaises(ValueError):
            _ = ParallelTempering(ws, sweeps=20, replicas=3, all_betas=[1,3,5,7,9])
            
    def test_SimulatedAnnealing_input_params(self):
        ws = _init_ws_()

        good = SimulatedAnnealing(ws, timeout=1011, seed=4321)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing-parameterfree.cpu", good.target)
        self.assertEqual({ "timeout": 1011, "seed": 4321 }, good.params["params"])

        good = SimulatedAnnealing(ws, timeout=1011, seed=4321, platform=HardwarePlatform.FPGA)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing-parameterfree.fpga", good.target)
        self.assertEqual({ "timeout": 1011, "seed": 4321 }, good.params["params"])

        good = SimulatedAnnealing(ws, beta_start=21)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing.cpu", good.target)
        self.assertEqual({ "beta_start": 21 }, good.params["params"])
        
        good = SimulatedAnnealing(ws, beta_start=21, platform=HardwarePlatform.FPGA)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.simulatedannealing.fpga", good.target)
        self.assertEqual({ "beta_start": 21 }, good.params["params"])
    
    def test_QuantumMonteCarlo_input_params(self):
        ws = _init_ws_()
        good = QuantumMonteCarlo(ws,trotter_number=100,seed=4321)
        self.assertIsNotNone(good)
        self.assertEqual("microsoft.qmc.cpu",good.target)
        self.assertEqual({"trotter_number":100,"seed":4321},good.params["params"])


# TODO AB#11076: Add tests for:
#  * [ ] Problem upload
#  * [ ] Solvers.optimize
#  * [ ] Job
#  * [ ] Workspace

if __name__ == "__main__":
    unittest.main()
