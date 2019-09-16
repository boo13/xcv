import os
from time import sleep
import click
from loguru import logger

import xcv.settings
from xcv.emojis import (
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
    default=xcv.settings.serial_api.port,
    help=f"Controller port, default is 0",
)
@click.option(
    "--push",
    type=click.Choice(_btnList),
    help="Enter character code for button to push",
)
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

    The project's goal is to make OpenCV experiments easier.
    This app avoids all controller-driver nonsense and just
    hacks into the gaming controller, and connects the buttons
    to an arduino/teensy/whatever. 
    
    On the arduino/teensy side of things, we then just parse out
    the commands and send some high/low signals to I/O pins.
    
    Joystick/trigger values (potentiometers on the controller) are
    not implemented yet. Intending to use 10k digi-pots to handle.

    \n
    \n\t ____________ Xbox Commands ____________                               
    \n\t        ⒮ tart   ⒳ box    s⒠ lect 
    \n
    \n\t        Ⓐ = A  Ⓑ = B  Ⓧ = X  Ⓨ =Y                               
    \n
    \n\t                 DU = w   
    \n\t           DL = a      DR = d     
    \n\t                 DD = s 
    \n
    \n\t          Ⓛ Stick      Ⓡ Stick
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
        import xcv.xcontroller

        xcv.xcontroller.single_btn_press(push)

    elif gui:
        from xcv.gui import GUI

        GUI()

    else:
        click.echo(f"{HAZARD}No options passed. Try --help or --gui\n")

    return 0  # indicates finished without error


if __name__ == "__main__":
    main_input()
