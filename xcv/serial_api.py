# PICKLE - we use it to properly encode the btns_command string
# before sending it to teensy/arduino over serial connection.
import pickle

# PYSERIAL - connects via serial (ie. hardwared USB) to teensy/arduino/whatever
import serial

# COLORAMA - for pretty colors in the command line
from colorama import Fore, Style

from loguru import logger

from xcv.emojis import HAZARD

import sys


class SerialApiError(Exception):
    pass

serial_session = serial_api()

@logger.catch
class serial_port:
    """Iterator"""

    def __init__(self):
        WIN_WHITE_LIST = ["COM17", "COM18", "COM19", "COM20", "COM21"]
        MAC_WHITE_LIST = ["/dev/cu.SLAB_USBtoUART", "/dev/cu.usbmodem5821674", "/dev/cu.usbmodem5821675"]
        BLACK_LIST = ["/dev/cu.Bluetooth", "/dev/cu.rara"]
        HWID_WHITE_LIST = []
        HWID_BLACK_LIST = []

        if sys.platform.startswith("win"):
            self._ports = WIN_WHITE_LIST
        elif sys.platform.startswith("darwin"):
            self._ports = MAC_WHITE_LIST
        else:
            self._ports = [input("Enter Serial Port: ")]

        self._port = self._ports[0]

    def __iter__(self):
        i = 0
        self.port = self._ports[i]
        return self

    def __next__(self):
        x = self.port
        i += 1
        return x

    def port_add(self, ser):
        self._ports.append(ser)

    def port_set(self, ser):
        self._port = ser

    def print_ports(self):
        [print(_sp) for _sp in self._ports]

    def list_available_ports(self):
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if desc != "n/a":
                logger.debug(f"\n\t{port}\n\t  DESC: {desc}\n\t  HWID: {hwid}")
            else:
                for b in BLACK_LIST if not port.startswith(b):
                    logger.debug("\t", port)


@logger.catch
class SerialApi:
    """Serial API for handling a list of possible ports (class contains no data)

        Attributes:
            port: return current serial port
            BAUD: defaults to 115200
            btn: single value change
            buttons: multiple value changes
    """

    self.BAUD = 115200

    @property
    def port(self):
        return self._port

    def port_next(self):
        p = serial_port()
        p.next()
        # try:
        #     self._port = self._ports.pop()
        # except IndexError:
        #     logger.warning(("No other known serial ports, returning the last port"))
        # return self._port


    def send(self, **kwargs):
        """Convert button/stick command value to expected list, `buttons`.
            Send the output to be verified by `_check_pending_send`
        """
        print(kwargs)

    def _check_pending_send(self, buttons):
        """ String order matters!
            ⚠️ CAREFUL ...The command string is sent to the arduino script, 
            which parses it out, but it's hardcoded.

            Also, the arduino script uses the [brackets] on the string as the
            start/end markers
        """
        pass

    def _send_pending_send(self, checkedbuttons):
        """
        """
        pass

    def serial_send(self, btns_sending):
        """Send the commands as a dict converted into a list, converted into a string.
            """

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
            raise SerialApiError(serial_error)
        except Exception as e:
            raise SerialApiError(f"\n\n{HAZARD} I have no idea - CHECK the logs\n\n{str(e)}")