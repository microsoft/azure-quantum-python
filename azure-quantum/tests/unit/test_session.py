##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Dict
import pytest

from common import QuantumTestBase
from test_job_payload_factory import JobPayloadFactory
from azure.quantum import Job, JobStatus, Session, SessionStatus, SessionJobFailurePolicy
from azure.quantum.qiskit.backends.quantinuum import QuantinuumQPUQirBackend
from azure.quantum.qiskit.provider import AzureQuantumProvider
from import_qsharp import skip_if_no_qsharp


ECHO_PROVIDER_NAME = "microsoft.test"


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
                          provider_id=ECHO_PROVIDER_NAME)
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
                          provider_id=ECHO_PROVIDER_NAME)
        self.assertIsNone(session.details.status)
        session.open()
        self.assertEqual(session.details.status, SessionStatus.WAITING)
        session.close()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.echo_targets
    def test_session_target_open_session(self):
        target = self._get_target("echo-quantinuum")
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
        target = self._get_target("echo-quantinuum")
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

    def _get_cirq_target(self, target_name):
        workspace = self.create_workspace()
        if "echo-quantinuum" in target_name:
            from azure.quantum.cirq.targets import QuantinuumTarget
            return QuantinuumTarget(workspace=workspace,
                                    provider_id=ECHO_PROVIDER_NAME,
                                    name=target_name)
        from azure.quantum.cirq import AzureQuantumService
        service = AzureQuantumService(workspace=workspace)
        target = service.get_target(target_name)
        self.assertIsNotNone(target)
        return target

    def _test_session_job_cirq_circuit(self, target_name):
        workspace = self.create_workspace()
        target = self._get_cirq_target(target_name)

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

    def _get_qiskit_backend(self, target_name):
        from azure.quantum.qiskit import AzureQuantumProvider
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        if "echo-quantinuum" in target_name:
            return EchoQuantinuumQPUQirBackend("echo-quantinuum", provider)
        backend = provider.get_backend(target_name)
        self.assertIsNotNone(backend)
        return backend

    def _test_session_job_qiskit_circuit(self, target_name):
        from qiskit.tools.monitor import job_monitor

        workspace = self.create_workspace()
        backend = self._get_qiskit_backend(target_name)
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

    def _get_target(self, target_name):
        workspace = self.create_workspace()
        if "echo-quantinuum" in target_name:
            from azure.quantum.target.quantinuum import Quantinuum
            target = Quantinuum(workspace=workspace,
                                name=target_name,
                                provider_id=ECHO_PROVIDER_NAME)
            return target
        target = workspace.get_targets(target_name)
        self.assertIsNotNone(target)
        return target

    def _test_session_job_qsharp_callable(self, target_name):
        workspace = self.create_workspace()
        target = self._get_target(target_name)

        qsharp_callable = JobPayloadFactory.get_qsharp_inline_callable_bell_state()[0]

        output_data_format = "honeywell.qir.v1" if "echo-quantinuum" in target_name else None

        with target.open_session() as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)
            session_id = session.id
            job1 = target.submit(qsharp_callable,
                                 name="Job 1",
                                 output_data_format=output_data_format)

            target.submit(qsharp_callable,
                          name="Job 2",
                          output_data_format=output_data_format)

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

    def _test_session_job_failure_policies(self, target_name):
        """
        This test case checks the session job failure policies
        behavior in more detail.

        First it checks the behavior of the SessionJobFailurePolicy.ABORT
        policy by submitting a failing job right away.

        Then it checks the behavior of the SessionJobFailurePolicy.CONTINUE
        policy by submitting a failing job in the middle of two
        successful jobs.

        Note: all other tests that submit jobs for a session
        defaults to using the SessionJobFailurePolicy.ABORT policy
        and they have check the expected behavior by asserting
        the session status WAITING->EXECUTING->SUCCEEDED
        """

        workspace = self.create_workspace()
        target = self._get_target(target_name)

        qsharp_callable = JobPayloadFactory.get_qsharp_inline_callable_bell_state()[0]

        output_data_format = "honeywell.qir.v1" if "echo-quantinuum" in target_name else None

        with target.open_session(job_failure_policy=SessionJobFailurePolicy.ABORT) as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)

            # pass an invalid output_data_format to make the job fail
            job1 = target.submit(qsharp_callable,
                                 name="Bad Job 1",
                                 output_data_format="invalid_output_format")
            job1.wait_until_completed()
            self.assertEqual(job1.details.status, JobStatus.FAILED)
            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.FAILED)

            from azure.core.exceptions import HttpResponseError
            with self.assertRaises(HttpResponseError) as context:
                target.submit(qsharp_callable,
                              name="Good Job 2",
                              output_data_format=output_data_format)
            self.assertIn("Session is already in a terminal state.",
                          context.exception.message)

            session_jobs = session.list_jobs()
            self.assertEqual(len(session_jobs), 1)
            self.assertEqual(session_jobs[0].details.name, "Bad Job 1")

        with target.open_session(job_failure_policy=SessionJobFailurePolicy.CONTINUE) as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)
            job1 = target.submit(qsharp_callable,
                                 name="Good Job 1",
                                 output_data_format=output_data_format)
            job1.wait_until_completed()
            self.assertEqual(job1.details.status, JobStatus.SUCCEEDED)
            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.EXECUTING)

            # pass an invalid output_data_format to make the job fail
            job2 = target.submit(qsharp_callable,
                                 name="Bad Job 2",
                                 output_data_format="invalid_output_format")
            job2.wait_until_completed()
            self.assertEqual(job2.details.status, JobStatus.FAILED)
            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.FAILURE_S_)

            job3 = target.submit(qsharp_callable,
                                 name="Good Job 3",
                                 output_data_format=output_data_format)
            job3.wait_until_completed()
            self.assertEqual(job3.details.status, JobStatus.SUCCEEDED)
            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.FAILURE_S_)

            session_jobs = session.list_jobs()
            self.assertEqual(len(session_jobs), 3)
            self.assertEqual(session_jobs[0].details.name, "Good Job 1")
            self.assertEqual(session_jobs[1].details.name, "Bad Job 2")
            self.assertEqual(session_jobs[2].details.name, "Good Job 3")

    # Session job failure policy tests

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qsharp
    @pytest.mark.echo_targets
    def test_session_job_failure_policies_echo_quantinuum(self):
        self._test_session_job_failure_policies(target_name="echo-quantinuum")

    # Session support for Cirq jobs

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.cirq
    @pytest.mark.ionq
    def test_session_job_cirq_circuit_ionq(self):
        self._test_session_job_cirq_circuit(target_name="ionq.simulator")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.cirq
    @pytest.mark.quantinuum
    def test_session_job_cirq_circuit_quantinuum(self):
        self._test_session_job_cirq_circuit(target_name="quantinuum.sim.h1-1sc")

    @pytest.mark.skip(reason="Currently the echo-quantinuum is only accepting QIR input formats and Cirq is using qasm.")
    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.cirq
    @pytest.mark.echo_targets
    def test_session_job_cirq_circuit_echo_quantinuum(self):
        self._test_session_job_cirq_circuit(target_name="echo-quantinuum")

    # Session support for Qiskit jobs

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.ionq
    def test_session_job_qiskit_circuit_ionq(self):
        self._test_session_job_qiskit_circuit(target_name="ionq.simulator")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.quantinuum
    def test_session_job_qiskit_circuit_quantinuum(self):
        self._test_session_job_qiskit_circuit(target_name="quantinuum.sim.h1-1sc")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qiskit
    @pytest.mark.echo_targets
    def test_session_job_qiskit_circuit_echo_quantinuum(self):
        self._test_session_job_qiskit_circuit(target_name="echo-quantinuum")

    # Session support for Q# jobs

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qsharp
    @pytest.mark.quantinuum
    @skip_if_no_qsharp
    def test_session_job_qsharp_callable_quantinuum(self):
        self._test_session_job_qsharp_callable(target_name="quantinuum.sim.h1-1sc")

    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qsharp
    @pytest.mark.echo_targets
    @skip_if_no_qsharp
    def test_session_job_qsharp_callable_echo_quantinuum(self):
        self._test_session_job_qsharp_callable(target_name="echo-quantinuum")

    @pytest.mark.skip(reason="IonQ does not support Q#->QIR programs yet.")
    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qsharp
    @pytest.mark.ionq
    @skip_if_no_qsharp
    def test_session_job_qsharp_callable_ionq(self):
        self._test_session_job_qsharp_callable(target_name="ionq.simulator")


class EchoQuantinuumQPUQirBackend(QuantinuumQPUQirBackend):
    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": ECHO_PROVIDER_NAME,
                "output_data_format": "honeywell.qir.v1"
            }
        )
        return config

    def __init__(self,
                 name: str,
                 provider: AzureQuantumProvider,
                 **kwargs):
        super().__init__(name=name, provider=provider)
        self._provider_id = ECHO_PROVIDER_NAME
        self._provider_name = ECHO_PROVIDER_NAME
