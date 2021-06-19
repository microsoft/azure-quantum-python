# Unit tests #

## Environment Pre-reqs ##

Refer to [the parent README](../README.md) for how to prepare the development environment before running the unit tests.

### Environment variables for Recording and Live-Tests ###

The 'recordings' directory is used to replay network connections.
To manually **create new recordings**, remove the 'recordings' subdirectory and run the tests.

To **force the tests to run live**, even with existing recordings, set the environment variable:
```plaintext
AZURE_TEST_RUN_LIVE="yes"
```

To be able to run the tests in recording or live mode, make sure to set the following environment variables:

```plaintext
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID 
RESOURCE_GROUP
SUBSCRIPTION_ID
WORKSPACE_NAME
LOCATION
```

Optionally, to test 3rd party solvers, set:
```plaintext
AZURE_QUANTUM_1QBIT=1
AZURE_QUANTUM_TOSHIBA=1
```

## Unit tests ##

To run the unit tests, simply run `pytest` from the root of the `azure-quantum` directory:

```bash
pytest
```

To run the a specific unit test class, run `pytest [test_file.py]`.
Example:

```bash
pytest ./tests/unit/test_job.py
```

To run the a specific unit test case, run `pytest -k [test_method_name]`. 
Example:

```bash
pytest -k test_job_refresh
```
