# settings.py
# I appreciate multiple people giving their take, it's really helping me think about the problem and how the language works more than a surface-level hack-it-together approach.
# TODO:
#   - Is it best practice to create custom Exception Errors like I did with `OS_Error`, even if only used once?
#       - Is this being 'explicit vs implicit' or overly-verbsoe?
#   - Maybe overthinking this, but I figure: with `UserSettings` I know I want particular values for debugging later when I start passing set-and-forget values
#   - But when it cames to the serial port handling, because I wanted to
# DONE:
#   - REMOVED - repetitive package info variables (Thanks to @bpeterso2000)
#   - FIXED - Tried to be more explicit in naming


import sys
from pathlib import Path
from dataclasses import dataclass


class OS_Error(Exception):
    pass


class Serial_Error(Exception):
    pass


@dataclass
class UserSettings:
    path: Path = Path(__file__).resolve().parent
    timezone: str = "US/Eastern"
    timer: int = 10
    verbose: bool = False
    SERIALBAUD: int = 115200


class os_api:
    """Operating System API (class contains no data)"""

    @property
    def serial_port(self):
        return self._serial_port

    def serial_port_next(self):
        self._serial_port = self._serial_ports.pop()
        return self._serial_port

    def add_serial_port(self, str):
        return self._serial_ports.append(str)

    def print_serial_ports(self):
        [print(_sp) for _sp in self._serial_ports]


class os_is_win(os_api):
    def __init__(self):
        """USB Port and Emoji CLI Setings that have to be customized for Windows"""
        self._serial_port = "COM17"
        self._serial_ports = ["COM18", "COM19", "COM20", "COM21"]
        self.emojis = {"boo": "Boo!", "robot": "", "stars": "Yay"}


class os_is_mac(os_api):
    def __init__(self):
        """USB Port and Emoji CLI Setings that have to be customized for Mac"""
        self._serial_port = "/dev/cu.SLAB_USBtoUART"
        self._serial_ports = ["/dev/cu.usbmodem5821674", "/dev/cu.usbmodem5821675"]
        self.emojis = {"boo": "👻", "robot": "🤖", "stars": "✨ ✨ ✨"}
        # other inits ....


if sys.platform.startswith("win"):
    os_config = os_is_win()
elif sys.platform.startswith("darwin"):
    os_config = os_is_mac()
elif sys.platform.startswith("linux"):
    os_config = os_is_linux()
else:
    raise OS_Error("Unknown System")

if __name__ == "__main__":
    from loguru import logger

    logger.debug(f"Windows? {isinstance(os_config, os_is_win)}")
    logger.debug(f"Serial Port: {os_config.serial_port}")
    os_config.serial_port_next()
    logger.debug(f"Serial Port: {os_config.serial_port}")

    print(os_config.emojis["stars"], os_config.emojis["boo"])
