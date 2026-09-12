from pathlib import Path

import pytest

from lesson73 import backup_utility


def test_failure_case1():
    # test missing path
    with pytest.raises(ValueError):
        backup_utility.audit_directory_space("")

def test_normal_case1():
    dst_dir = backup_utility.create_staged_backup(
        Path.cwd() / Path('src') / Path('sample_resource') / Path('sample_target'),
        Path.cwd(),
        'cmprsd_fldr'
    )
    assert Path(dst_dir) == (Path.cwd() / 'cmprsd_fldr.zip')

def test_normal_case2():
    key_set = ["total", "used", "free"]
    usage_dict = backup_utility.audit_directory_space(Path.home())
    for key in usage_dict:
        assert key in key_set
        assert usage_dict[key] > 0