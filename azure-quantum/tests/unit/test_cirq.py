#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_cirq.py: Tests for Cirq plugin
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import mock
import unittest
import warnings
import pytest

import numpy as np

from cirq import ParamResolver

from azure.quantum.job.job import Job
from azure.quantum.cirq import AzureQuantumService
from azure.quantum.cirq.targets.target import Target

from cirq_ionq import Job as CirqIonqJob

from common import QuantumTestBase, ZERO_UID


class TestCirq(QuantumTestBase):
    mock_create_job_id_name = "create_job_id"
    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
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
            assert app_id in service._workspace.user_agent
            assert "-azure-quantum-cirq" in service._workspace.user_agent

    @pytest.mark.quantinuum
    @pytest.mark.honeywell
    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_cirq_get_targets(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        assert "azure-quantum-cirq" in service._workspace.user_agent
        targets = service.targets()
        target_names = [t.name for t in targets]
        assert all([isinstance(t, Target) for t in targets])
        assert "honeywell.hqs-lt-s1-apival" in target_names
        assert "ionq.simulator" in target_names
        assert "quantinuum.hqs-lt-s1-apival" in target_names
        assert "quantinuum.sim.h1-1sc" in target_names
        assert "quantinuum.sim.h1-1e" in target_names

    def test_plugins_estimate_cost_cirq_ionq(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="ionq.simulator"
        )
        assert cost.estimated_total == 0.0

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=1024,
            target="ionq.qpu"
        )
        assert np.round(cost.estimated_total) == 1.0

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="ionq.qpu"
        )
        assert np.round(cost.estimated_total) == 63.0

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
            try:
                # Modify the Job.wait_until_completed method
                # such that it only records once
                # See: https://github.com/microsoft/qdk-python/issues/118
                with mock.patch.object(
                    CirqIonqJob,
                    "results",
                    self.mock_wait(CirqIonqJob.results)
                ):
                    run_result = service.run(
                        program=self._3_qubit_ghz_cirq(),
                        repetitions=500,
                        target="ionq.simulator",
                        timeout_seconds=60
                    )

            except TimeoutError as e:
                # Pass on timeout
                warnings.warn("IonQ execution exceeded timeout. \
                    Skipping fetching results.")
                if self.is_playback:
                    raise e

            except RuntimeError as e:
                # cirq_ionq currently throws a RuntimeError both if the job 
                # failed and on timeout.
                # See: https://github.com/quantumlib/Cirq/issues/4507
                if 'Job failed' in str(e) or self.is_playback:
                    warnings.warn(f"IonQ job execution failed: {str(e)}")
                    raise e
                else:
                    warnings.warn("IonQ execution exceeded timeout. \
                        Skipping fetching results.")

            else:
                job = service.get_job(self.get_test_job_id())
                job_result = job.results().to_cirq_result()
                for result in [run_result, job_result]:
                    assert "q0" in result.measurements
                    assert "q1" in result.measurements
                    assert "q2" in result.measurements
                    assert len(result.measurements["q0"]) == 500
                    assert len(result.measurements["q1"]) == 500
                    assert len(result.measurements["q2"]) == 500
                    assert result.measurements["q0"].sum() == result.measurements["q1"].sum()
                    assert result.measurements["q1"].sum() == result.measurements["q2"].sum()

    @pytest.mark.honeywell
    def test_plugins_estimate_cost_cirq_honeywell(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="honeywell.hqs-lt-s1-apival"
        )
        assert cost.estimated_total == 0.0

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="honeywell.hqs-lt-s1"
        )
        assert np.round(cost.estimated_total) == 725.0

    @pytest.mark.honeywell
    def test_plugins_estimate_cost_cirq_quantinuum(self):
        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.hqs-lt-s1-apival"
        )
        assert cost.estimated_total == 0.0

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.sim.h1-1sc"
        )
        assert cost.estimated_total == 0.0

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.hqs-lt-s1"
        )
        assert np.round(cost.estimated_total) == 725.0

        cost = service.estimate_cost(
            program=self._3_qubit_ghz_cirq(),
            repetitions=100e3,
            target="quantinuum.qpu.h1-1"
        )
        assert np.round(cost.estimated_total) == 725.0

    @pytest.mark.honeywell
    @pytest.mark.live_test
    def test_plugins_honeywell_cirq(self,
                                    provider_id: str = "honeywell"):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            service = AzureQuantumService(workspace=workspace)
            program = self._3_qubit_ghz_cirq()
            try:
                # Modify the Job.wait_until_completed method
                # such that it only records once
                # See: https://github.com/microsoft/qdk-python/issues/118
                with mock.patch.object(
                    Job,
                    "wait_until_completed",
                    self.mock_wait(Job.wait_until_completed)
                ):
                    run_result = service.run(
                        program=program,
                        repetitions=500,
                        target=f"{provider_id}.hqs-lt-s1-apival",
                        timeout_seconds=60
                    )

            except TimeoutError as e:
                # Pass on timeout
                warnings.warn("Quantinuum (formerly Honeywell) execution exceeded timeout. \
                    Skipping fetching results.")
                if self.is_playback:
                    raise e

            except RuntimeError as e:
                # cirq_ionq currently throws a RuntimeError both if the job 
                # failed and on timeout.
                # See: https://github.com/quantumlib/Cirq/issues/4507
                if 'Job failed' in str(e) or self.is_playback:
                    warnings.warn(f"Quantinuum (formerly Honeywell) job execution failed: {str(e)}")
                    raise e
                else:
                    warnings.warn("Quantinuum (formerly Honeywell) execution exceeded timeout. \
                    Skipping fetching results.")

            else:
                job_no_program = service.get_job(self.get_test_job_id())
                job_with_program = service.get_job(
                    self.get_test_job_id(), program=program)
                target = service._target_factory.create_target(
                    provider_id=provider_id, name=f"{provider_id}.hqs-lt-s1-apival")
                job_result1 = target._to_cirq_result(
                    result=job_no_program.results(), param_resolver=ParamResolver({}))
                job_result2 = target._to_cirq_result(
                    result=job_with_program.results(), param_resolver=ParamResolver({}))
                for result in [run_result, job_result1, job_result2]:
                    assert "q0" in result.measurements
                    assert "q1" in result.measurements
                    assert "q2" in result.measurements
                    assert len(result.measurements["q0"]) == 500
                    assert len(result.measurements["q1"]) == 500
                    assert len(result.measurements["q2"]) == 500
                    assert result.measurements["q0"].sum() == result.measurements["q1"].sum()
                    assert result.measurements["q1"].sum() == result.measurements["q2"].sum()

    @pytest.mark.quantinuum
    @pytest.mark.live_test
    def test_plugins_quantinuum_cirq(self):
        self.test_plugins_honeywell_cirq(provider_id="quantinuum")
