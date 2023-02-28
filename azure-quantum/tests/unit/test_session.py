##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import pytest

from common import QuantumTestBase, ZERO_UID
from test_job_payload_factory import JobPayloadFactory
from azure.quantum import Job, Session, JobDetails, SessionStatus

@pytest.mark.skip()
class TestSession(QuantumTestBase):


    def _get_test_id(self):
        session_id = None
        from common import ZERO_UID
        if self.is_playback:
            session_id = ZERO_UID
        return session_id


    def _get_job_id(self):
        job_id = Job.create_job_id()
        from common import ZERO_UID
        if self.is_playback:
            job_id = ZERO_UID
        return job_id


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
    def test_session_get_session(self):
        workspace = self.create_workspace()
        session_id = self._get_test_id()
        session = Session(workspace=workspace,
                          session_id=session_id,
                          target="ionq.simulator")
        session_id = session.id if session_id is None else session.id
        self.assertIsNone(session.details.status)

        session.open()
        self.assertEqual(session.details.status, SessionStatus.WAITING)

        obtained_session = workspace.get_session(session_id=session_id)
        self.assertIsInstance(obtained_session, Session)
        self.assertEqual(obtained_session.id, session.id)
        self.assertEqual(obtained_session.details.id, session.details.id)
        self.assertEqual(obtained_session.details.target, session.details.target)
        self.assertEqual(obtained_session.details.provider_id, session.details.provider_id)
        self.assertEqual(obtained_session.details.name, session.details.name)
        self.assertEqual(obtained_session.details.status, session.details.status)


    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_start_end(self):
        workspace = self.create_workspace()
        session_id = self._get_test_id()
        session = Session(workspace=workspace,
                          session_id=session_id,
                          target="ionq.simulator")
        self.assertIsNone(session.details.status)

        session.open()
        self.assertEqual(session.details.status, SessionStatus.WAITING)

        session.close()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)


    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_list_session_jobs(self):
        workspace = self.create_workspace()

        session_id = self._get_test_id()
        session = Session(workspace=workspace,
                          session_id=session_id,
                          target="ionq.simulator")
        self.assertIsNone(session.details.status)

        session.open()
        self.assertEqual(session.details.status, SessionStatus.WAITING)

        job_id = self._get_job_id()
        job = workspace.submit_job(
            Job(workspace=workspace,
                job_details=JobDetails(id=job_id,
                                       name=f"job-{job_id}",
                                       provider_id="ionq",
                                       target="ionq.simulator",
                                       container_uri="https://mystorage.blob.core.windows.net/job-00000000-0000-0000-0000-000000000000/inputData",
                                       input_data_format="mydataformat",
                                       output_data_format="mydataformat",
                                       session_id=session.id)
                                 ))

        jobs = workspace.list_session_jobs(session_id=session.id)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(job.id, jobs[0].id)
        self.assertEqual(job.details.id, jobs[0].details.id)
        self.assertEqual(job.details.name, jobs[0].details.name)
        self.assertEqual(job.details.provider_id, jobs[0].details.provider_id)
        self.assertEqual(job.details.target, jobs[0].details.target)
        self.assertEqual(job.details.container_uri, jobs[0].details.container_uri)
        self.assertEqual(job.details.input_data_format, jobs[0].details.input_data_format)
        self.assertEqual(job.details.output_data_format, jobs[0].details.output_data_format)
        self.assertEqual(job.details.session_id, jobs[0].details.session_id)

        session.close()
        self.assertNotEquals(session.details.status, SessionStatus.WAITING)


    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_target_start_session(self):
        workspace = self.create_workspace()
        target = workspace.get_targets("ionq.simulator")

        self.assertIsNone(target.current_session)

        session_id = self._get_test_id()
        session = target.start_session(session_id=session_id)
        self.assertEqual(target.current_session, session)
        self.assertEqual(session.details.status, SessionStatus.WAITING)
        session.close()
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)


    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_with_target_start_session(self):
        workspace = self.create_workspace()
        target = workspace.get_targets("ionq.simulator")

        self.assertIsNone(target.current_session)

        session_id = self._get_test_id()
        with target.start_session(session_id=session_id) as session:
            self.assertEqual(target.current_session, session)
            self.assertEqual(session.details.status, SessionStatus.WAITING)

        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)


    @pytest.mark.live_test
    @pytest.mark.session
    def test_session_with_target_job(self):
        workspace = self.create_workspace()
        target = workspace.get_targets("ionq.simulator")

        self.assertIsNone(target.current_session)

        session_id = self._get_test_id()
        with target.start_session(session_id=session_id) as session:
            self.assertEqual(target.current_session, session)
            self.assertEqual(session.details.status, SessionStatus.WAITING)

        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)


    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.qio
    @pytest.mark.skip()
    def test_session_job_qio_ising(self):
        self.pause_recording()

        workspace = self.create_workspace()
        problem = JobPayloadFactory.get_qio_ising_problem()

        from azure.quantum.optimization import ParallelTempering
        solver = ParallelTempering(workspace, timeout=100)

        session_id = self._get_test_id()
        with solver.start_session(session_id=session_id) as session:
            session_id = session.id
            problem.name = "Problem 1"
            solver.optimize(problem)
            problem.name = "Problem 2"
            solver.optimize(problem)
            problem.name = "Problem 3"
            solver.optimize(problem)

        session_jobs = workspace.list_session_jobs(session_id=session_id)
        self.assertEqual(len(session_jobs), 3)
        self.assertEqual(session_jobs[0].details.name, "Problem 1")
        self.assertEqual(session_jobs[1].details.name, "Problem 2")
        self.assertEqual(session_jobs[2].details.name, "Problem 3")


    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.cirq
    @pytest.mark.skip()
    def test_session_job_cirq_circuit(self):
        self.pause_recording()

        from azure.quantum.cirq import AzureQuantumService

        workspace = self.create_workspace()
        service = AzureQuantumService(workspace=workspace)
        target = service.get_target("ionq.simulator")

        circuit = JobPayloadFactory.get_cirq_circuit_bell_state()

        session_id = self._get_test_id()
        with target.start_session(session_id=session_id) as session:
            self.assertEqual(session.details.status, SessionStatus.WAITING)
            session_id = session.id
            job1 = target.submit(program=circuit, name="Job 1")
            job1 = workspace.get_job(job_id=job1._job["id"])

            target.submit(program=circuit, name="Job 2")
            target.submit(program=circuit, name="Job 3")

            job1.wait_until_completed()
            session.refresh()
            self.assertEqual(session.details.status, SessionStatus.EXECUTING)

        session_jobs = workspace.list_session_jobs(session_id=session_id)
        self.assertEqual(len(session_jobs), 3)
        self.assertEqual(session_jobs[0].details.name, "Job 1")
        self.assertEqual(session_jobs[1].details.name, "Job 2")
        self.assertEqual(session_jobs[2].details.name, "Job 3")

        [job.wait_until_completed() for job in session_jobs]
        session = workspace.get_session(session_id=session_id)
        self.assertEqual(session.details.status, SessionStatus.SUCCEEDED)


    @pytest.mark.live_test
    @pytest.mark.session
    @pytest.mark.skip()
    def test_session_job_qir(self):
        self.pause_recording()
        workspace = self.create_workspace()
        target = workspace.get_targets("rigetti.sim.qvm")

        session_id = self._get_test_id()
        job_id = self._get_test_id()
        job_name = f"job-{job_id}"
        shots = 100
        (qir_bitcode, entrypoint) = JobPayloadFactory.get_qsharp_qir_bitcode_bell_state(target=target.name)
        
        job = target.submit(
            input_data=qir_bitcode,
            input_data_format="qir.v1",
            content_type="qir.v1",
            encoding="",
            output_data_format="microsoft.quantum-results.v1",
            name=job_name, 
            job_id=job_id,
            input_params={
                "count": shots,
                "shots": shots,
                "targetCapability": "BasicExecution",
                "entryPoint": entrypoint,
                "arguments": []
            }
        )

        result = job.get_results(timeout_secs=240)


    @pytest.mark.skip()
    def test_session_job_qiskit(self):
        self.pause_recording()

        from azure.quantum.qiskit import AzureQuantumProvider
        workspace = self.create_workspace()
        provider = AzureQuantumProvider(workspace=workspace)
        backend = provider.get_backend("ionq.simulator")
        backend2 = provider.get_backend("ionq.simulator")
        self.assertIs(backend, backend)
        self.assertIsNot(backend, backend2)

        circuit = JobPayloadFactory.get_qiskit_circuit_bell_state()

        session_id = self._get_test_id()
        with backend.start_session(session_id=session_id) as session:
            session_id = session.id
            job1 = backend.run(circuit=circuit, shots=100, job_name="Job 1")
            job2 = backend.run(circuit=circuit, shots=100, job_name="Job 2")
            job3 = backend.run(circuit=circuit, shots=100, job_name="Job 3")

        session_jobs = workspace.list_session_jobs(session_id=session_id)
        self.assertEqual(len(session_jobs), 3)
        self.assertEqual(session_jobs[0].details.name, "Job 1")
        self.assertEqual(session_jobs[1].details.name, "Job 2")
        self.assertEqual(session_jobs[2].details.name, "Job 3")
