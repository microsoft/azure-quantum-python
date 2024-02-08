##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import unittest
from azure.quantum.workspace import Workspace
import pytest
import numpy as np

from cirq import ParamResolver

from azure.quantum.job.job import Job
from azure.quantum.cirq import AzureQuantumService
from azure.quantum.cirq.targets.target import Target

from common import QuantumTestBase, ONE_UID, DEFAULT_TIMEOUT_SECS


class TestCirq(QuantumTestBase):
    mock_create_job_id_name = "create_job_id"

    def get_test_job_id(self):
        return ONE_UID if self.is_playback \
               else Job.create_job_id()

    def _3_qubit_ghz_cirq(self):
        import cirq

        # Create qubits
        q0 = cirq.LineQubit(0)
        q1 = cirq.LineQubit(1)
        q2 = cirq.LineQubit(2)

        # Create a circuit
        circuit = cirq.Circuit(
            cirq.H(q0),  # H gate
            cirq.CNOT(q0, q1),
            cirq.CNOT(q1, q2),
            cirq.measure(q0, key='q0'),
            cirq.measure(q1, key='q1'),
            cirq.measure(q2, key='q2'),
        )

        return circuit

    def test_plugins_cirq_user_agent(self):
        # VCR is incompatible with parametrized tests
        for app_id in [
            "test-user-agent",
            "test-very-very-very-very-very-very-very-very-long-user-agent"
        ]:
            workspace = self.create_workspace(user_agent=app_id)
            service = AzureQuantumService(workspace=workspace)
            self.assertIn(app_id, service._workspace.user_agent)
            self.assertIn("-azure-quantum-cirq", service._workspace.user_agent)

    def test_cirq_service_init_with_workspace_not_raises_deprecation(self):
        # testing warning according to https://docs.python.org/3/library/warnings.html#testing-warnings
        import warnings
                
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Try to trigger a warning.
            workspace = Workspace(resource_id = "/subscriptions/00000000-0000-0000-0000-00000000000/resourceGroups/rg-test/providers/Microsoft.Quantum/Workspaces/test",
                    location = "<region>")
            AzureQuantumService(workspace)

            # Verify
            assert len(w) == 0

    def test_cirq_service_init_without_workspace_raises_deprecation(self):
        # testing warning according to https://docs.python.org/3/library/warnings.html#testing-warnings
        import warnings
                
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Try to trigger a warning.
            AzureQuantumService(
                    resource_id = "/subscriptions/00000000-0000-0000-0000-00000000000/resourceGroups/rg-test/providers/Microsoft.Quantum/Workspaces/test",
                    location = "<region>")
            # Verify
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "Consider passing \"workspace\" argument explicitly" in str(w[-1].message)

        # Validate rising deprecation warning even if workspace is passed, but other parameters are also passed
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Try to trigger a warning.
            workspace = Workspace(resource_id = "/subscriptions/00000000-0000-0000-0000-00000000000/resourceGroups/rg-test/providers/Microsoft.Quantum/Workspaces/test",
                    location = "<region>")
            AzureQuantumService(
                    workspace=workspace,
                    resource_id = "/subscriptions/00000000-0000-0000-0000-00000000000/resourceGroups/rg-test/providers/Microsoft.Quantum/Workspaces/test",
                    location = "<region>")
            # Verify
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "Consider passing \"workspace\" argument explicitly" in str(w[-1].message)

    @pytest.mark.quantinuum
    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_cirq_get_targets(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        self.assertIn("azure-quantum-cirq", service._workspace.user_agent)
        targets = service.targets()
        target_names = [t.name for t in targets]
        for t in targets:
            self.assertIsInstance(t, Target)
        self.assertIn("ionq.simulator", target_names)
        self.assertIn("quantinuum.sim.h1-1sc", target_names)
        self.assertIn("quantinuum.sim.h1-2sc", target_names)

    def test_plugins_estimate_cost_cirq_ionq(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="ionq.simulator"
        )
        self.assertEqual(cost.estimated_total, 0.0)

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=1024,
            target="ionq.qpu"
        )
        self.assertEqual(np.round(cost.estimated_total), 1.0)

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="ionq.qpu"
        )
        self.assertEqual(np.round(cost.estimated_total), 63.0)

    @pytest.mark.live_test
    def test_plugins_cirq_nonexistent_target(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        with pytest.raises(RuntimeError):
            service.run(
                program=self._3_qubit_ghz_cirq(),
                repetitions=500,
                target="provider.doesnotexist",
                timeout_seconds=60
            )

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_ionq_cirq(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            service = AzureQuantumService(workspace=workspace)
            run_result = service.run(
                program=self._3_qubit_ghz_cirq(),
                repetitions=500,
                target="ionq.simulator",
                timeout_seconds=60
            )
            job = service.get_job(self.get_test_job_id())
            job_result = job.results(timeout_seconds=DEFAULT_TIMEOUT_SECS).to_cirq_result()
            for result in [run_result, job_result]:
                self.assertIn("q0", result.measurements)
                self.assertIn("q1", result.measurements)
                self.assertIn("q2", result.measurements)
                self.assertEqual(len(result.measurements["q0"]), 500)
                self.assertEqual(len(result.measurements["q1"]), 500)
                self.assertEqual(len(result.measurements["q2"]), 500)
                self.assertEqual(result.measurements["q0"].sum(), result.measurements["q1"].sum())
                self.assertEqual(result.measurements["q1"].sum(), result.measurements["q2"].sum())

    @pytest.mark.quantinuum
    def test_plugins_estimate_cost_cirq_quantinuum(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.sim.h1-1sc"
        )
        self.assertEqual(cost.estimated_total, 0.0)

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.sim.h1-1sc"
        )
        self.assertEqual(cost.estimated_total, 0.0)

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.sim.h1-2sc"
        )
        self.assertEqual(cost.estimated_total, 0.0)

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.sim.h1-1e"
        )
        self.assertEqual(np.round(cost.estimated_total), 725.0)

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.qpu.h1-1"
        )
        self.assertEqual(np.round(cost.estimated_total), 725.0)

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.qpu.h1-2"
        )
        self.assertEqual(np.round(cost.estimated_total), 725.0)

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_quantinuum_cirq(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            service = AzureQuantumService(workspace=workspace)
            program = self._3_qubit_ghz_cirq()
            run_result = service.run(
                program=program,
                repetitions=500,
                target="quantinuum.sim.h1-1e",
                timeout_seconds=DEFAULT_TIMEOUT_SECS
            )
            job_no_program = service.get_job(self.get_test_job_id())
            job_with_program = service.get_job(
                self.get_test_job_id(), program=program)
            target = service._target_factory.create_target(
                provider_id="quantinuum", name="quantinuum.sim.h1-1e")
            job_result1 = target._to_cirq_result(
                result=job_no_program.results(timeout_seconds=DEFAULT_TIMEOUT_SECS), param_resolver=ParamResolver({}))
            job_result2 = target._to_cirq_result(
                result=job_with_program.results(timeout_seconds=DEFAULT_TIMEOUT_SECS), param_resolver=ParamResolver({}))
            for result in [run_result, job_result1, job_result2]:
                self.assertIn("q0", result.measurements)
                self.assertIn("q1", result.measurements)
                self.assertIn("q2", result.measurements)
                self.assertEqual(len(result.measurements["q0"]), 500)
                self.assertEqual(len(result.measurements["q1"]), 500)
                self.assertEqual(len(result.measurements["q2"]), 500)
                self.assertAlmostEqual(result.measurements["q0"].sum(), result.measurements["q1"].sum(), delta=10)
                self.assertAlmostEqual(result.measurements["q1"].sum(), result.measurements["q2"].sum(), delta=10)
