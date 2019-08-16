# PICKLE - we use it to properly encode the btns_command string
# before sending it to teensy/arduino over serial connection.
import pickle

# PYSERIAL - connects via serial (ie. hardwared USB) to teensy/arduino/whatever-you-want
import serial

# COLORAMA - for pretty colors in the command line
from colorama import Fore, Style

# Don't spam the button
from time import sleep

# DATACLASSES - req. python 3.7^
from dataclasses import dataclass
from typing import List

from settings import serial_session
from commands import XcvError

import cli
from emojis import HAZARD

# @dataclass(order=True)
# class Buttons:
#     aBtn: int = 0
#     bBtn: int = 0
#     xBtn: int = 0
#     yBtn: int = 0
    # lbBtn: int = 0
    # rbBtn: int = 0
    # duBtn: int = 0
    # ddBtn: int = 0
    # dlBtn: int = 0
    # drBtn: int = 0
    # ltBtn: float = 0.0
    # rtBtn: float = 0.0
    # lsx: float = 0.0
    # lsy: float = 0.0
    # rsx: float = 0.0
    # rsy: float = 0.0
    # startBtn: int = 0
    # selectBtn: int = 0
    # xboxBtn: int = 0

#     def show(self):
#         for k, v in self.__dict__.items():
#             print(k, v)
#
#     def make_string(self):
#         return str(list(self.__dict__.values()))
# #
#
# @dataclass(order=True)
# class Buttons:
#     aBtn: int = 0
#     bBtn: int = 0
#     xBtn: int = 0
#     yBtn: int = 0
#     lbBtn: int = 0
#     rbBtn: int = 0
#     duBtn: int = 0
#     ddBtn: int = 0
#     dlBtn: int = 0
#     drBtn: int = 0
#     ltBtn: float = 0.0
#     rtBtn: float = 0.0
#     lsx: float = 0.0
#     lsy: float = 0.0
#     rsx: float = 0.0
#     rsy: float = 0.0
#     startBtn: int = 0
#     selectBtn: int = 0
#     xboxBtn: int = 0
#
#     def show(self):
#         for k, v in self.__dict__.items():
#             print(k, v)
#
#     def make_string(self):
#         return str(list(self.__dict__.values()))


def single_btn_press(btnInput: object):
    btns = Buttons()

    if btnInput == "_btnA_":
        btns.aBtn = 1
    elif btnInput == "_btnB_":
        btns.bBtn = 1
    elif btnInput == "_btnX_":
        btns.xBtn = 1
    elif btnInput == "_btnY_":
        btns.yBtn = 1
    elif btnInput == "_btnStart_":
        btns.startBtn = 1
    elif btnInput == "_btnLB_":
        btns.lbBtn = 1
    elif btnInput == "_btnRB_":
        btns.rbBtn = 1
    elif btnInput == "_btnDU_":
        btns.duBtn = 1
    elif btnInput == "_btnDL_":
        btns.dlBtn = 1
    elif btnInput == "_btnDD_":
        btns.ddBtn = 1
    elif btnInput == "_btnDR_":
        btns.drBtn = 1
    else:
        print(
            f"\n\t{HAZARD} Error - Could not find that button.\n\t\t (suggest) To list the buttons accepted use --help \n"
        )
        return

    # 🎯 Send it!
    serial_send(btns, serial_session.port, serial_session.BAUD)

    sleep(0.2)


def serial_send(btns_sending, serialPort, serialBaud):
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
        + f"\t{HAZARD}CHECK"
        + Fore.WHITE
        + " - your serial port in 'constants.py'\n"
        + Fore.WHITE
        + f"\t(suggest) TRY - checking the wiring and the port, is this the correct port?\n\t\t\t"
        + Fore.CYAN
        + f"{str(serialPort)}"
        + Style.RESET_ALL
    )

    try:
        # Be safe kids - use a Context Manager
        with serial.Serial(serialPort, serialBaud) as ser:
            pickle.dump(btns_sending.make_string(), ser)
    except serial.serialutil.SerialException as e:
        raise XcvError(serial_error)
    except Exception as e:
        raise XcvError(f"\n\n{HAZARD} I have no idea - CHECK the logs\n\n{str(e)}")


# In case we're just testing the controller...
if __name__ == "__main__":
    testButtons = Buttons()
    testButtons.xBtn = 1
    serial_send(testButtons, serial_session.port, serial_session.BAUD)

