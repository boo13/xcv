from dataclasses import dataclass


def set_the_settings():
    """Return the operating system python is currently using"""
    import platform

    if platform.system() == "Darwin":
        print("Woo using a Mac! ⚡ Let's use emojis in the command line!")
        return False

    if platform.system() == "Windows":
        print("You're using Windows, which is ok too.. it's a personal choice.")
        return True


WINDOWS = set_the_settings()
# ====================================
#   Serial
# ====================================

WIN_DEFAULT_SERIAL_PORT = "COM17"
MAC_DEFAULT_SERIAL_PORT = "/dev/cu.SLAB_USBtoUART"

# System Logic
if WINDOWS:
    SERIAL_PORT = WIN_DEFAULT_SERIAL_PORT
else:
    SERIAL_PORT = MAC_DEFAULT_SERIAL_PORT

# LOCAL SETTINGS - we use these to set (and mostly forget) the Serial connection config
@dataclass
class Settings:
    timerFlag: int = 10
    verbose: bool = False
    SERIAL_BAUD: int = 115200
    debug_indent: str = "\n\t\t"
    centered_indent: str = "\n\t\t\t\t"
