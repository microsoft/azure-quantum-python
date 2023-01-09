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
This will force the recording files to be deleted before running the tests.

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

### Cannot Overwrite Existing Cassette Exception ###

Even when you intend to simply playback the recordings, without recording it again, sometimes the Python VCR framework may give you an error like "Cannot Overwrite Existing Cassette".

#### Cause ####
The way VCR works is by working like a HTTP proxy.

If the request (coming from the SDK api calls) is found (by matching the full URI and HTTP headers) on the recorded file, it will playback the corresponding response. Otherwise, if not found, it will attempt to do a live cal to the web API and will try to record the results at the end. But if there is a recording file (cassete) already, it will give the error you are mentioning.

The environment variables to control whether to playback records or run live and re-create them is just a little logic to decide if we want to delete the recording files first before running the tests (which will force a call to the live APIs and re-record the calls).

But it does not handle the case when the recording file is there but a specific HTTP request/response can’t be found in the existing recording, which gives the error you are seeing.

This error could also be caused if the recorded files are manually updated and do not really match the requests that the SDK will actually request.

#### Potential solutions ####
1) One way to remove the error is to delete the existing recording file and let it do all the live calls, and create a new recording file that contains all the requests/responses that the tests need. Then, next time, you should be able to simple playback the recordings with no errors.

2) If the error still persist after trying (1), then probably there is something unique in the URL or HTTP headers of the HTTP request that changes at every time you run the tests. In this case, we need to either make that thing constant in the tests, or, if they are genuinely unique, we need to replace that unique value in the request recording pipeline such that, at least in the recording file, it will be unique.

For example, see the [process_request](https://github.com/microsoft/qdk-python/blob/main/azure-quantum/tests/unit/common.py#L372) method in the [tests/unit/common.py](https://github.com/microsoft/qdk-python/blob/main/azure-quantum/tests/unit/common.py) file.
In there, we replace several Guids and resource identifiers in the URL and in the HTTP Headers to make sure that the request that will be searched for (during a playback) or recorded (during recording) will have no unique values that could cause VCR to not find the request recording and attempt to do a new live call and rewrite the recording. Another reason we replace the identifiers is to remove potentially sensitive information from the recordings (like authentication tokens, access keys, etc).

### Recording sanitization ###
To prevent potentially sensitive information to be checked-in in the repository (like authentication tokens, access keys, etc) inside the recordings, we do several text replacements in the HTTP requests and responses in the VCR pipeline before they end-up persisted in the recorded files.

The [QuantumTestBase __init__ method](https://github.com/microsoft/qdk-python/blob/main/azure-quantum/tests/unit/common.py#L51) contains several rules (mostly regular expressions) that are applied in the HTTP requests and reponses via several recording and playback processors that are injected in the VCR HTTP pipeline.
We use some common processors provided by the Azure SDK framework (including AccessTokenReplacer, InteractiveAccessTokenReplacer, RequestUrlNormalizer) but we also apply custom text replacement logic in URLs and HTTP Headers via the `process_request` and `process_response` methods and some other processors/filters found at the end of the file.

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
