# PICKLE - we use it to properly encode the btns_command string
# before sending it to teensy/arduino over serial connection.
import pickle

# PYSERIAL - connects via serial (ie. hardwared USB) to teensy/arduino/whatever-you-want
import serial

# DATACLASSES - req. python 3.7^
from dataclasses import dataclass
from typing import List

# LOCAL SETTINGS - we use these to set (and mostly forget) the Serial connection config
@dataclass
class Settings:
    timerFlag: int = 10
    verbose: bool = False
    serialPort: str = "/dev/cu.usbmodem58290301"
    serialBaud: int = 9600


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
    ltBtn: float = 1
    rtBtn: float = 1
    lsx: float = 1
    lsy: float = 1
    rsx: float = 1
    rsy: float = 1
    startBtn: bool = 0
    selectBtn: bool = 0
    xboxBtn: bool = 0

    def show(self):
        for k, v in self.__dict__.items():
            print(k, v)

    def make_string(self):
        return str(list(self.__dict__.values()))


def serial_send(btns_sending):
    """ ⚠️ Order matters! ⚠️ 
    The command string is an order that is parsed out in a hardcoded way in the arduino script. """

    # Be safe kids - use a Context Manager
    with serial.Serial(Settings.serialPort, Settings.serialBaud) as ser:
        pickle.dump(btns_sending.make_string(), ser)


# In case we're just testing the controller...
if __name__ == "__main__":
    testButtons = Buttons()
    testButtons.xBtn = 1
    serial_send(testButtons)
