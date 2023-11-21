#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os

major_minor = "0.29"

BUILD_TYPE = os.environ.get("BUILD_TYPE") or "dev"
PATCH_NUMBER = os.environ.get("PATCH_NUMBER")

if BUILD_TYPE not in ["dev", "rc", "stable"]:
    print(f"BUILD_TYPE environment variable must be 'dev', 'rc', or 'stable'. Current value: {BUILD_TYPE}")
    exit(1)

try:
    patch_ver = int(PATCH_NUMBER)
except:
    print(f"PATCH_NUMBER environment variable must be set to a valid integer. Current value: {PATCH_NUMBER}")
    exit(1)

version_triple = "{}.{}".format(major_minor, patch_ver)

pip_suffix = {"stable": "", "rc": "rc0", "dev": "dev0"}
pip_version = "{}{}".format(version_triple, pip_suffix.get(BUILD_TYPE))

print("PYTHON_VERSION: {}".format(pip_version))

# Set PYTHON_VERSION variable for steps in same job to reference as $(PYTHON_VERSION)
print(f"##vso[task.setvariable variable=PYTHON_VERSION;]{pip_version}")

# Set build tags
print(f"##vso[build.addbuildtag]v{pip_version}")
print(f"##vso[build.addbuildtag]{BUILD_TYPE}")
