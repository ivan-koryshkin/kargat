import pytest

from kargat.pm import BaseManager
from kargat.pm import PackageManager
from kargat.pm import config as c


REQ_DEV = {
    "package_dev0": "1.0",
    "package_dev1": "1.1",
    "package_dev2": "1.2"
}


REQ_PROD = {
    "package_prod0": "1.0",
    "package_prod1": "1.1",
    "package_prod2": "1.2"
}


REQS_TEST = {
    "package_test0": "1.0",
    "package_test1": "1.1",
    "package_test2": "1.2"
}

@pytest.fixture(scope="function")
def file_repr():
    base = BaseManager(None, None)
    pattern = base.pattern("test_name", "1,0", "test")
    pattern[c.ROOT][c.REQUIREMENTS][c.DEV] = REQ_DEV
    pattern[c.ROOT][c.REQUIREMENTS][c.PROD] = REQ_PROD
    pattern[c.ROOT][c.REQUIREMENTS][c.TEST] = REQS_TEST
    return pattern


@pytest.mark.parametrize("mode,expected", (
        (c.TEST, [REQ_PROD, REQ_DEV, REQS_TEST]),
        (c.DEV, [REQ_DEV, REQ_PROD]),
        (c.PROD, [REQ_PROD])
))
def test_parse_packages_for_mode(mode, expected, file_repr):
    manager = PackageManager(None)
    manager.file_repr = file_repr
    manager.mode = mode
    packages = manager.parse_packages()
    assert packages is not None
    for section in expected:
        for pkg_name in section:
            assert pkg_name in packages
            assert packages[pkg_name] == section[pkg_name]