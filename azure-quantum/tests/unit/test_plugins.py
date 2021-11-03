
import unittest
import warnings
import pytest

from qiskit import QuantumCircuit
from cirq import ParamResolver

from qiskit.providers import JobStatus

from azure.quantum.job.job import Job
from azure.quantum.qiskit import AzureQuantumProvider
from azure.quantum.cirq import AzureQuantumService
from azure.quantum.cirq.targets.target import Target

from common import QuantumTestBase, ZERO_UID

class TestQiskit(QuantumTestBase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """
    

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()
    
    def _3_qubit_ghz(self):
        circuit = QuantumCircuit(3, 3)
        circuit.name = "Qiskit Sample - 3-qubit GHZ circuit"
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.cx(1, 2)
        circuit.measure([0,1,2], [0, 1, 2])

        return circuit

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq(circuit=circuit, num_shots=500, num_shots_actual=500)
    
    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_qobj_to_ionq(self):
        from qiskit import assemble
        circuit = self._3_qubit_ghz()
        qobj = assemble(circuit)
        self._test_qiskit_submit_ionq(circuit=qobj, num_shots=1024, num_shots_actual=1024)
    
    def _qiskit_wait_to_complete(self, qiskit_job, provider):
        job = qiskit_job._azure_job
        self.pause_recording()
        try:
            job.wait_until_completed(timeout_secs=60)
        except TimeoutError:
            self.resume_recording()
            warnings.warn(f"Qiskit Job {job.id} exceeded timeout. Skipping fetching results.")
        else:
            self.resume_recording()
            self.assertEqual(JobStatus.DONE, qiskit_job.status())
            qiskit_job = provider.get_job(job.id)
            self.assertEqual(JobStatus.DONE, qiskit_job.status())

    def _test_qiskit_submit_ionq(self, circuit, num_shots, num_shots_actual):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            assert "azure-quantum-qiskit" in provider._workspace.user_agent
            backend = provider.get_backend("ionq.simulator")

            qiskit_job = backend.run(
                circuit=circuit,
                shots=num_shots
            )

            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if self.in_recording:
                self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert result.data()["counts"] == {
                    '000': num_shots_actual//2, '111': num_shots_actual//2
                }
                assert result.data()["probabilities"] == {'000': 0.5, '111': 0.5}
                counts = result.get_counts()
                assert counts == result.data()["counts"]

    @pytest.mark.ionq
    @pytest.mark.live_test
    def test_plugins_retrieve_job(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("ionq.simulator")
            circuit = self._3_qubit_ghz()
            qiskit_job = backend.run(
                circuit=circuit,
                num_shots=100
            )

            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if self.in_recording:
                self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                fetched_job = backend.retrieve_job(qiskit_job.id())
                assert fetched_job.id() == qiskit_job.id()
                result = fetched_job.result()
                assert result.data() == {
                    'counts': {
                        '000': 250,
                        '111': 250
                    }, 
                    'probabilities': {
                        '000': 0.5,
                        '111': 0.5
                    }
                }

    @pytest.mark.honeywell
    @pytest.mark.live_test
    def test_plugins_submit_qiskit_to_honeywell(self):
        self._test_qiskit_submit_honeywell(num_shots=None)

    def _test_qiskit_submit_honeywell(self, num_shots):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("honeywell.hqs-lt-s1-apival")
            assert "honeywell.hqs-lt-s1-apival" in backend.backend_names
            assert backend.backend_names[0] in [t.name for t in workspace.get_targets(provider_id="honeywell")]
            circuit = self._3_qubit_ghz()
            qiskit_job = backend.run(
                circuit=circuit,
                num_shots=num_shots
            )
   
            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if self.in_recording:
                self._qiskit_wait_to_complete(qiskit_job, provider)

            if JobStatus.DONE == qiskit_job.status():
                result = qiskit_job.result()
                assert result.data()["counts"] == {'000': 500}
                assert result.data()["probabilities"] == {'000': 1.0}


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
    @pytest.mark.live_test
    def test_plugins_honeywell_cirq(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            service = AzureQuantumService(workspace=workspace)
            program = self._3_qubit_ghz_cirq()
            try:
                run_result = service.run(
                    program=program,
                    repetitions=500,
                    target="honeywell.hqs-lt-s1-apival",
                    timeout_seconds=60
                )

            except TimeoutError as e:
                # Pass on timeout
                warnings.warn("Honeywell execution exceeded timeout. \
                    Skipping fetching results.")
                if self.is_playback:
                    raise e

            except RuntimeError as e:
                # cirq_ionq currently throws a RuntimeError both if the job 
                # failed and on timeout.
                # See: https://github.com/quantumlib/Cirq/issues/4507
                if 'Job failed' in str(e) or self.is_playback:
                    warnings.warn(f"Honeywell job execution failed: {str(e)}")
                    raise e
                else:
                    warnings.warn("Honeywell execution exceeded timeout. \
                    Skipping fetching results.")

            else:
                job_no_program = service.get_job(self.get_test_job_id())
                job_with_program = service.get_job(
                    self.get_test_job_id(), program=program)
                target = service._target_factory.create_target(
                    provider_id="honeywell", name="honeywell.hqs-lt-s1-apival")
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