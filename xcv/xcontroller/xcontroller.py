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

from xcv.settings import Settings, SERIAL_PORT
from xcv.commands import XcvError

from xcv.cli.cli import hazard, sleep, warning, exiting, suggest


@dataclass(order=True)
class Buttons:
    aBtn: bool = 0
    bBtn: bool = 0
    xBtn: bool = 0
    yBtn: bool = 0
    lbBtn: bool = 0
    rbBtn: bool = 0
    duBtn: bool = 0
    ddBtn: bool = 0
    dlBtn: bool = 0
    drBtn: bool = 0
    ltBtn: float = 0.0
    rtBtn: float = 0.0
    lsx: float = 0.0
    lsy: float = 0.0
    rsx: float = 0.0
    rsy: float = 0.0
    startBtn: bool = 0
    selectBtn: bool = 0
    xboxBtn: bool = 0

    def show(self):
        for k, v in self.__dict__.items():
            print(k, v)

    def make_string(self):
        return str(list(self.__dict__.values()))


def single_btn_press(btnInput: object, cnt_down: int = 2):
    from cli import cli

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
            f"\n\t{warning} Error - Couldn't find that button.\n\t\t {suggest}To list the buttons accepted use --help \n"
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
        + f"\n\n{warning}"
        + Fore.WHITE
        + " - No Serial Communication\n"
        + Fore.YELLOW
        + f"\t{hazard}CHECK"
        + Fore.WHITE
        + " - your serial port in 'constants.py'\n"
        + Fore.WHITE
        + f"\t{suggest}TRY - checking the wiring and the port, is this the correct port?\n\t\t\t"
        + Fore.CYAN
        + f"{str(SERIAL_PORT)}"
        + Style.RESET_ALL
    )

    try:
        # Be safe kids - use a Context Manager
        with serial.Serial(SERIAL_PORT, Settings.SERIAL_BAUD) as ser:
            pickle.dump(btns_sending.make_string(), ser)
    except serial.serialutil.SerialException as e:
        raise XcvError(serial_error)
    except Exception as e:
        raise XcvError(
            f"\n\n{exiting} I have no idea - {hazard} CHECK the logs\n\n{str(e)}"
        )


# In case we're just testing the controller...
if __name__ == "__main__":
    testButtons = Buttons()
    testButtons.xBtn = 1
    serial_send(testButtons)
