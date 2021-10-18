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
AZURE_QUANTUM_SUBSCRIPTION_ID
AZURE_QUANTUM_WORKSPACE_RG
AZURE_QUANTUM_WORKSPACE_NAME
AZURE_QUANTUM_WORKSPACE_LOCATION
```

Optionally, to test 3rd party solvers, set:
```plaintext
AZURE_QUANTUM_1QBIT=1
AZURE_QUANTUM_TOSHIBA=1
```

## Recordings ##

Our testing infrastructure uses Python VCR to record HTTP calls against a live service and then use
the recordings (aka "cassetes") to playback the responses, essentially creating a mock of the live-service.

This is great, but it has some caveats and limitations, including that by default VCR does not allow the same
request (identified by URI, HTTP Headers and Body) to have multiple responses associated with it.
For example, when a job is submitted and we want to fetch the job status, the HTTP request to get the job status
is the same, but the response can be different, initially returning Status="In-Progress" and later returning
Status="Completed".

### Ability to Pause Recordings ###

To circumvent the problem of repeated requests (see https://github.com/microsoft/qdk-python/issues/118), in our tests we are
temporarily pausing the recording after submitting the job and while we await/polling for the job to complete.
After the job completes, we resume the recording and perform the unit test asserts.

Example:

```python
job = solver.submit(input_data_uri)

# For recording purposes, we only want to record and
# and resume recording when the job has completed
self.pause_recording()
job.wait_until_completed()
self.resume_recording()

# After resuming recording, the next call to get job
# status is guaranteed to be recorded with a 
# "Job Completed" status

job.refresh()
assert job.has_completed()
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
