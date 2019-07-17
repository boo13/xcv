# -*- coding: utf-8 -*-

from time import sleep
from dataclasses import dataclass
import itertools
from xcontroller import xcontroller

# Local
import cli
from settings import Settings

# def start_btn_press_sequence():
#     cli.countdown(Settings.timerFlag)
#     count = itertools.count(48)

#     while True:
#         next(count)

#         if Settings.verbose:
#             print(f"Sending command set: {count}")

#         btns = xcontroller.Buttons()
#         btns.aBtn = on
#         xcontroller.serial_send(btns)
#         sleep(0.2)


def single_btn_press(btnInput):
    cli.countdown(Settings.timerFlag)
    btns = xcontroller.Buttons()

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
            "\n\t🛑 Error - Couldn't find that button.\n\t\t ⚠️ To list the buttons accepted use --help \n"
        )
        return

    xcontroller.serial_send(btns)
    sleep(0.2)


import sys

sys.exit(cli.main_input())  # pragma: no cover
