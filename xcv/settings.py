# settings.py

import sys
from pathlib import Path
from dataclasses import dataclass


@dataclass
class UserSettings:
    path: Path = Path(__file__).resolve().parent
    timezone: str = "US/Eastern"
    countdown_timer: int = 10
    # ...
    # CLI stuff
    verbose: bool = False
    debug_serial: bool = False
    # ...
    # Game stuff
    btn_utf_send_commands = [
        "A",
        "B",
        "X",
        "Y",
        "S",
        "l",
        "r",
        "w",
        "a",
        "s",
        "d",
        "o",
        "p",
    ]


#
class serial_api:
    """Serial API for handling a list of possible ports (class contains no data)


        :attribute port: return current serial port
        :attribute BAUD: defaults to 115200
        :attribute btn: single value change
        :attribute buttons: multiple value changes
    """

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

    def send(self, **kwargs):
        """Convert button/stick command value to expected list, `buttons`.
            Send the output to be verified by `_check_pending_send`
        """
        print(kwargs)

    def _check_pending_send(self, buttons):
        pass

    def _send_pending_send(self, checkedbuttons):
        pass


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
elif sys.platform.startswith("darwin"):
    serial_config = os_is_mac()
else:
    serial_config = os_is_other()

if __name__ == "__main__":
    from loguru import logger

    logger.debug(serial_config._port)

    ser = serial_api()

    ser.send(key1="xyz")

    # logger.debug(f"Windows? {isinstance(serial_config, os_is_win)}")

    # logger.debug(f"Serial Port: {serial_config._port}")

    # serial_config.port_next()

    # logger.debug(f"Serial Port: {serial_config._port}")

    # print(xcv_api.emojis["stars"], emojis["boo"])
