# settings.py

import sys
from pathlib import Path
from dataclasses import dataclass

# class SerialError(Exception):
#     pass


class xcv_api:
    os_is_windows = False
    if not os_is_windows:
        emojis = {"boo": "👻", "robot": "🤖", "stars": "✨ ✨ ✨"}
    path: Path = Path(__file__).resolve().parent
    timezone = "US/Eastern"
    timer = 10
    verbose = False
    # ...
    debug_serial = False
    # Game stuff
    btn_utf_send_commands = ["A", "B", "X", "Y", "S", "l", "r", "w", "a", "s", "d", "o", "p"]
    

# > PEP8: The naming convention for functions may be used instead in cases where the interface is documented and used primarily as a callable.
# QUESTION: Does that apply here?
class serial_api(xcv_api):
    """Serial API for handling a list of possible ports (class contains no data)"""

    BAUD = 115200

    @property
    def port(self):
        return self._port

    def port_next(self):
        try:
            self._port = self._ports.pop()
        except IndexError:
            pass
        return self._port

    def port_add(self, ser):
        self._ports.append(ser)

    def port_set(self, ser):
        self._port = ser

    def print_ports(self):
        [print(_sp) for _sp in self._ports]


class os_is_win(serial_api):
    def __init__(self):
        """USB serial port settings for Windows"""
        self._port = "COM17"
        self._ports = ["COM18", "COM19", "COM20", "COM21"]


class os_is_mac(serial_api):
    def __init__(self):
        """USB serial port settings for Mac"""
        self._port = "/dev/cu.SLAB_USBtoUART"
        self._ports = ["/dev/cu.usbmodem5821674", "/dev/cu.usbmodem5821675"]


class os_is_other(serial_api):
    def __init__(self):
        """Empty USB serial port settings for Linux, FreeBSD, etc."""
        self._port = input("Unknown OS - enter a USB Port: ")
        self._ports = []


if sys.platform.startswith("win"):
    serial_config = os_is_win()
    xcv_api.os_is_windows = True
    emojis = {"boo": "Boo!", "robot": "", "stars": "Yay"}
elif sys.platform.startswith("darwin"):
    serial_config = os_is_mac()
else:
    serial_config = os_is_other()


if __name__ == "__main__":
    from loguru import logger

    logger.debug(f"Windows? {isinstance(os_config, os_is_win)}")

    logger.debug(f"Serial Port: {os_config._port}")

    os_config.port_next()

    logger.debug(f"Serial Port: {os_config._port}")

    print(os_config.emojis["stars"], os_config.emojis["boo"])
