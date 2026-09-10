import shutil
from pathlib import Path


def audit_directory_space(target_path: str) -> dict:
    """Evaluates disk space and returnes a dictionary with total, used, and free capacity.\n
    shutil.disk_usage returns a named tuple with the keys named 'total' and 'used', 'free'."""

    # correct error handling will be implemented in feature
    try:
        usge_named_tuple = shutil.disk_usage(target_path)
        return {"total": int(usge_named_tuple.total / (1024 * 1024)), 
                "used": int(usge_named_tuple.used / (1024 * 1024)),
                "free": int(usge_named_tuple.free / (1024 * 1024))}
    except FileNotFoundError:
        print(f'File not found: {target_path}')
        raise
    except PermissionError:
        print(f'Not allowed to access: {target_path}' )
        raise
    except OSError as e:
        print(f'Failed to reach the storage. path: {target_path}, error: ({e})')
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
        return discovered_files
    except FileNotFoundError:
        print(f'File not found: {source_dir}')
        raise
    except PermissionError:
        print(f'Not allowed to access: {source_dir}' )
        raise
    except OSError:
        print(f'Failed to reach the storage. path: {source_dir}')
        raise



def create_staged_backup(source_dir: str, stage_dir: str, archive_name: str) -> str:
    """Copies discovered files into a staging directory using shutil.copy2(),\n
    compress the staged directory into a zip archive, and returns the final archive file path."""

    try:
    # find file and staging directory: need to implemented after


    # compress the staged directory into a zip archive

        target_base_name = (Path(stage_dir) / archive_name).resolve()
        shutil.make_archive(
            base_name= target_base_name,
            format= 'zip',
            root_dir= Path(source_dir).parent,
            base_dir= Path(source_dir).name
        )
    except (FileNotFoundError, PermissionError, OSError):
        print(f"Couldn't reach the pathes. source: {source_dir}, stage_dir: {stage_dir}")
        raise

    # return final archive file path
    return target_base_name



def run_debug() -> None:
    usage_dict = audit_directory_space(Path.home())
    for key in usage_dict:
        print(f'{key}: {usage_dict[key]} MB')


    print(f'including .log: {correct_target_logs(".", ".log")}')


    print(f'{create_staged_backup(
        Path.cwd() / Path('sample_target'),
        Path.cwd(),
        'cmprsd_fldr'
    )}')



run_debug()