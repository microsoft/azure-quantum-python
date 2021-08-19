import unittest
import warnings

from azure.core.exceptions import HttpResponseError
from azure.quantum.job.job import Job
from azure.quantum.target import IonQ, Honeywell, FleetManagement

from common import QuantumTestBase, ZERO_UID


class TestIonQ(QuantumTestBase):
    """TestIonq

    Tests the azure.quantum.target.ionq module.
    """

    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()
    
    def _3_qubit_ghz(self):
        return {
            "qubits": 3,
            "circuit": [
                {
                "gate": "h",
                "target": 0
                },
                {
                "gate": "cnot",
                "control": 0,
                "target": 1
                },
                {
                "gate": "cnot",
                "control": 0,
                "target": 2
                },
            ]
        }

    def test_job_submit_ionq(self):
        self._test_job_submit_ionq(num_shots=None)

    def test_job_submit_ionq_100_shots(self):
        self._test_job_submit_ionq(num_shots=100)

    def _test_job_submit_ionq(self, num_shots):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            circuit = self._3_qubit_ghz()
            target = IonQ(workspace=workspace)
            job = target.submit(
                circuit=circuit,
                name="ionq-3ghz-job",
                num_shots=num_shots
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
                job = workspace.get_job(job.id)
                self.assertEqual(True, job.has_completed())

            results = job.get_results()
            assert "histogram" in results
            assert results["histogram"]["0"] == 0.5
            assert results["histogram"]["7"] == 0.5

            if num_shots:
                assert job.details.input_params.get("shots") == num_shots
            else:
                assert job.details.input_params.get("shots") is None


class TestHoneywell(QuantumTestBase):
    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def _teleport(self):
        return """OPENQASM 2.0;
        include "qelib1.inc";

        qreg q[3];
        creg c0[1];
        creg c1[3];

        h q[0];
        cx q[0], q[1];
        x q[2];
        h q[2];
        cx q[2], q[0];
        h q[2];
        measure q[0] -> c1[0];
        c0[0] = c1[0];
        if (c0==1) x q[1];
        c0[0] = 0;
        measure q[2] -> c1[1];
        c0[0] = c1[1];
        if (c0==1) z q[1];
        c0[0] = 0;
        h q[1];
        measure q[1] -> c1[2];
        """

    def test_job_submit_honeywell(self):

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            circuit = self._teleport()
            target = Honeywell(workspace=workspace)
            try:
                job = target.submit(circuit)
            except HttpResponseError as e:
                if "InvalidJobDefinition" not in e.message \
                and "The provider specified does not exist" not in e.message:
                    raise(e)
                warnings.warn(e.message)
            else:
                # Make sure the job is completed before fetching the results
                # playback currently does not work for repeated calls
                if not self.is_playback:
                    self.assertEqual(False, job.has_completed())
                    try:
                        # Set a timeout for Honeywell recording
                        job.wait_until_completed(timeout_secs=60)
                    except TimeoutError:
                        warnings.warn("Honeywell execution exceeded timeout. Skipping fetching results.")
                    else:
                        # Check if job succeeded
                        self.assertEqual(True, job.has_completed())
                        assert job.details.status == "Succeeded"

                if job.has_completed():
                    results = job.get_results()
                    assert results["c0"] == ["0"]
                    assert results["c1"] == ["000"]

class TestFleetManagement(QuantumTestBase):
    mock_create_job_id_name = "create_job_id"
    create_job_id = Job.create_job_id

    def get_test_job_id(self):
        return ZERO_UID if self.is_playback \
               else Job.create_job_id()

    def test_job_submit_fleet_management(self):
        if not self.is_playback:
            # We expect breaking changes from the service during internal preview
            return

        with unittest.mock.patch.object(
            Job,
            self.mock_create_job_id_name,
            return_value=self.get_test_job_id(),
        ):
            workspace = self.create_workspace()
            input = self.get_input()
            input_params = {    
                "params": {        
                    "solver": "stack",        
                    "depot_allowed": True    
                }
            }

            target = FleetManagement(workspace=workspace)
            try:
                job = target.submit(input=input, input_params=input_params)
            except HttpResponseError as e:
                    raise(e)
            else:
                # Make sure the job is completed before fetching the results
                # playback currently does not work for repeated calls
                if not self.is_playback:
                    self.assertEqual(False, job.has_completed())
                    try:
                        # Set a timeout for Honeywell recording
                        job.wait_until_completed(timeout_secs=60)
                    except TimeoutError:
                        warnings.warn("FleetManagement execution exceeded timeout. Skipping fetching results.")
                    else:
                        # Check if job succeeded
                        self.assertEqual(True, job.has_completed())
                        assert job.details.status == "Succeeded"

                job.refresh()
                assert job.has_completed() == True
                results = job.get_results()
                assert len(results["vehicles"]) == 5

    def get_input(self):
        return '{"instance":{"problem":{"type":"routing","data":{"distances":{"num_nodes":2,"values":[[0.0,23.249],[23.249,0.0]]},"fleet":{"num_vehicles":1,"vehicles":[{"model":"large","number":5,"starting_node":0,"ending_node":0,"capacity":{"quantity":200.0},"starting_time":1519804800,"ending_time":1519848000,"base_cost":50.0,"cost_per_sec":0.004722222222222222,"cost_per_km":0.5}],"vehicle_start_points":null,"vehicle_end_points":null},"requests":[{"id":"1","name":null,"source":0,"source_type":"0","loading_time":0,"earliest_load_time":1519804800,"latest_load_time":1519847880,"destination":1,"destination_lat":47.443501,"destination_long":-122.302594,"destination_type":"1","unloading_time":120.0,"earliest_unload_time":1519804800,"latest_unload_time":1519847880,"requirement":{"quantity":1.0},"available_hubs":null,"priority":0}],"times":[[0.0,23.249],[23.249,0.0]]}}}}'
