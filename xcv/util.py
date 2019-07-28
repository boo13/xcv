""" Based on code I straight-lifted from the talented folks at pipx: https://github.com/pipxproject/pipx/blob/master/pipx/util.py"""
import os
from pathlib import Path
import logging
import shutil
import subprocess
import sys
from typing import List
import datetime

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

def print_all_constants() -> None:
    from xcv.constants import(
        PACKAGE_NAME,
        XCV_VERSION,
        XCV_AUTHOR,
        XCV_EMAIL,
        XCV_DESCRIPTION,
        DEFAULT_PYTHON,
        HOME_PATH,
        XCV_HOME,
        WINDOWS,
        SERIAL_BAUD,
        SERIAL_PORT,
        WIN_DEFAULT_SERIAL_PORT,
        MAC_DEFAULT_SERIAL_PORT,
        TIMEZONE,
    )
    print(f"""
            INFO
            Package Name: {PACKAGE_NAME}
            Version: {XCV_VERSION}
            Author: {XCV_AUTHOR}
            Email: {XCV_EMAIL}
            Description: {XCV_DESCRIPTION}
            
            SYSTEM
            Python: {DEFAULT_PYTHON}
            Home Path: {HOME_PATH}
            XCV Home: {XCV_HOME}
            Windows Machine? {WINDOWS}

            SERIAL
            Serial Baud: {SERIAL_BAUD} 
            Windows Serial Port Default: {WIN_DEFAULT_SERIAL_PORT}
            Mac Serial Port Default: {MAC_DEFAULT_SERIAL_PORT}

            SETTINGS
            Timezone: {TIMEZONE}
            """)


# FPS class is mostly courtesy of imutils
class FPS:
    ''' Frames Per Second for OpenCV Videos. Code is courtesy of https://github.com/jrosebr1/imutils, with a few minor changes.
    '''
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    @property
    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    @property
    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


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

if __name__ == "__main__":
    print_all_constants()