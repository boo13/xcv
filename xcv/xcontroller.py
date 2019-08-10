# PICKLE - we use it to properly encode the btns_command string
# before sending it to teensy/arduino over serial connection.
import pickle

# PYSERIAL - connects via serial (ie. hardwared USB) to teensy/arduino/whatever-you-want
import serial

# COLORAMA - for pretty colors in the command line
from colorama import Fore, Style

# DATACLASSES - req. python 3.7^
from dataclasses import dataclass
from typing import List

from settings import serial_api
from commands import XcvError

import cli


@dataclass(order=True)
class Buttons:
    aBtn: int = 0
    bBtn: int = 0
    xBtn: int = 0
    yBtn: int = 0
    lbBtn: int = 0
    rbBtn: int = 0
    duBtn: int = 0
    ddBtn: int = 0
    dlBtn: int = 0
    drBtn: int = 0
    ltBtn: float = 0.0
    rtBtn: float = 0.0
    lsx: float = 0.0
    lsy: float = 0.0
    rsx: float = 0.0
    rsy: float = 0.0
    startBtn: int = 0
    selectBtn: int = 0
    xboxBtn: int = 0

    def show(self):
        for k, v in self.__dict__.items():
            print(k, v)

    def make_string(self):
        return str(list(self.__dict__.values()))


def single_btn_press(btnInput: object, cnt_down: int = 2):
    cli.countdown(cnt_down)
    btns = Buttons()

    if btnInput == "A":
        btns.aBtn = 1
    elif btnInput == "B":
        btns.bBtn = 1
    elif btnInput == "X":
        btns.xBtn = 1
    elif btnInput == "Y":
        btns.yBtn = 1
    elif btnInput == "S":
        btns.startBtn = 1
    elif btnInput == "l":
        btns.lbBtn = 1
    elif btnInput == "r":
        btns.rbBtn = 1
    elif btnInput == "w":
        btns.duBtn = 1
    elif btnInput == "a":
        btns.dlBtn = 1
    elif btnInput == "s":
        btns.ddBtn = 1
    elif btnInput == "d":
        btns.drBtn = 1
    else:
        print(
            f"\n\t{cli.warning} Error - Couldn't find that button.\n\t\t {cli.suggest}To list the buttons accepted use --help \n"
        )
        return

    # 🎯 Send it!
    serial_send(btns)

    # Don't spam the button
    from time import sleep

    sleep(0.2)


def serial_send(btns_sending, serialPort=None, serialBaud=None):
    """ 🎯 Send the commands as a dict converted into a list, converted into a string. 
    
        ⚠️ CAREFUL - string order matters!
        ...The command string is sent to the arduino script, which parses it out, but it's hardcoded.
        
        FYI: The arduino script uses the [brackets] on the string as the start/end markers
        
        - Probably won't ever really bother with fixing-up the arduino script too much, unless others feel compelled."""

    # In case things go bad
    serial_error = (
        Fore.RED
        + f"\n\n{cli.warning}"
        + Fore.WHITE
        + " - No Serial Communication\n"
        + Fore.YELLOW
        + f"\t{cli.hazard}CHECK"
        + Fore.WHITE
        + " - your serial port in 'constants.py'\n"
        + Fore.WHITE
        + f"\t{cli.suggest}TRY - checking the wiring and the port, is this the correct port?\n\t\t\t"
        + Fore.CYAN
        + f"{str(serial_api.port)}"
        + Style.RESET_ALL
    )

    try:
        # Be safe kids - use a Context Manager
        with serial.Serial(serial_api.port, serial_api.BAUD) as ser:
            pickle.dump(btns_sending.make_string(), ser)
    except serial.serialutil.SerialException as e:
        raise XcvError(serial_error)
    except Exception as e:
        raise XcvError(
            f"\n\n{cli.exiting} I have no idea - {cli.hazard} CHECK the logs\n\n{str(e)}"
        )


# In case we're just testing the controller...
if __name__ == "__main__":
    testButtons = Buttons()
    testButtons.xBtn = 1
    serial_send(testButtons)
