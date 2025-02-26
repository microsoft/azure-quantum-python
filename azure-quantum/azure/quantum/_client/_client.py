# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) Python Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from copy import deepcopy
from typing import Any, TYPE_CHECKING, Union
from typing_extensions import Self

from azure.core import PipelineClient
from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline import policies
from azure.core.rest import HttpRequest, HttpResponse

from ._configuration import ServicesClientConfiguration
from ._serialization import Deserializer, Serializer
from .operations import (
    JobsOperations,
    ProvidersOperations,
    QuotasOperations,
    SessionsOperations,
    StorageOperations,
    TopLevelItemsOperations,
)

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential


class ServicesClient:
    """Azure Quantum Workspace Services.

    :ivar jobs: JobsOperations operations
    :vartype jobs: azure.quantum.operations.JobsOperations
    :ivar sessions: SessionsOperations operations
    :vartype sessions: azure.quantum.operations.SessionsOperations
    :ivar providers: ProvidersOperations operations
    :vartype providers: azure.quantum.operations.ProvidersOperations
    :ivar storage: StorageOperations operations
    :vartype storage: azure.quantum.operations.StorageOperations
    :ivar quotas: QuotasOperations operations
    :vartype quotas: azure.quantum.operations.QuotasOperations
    :ivar top_level_items: TopLevelItemsOperations operations
    :vartype top_level_items: azure.quantum.operations.TopLevelItemsOperations
    :param region: The Azure region where the Azure Quantum Workspace is located. Required.
    :type region: str
    :param credential: Credential used to authenticate requests to the service. Is either a
     TokenCredential type or a AzureKeyCredential type. Required.
    :type credential: ~azure.core.credentials.TokenCredential or
     ~azure.core.credentials.AzureKeyCredential
    :keyword service_base_url: The Azure Quantum service base url. Default value is
     "quantum.azure.com".
    :paramtype service_base_url: str
    :keyword api_version: The API version to use for this operation. Default value is
     "2024-10-01-preview". Note that overriding this default value may result in unsupported
     behavior.
    :paramtype api_version: str
    """

    def __init__(
        self,
        region: str,
        credential: Union["TokenCredential", AzureKeyCredential],
        *,
        service_base_url: str = "quantum.azure.com",
        **kwargs: Any
    ) -> None:
        _endpoint = "https://{region}.{serviceBaseUrl}"
        self._config = ServicesClientConfiguration(
            region=region, credential=credential, service_base_url=service_base_url, **kwargs
        )
        _policies = kwargs.pop("policies", None)
        if _policies is None:
            _policies = [
                policies.RequestIdPolicy(**kwargs),
                self._config.headers_policy,
                self._config.user_agent_policy,
                self._config.proxy_policy,
                policies.ContentDecodePolicy(**kwargs),
                self._config.redirect_policy,
                self._config.retry_policy,
                self._config.authentication_policy,
                self._config.custom_hook_policy,
                self._config.logging_policy,
                policies.DistributedTracingPolicy(**kwargs),
                policies.SensitiveHeaderCleanupPolicy(**kwargs) if self._config.redirect_policy else None,
                self._config.http_logging_policy,
            ]
        self._client: PipelineClient = PipelineClient(base_url=_endpoint, policies=_policies, **kwargs)

        self._serialize = Serializer()
        self._deserialize = Deserializer()
        self._serialize.client_side_validation = False
        self.jobs = JobsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.sessions = SessionsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.providers = ProvidersOperations(self._client, self._config, self._serialize, self._deserialize)
        self.storage = StorageOperations(self._client, self._config, self._serialize, self._deserialize)
        self.quotas = QuotasOperations(self._client, self._config, self._serialize, self._deserialize)
        self.top_level_items = TopLevelItemsOperations(self._client, self._config, self._serialize, self._deserialize)

    def send_request(self, request: HttpRequest, *, stream: bool = False, **kwargs: Any) -> HttpResponse:
        """Runs the network request through the client's chained policies.

        >>> from azure.core.rest import HttpRequest
        >>> request = HttpRequest("GET", "https://www.example.org/")
        <HttpRequest [GET], url: 'https://www.example.org/'>
        >>> response = client.send_request(request)
        <HttpResponse: 200 OK>

        For more information on this code flow, see https://aka.ms/azsdk/dpcodegen/python/send_request

        :param request: The network request you want to make. Required.
        :type request: ~azure.core.rest.HttpRequest
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~azure.core.rest.HttpResponse
        """

        request_copy = deepcopy(request)
        path_format_arguments = {
            "region": self._serialize.url("self._config.region", self._config.region, "str"),
            "serviceBaseUrl": self._serialize.url(
                "self._config.service_base_url", self._config.service_base_url, "str"
            ),
        }

        request_copy.url = self._client.format_url(request_copy.url, **path_format_arguments)
        return self._client.send_request(request_copy, stream=stream, **kwargs)  # type: ignore

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        self._client.__enter__()
        return self

    def __exit__(self, *exc_details: Any) -> None:
        self._client.__exit__(*exc_details)
