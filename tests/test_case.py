import pytest

from lesson73 import backup_utility


# Test at least six distinct scenarios (including empty folders, missing paths, and non-log file exclusions)
def test_failure_case1():
    # test missing path
    with pytest.raises(ValueError):
        backup_utility.audit_directory_space("")

def test_normal_case():
    pass