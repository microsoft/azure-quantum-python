##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

import unittest


class _DummyWorkspace:
    def append_user_agent(self, *_args, **_kwargs):
        return None


class _DummyStatus:
    def __init__(
        self,
        target_id: str,
        *,
        target_profile: str | None = None,
        num_qubits: int | None = None,
        average_queue_time: int = 0,
        current_availability: str = "Available",
    ):
        self.id = target_id
        self.target_profile = target_profile
        self.num_qubits = num_qubits
        self.average_queue_time = average_queue_time
        self.current_availability = current_availability


class TestCirqGenericQirTarget(unittest.TestCase):
    def test_from_target_status_sets_defaults(self):
        from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

        ws = _DummyWorkspace()
        status = _DummyStatus("contoso.qir.target", target_profile="Base", num_qubits=4)
        target = AzureGenericQirCirqTarget.from_target_status(ws, "contoso", status)

        self.assertEqual(target.name, "contoso.qir.target")
        self.assertEqual(target.provider_id, "contoso")
        self.assertEqual(target.input_data_format, "qir.v1")
        self.assertEqual(target.output_data_format, "microsoft.quantum-results.v2")
        self.assertEqual(str(target.content_type), "qir.v1")

    def test_qir_display_to_bitstring(self):
        from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

        self.assertEqual(
            AzureGenericQirCirqTarget._qir_display_to_bitstring("[0, 1, 0]"),
            "010",
        )
        self.assertEqual(
            AzureGenericQirCirqTarget._qir_display_to_bitstring("([0, 1], [1])"),
            "01 1",
        )

    def test_split_registers(self):
        from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

        # Explicit register delimiter.
        self.assertEqual(
            AzureGenericQirCirqTarget._split_registers("01 1", [2, 1]),
            ["01", "1"],
        )
        # No delimiter: use lengths.
        self.assertEqual(
            AzureGenericQirCirqTarget._split_registers("011", [2, 1]),
            ["01", "1"],
        )

    def test_shots_to_rows_multi_register(self):
        from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget

        # Two measurement keys: a has 2 bits, b has 1 bit.
        measurement_dict = {"a": [0, 1], "b": [2]}

        # Two shots encoded as (reg_a_bits, reg_b_bits).
        shots = [([0, 1], [1]), ([1, 0], [0])]

        rows = AzureGenericQirCirqTarget._shots_to_rows(
            shots=shots,
            measurement_dict=measurement_dict,
        )

        self.assertEqual(rows["a"], [[0, 1], [1, 0]])
        self.assertEqual(rows["b"], [[1], [0]])


if __name__ == "__main__":
    unittest.main()
