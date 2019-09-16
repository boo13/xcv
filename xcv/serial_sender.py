# PICKLE - we use it to properly encode the btns_command string
# before sending it to teensy/arduino over serial connection.
import pickle

# PYSERIAL - connects via serial (ie. hardwared USB) to teensy/arduino/whatever-you-want
import serial


# COLORAMA - for pretty colors in the command line
from colorama import Fore, Style

from loguru import logger

from xcv.emojis import HAZARD

import sys

class XcvError(Exception):
    pass


class serial_api:
    """Serial API for handling a list of possible ports (class contains no data)


        :attribute port: return current serial port
        :attribute BAUD: defaults to 115200
        :attribute btn: single value change
        :attribute buttons: multiple value changes
    """

    BAUD = 115200

    def __init__(self):


        if sys.platform.startswith("win"):
            self._port = "COM17"
            self._ports = ["COM18", "COM19", "COM20", "COM21"]
        elif sys.platform.startswith("darwin"):
            self._port = "/dev/cu.SLAB_USBtoUART"
            self._ports = ["/dev/cu.usbmodem5821674", "/dev/cu.usbmodem5821675"]
        else:
            self._port = input("Enter Serial Port: ")

    @property
    def port(self):
        return self._port

    def port_next(self):
        try:
            self._port = self._ports.pop()
        except IndexError:
            logger.warning(("No other known serial ports, returning the last port"))
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

    def serial_send(self, btns_sending):
        """ 🎯 Send the commands as a dict converted into a list, converted into a string.

            ⚠️ CAREFUL - string order matters!
            ...The command string is sent to the arduino script, which parses it out, but it's hardcoded.

            FYI: The arduino script uses the [brackets] on the string as the start/end markers

            - Probably won't ever really bother with fixing-up the arduino script too much, unless others feel compelled."""

        # In case things go bad
        serial_error = (
            Fore.RED
            + f"\n\n{HAZARD}"
            + Fore.WHITE
            + " - No Serial Communication\n"
            + Fore.YELLOW
            + f"\t(suggest) TRY - checking the wiring and the port, is this the correct port?\n\t\t\t"
            + Fore.CYAN
            + f"{str(self._port)}"
            + Style.RESET_ALL
        )

        try:
            # Be safe kids - use a Context Manager
            with serial.Serial(self._port, self.BAUD) as ser:
                pickle.dump(btns_sending.make_string(), ser)
        except serial.serialutil.SerialException as e:
            raise XcvError(serial_error)
        except Exception as e:
            raise XcvError(f"\n\n{HAZARD} I have no idea - CHECK the logs\n\n{str(e)}")

    #

serial_session = serial_api()
