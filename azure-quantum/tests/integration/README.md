# Integration tests

These integration tests are for running end-to-end tests against a live service.
To be able to run the tests, make sure to add a the following environment variables:

```plaintext
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID 
RESOURCE_GROUP
SUBSCRIPTION_ID
WORKSPACE_NAME
AZURE_QUANTUM_1QBIT
```

`AZURE_QUANTUM_1QBIT` is optional and can be `0` or `1` and it defaults to `0`.

To run the tests, run `python tests/integration/test_integration.py`.
