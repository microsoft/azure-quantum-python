# Unit tests #

## Environment Pre-reqs ##

Refer to [the parent README](../README.md) for how to prepare the development environment before running the unit tests.

### Environment variables for Recording and Live-Tests ###

The 'recordings' directory is used to replay network connections.
To manually create new recordings, remove the 'recordings' subdirectory and run the tests.

To be able to run the tests, make sure to set the following environment variables:

```plaintext
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID 
RESOURCE_GROUP
SUBSCRIPTION_ID
WORKSPACE_NAME
```
