# Tests for "set_version.py" module.
# !! Don't forget to run this test in case you change "set_version.py" to make sure the asserts still pass !!

import pytest

import set_version
from set_version import (
    _get_build_version,
    _version_sort_key,
    get_build_version,
    resolve_build_version,
    VERSION_RE,
)

def test_set_version():
    assert "1.0.0" == _get_build_version("major", "stable", [])
    assert "2.0.0" == _get_build_version("major", "stable", ["1.1.0"])
    assert "1.0.0" == _get_build_version("major", "stable", ["0.1.1.rc1", "0.1.1.rc0", "0.1.0", "0.0.1"])
    assert "1.0.0" == _get_build_version("major", "stable", ["0.1.1.dev0", "0.1.1.rc0", "0.1.0", "0.0.1"])
    assert "0.1.0" == _get_build_version("minor", "stable", ["0.0.2", "0.0.1"])
    assert "0.2.0" == _get_build_version("minor", "stable", ["0.1.1.dev0", "0.1.1.rc0", "0.1.0", "0.0.1"])
    assert "0.1.2" == _get_build_version("patch", "stable", ["0.1.1", "0.0.1"])
    assert "0.1.1" == _get_build_version("patch", "stable", ["0.1.1.rc1", "0.1.1.rc0", "0.1.0", "0.0.1"])
    
    assert "1.0.0.rc0" == _get_build_version("major", "rc", [])
    assert "2.0.0.rc0" == _get_build_version("major", "rc", ["3.0.0.dev0", "1.1.0"])
    assert "3.0.0.rc1" == _get_build_version("major", "rc", ["3.0.0.rc0", "2.1.0", "1.1.0"])
    assert "0.1.0.rc0" == _get_build_version("minor", "rc", ["0.0.2", "0.0.1"])
    assert "0.1.2.rc0" == _get_build_version("patch", "rc", ["0.1.1", "0.0.1"])
    assert "0.1.1.rc1" == _get_build_version("patch", "rc", ["1.0.0.dev0", "0.1.1.rc0", "0.1.0", "0.0.1"])

    assert "1.0.0.dev0" == _get_build_version("major", "dev", [])
    assert "2.0.0.dev0" == _get_build_version("major", "dev", ["3.0.0.rc0", "1.1.0"])
    assert "3.0.0.dev1" == _get_build_version("major", "dev", ["3.0.0.dev0", "2.1.0", "1.1.0"])
    assert "0.1.0.dev0" == _get_build_version("minor", "dev", ["0.0.2", "0.0.1"])
    assert "0.2.0.dev0" == _get_build_version("minor", "dev", ["1.0.0.rc0", "1.0.0.dev0", "0.1.0", "0.0.1"])
    assert "0.1.2.dev0" == _get_build_version("patch", "dev", ["0.1.1", "0.0.1"])
    assert "0.1.1.dev0" == _get_build_version("patch", "dev", ["1.0.0.rc0", "0.1.0.dev0", "0.1.0", "0.0.1"])
    assert "0.1.1.dev1" == _get_build_version("patch", "dev", ["1.0.0.rc0", "0.1.1.dev0", "0.1.0", "0.0.1"])


def test_version_regex_matches_wheel_and_sdist_filenames():
    # Representative distribution filenames as they appear on a PEP 503 simple index,
    # covering wheels, sdists (.tar.gz / .zip), the "-"/"_" name normalization, and
    # the .devN / .rcN pre-release suffixes.
    html = (
        '<a href="x">azure_quantum-3.10.0-py3-none-any.whl</a>'
        '<a href="x">azure-quantum-3.10.0.tar.gz</a>'
        '<a href="x">azure_quantum-1.1.0.dev0-py3-none-any.whl</a>'
        '<a href="x">azure-quantum-2.0.0.rc0.tar.gz</a>'
        '<a href="x">azure-quantum-1.0.0.zip</a>'
    )
    assert sorted(set(VERSION_RE.findall(html))) == [
        "1.0.0",
        "1.1.0.dev0",
        "2.0.0.rc0",
        "3.10.0",
    ]


def test_version_regex_skips_unsupported_filenames():
    # Legacy 4-part and alpha/beta ("bN") versions must be skipped entirely rather
    # than silently truncated to a bogus 3-part version, and unrelated tokens on the
    # page must never match.
    html = (
        '<a href="x">azure_quantum-0.11.2004.2825-py3-none-any.whl</a>'
        '<a href="x">azure-quantum-0.11.2004.2825.tar.gz</a>'
        '<a href="x">azure_quantum-0.13.2011.119705b1-py3-none-any.whl</a>'
        '<a href="x">some-other-package-9.9.9-py3-none-any.whl</a>'
        '<a href="/download/azure-quantum/1.2.3/">1.2.3</a>'
    )
    assert VERSION_RE.findall(html) == []


def test_version_sort_key_orders_prereleases_before_final():
    # Within the same major.minor.patch: dev < rc < final, with numeric (not
    # lexical) ordering of the pre-release number.
    unsorted = [
        "1.1.0",
        "1.1.0.rc0",
        "1.1.0.dev10",
        "1.1.0.dev2",
        "1.0.0",
    ]
    assert sorted(unsorted, key=_version_sort_key) == [
        "1.0.0",
        "1.1.0.dev2",
        "1.1.0.dev10",
        "1.1.0.rc0",
        "1.1.0",
    ]


