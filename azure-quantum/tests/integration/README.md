# Integration tests

These integration tests are for running end-to-end tests against a live service.
To be able to run the tests, make sure to add a `config.ini` file to the package root (`azure-quantum`) containing your credential info in the following format:

```plaintext
[azure.quantum]
subscription_id=<enter subscription ID here>
resource_group=<enter resource group here>
workspace_name=<enter workspace name here>
1qbit_enabled=<optional, true or false>
```

To run the tests, run `python tests/integration/test_integration.py`.
