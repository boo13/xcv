#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from dataclasses import dataclass
import itertools
from xcontroller import xcontroller

# Local
import cli
from settings import Settings

# ASCII lookup table
on = 49  # '1'
off = 48  # '0'


def start_btn_press_sequence():
    cli.countdown(Settings.timerFlag)
    count = itertools.count(48)

    while True:
        next(count)

        if Settings.verbose:
            print(f"Sending command set: {count}")

        btns = xcontroller.Buttons()
        btns.aBtn = on
        xcontroller.serial_send(btns)
        sleep(0.2)


def single_btn_press(btnInput):
    cli.countdown(Settings.timerFlag)
    btns = xcontroller.Buttons()

    if btnInput == "A":
        btns.aBtn = on
    elif btnInput == "B":
        btns.bBtn = on
    elif btnInput == "X":
        btns.xBtn = on
    elif btnInput == "Y":
        btns.yBtn = on
    elif btnInput == "S":
        btns.startBtn = on
    elif btnInput == "l":
        btns.lbBtn = on
    elif btnInput == "r":
        btns.rbBtn = on
    elif btnInput == "w":
        btns.duBtn = on
    elif btnInput == "a":
        btns.dlBtn = on
    elif btnInput == "s":
        btns.ddBtn = on
    elif btnInput == "d":
        btns.drBtn = on
    else:
        print(
            "\n\t🛑 Error - Couldn't find that button.\n\t\t ⚠️ To list the buttons accepted use --help \n"
        )
        return

    xcontroller.serial_send(btns)
    sleep(0.2)


import sys

sys.exit(cli.main_input())  # pragma: no cover
