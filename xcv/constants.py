# ====================================
#   Package Info
# ====================================
from xcv.tools.os_is_windows import WINDOWS
from xcv import __version__, __author__, __email__

PACKAGE_NAME = "xcv"
XCV_VERSION = __version__
XCV_AUTHOR = __author__
XCV_EMAIL = __email__
XCV_DESCRIPTION = f"""
        The project's goal is to make game-based OpenCV experiments easier.

        By avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. 
        On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins
        (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.
    """


# ====================================
#   System
# ====================================
# Datetime
TIMEZONE = "US/Eastern"

import os
import sys
from pathlib import Path, PureWindowsPath

DEFAULT_PYTHON = sys.executable
HOME_PATH = Path.home()
XCV_HOME = Path()
ABSPATH = os.path.abspath(os.path.dirname(__file__))
IMAGE_PATH = PureWindowsPath(ABSPATH)

if __name__ == "__main__":
    from xcv.tools.print_sysinfo import print_all_constants

    print_all_constants()
