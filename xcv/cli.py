from time import sleep
from dataclasses import dataclass
from textwrap import TextWrapper

wrapper = TextWrapper()

import click
from loguru import logger

import settings
from emojis import STARS, ROBOT, BOO, HAZARD

# _settings = settings
# print(_settings.xcv_api.emojis["stars"])

# x = _settings.serial_config.port_next()

# print(x)
# print(_settings.serial_config.port)

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
@click.option("--count", type=int, default=3, help="Time in seconds before commands")
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
    """XCV ushes OpenCV to push controller buttons with PySerial.

    The project's goal is to make OpenCV experiments easier, by avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.

    \n
    \n\t ____________________ Xbox Commands ____________________                               
    \n\t                 ⒮ tart   ⒳ box    s⒠ lect               
    \n\t                 Ⓐ = A  Ⓑ = B  Ⓧ = X  Ⓨ =Y                               
    \n\t      DU = w   
    \n\tDL = a      DR = d   Ⓛ Stick          Ⓡ Stick
    \n\t      DD = s 
    \n\t _____________________________________________________  
    """

    # if not Settings.WINDOWS:
    #     print("🕹 XCV uses 👾OpenCV for 🐍Python to 👷‍operate a ✨magic 🤖robot 🎮controller")

    if verbose:
        click.echo(f"Successfully connected to port: {port}")
        click.echo(f"{ROBOT}XCV go...{BOO}Try to do things...\n")

    elif debug:
        from xcv.tools import list_ports

        list_ports.list_ports()

    elif push:
        import xcontroller

        xcontroller.single_btn_press(push)

    elif autopilot:
        print("WIP feature")

    elif gui:
        from gui import mainGUI

        mainGUI()

    else:
        click.echo(f"{HAZARD}No options passed. Try --help or --gui\n")

    return 0  # indicates finished without error


def countdown(secs):

    if secs is 0:  # In case we pass in a 0 from CLI
        logger.info(rocketLaunchList[3])
    else:
        logger.info(launch)


if __name__ == "__main__":
    main_input()
    print(HAZARD, STARS)
