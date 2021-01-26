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

def create_workspace_mock_login(**kwds) -> Workspace:
    workspace = Workspace(**kwds)

    with unittest.mock.patch.object(MsalWrapper, 'acquire_auth_token', return_value=None):
        workspace.login(False)

    return workspace

def get_config() -> configparser.ConfigParser:
    """Read config file and return config parser

    :return: Config parser for reading config file
    :rtype: configparser.ConfigParser
    """
    config = None
    path = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", ".."))
    if os.path.exists(path):
        config = configparser.ConfigParser()
        config_path = os.path.join(path, "config.ini")
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
            storage="")

        # try to login - this should trigger the device flow
        workspace.login(False)
    else:
        workspace = create_workspace_mock_login()

    return workspace
