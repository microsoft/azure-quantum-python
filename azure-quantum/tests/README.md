# Unit tests

## Environment Pre-reqs

Before running the unit tests, set up your development environment using the venv-based setup:

### On Windows (PowerShell):
```powershell
.\eng\Setup-Dev-Env.ps1
```

This will install the package with common optional dependencies (qiskit, cirq, qsharp). To install additional provider dependencies, run:
```bash
source venv/bin/activate        # Activate the virtual environment first
pip install -e .[pulser,quil]   # for specific providers
pip install -e .[all]           # for all providers (requires Rust toolchain)
```

### Environment variables for Recording and Live-Tests

The 'recordings' directory is used to replay network connections.
To manually **create new recordings**, remove the 'recordings' subdirectory and run the tests.

To **force the tests to run live**, even with existing recordings, set the environment variable:

```plaintext
AZURE_TEST_RUN_LIVE="True"
```

This will force the recording files to be deleted before running the tests.

To be able to run the tests in recording or live mode, make sure:

- You have a client app registered in Microsoft Entra ID (formerly Azure Active Directory)
- The client app is configured with [certificate-based authentication](https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-certificate-based-authentication)
- The client app has "Contributor" permissions to your Azure Quantum Workspace
- The following environment variables are set:  
  - `AZURE_CLIENT_ID` - application (client) ID from Microsoft Entra ID
  - `AZURE_TENANT_ID` - directory (tenant) ID from Microsoft Entra ID
  - `AZURE_CLIENT_CERTIFICATE_PATH` - path to PEM or PKCS12 certificate file (including the private key) that is configured for the client app
  - `AZURE_CLIENT_SEND_CERTIFICATE_CHAIN=True` - prompts Azure.Identity to set X5C header (specifying certificate chain) required to support SNI authentication
  - `AZURE_QUANTUM_SUBSCRIPTION_ID` - ID of the Subscription where Azure Quantum Workspace is deployed
  - `AZURE_QUANTUM_WORKSPACE_RG` - name of the Resource Group where Azure Quantum Workspace is deployed
  - `AZURE_QUANTUM_WORKSPACE_NAME` - name of the Azure Quantum Workspace
  - `AZURE_QUANTUM_WORKSPACE_LOCATION` - Azure region where the Azure Quantum Workspace is deployed


## Recordings

Our testing infrastructure uses Python VCR to record HTTP calls against a live service and then use
the recordings (aka "cassettes") to playback the responses, essentially creating a mock of the live-service.

### Cannot Overwrite Existing Cassette Exception

When the intention is to simply playback the recordings without recording it again, sometimes the Python VCR framework may give an error "Cannot Overwrite Existing Cassette".

#### Cause

The VCR works like a HTTP proxy. It attempts to find the request by matching the full URI and HTTP headers in the recorded file. If found, it will playback the corresponding response. Otherwise, it will attempt to do a live call to the web API and will try to record the results at the end. When it tries to do a recording, if there is already a recording file, it will give the error `CannotOverwriteExistingCassetteException`.

This error could also be caused if the recorded files are manually updated and do not really match the requests that the SDK will actually request.

#### Potential solutions

1. One way to remove the error is to delete the existing recording file and let it do all the live calls and create a new recording file that contains all the requests/responses that the tests need. After that, you should be able to simple playback the recordings with no errors.

2. If the error still persist after trying (1), then probably there is something unique in the URL or HTTP headers of the HTTP request that changes every time you run the tests. In this case, we need to either make that thing constant in the tests, or if they are genuinely unique, we need to replace that unique value in the request recording pipeline such that, at least in the recording file, it will be unique.

