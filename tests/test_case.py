from pathlib import Path

import pytest

from lesson73 import backup_utility


def test_failure_case1():
    # test missing path
    with pytest.raises(ValueError):
        backup_utility.audit_directory_space("")

def test_normal_case():
    backup_utility.create_staged_backup(
        Path.cwd() / Path('src') / Path('sample_resource') / Path('sample_target'),
        Path.cwd(),
        'cmprsd_fldr'
    )