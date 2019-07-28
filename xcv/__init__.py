"""XCV - An open-source project. Using PySerial and Opencv-Python to take a video feed and send commands to a teensy, which is connected to a hacked controller. 

"""
__author__ = """Randy Boo13 Boo"""
__email__ = "boo13bot@gmail.com"
__version__ = "0.1.0"
__all__ = ["Constants", "cli", "api", "game", "commands"]

import os
import sys

assert sys.version_info >= (3, 7, 0), ("Python 3.7+ is required")

os.system("cls||clear")