For example, see the [process_request](https://github.com/microsoft/qdk-python/blob/main/azure-quantum/tests/unit/common.py) method in the [tests/unit/common.py](https://github.com/microsoft/qdk-python/blob/main/azure-quantum/tests/unit/common.py) file.
In there, we replace several Guids and resource identifiers in the URL and in the HTTP Headers to make sure that the request that will be searched for (during a playback) or recorded (during recording) will have no unique values that could cause VCR to not find the request recording and attempt to do a new live call and rewrite the recording. Another reason we replace the identifiers is to remove potentially sensitive information from the recordings (like authentication tokens, access keys, etc).

See [Sequence ids](#Sequence-ids) and [Non-deterministic Job ids and Session ids](#Non-deterministic-Job-ids-and-Session-ids) for more ideas.

### Recording sanitization

To prevent potentially sensitive information to be checked-in in the repository (like authentication tokens, access keys, etc) inside the recordings, we do several text replacements in the HTTP requests and responses in the VCR pipeline before they end-up persisted in the recorded files.

The [QuantumTestBase.\_\_init\_\_ method](https://github.com/microsoft/azure-quantum-python/blob/main/azure-quantum/tests/unit/common.py#L73) contains several rules (mostly regular expressions) that are applied in the HTTP requests and responses via several recording and playback processors that are injected in the VCR HTTP pipeline.
We use some common processors provided by the Azure SDK framework (including AccessTokenReplacer, InteractiveAccessTokenReplacer, RequestUrlNormalizer) but we also apply custom text replacement logic in URLs and HTTP Headers via the `process_request` and `process_response` methods and some other processors/filters found at the end of the file.

### Ability to Pause Recordings

If there are certain requests that you don't want to be recorded,
you can pause the recording before doing those requests.
Then, you can resume the recordings.
Note that if during playback the recordings are needed, the test will fail as
the recordings won't be found.

Example:

```python
if self.in_recording:
    self.pause_recording()
    # do stuff that could generate HTTP requests
    # but that you don't want to end-up in the recordings
    self.resume_recording()
```

### Sequence ids

By default, VCR does not allow the same request (identified by URI and HTTP Headers) to have multiple responses associated with it.
For example, when a job is submitted and we want to fetch the job status, the HTTP request to get the job status is the same, but the response can be different, initially returning Status="In-Progress" and later returning Status="Completed".

This limitation is solved by the test base class automatically injecting a `test-sequence-id` in the query string via the [CustomRecordingProcessor.\_append_sequence_id method](https://github.com/microsoft/azure-quantum-python/blob/main/azure-quantum/tests/unit/common.py#L458).

### Non-deterministic Job ids and Session ids

By default, the Azure Quantum Python SDK automatically creates a random guid when creating a new job or session if an id is not specified.
This non-deterministic behavior can cause problems when the test recordings are played-back and the ids in the recordings won't match the random ids created the by SDK when the tests run again.

To mitigate this problem, the `CustomRecordingProcessor` automatically looks for guids (registered with the `register_guid_regex` method) in the HTTP requests and replace them with a deterministic and sequential guid via the [CustomRecordingProcessor.\_search_for_guids method](https://github.com/microsoft/azure-quantum-python/blob/main/azure-quantum/tests/unit/common.py#L438) and the same mechanism to sanitize the recordings (regex replacement of URI, Headers and Body).

## Tests

To run the tests, simply run `pytest` from the root of the `azure-quantum` directory:

```bash
pytest
```

To run a specific test class, run `pytest [test_file.py]`.
Example:

```bash
pytest ./tests/unit/test_job.py
```

To run a specific test case, run `pytest -k [test_method_name]`.
Example:

```bash
pytest -k test_job_refresh
```

## E2E Live Test Pipeline

We have a private E2E test pipeline that run all the tests against
a live environment on a regular basis.

By default that pipeline will use the latest tests from the `main` branch
of this repository, but will install the latest released `azure-quantum` package from PyPI.

That can create an issue if you add tests for a new feature that has not been
released/published yet, since the tests will expect that feature but the current released
package does not have it.

To mitigate this issue you can add a `pytest.mark.skipif` mark to those new tests if the version
if less or equal to the latest published version.

For example:

```python
import pytest
from azure.quantum.version import __version__
skip_older_version = pytest.mark.skipif(__version__ != "0.0.1" and __version__ <= "0.28.263081", reason="Test requires the version to be > 0.28.263081.")

@skip_older_version
def test_my_test(self):
    pass
```
