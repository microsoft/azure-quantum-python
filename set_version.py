#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
from typing import List
from urllib.request import urlopen
import json

ALLOWED_RELEASE_TYPES = ["major", "minor", "patch"]
ALLOWED_BUILD_TYPES = ["stable", "rc", "dev"]
PACKAGE_NAME = "azure-quantum"
PYPI_URL = f"https://pypi.python.org/pypi/{PACKAGE_NAME}/json"


RELEASE_TYPE = os.environ.get("RELEASE_TYPE") or "patch"
BUILD_TYPE = os.environ.get("BUILD_TYPE") or "dev"


if RELEASE_TYPE not in ALLOWED_RELEASE_TYPES:
    print(f"RELEASE_TYPE environment variable must be {', '.join(ALLOWED_RELEASE_TYPES)}. Current value: {RELEASE_TYPE}")
    exit(1)

if BUILD_TYPE not in ALLOWED_BUILD_TYPES:
    print(f"BUILD_TYPE environment variable must be {', '.join(ALLOWED_BUILD_TYPES)}. Current value: {BUILD_TYPE}")
    exit(1)


def _get_build_version(version_type: str, build_type: str, package_versions: List[str]) -> str:
    
    stable_version_parts = None

    # find last stable version
    for version in package_versions:
        version_parts = str(version).split(".")
        if len(version_parts) == 3:
            stable_version_parts = version_parts
            break

    if stable_version_parts is None:
        stable_version_parts = ["0", "0", "0"]

    if version_type == "major":
        next_stable_version = f"{int(stable_version_parts[0]) + 1}.0.0"
    elif version_type == "minor":
        next_stable_version = f"{stable_version_parts[0]}.{int(stable_version_parts[1]) + 1}.0"
    elif version_type == "patch":
        next_stable_version = f"{stable_version_parts[0]}.{stable_version_parts[1]}.{int(stable_version_parts[2]) + 1}"
    else:
        raise ValueError(f"Version type \"{version_type}\" is not supported.")

    if build_type == "stable":
        return next_stable_version

    # in case the build type is not "stable" find last "rc"/"dev" release and bump up it's suffix-number
    for i in range(0, 100):
        next_version = f"{next_stable_version}.{build_type}{i}"
        if next_version not in package_versions:
            return next_version

    raise RuntimeError(f"Build version could not be determined for version type \"{version_type}\" and build type \"{build_type}\"")


def get_build_version(version_type: str, build_type: str) -> str:

    # get all releases from PyPi
    with urlopen(PYPI_URL) as response:
        if response.status == 200:
            response_content = response.read()
            response = json.loads(response_content.decode("utf-8"))
        else:
            raise RuntimeError(f"Request \"GET:{PYPI_URL}\" failed. Status code: \"{response.status}\"")
    
    # assuming versions are SYMVER (major.minor.patch[.dev0|.rc0]) and in chronological order "1.0.0", "1.0.1", "1.1.0", "1.1.0.dev0", "1.1.0.dev1", "1.1.0.rc0"
    # "rc" and "dev" versions don't have to be in order between each other, but both of them must follow the last "stable" version
    package_versions_sorted = sorted(response["releases"].items(), key=lambda k: k[1][0]["upload_time_iso_8601"], reverse=True)
    package_versions = [version[0] for version in package_versions_sorted]

    return _get_build_version(version_type, build_type, package_versions)


if __name__ == "__main__":
    build_version = get_build_version(RELEASE_TYPE, BUILD_TYPE)

    print(f"Package version: {build_version}")

    # Set PYTHON_VERSION variable for steps in same job to reference as $(PYTHON_VERSION)
    print(f"##vso[task.setvariable variable=PYTHON_VERSION;]{build_version}")

    # Set build tags
    print(f"##vso[build.addbuildtag]v{build_version}")
    print(f"##vso[build.addbuildtag]{BUILD_TYPE}")