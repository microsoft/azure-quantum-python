##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import pytest

from common import QuantumTestBase
from test_job_payload_factory import JobPayloadFactory
from azure.quantum import Job, Session, SessionStatus
from import_qsharp import skip_if_no_qsharp


class TestSession(QuantumTestBase):
    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_list_top_level_items(self):
        workspace = self.create_workspace()
        result = workspace.list_top_level_items()
        result_types = map(type, result)
        self.assertIn(Job, result_types)
        self.assertIn(Session, result_types)

    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_list_sessions(self):
        workspace = self.create_workspace()
        result = workspace.list_sessions()
        result_types = map(type, result)
        self.assertIn(Session, result_types)

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.echo_targets
    def test_session_get_session(self):
        workspace = self.create_workspace()
        session = Session(workspace=workspace,
                          name="My Session",
                          target="echo-quantinuum",
                          provider_id="microsoft.test")
        self.assertIsNone(session.details.status)
        session.open()
        self.assertEqual(session.details.status, SessionStatus.WAITING)
        obtained_session = workspace.get_session(session_id=session.id)
        self.assertIsInstance(obtained_session, Session)
        self.assertEqual(obtained_session.id, session.id)
        self.assertEqual(obtained_session.details.id, session.details.id)
        self.assertEqual(obtained_session.details.target, session.details.target)
        self.assertEqual(obtained_session.details.provider_id, session.details.provider_id)
        self.assertEqual(obtained_session.details.name, session.details.name)
        self.assertEqual(obtained_session.details.status, session.details.status)

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.echo_targets
    def test_session_open_close(self):
        workspace = self.create_workspace()
        session = Session(workspace=workspace,
                          target="echo-quantinuum",
                          provider_id="microsoft.test")
        self.assertIsNone(session.details.status)
        session.open()
        self.assertEqual(session.details.status, SessionStatus.WAITING)
        session.close()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.echo_targets
    def test_session_target_open_session(self):
        workspace = self.create_workspace()
        target = workspace.get_targets("echo-quantinuum")
        self.assertIsNone(target.latest_session)
        session = target.open_session()
        self.assertIsNotNone(target.latest_session)
        self.assertEqual(target.latest_session.id, session.id)
        self.assertEqual(target.get_latest_session_id(), session.id)
        self.assertEqual(session.details.status, SessionStatus.WAITING)
        session.close()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.echo_targets
    def test_session_with_target_open_session(self):
        workspace = self.create_workspace()
        target = workspace.get_targets("echo-quantinuum")
        self.assertIsNone(target.latest_session)
        with target.open_session() as session:
            self.assertIsNotNone(target.latest_session)
            self.assertEqual(target.latest_session.id, session.id)
            self.assertEqual(target.get_latest_session_id(), session.id)
            self.assertEqual(session.details.status, SessionStatus.WAITING)
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qio
    def test_session_job_qio_ising(self):
        workspace = self.create_workspace()
        problem = JobPayloadFactory.get_qio_ising_problem()

        from azure.quantum.optimization import ParallelTempering
        solver = ParallelTempering(workspace, timeout=100)

        with solver.open_session() as session:
            session_id = session.id
            problem.name = "Problem 1"
            solver.submit(problem)
            problem.name = "Problem 2"
            solver.submit(problem)
            problem.name = "Problem 3"
            solver.submit(problem)

        session_jobs = workspace.list_session_jobs(session_id=session_id)
        self.assertEqual(len(session_jobs), 3)
        self.assertEqual(session_jobs[0].details.name, "Problem 1")
        self.assertEqual(session_jobs[1].details.name, "Problem 2")
        self.assertEqual(session_jobs[2].details.name, "Problem 3")

    def _test_session_job_cirq_circuit(self, target):
        from azure.quantum.cirq import AzureQuantumService

        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        target = service.get_target(target)
        self.assertIsNotNone(target)

        circuit = JobPayloadFactory.get_cirq_circuit_bell_state()

        with target.open_session() as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)
            session_id = session.id
            job1 = target.submit(circuit, name="Job 1")
            azure_job = job1._azure_job if hasattr(job1, '_azure_job') \
                        else workspace.get_job(job_id=job1._job["id"])

            target.submit(circuit, name="Job 2")

            azure_job.wait_until_completed()

            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.EXECUTING)

        session = workspace.get_session(session_id=session_id)
        session_jobs = session.list_jobs()
        self.assertEqual(len(session_jobs), 2)
        self.assertEqual(session_jobs[0].details.name, "Job 1")
        self.assertEqual(session_jobs[1].details.name, "Job 2")

        [job.wait_until_completed() for job in session_jobs]
        session.refresh()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    def _test_session_job_qiskit_circuit(self, target):
        from azure.quantum.qiskit import AzureQuantumProvider
        from qiskit.tools.monitor import job_monitor

        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend(target)
        self.assertIsNotNone(backend)

        circuit = JobPayloadFactory.get_qiskit_circuit_bell_state()

        with backend.open_session() as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)
            session_id = session.id
            job1 = backend.run(circuit, shots=100, job_name="Job 1")

            backend.run(circuit, shots=100, job_name="Job 2")

            job_monitor(job1)

            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.EXECUTING)

        session = workspace.get_session(session_id=session_id)
        session_jobs = session.list_jobs()
        self.assertEqual(len(session_jobs), 2)
        self.assertEqual(session_jobs[0].details.name, "Job 1")
        self.assertEqual(session_jobs[1].details.name, "Job 2")

        [job.wait_until_completed() for job in session_jobs]
        session.refresh()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    def _test_session_job_qsharp_callable(self, target):
        workspace = self.create_workspace()
        target = workspace.get_targets(target)

        qsharp_callable = JobPayloadFactory.get_qsharp_inline_callable_bell_state()[0]

        with target.open_session() as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)
            session_id = session.id
            job1 = target.submit(qsharp_callable, name="Job 1")

            target.submit(qsharp_callable, name="Job 2")

            job1.wait_until_completed()

            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.EXECUTING)

        session = workspace.get_session(session_id=session_id)
        session_jobs = session.list_jobs()
        self.assertEqual(len(session_jobs), 2)
        self.assertEqual(session_jobs[0].details.name, "Job 1")
        self.assertEqual(session_jobs[1].details.name, "Job 2")

        [job.wait_until_completed() for job in session_jobs]
        session.refresh()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.cirq
    @pytest.mark.ionq
    def test_session_job_cirq_circuit_ionq(self):
        self._test_session_job_cirq_circuit(target="ionq.simulator")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.cirq
    @pytest.mark.quantinuum
    def test_session_job_cirq_circuit_quantinuum(self):
        self._test_session_job_cirq_circuit(target="quantinuum.sim.h1-1sc")

    @pytest.mark.skip(reason="There are no Cirq provider/targets implemented for echo targets.")
    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.cirq
    @pytest.mark.echo_targets
    def test_session_job_cirq_circuit_echo_quantinuum(self):
        self._test_session_job_qiskit_circuit(target="echo-quantinuum")

    # Session support for Qiskit jobs

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.ionq
    def test_session_job_qiskit_circuit_ionq(self):
        self._test_session_job_qiskit_circuit(target="ionq.simulator")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.quantinuum
    def test_session_job_qiskit_circuit_quantinuum(self):
        self._test_session_job_qiskit_circuit(target="quantinuum.sim.h1-1sc")

    @pytest.mark.skip(reason="There are no Qiskit provider/backend implemented for echo targets.")
    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.echo_targets
    def test_session_job_qiskit_circuit_echo_quantinuum(self):
        self._test_session_job_qiskit_circuit(target="echo-quantinuum")

    # Session support for Q# jobs

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qsharp
    @pytest.mark.quantinuum
    @skip_if_no_qsharp
    def test_session_job_qsharp_callable_quantinuum(self):
        self._test_session_job_qsharp_callable(target="quantinuum.sim.h1-1sc")

    @pytest.mark.skip(reason="echo-quantinuum target is setting job state to failure and now passing the test asserts.")
    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qsharp
    @pytest.mark.echo_targets
    @skip_if_no_qsharp
    def test_session_job_qsharp_callable_echo_quantinuum(self):
        self._test_session_job_qsharp_callable(target="echo-quantinuum")

    @pytest.mark.skip(reason="IonQ does not support Q#->QIR programs yet.")
    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qsharp
    @pytest.mark.ionq
    @skip_if_no_qsharp
    def test_session_job_qsharp_callable_ionq(self):
        self._test_session_job_qsharp_callable(target="ionq.simulator")
