#!/bin/env python
# -*- coding: utf-8 -*-
##
# recording_updater.py: Updates test recordings with dummy values
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

## IMPORTS ##

import glob
import os
import re


class RecordingUpdater:
    """RecordingUpdater
    
    Replaces secrets with dummy values in network recordings.
    """
    dummy_uid = "00000000-0000-0000-0000-000000000000"
    dummy_rg = "dummy-rg"
    dummy_ws = "dummy-ws"

    def __init__(self, recording_directory, recording_glob):
        super().__init__()
        path = os.path.join(recording_directory, recording_glob)
        self._recording_file_names = glob.glob(path)
        self._auth_prog = re.compile(r'authorization_uri="https://login.windows.net/(?P<authid>([a-f0-9]+[-]){4}[a-f0-9]+)"')

    def update_recordings_with_dummy_values(self):
        progs = self._get_regex_programs()
        for file_name in self._recording_file_names:
            with open(file_name) as afile:
                contents = afile.read()
                for prog, replacement in progs:
                    contents = prog.sub(replacement, contents)
                contents = self._replace_auth_with_dummy_values(contents)
            with open(file_name, 'w') as afile:
                afile.write(contents)
            
    def _get_regex_programs(self):
        progs = []
        # progs.append((re.compile(<regex>), <replacemnt-string>))
        progs.append((re.compile(r'/subscriptions/([a-f0-9]+[-]){4}[a-f0-9]+'), "/subscriptions/" + self.dummy_uid))
        progs.append((re.compile(r'job-([a-f0-9]+[-]){4}[a-f0-9]+'), "job-" + self.dummy_uid))
        progs.append((re.compile(r'jobs/([a-f0-9]+[-]){4}[a-f0-9]+'), "jobs/" + self.dummy_uid))
        progs.append((re.compile(r'"id":\s*"([a-f0-9]+[-]){4}[a-f0-9]+"'), '"id": "{}"'. format(self.dummy_uid)))
        progs.append((re.compile(r'/resourceGroups/[a-z0-9-]+/'), "/resourceGroups/dummy-rg/"))
        progs.append((re.compile(r'/workspaces/[a-z0-9-]+/'), "/workspaces/dummy-ws/"))
        progs.append((re.compile(r'sig=[0-9a-zA-Z%]+\&'), "sig=sanitized&"))
        return progs

    def _replace_auth_with_dummy_values(self, contents):
        match = self._auth_prog.search(contents)
        if match:
            info = match.groupdict()
            auth_id = info["authid"]
            contents = contents.replace(auth_id, self.dummy_uid)
        return contents
