# Tests for "set_version.py" module.
# !! Don't forget to run this test in case you change "set_version.py" to make sure the asserts still pass !!

from set_version import _get_build_version

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
    assert "0.1.2.dev0" == _get_build_version("patch", "dev", ["0.1.1", "0.0.1"])
    assert "0.1.1.dev1" == _get_build_version("patch", "dev", ["1.0.0.rc0", "0.1.1.dev0", "0.1.0", "0.0.1"])