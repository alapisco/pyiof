import hashlib
import os
from pathlib import Path


def calculate_md5(file_path: str):
    """
    Calculate the MD5 checksum of a file.

    This function reads the file specified by `file_path` in binary mode, processes it in chunks to
    efficiently handle large files, and calculates the MD5 checksum of its contents.

    Args:
        file_path (str): The path to the file whose MD5 checksum is to be calculated.

    Returns:
        str: The hexadecimal MD5 checksum string of the file's contents.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_resources_dir() -> str:
    """
    Returns the absolute path to the resources directory of the package.

    Returns:
        str: The absolute path to the 'resources' directory.
    """
    module_dir = Path(__file__).resolve().parent.parent
    return os.path.join(module_dir, 'resources')


def get_test_resources_dir() -> str:
    """
    Returns the absolute path to the test resources directory of the package.

    Returns:
        str: The absolute path to the test 'resources' directory.
    """
    test_resources_dir = Path(__file__).resolve().parent.parent
    return os.path.join(test_resources_dir, 'tests', 'resources')