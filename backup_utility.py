import shutil
from pathlib import Path


def audit_directory_space(target_path: str) -> dict:
    """Evaluates disk space and returnes a dictionary with total, used, and free capacity.\n
    shutil.disk_usage returns a named tuple with the keys named 'total' and 'used', 'free'."""

    target_dir = Path(target_path).resolve()
    if not target_dir.is_dir():
        raise FileNotFoundError(f'[ERROR]Given target is not found: {target_dir}')

    try:
        usage_named_tuple = shutil.disk_usage(target_dir)
        return {"total": int(usage_named_tuple.total / (1024 * 1024)), 
                "used": int(usage_named_tuple.used / (1024 * 1024)),
                "free": int(usage_named_tuple.free / (1024 * 1024))}
    except FileNotFoundError:
        print(f'[ERROR]File not found: {target_dir}')
        raise
    except PermissionError:
        print(f'[ERROR]Not allowed to access: {target_dir}' )
        raise
    except OSError as e:
        print(f'[ERROR]Failed to reach the storage. path: {target_dir}, error: ({e})')
        raise



def correct_target_logs(source_dir: str, extension: str) -> list:
    """Discover all files matching a specific extension (e.g., .log, .txt)"""

    # try to reach the dir and return files that including the extension
    dir_path = Path(source_dir).resolve()
    try:
        discovered_files = []
        for file_path in dir_path.glob(f'*{extension}'):
            if file_path.is_file() and file_path.stat().st_size > 0 :
                discovered_files.append(file_path)
        print('[DONE]')
        return discovered_files
    except FileNotFoundError:
        print(f'[ERROR]File not found: {source_dir}')
        raise
    except PermissionError:
        print(f'[ERROR]Not allowed to access: {source_dir}')
        raise
    except OSError:
        print(f'[ERROR]Failed to reach the storage. path: {source_dir}')
        raise



def create_staged_backup(source_dir: str, stage_dir: str, archive_name: str) -> str:
    """Copies discovered files into a staging directory using shutil.copy2(),\n
    compress the staged directory into a zip archive, and returns the final archive file path."""

    source_dir_path = Path(source_dir)
    stage_dir_path = Path(stage_dir)
    archive_name_path = Path(archive_name)

    # check whether the partition has enough storage for copy and archive
    # the free disk needs to have a multiplier of 3 times the source file size in this function
    free_disk_MB = shutil.disk_usage(stage_dir_path).free
    source_usage_MB = Path.stat(source_dir_path).st_size
    if source_usage_MB * 3 > free_disk_MB:
        raise OSError(f"Insufficient disk space: need {source_usage_MB * 3} MB, have {free_disk_MB} MB")

    try:
    # find file and staging directory
        staged_source_dir = shutil.copy2(
            src= source_dir_path.resolve(),
            dst= stage_dir_path.resolve())

    # compress the staged directory into a zip archive
        target_base_name = (stage_dir_path / archive_name_path).resolve()
        compressed_file_dst = shutil.make_archive(
            base_name= target_base_name,
            format= 'zip',
            root_dir= Path(staged_source_dir).parent,
            base_dir= Path(staged_source_dir).name
        )
    except (FileNotFoundError, PermissionError, OSError):
        print(f"[ERROR]Couldn't reach the pathes. source: {source_dir}, stage_dir: {stage_dir}")
        raise

    # return final archive file path
    return compressed_file_dst



def run_debug() -> None:

    usage_dict = audit_directory_space(Path.home())
    for key in usage_dict:
        print(f'{key}: {usage_dict[key]} MB')


    print(f'[INFO]including .log: {correct_target_logs(".", ".log")}')


    print(f'{create_staged_backup(
        Path.cwd() / Path('sample_target'),
        Path.cwd(),
        'cmprsd_fldr'
    )}')


if __name__ == '__main__':
    run_debug()