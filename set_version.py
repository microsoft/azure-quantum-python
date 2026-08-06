#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import re
import base64
from typing import List
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit, unquote

ALLOWED_RELEASE_TYPES = ["major", "minor", "patch"]
ALLOWED_BUILD_TYPES = ["stable", "rc", "dev"]
PACKAGE_NAME = "azure-quantum"
# Public PyPI simple-index fallback, used only for local runs where PIP_INDEX_URL is
# not set. In CI, PipAuthenticate@1 sets PIP_INDEX_URL to the Azure Artifacts feed so
# this script never contacts pypi.org directly (network-isolation / CFS policy).
DEFAULT_INDEX_URL = "https://pypi.org/simple"
# Matches distribution filenames like "azure_quantum-1.2.3-..." or
# "azure-quantum-1.2.3.dev0.tar.gz", so only this package's own versions are captured
# and never a version-like token appearing elsewhere on the index page. The trailing
# boundary (archive suffix or the wheel tag separator) ensures unexpected version
# formats (e.g. legacy 4-part "0.11.2004.2825" or "...b1") are skipped, not truncated.
VERSION_RE = re.compile(
    r"azure[-_]quantum-(\d+\.\d+\.\d+(?:\.(?:dev|rc)\d+)?)(?:-|\.tar\.gz|\.zip)",
    re.IGNORECASE,
)
# Anchored full-string match used to validate a manually supplied version.
# Accepts the same subset the automated path produces: "major.minor.patch" optionally
# followed by ".devN" or ".rcN".
VERSION_INPUT_RE = re.compile(r"^\d+\.\d+\.\d+(?:\.(?:dev|rc)\d+)?$")


RELEASE_TYPE = os.environ.get("RELEASE_TYPE") or "patch"
BUILD_TYPE = os.environ.get("BUILD_TYPE") or "dev"
# Optional manually specified version. When set, this exact version is used and the
# automated computation (which reads the package index) is skipped. Useful when the
# Azure Artifacts feed cache is stale relative to PyPI, e.g. during releases in quick
# succession.
VERSION = (os.environ.get("VERSION") or "").strip()


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


def _version_sort_key(version: str):
    """Return a tuple that orders versions per PEP 440 for the subset used here
    (major.minor.patch optionally followed by ".devN" or ".rcN").

    Ordering within the same major.minor.patch is: dev < rc < final.
    """
    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if len(parts) == 3:
        # A final release sorts after any pre-release of the same number.
        phase, suffix_num = 2, 0
    else:
        match = re.fullmatch(r"(dev|rc)(\d+)", parts[3])
        if not match:
            raise ValueError(
                f"Unsupported pre-release segment in version '{version}'. Expected '.devN' or '.rcN'."
            )
        phase = 0 if match.group(1) == "dev" else 1
        suffix_num = int(match.group(2))
    return (major, minor, patch, phase, suffix_num)


def _get_index_url() -> str:
    """Build the PEP 503 simple-index URL for the package.

    Uses PIP_INDEX_URL (set by PipAuthenticate@1 to the Azure Artifacts feed in CI)
    and falls back to public PyPI for local runs where it is not set.
    """
    index = os.environ.get("PIP_INDEX_URL") or DEFAULT_INDEX_URL
    return index.rstrip("/") + "/" + PACKAGE_NAME + "/"


def _fetch_versions(index_url: str) -> List[str]:
    """Fetch all published versions of the package from a PEP 503 simple index.

    Credentials embedded in the index URL (as PipAuthenticate@1 provides) are moved
    into an Authorization header, since urllib does not use URL userinfo directly.
    """
    parsed = urlsplit(index_url)
    netloc = parsed.hostname or ""
    if parsed.port:
        netloc = f"{netloc}:{parsed.port}"
    sanitized_url = urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, ""))

    request = Request(sanitized_url)
    if parsed.username:
        credentials = f"{unquote(parsed.username)}:{unquote(parsed.password or '')}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("ascii")
        request.add_header("Authorization", f"Basic {encoded}")

    # urlopen raises HTTPError for non-2xx responses and URLError for connection
    # problems, so failures surface as exceptions rather than a checkable status.
    # Re-raise as a RuntimeError with the sanitized URL (never the credentialed one)
    # and the status/reason for a clear, consistent message.
    try:
        with urlopen(request) as response:
            html = response.read().decode("utf-8")
    except HTTPError as error:
        raise RuntimeError(f"Request \"GET:{sanitized_url}\" failed. Status code: \"{error.code}\"") from None
    except URLError as error:
        raise RuntimeError(f"Request \"GET:{sanitized_url}\" failed. Reason: \"{error.reason}\"") from None

    return list(set(VERSION_RE.findall(html)))


