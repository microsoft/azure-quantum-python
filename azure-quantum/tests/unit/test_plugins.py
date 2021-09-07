import unittest
from qiskit import QuantumCircuit

from azure.quantum.job.job import Job
from azure.quantum.plugins.qiskit import AzureQuantumProvider
from azure.quantum.plugins.cirq import AzureQuantumService

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

    def test_plugins_submit_qiskit_to_ionq(self):
        circuit = self._3_qubit_ghz()
        self._test_qiskit_submit_ionq(circuit=circuit, num_shots=None, num_shots_actual=500)
    
    def test_plugins_submit_qiskit_qobj_to_ionq(self):
        from qiskit import assemble
        circuit = self._3_qubit_ghz()
        qobj = assemble(circuit)
        self._test_qiskit_submit_ionq(circuit=qobj, num_shots=None, num_shots_actual=1024)

    def _test_qiskit_submit_ionq(self, circuit, num_shots, num_shots_actual):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            provider = AzureQuantumProvider(workspace=workspace)
            backend = provider.get_backend("ionq.simulator")
            
            qiskit_job = backend.run(
                circuit=circuit,
                shots=num_shots
            )

            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if not self.is_playback:
                job = qiskit_job._azure_job
                self.assertEqual(False, job.has_completed())
                if self.in_recording:
                    import time
                    time.sleep(3)
                job.refresh()
                job.wait_until_completed()
                self.assertEqual(True, job.has_completed())
                job = provider.get_job(job.id)._azure_job
                self.assertEqual(True, job.has_completed())

            result = qiskit_job.result()
            assert result.data()["counts"] == {
                '000': num_shots_actual//2, '111': num_shots_actual//2
            }
            assert result.data()["probabilities"] == {'000': 0.5, '111': 0.5}
            counts = result.get_counts()
            assert counts == result.data()["counts"]
    
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
            job = qiskit_job._azure_job

            # Make sure the job is completed before fetching the job
            if not self.is_playback:
                self.assertEqual(False, job.has_completed())
                if self.in_recording:
                    import time
                    time.sleep(3)
                job.refresh()
                job.wait_until_completed()
                self.assertEqual(True, job.has_completed())
                job = workspace.get_job(job.id)
                self.assertEqual(True, job.has_completed())

            fetched_job = backend.retrieve_job(qiskit_job.id())
            assert fetched_job.id() == qiskit_job.id()

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
            assert backend.backend_name == "honeywell.hqs-lt-s1-apival"
            assert backend.backend_name in [t.name for t in workspace.get_targets(provider_id="honeywell")]
            circuit = self._3_qubit_ghz()
            qiskit_job = backend.run(
                circuit=circuit,
                num_shots=num_shots
            )

            job = qiskit_job._azure_job

            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if not self.is_playback:
                self.assertEqual(False, job.has_completed())
                if self.in_recording:
                    import time
                    time.sleep(3)
                job.refresh()
                job.wait_until_completed()
                self.assertEqual(True, job.has_completed())
                job = workspace.get_job(job.id)
                self.assertEqual(True, job.has_completed())

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

    def test_plugins_ionq_cirq(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            service = AzureQuantumService(workspace=workspace)
            job = service.run(
                circuit=self._3_qubit_ghz_cirq(),
                repetitions=None,
                target="ionq.simulator"
            )

            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if not self.is_playback:
                self.assertEqual(False, job.has_completed())
                if self.in_recording:
                    import time
                    time.sleep(3)
                job.refresh()
                job.wait_until_completed()
                self.assertEqual(True, job.has_completed())

            results = job.get_results()
            assert "histogram" in results
            assert results["histogram"]["0"] == 0.5
            assert results["histogram"]["7"] == 0.5
    
    def test_plugins_honeywell_cirq(self):
        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            service = AzureQuantumService(workspace=workspace)
            job = service.run(
                circuit=self._3_qubit_ghz_cirq(),
                repetitions=None,
                target="honeywell.hqs-lt-s1-apival"
            )

            # Make sure the job is completed before fetching the results
            # playback currently does not work for repeated calls
            # See: https://github.com/microsoft/qdk-python/issues/118
            if not self.is_playback:
                self.assertEqual(False, job.has_completed())
                if self.in_recording:
                    import time
                    time.sleep(3)
                job.refresh()
                job.wait_until_completed()
                self.assertEqual(True, job.has_completed())

            results = job.get_results()
            assert results["m_q0"] == ["0"]
            assert results["m_q1"] == ["0"]
            assert results["m_q2"] == ["0"]
