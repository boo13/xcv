import xcv
from xcv.version import XCV_VERSION
from xcv.emojis import BOO

def print_package_info():
    print(f"Author: {BOO}")
    print(f"Email: {xcv.__email__}")
    print(f"XCV Version: {XCV_VERSION}")