def get_build_version(version_type: str, build_type: str) -> str:
    """Get build version by analyzing released versions in the package index and figuring out the next version.
    Example: 
    - If the last stable version was "1.1.0" and version_type = "major" and build_type = "stable", then returned version will be "2.0.0".
    - If the last stable version was "1.1.0" and the last dev version was "1.2.0.dev0" and version_type = "patch" and build_type = "dev", 
    then returned version will be "1.1.1.dev0".
    - If the last stable version was "1.1.0" and the last dev version was "1.2.0.dev0" and version_type = "minor" and build_type = "dev", 
    then returned version will be "1.2.0.dev1".

    :param version_type: SYMVER type ("major"/"minor"/"patch")
    :type version_type: str
    :param build_type: Build type ("stable", "dev", "rc")
    :type build_type: str
    :return: build version
    :rtype: str
    """

    # Get all releases from the package index (the Azure Artifacts feed in CI, which
    # proxies the full version list from its PyPI upstream).
    index_url = _get_index_url()
    package_versions_all = _fetch_versions(index_url)

    # Guard: refuse to compute a version from an empty list. That would silently
    # produce a low version number that likely collides with an existing release.
    if not package_versions_all:
        raise RuntimeError(
            f"No published versions of \"{PACKAGE_NAME}\" were returned from the package "
            f"index. Refusing to compute a version from an empty list."
        )

    # Note: assuming versions are SYMVER (major.minor.patch[.dev0|.rc0]).
    # "1.0.0", "1.0.1", "1.1.0", "1.1.0.dev0", "1.1.0.dev1", "1.1.0.rc0"
    # The next "rc" and "dev" version must follow the last "stable" version.

    # Sort by version (descending) so the most recent releases come first, which is
    # the ordering _get_build_version expects.
    package_versions = sorted(package_versions_all, key=_version_sort_key, reverse=True)

    # Diagnostic output: the index host, the number of versions found, and the most
    # recent one, to confirm the index returned a sane published history.
    print(f"Package index host: {urlsplit(index_url).hostname}")
    print(f"Retrieved {len(package_versions)} version(s) of \"{PACKAGE_NAME}\" from the package index.")
    print(f"Most recent version: {package_versions[0]}")

    build_version = _get_build_version(version_type, build_type, package_versions)

    # Guard: never hand back a version that already exists in the published list.
    if build_version in package_versions:
        raise RuntimeError(
            f"Computed version \"{build_version}\" already exists in the package index. "
            f"Aborting to avoid republishing an existing version."
        )

    return build_version


def resolve_build_version(version_type: str, build_type: str, version: str = "") -> str:
    """Resolve the version to ship for this run.

    If ``version`` is a non-empty string, it is validated and used as-is, skipping the
    automated computation that reads the package index. Otherwise the next version is
    computed from the published version history.

    When a version is specified, it must agree with ``build_type``: a "dev" build must
    supply a ".devN" version, an "rc" build a ".rcN" version, and a "stable" build a
    plain "major.minor.patch" version (no pre-release suffix).

    :param version_type: SYMVER type ("major"/"minor"/"patch"); ignored when a version
        is specified.
    :param build_type: Build type ("stable"/"dev"/"rc"). Determines which pre-release
        suffix a specified version must carry.
    :param version: Exact version to use, or "" to compute automatically.
    :return: The version to ship.
    :rtype: str
    """
    specified_version = (version or "").strip()
    if specified_version:
        if not VERSION_INPUT_RE.match(specified_version):
            raise ValueError(
                f"Version \"{specified_version}\" is not a valid version. Expected "
                f"\"major.minor.patch\" optionally followed by \".devN\" or \".rcN\"."
            )

        # The specified version must match the selected build type, so a build tagged
        # "dev"/"rc" can't ship a version that lacks (or mismatches) the suffix.
        if build_type == "dev" and ".dev" not in specified_version:
            raise ValueError(
                f"Build type \"dev\" requires a \".devN\" version, but got "
                f"\"{specified_version}\"."
            )
        if build_type == "rc" and ".rc" not in specified_version:
            raise ValueError(
                f"Build type \"rc\" requires a \".rcN\" version, but got "
                f"\"{specified_version}\"."
            )
        if build_type == "stable" and (".dev" in specified_version or ".rc" in specified_version):
            raise ValueError(
                f"Build type \"stable\" requires a \"major.minor.patch\" version "
                f"without a pre-release suffix, but got \"{specified_version}\"."
            )

        print(f"Using manually specified version: {specified_version}")
        return specified_version

    return get_build_version(version_type, build_type)


if __name__ == "__main__":
    build_version = resolve_build_version(RELEASE_TYPE, BUILD_TYPE, VERSION)

    print(f"Package version: {build_version}")

    # Set PYTHON_VERSION variable for steps in same job to reference as $(PYTHON_VERSION)
    print(f"##vso[task.setvariable variable=PYTHON_VERSION;]{build_version}")

    # Set build tags
    print(f"##vso[build.addbuildtag]v{build_version}")
    print(f"##vso[build.addbuildtag]{BUILD_TYPE}")