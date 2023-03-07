from azure.quantum.target.microsoft.result import MicrosoftEstimatorResult

class ResourceEstimatorResult(MicrosoftEstimatorResult):
    """
    A customized result for a resource estimation job.
    """

    def __init__(
        self,
        data
    ) -> None:
        super().__init__(data)

    @classmethod
    def from_dict(cls, data):
        results = data["results"]
        if len(results) == 1:
            data = results[0]['data']
            return ResourceEstimatorResult(data)
        else:
            raise ValueError("Expected Qiskit results for RE be of length 1")
