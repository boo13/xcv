import os
from time import sleep
from dataclasses import dataclass
from textwrap import TextWrapper

wrapper = TextWrapper()

import click
from loguru import logger

import settings
from emojis import (
    HAZARD,
    STARS,
    ROBOT,
    BOO,
    HAZARD,
    JOYSTICK,
    XBOX_CONTROLLER,
    PYTHON,
    WORK,
    MAGIC,
    OPENCV,
)



# Main CLI
_btnList = ["A", "B", "X", "Y", "S", "l", "r", "w", "a", "s", "d", "o", "p"]


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Display debug information")
@click.option(
    "--port",
    default=settings.serial_api.port,
    help=f"Controller port, default is {settings.serial_api.port}",
)
@click.option("--autopilot", "-auto", is_flag=True, help="Initiate xcv sequence")
@click.option("--push", type=click.Choice(_btnList), help="Enter button to push")
@click.option("--gui", is_flag=True, help="Show the GUI")
@click.option(
    "--debug", is_flag=True, help="List USB ports and check the serial connection"
)
def main_input(
    verbose=False,
    port=None,
    autopilot=False,
    push=None,
    count=None,
    debug=None,
    gui=None,
):
    """XCV uses OpenCV to push controller buttons with PySerial.

    The project's goal is to make OpenCV experiments easier, by avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.

    \n
    \n\t _______________________ Xbox Commands _______________________                               
    \n\t ⒮ tart   ⒳ box    s⒠ lect Ⓐ = A  Ⓑ = B  Ⓧ = X  Ⓨ =Y                               
    \n\t      DU = w   
    \n\tDL = a      DR = d     Ⓛ Stick      Ⓡ Stick
    \n\t      DD = s 
    """

    if verbose:
        print(
            f"\n{JOYSTICK} XCV uses {OPENCV}OpenCV for {PYTHON}Python to {WORK}operate a {MAGIC}magic {ROBOT}robot {XBOX_CONTROLLER}controller"
        )
        click.echo(f"Successfully connected to port: {port}")
        click.echo(f"{ROBOT}XCV go...{BOO}Try to do things...\n")

    elif debug:
        from tools import list_usb_ports

        list_usb_ports.list_usb_ports()

    elif push:
        import xcontroller

        xcontroller.single_btn_press(push)

    elif autopilot:
        print("WIP feature")

    elif gui:
        from gui import VideoCapture
        VideoCapture()

    else:
        click.echo(f"{HAZARD}No options passed. Try --help or --gui\n")

    return 0  # indicates finished without error


if __name__ == "__main__":
    main_input()
