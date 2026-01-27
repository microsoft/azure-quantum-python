##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from typing import Dict
import unittest
import pytest
import qiskit

# from common import QuantumTestBase, DEFAULT_TIMEOUT_SECS
# from test_job_payload_factory import JobPayloadFactory
from azure.quantum.qiskit.backends.quantinuum import QuantinuumQPUQirBackend
from azure.quantum.qiskit.provider import AzureQuantumProvider
from azure.quantum import SessionStatus


ECHO_PROVIDER_NAME = "Microsoft.Test.FirstParty"
DEFAULT_TIMEOUT_SECS = 300


class EchoQuantinuumQPUQirBackend(QuantinuumQPUQirBackend):
    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": ECHO_PROVIDER_NAME,
                "output_data_format": "honeywell.qir.v1",
            }
        )
        return config

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        super().__init__(name=name, provider=provider)
        self._provider_id = ECHO_PROVIDER_NAME
        self._provider_name = ECHO_PROVIDER_NAME


class QiskitTestSession(unittest.TestCase):
    def _get_qiskit_backend(self, target_name):
        from azure.quantum.qiskit import AzureQuantumProvider

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        if "echo-quantinuum" in target_name:
            return EchoQuantinuumQPUQirBackend("echo-quantinuum", provider)
        backend = provider.get_backend(target_name)
        self.assertIsNotNone(backend)
        return backend
    
    def _get_qiskit_circuit_bell_state() -> qiskit.QuantumCircuit:
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(2, 2)
        circuit.name = "BellState"
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure([0, 1], [0, 1])
        return circuit

    def _test_session_job_qiskit_circuit(self, target_name):
        workspace = self.create_workspace()
        backend = self._get_qiskit_backend(target_name)
        circuit = self._get_qiskit_circuit_bell_state()

        with backend.open_session() as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)
            session_id = session.id
            job1 = backend.run(circuit, shots=100, job_name="Job 1")

            backend.run(circuit, shots=100, job_name="Job 2")

            job1.wait_for_final_state(wait=5 if not self.is_playback else 0)
            session.refresh()

            self.assertEqual(session.details.status, SessionStatus.EXECUTING)

        session = workspace.get_session(session_id=session_id)
        session_jobs = session.list_jobs()
        self.assertEqual(len(session_jobs), 2)
        job_names = [job.details.name for job in session_jobs]
        self.assertIn("Job 1", job_names)
        self.assertIn("Job 2", job_names)

        [
            job.wait_until_completed(timeout_secs=DEFAULT_TIMEOUT_SECS)
            for job in session_jobs
        ]
        session.refresh()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    def _get_target(self, target_name):
        workspace = self.create_workspace()
        if "echo-quantinuum" in target_name:
            from azure.quantum.target.quantinuum import Quantinuum

            target = Quantinuum(
                workspace=workspace, name=target_name, provider_id=ECHO_PROVIDER_NAME
            )
            return target
        target = workspace.get_targets(target_name)
        self.assertIsNotNone(target)
        return target

    # Session support for Qiskit jobs

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.ionq
    @pytest.mark.xdist_group(name="ionq.simulator")
    def test_session_job_qiskit_circuit_ionq(self):
        self._test_session_job_qiskit_circuit(target_name="ionq.simulator")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.quantinuum
    @pytest.mark.xdist_group(name="quantinuum.sim.h2-1sc")
    def test_session_job_qiskit_circuit_quantinuum(self):
        self._test_session_job_qiskit_circuit(target_name="quantinuum.sim.h2-1sc")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.echo_targets
    @pytest.mark.xdist_group(name="echo-quantinuum")
    def test_session_job_qiskit_circuit_echo_quantinuum(self):
        self._test_session_job_qiskit_circuit(target_name="echo-quantinuum")
