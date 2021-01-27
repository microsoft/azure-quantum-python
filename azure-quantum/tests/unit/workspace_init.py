# -*- coding: utf-8 -*-
##
# workspace_init.py: Utilty module that conatains functions that create the Workspace
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

## IMPORTS ##

import os
import configparser
import unittest.mock

from azure.quantum import Workspace
from azure.quantum.workspace import MsalWrapper

from recording_updater import RecordingUpdater

def create_workspace_mock_login(**kwds) -> Workspace:
"""Create a mock Workspace object by patching the Azure authentication and uses a dummy authentication token."""
    workspace = Workspace(**kwds)

    dummy_auth_token = {'access_token': 'eyJ1eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJidWQiOiJodHRwczovL3F1YW50dW0ubWljcm9zb2Z0LmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJpYXQiOjE2MTE2ODMwNjAsIm5iZiI6MTYxMTY4MzA2MCwiZXhwIjoxNjExNjg2OTYwLCJfY2xhaW1fbmFtZXMiOnsiZ3JvdXBzIjoic3JjMSJ9LCJfY2xhaW1fc291cmNlcyI6eyJzcmMxIjp7ImVuZHBvaW50IjoiaHR0cHM6Ly9ncmFwaC53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvdXNlcnMvZTlhNGE5ZTEtODcxNS00Yjc1LTk2NWQtYzBkZDQxMTIzODY4L2dldE1lbWJlck9iamVjdHMifX0sImFjciI6IjEiLCJhaW8iOiJBVlFBcS84U0FBQUFXMnNsMlRORXd5eXA2OGdvejM2RnRoSXFZSlJDdmRibDF0WVJPanUrUzNCZDV5MGsyeWMyOFdKUk9IQ283a0VuNGRpaDh1dkpLQm00TFNoTHRUQ3FsMHMwNkp6N3NYclNpNTFJOEljZThZcz0iLCJhbXIiOlsid2lhIiwibWZhIl0sImFwcGlkIjoiODRiYTA5NDctNmM1My00ZGQyLTljYTktYjM2OTQ3NjE1MjFiIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJCcm93biIsImdpdmVuX25hbWUiOiJUb20iLCJpbl9jb3JwIjoidHJ1ZSIsImlwYWRkciI6IjczLjgzLjM5LjEwIiwibmFtZSI6IlRvbSBCcm93biIsIm9pZCI6ImU5YTRhOWUxLTg3MTUtNGI3NS05NjVkLWMwZGQ0MTEyMzg2OCIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0yMTI3NTIxMTg0LTE2MDQwMTI5MjAtMTg4NzkyNzUyNy0xNzc1MDU1MSIsInB1aWQiOiIxMDAzN0ZGRTkyREI4MzEyIiwicmgiOiIwLkFSb0F2NGo1Y3ZHR3IwR1JxeTE4MEJIYlIwY0p1b1JUYk5KTm5LbXphVWRoVWhzYUFPOC4iLCJzY3AiOiJKb2JzLlJlYWRXcml0ZSIsInN1YiI6IjNxVk1XZ3cxRWozYVRlTEdTenE0bmVsMms1UHFVS1BBY2ZVNDBSUl9JZ3MiLCJ0aWQiOiI3MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDciLCJ1bmlxdWVfbmFtZSI6InRoYnJvQG1pY3Jvc29mdC5jb20iLCJ1cG4iOiJ0aGJyb0BtaWNyb3NvZnQuY29tIiwidXRpIjoiUzMxNVVqbk9JVWUzeDdRR3ZaVWFBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il19.PCWEtCdso3_jehm3Ppg9lCSy_VgwY96IG0_Lqji5tN3yEmBmsP4Du-6MA2IHlz7pbKfQ8Qdw4aeobWZkuDW71Zo9PCkBSLQewng5EMbDvZO3jPJfCOd0IepaPVdtvtaCL2KnPEZicEM4kIO_9f8hCC4Ik8MAem788HuutNhN_YExJDWtM-aNoXIBLtDm39u3bCr2WFk4he3xpISLD3ZqAk2UPKagMwuwO-tArtcoQvA1_n_owv-I5P8vEk1wOmUh6LTB6pUAIS4wFIMgINUE1dBSuQmyimEfc7rRuWl-YJrMH0WRdbgFutwbBv_5dKs6VcYGgrvA3nIGU_Xz5vuJMA', 'token_type': 'Bearer', 'expires_in': 485}
    with unittest.mock.patch.object(MsalWrapper, 'acquire_auth_token', return_value=dummy_auth_token):
        workspace.login(True)

    return workspace


def get_config() -> configparser.ConfigParser:
    """Read config file and return config parser

    :return: Config parser for reading config file
    :rtype: configparser.ConfigParser
    """
    config = None
    config_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", "..", "config.ini"))
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

    return config


def create_workspace() -> Workspace:
    """Create workspace using credentials stored in config file

    :return: Workspace
    :rtype: Workspace
    """
    config = get_config()
    if config:
        workspace = Workspace(
            subscription_id=config["azure.quantum"]["subscription_id"],
            resource_group=config["azure.quantum"]["resource_group"],
            name=config["azure.quantum"]["workspace_name"],
        )

        # try to login - this should trigger the device flow
        workspace.login(False)
    else:
        workspace = create_workspace_mock_login(
            subscription_id=RecordingUpdater.dummy_uid,
            resource_group=RecordingUpdater.dummy_rg,
            name=RecordingUpdater.dummy_ws,
        )

    return workspace
