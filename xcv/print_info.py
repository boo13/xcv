import xcv
from xcv.emojis import BOO

def print_package_info():
    print(f"     {BOO}")
    print(f"{xcv.__email__}")
    print(f" XCV Version: {xcv.version.XCV_VERSION}")
