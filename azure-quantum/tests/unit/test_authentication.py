#!/bin/env python
# -*- coding: utf-8 -*-
##
# test_authentication.py: Checks correctness of azure.quantum._authentication module.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import json
import os
from pathlib import Path
import time

import pytest
from unittest.mock import patch

from azure.identity import CredentialUnavailableError
from azure.quantum._authentication import _TokenFileCredential
from .common import QuantumTestBase

_AZURE_QUANTUM_SCOPE = "https://quantum.microsoft.com/.default"


class TestWorkspace(QuantumTestBase):
    def test_azure_quantum_token_credential_file_not_set(self):
        credential = _TokenFileCredential()
        with pytest.raises(CredentialUnavailableError) as exception:
            credential.get_token(_AZURE_QUANTUM_SCOPE)

        assert "Token file location not set." in str(exception.value)

    def test_azure_quantum_token_credential_file_not_exists(self):
        with patch.dict(os.environ, { "AZURE_QUANTUM_TOKEN_FILE": "fake_file_path" }, clear=True):
            with patch('os.path.isfile') as mock_isfile:
                mock_isfile.return_value = False
                credential = _TokenFileCredential()                
                with pytest.raises(CredentialUnavailableError) as exception:
                    credential.get_token(_AZURE_QUANTUM_SCOPE)
                
                assert "Token file at fake_file_path does not exist." in str(exception.value)

    def test_azure_quantum_token_credential_file_invalid_json(self):
        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text("not a json")
        with patch.dict(os.environ, { "AZURE_QUANTUM_TOKEN_FILE": str(file.resolve()) }, clear=True):
            credential = _TokenFileCredential()                
            with pytest.raises(CredentialUnavailableError) as exception:
                credential.get_token(_AZURE_QUANTUM_SCOPE)
            
            assert "Failed to parse token file: Invalid JSON." in str(exception.value)

    def test_azure_quantum_token_credential_file_missing_expires_on(self):
        content = {
            "access_token": "fake_token",
        }

        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text(json.dumps(content))
        with patch.dict(os.environ, { "AZURE_QUANTUM_TOKEN_FILE": str(file.resolve()) }, clear=True):
            credential = _TokenFileCredential()                
            with pytest.raises(CredentialUnavailableError) as exception:
                credential.get_token(_AZURE_QUANTUM_SCOPE)
            
            assert "Failed to parse token file: Missing expected value: 'expires_on'" in str(exception.value)

    def test_azure_quantum_token_credential_file_token_expired(self):
        content = {
            "access_token": "fake_token",
            "expires_on": 1628543125086 # Matches timestamp in error message below
        }

        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text(json.dumps(content))
        with patch.dict(os.environ, { "AZURE_QUANTUM_TOKEN_FILE": str(file.resolve()) }, clear=True):
            credential = _TokenFileCredential()                
            with pytest.raises(CredentialUnavailableError) as exception:
                credential.get_token(_AZURE_QUANTUM_SCOPE)
            
            assert "Token already expired at Mon Aug  9 21:05:25 2021" in str(exception.value)

    def test_azure_quantum_token_credential_file_valid_token(self):
        one_hour_ahead = time.time() + 60*60
        content = {
            "access_token": "fake_token",
            "expires_on": one_hour_ahead * 1000 # Convert to milliseconds
        }

        tmpdir = self.create_temp_dir()
        file = Path(tmpdir) / "token.json"
        file.write_text(json.dumps(content))
        with patch.dict(os.environ, { "AZURE_QUANTUM_TOKEN_FILE": str(file.resolve()) }, clear=True):
            credential = _TokenFileCredential()                
            token = credential.get_token(_AZURE_QUANTUM_SCOPE)
        
        assert token.token == "fake_token"
        assert token.expires_on == pytest.approx(one_hour_ahead)