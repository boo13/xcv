""" Based on code I straight-lifted from the talented folks at pipx: https://github.com/pipxproject/pipx/blob/master/pipx/util.py"""
import os
from pathlib import Path
import logging
import shutil
import subprocess
import sys
from typing import List


class XcvError(Exception):
    pass

try:
    WindowsError
except NameError:
    WINDOWS = False
else:
    WINDOWS = True


def print_version() -> None:
    from xcv import __version__
    print(f"xcv version: {__version__}")

def print_info() -> None:
    from xcv import __version__, __doc__, __author__, __email__
    print(f"{__doc__}\nxcv version: {__version__}\nAuthor: {__author__}\nEmail: {__email__}\n")


# def rmdir(path: Path):
#     logging.info(f"removing directory {path}")
#     if WINDOWS:
#         os.system(f'rmdir /S /Q "{str(path)}"')
#     else:
#         shutil.rmtree(path)


# def mkdir(path: Path) -> None:
#     if path.is_dir():
#         return
#     logging.info(f"creating directory {path}")
#     path.mkdir(parents=True, exist_ok=True)


# def get_pypackage_bin_path(binary_name: str) -> Path:
#     return (
#         Path("__pypackages__")
#         / (str(sys.version_info.major) + "." + str(sys.version_info.minor))  # noqa E503
#         / "lib"  # noqa E503
#         / "bin"  # noqa E503
#         / binary_name  # noqa E503
#     )