def test_version_sort_key_rejects_unsupported_segment():
    with pytest.raises(ValueError):
        _version_sort_key("0.13.2011.119705b1")


def test_get_build_version_sorts_before_selecting(monkeypatch):
    # _fetch_versions returns versions in arbitrary order; get_build_version must
    # sort them (descending) before picking the latest stable to bump from. If the
    # sort were skipped, the first 3-part entry ("1.0.0") would be chosen instead of
    # the true latest stable ("1.1.0").
    unsorted = [
        "1.0.0.dev0",
        "1.0.0",
        "1.1.0",
        "1.0.0.rc0",
        "2.0.0.dev1",
        "1.1.0.dev0",
    ]
    monkeypatch.setattr(set_version, "_fetch_versions", lambda index_url: list(unsorted))

    # The latest *stable* (3-part final) version is 1.1.0. 2.0.0 exists only as a
    # pre-release ("2.0.0.dev1"), so it is not a release that can be patched from.
    assert get_build_version("patch", "stable") == "1.1.1"
    assert get_build_version("patch", "dev") == "1.1.1.dev0"
    assert get_build_version("minor", "dev") == "1.2.0.dev0"
    # 2.0.0.dev1 exists but 2.0.0.dev0 does not, so dev0 is the next major dev build.
    assert get_build_version("major", "dev") == "2.0.0.dev0"


def test_get_build_version_empty_list_raises(monkeypatch):
    monkeypatch.setattr(set_version, "_fetch_versions", lambda index_url: [])
    with pytest.raises(RuntimeError):
        get_build_version("patch", "dev")


def test_get_build_version_existing_version_raises(monkeypatch):
    # Guard: if the computed version already exists in the published list, abort
    # rather than risk republishing an existing version.
    monkeypatch.setattr(set_version, "_fetch_versions", lambda index_url: ["1.0.0"])
    monkeypatch.setattr(set_version, "_get_build_version", lambda *args: "1.0.0")
    with pytest.raises(RuntimeError):
        get_build_version("patch", "stable")


@pytest.mark.parametrize(
    "version",
    ["1.2.3", "1.2.3.dev0", "10.20.30.rc5"],
)
def test_resolve_build_version_uses_specified_version(monkeypatch, version):
    # A valid specified version is returned as-is and the automated computation is
    # skipped entirely (so the package index is never contacted).
    def _should_not_be_called(*args, **kwargs):
        raise AssertionError("get_build_version must not be called when a version is given")

    monkeypatch.setattr(set_version, "get_build_version", _should_not_be_called)
    # Pick a build type that matches each version so the agreement check passes.
    build_type = "stable"
    if ".dev" in version:
        build_type = "dev"
    elif ".rc" in version:
        build_type = "rc"
    assert resolve_build_version("patch", build_type, version) == version


@pytest.mark.parametrize(
    "blank",
    ["", "   ", None],
)
def test_resolve_build_version_falls_back_when_blank(monkeypatch, blank):
    # A blank/whitespace/None version falls back to the automated computation.
    monkeypatch.setattr(
        set_version, "get_build_version", lambda vt, bt: f"computed-{vt}-{bt}"
    )
    assert resolve_build_version("minor", "rc", blank) == "computed-minor-rc"


@pytest.mark.parametrize(
    "version",
    ["1.2", "1.2.3.4", "1.2.3.beta0", "1.2.3.dev", "v1.2.3"],
)
def test_resolve_build_version_rejects_invalid_version(monkeypatch, version):
    # A malformed version fails loud rather than shipping a bad version.
    monkeypatch.setattr(
        set_version, "get_build_version", lambda *a, **k: "should-not-be-used"
    )
    with pytest.raises(ValueError):
        resolve_build_version("patch", "dev", version)


@pytest.mark.parametrize(
    "build_type,version",
    [
        # Build type expects a suffix the version doesn't carry (or vice versa).
        ("dev", "1.2.3"),
        ("dev", "1.2.3.rc0"),
        ("rc", "1.2.3"),
        ("rc", "1.2.3.dev0"),
        ("stable", "1.2.3.dev0"),
        ("stable", "1.2.3.rc0"),
    ],
)
def test_resolve_build_version_rejects_build_type_mismatch(monkeypatch, build_type, version):
    # A specified version whose suffix disagrees with the build type fails loud.
    monkeypatch.setattr(
        set_version, "get_build_version", lambda *a, **k: "should-not-be-used"
    )
    with pytest.raises(ValueError):
        resolve_build_version("patch", build_type, version)


@pytest.mark.parametrize(
    "build_type,version",
    [
        ("dev", "1.2.3.dev0"),
        ("rc", "1.2.3.rc7"),
        ("stable", "1.2.3"),
    ],
)
def test_resolve_build_version_accepts_matching_build_type(monkeypatch, build_type, version):
    # A specified version whose suffix matches the build type is accepted.
    monkeypatch.setattr(
        set_version, "get_build_version", lambda *a, **k: "should-not-be-used"
    )
    assert resolve_build_version("patch", build_type, version) == version