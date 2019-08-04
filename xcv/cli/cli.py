from time import sleep
from dataclasses import dataclass
import click
import xcv.constants

from loguru import logger

from xcv.settings import Settings

# Emoji handling
if Settings.WINDOWS:
    stars = f"{Settings.centered_indent}✨ ✨ ✨\n\n"
    hazard = f"{Settings.debug_indent}⚠️  "
    sleep = f"{Settings.debug_indent}😴 "
    suggest = f"{Settings.debug_indent}✏️  "
    gamerobot = ""
    gamesnake = ""
    launch = f"{Settings.debug_indent}LAUNCHING"
    warning = f"{Settings.debug_indent} WARNING"
    exiting = f"{Settings.debug_indent}👟 ️ EXITING"
    rocketLaunchList = [
        f"{Settings.debug_indent}... ",
        f"{Settings.debug_indent} .. ",
        f"{Settings.debug_indent}  . ",
        f"{Settings.debug_indent}XCV!\n",
        f"{Settings.debug_indent}XCV!\n",
    ]
else:
    stars = f"{Settings.centered_indent}✨ 🌟 ✨\n\n"
    hazard = f"{Settings.debug_indent}⚠️  "
    sleep = f"{Settings.debug_indent}😴 "
    suggest = f"{Settings.debug_indent}✏️  "
    gamerobot = f"{Settings.debug_indent}👾 🕹  "
    gamesnake = f"{Settings.debug_indent}🎮 🐍  "
    launch = f"{Settings.debug_indent}🧨  LAUNCHING"
    warning = f"{Settings.debug_indent}🥵  WARNING"
    exiting = f"{Settings.debug_indent}👟 ️ EXITING"
    rocketLaunchList = [
        f"{Settings.debug_indent}🔥 ... ",
        f"{Settings.debug_indent} 🔥 .. ",
        f"{Settings.debug_indent}  🔥 . ",
        f"{Settings.debug_indent}    💨  XCV 🚀\n",
        "🚀",
    ]

# Main CLI
_btnList = ["A", "B", "X", "Y", "S", "l", "r", "w", "a", "s", "d", "o", "p"]
_defaultUSBport = "/dev/cu.SLAB_USBtoUART"


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Display debug information")
@click.option(
    "--port",
    default=_defaultUSBport,
    help=f"Controller port, default is {_defaultUSBport}",
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

    The project's goal is to make OpenCV experiments easier, by avoiding controller-driver 
    nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. 
    On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals
    to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.

    \n
    \n\t____________________ Xbox Commands ____________________                               
    \n\t                 ⒮ tart   ⒳ box    s⒠ lect               
    \n\t                 Ⓐ = A  Ⓑ = B  Ⓧ = X  Ⓨ =Y                               
    \n\t      DU = w   
    \n\tDL = a      DR = d   Ⓛ Stick          Ⓡ Stick
    \n\t      DD = s 
    \n\t_____________________________________________________  """

    if not Settings.WINDOWS:
        print("🕹 XCV uses 👾OpenCV for 🐍Python to 👷‍operate a ✨magic 🤖robot 🎮controller")

    if verbose:
        click.echo(f"Successfully connected to port: {port}")
        click.echo(f"{stars}{gamerobot}XCV go...{gamesnake}Try to do things...\n")

    elif debug:
        from xcv.tools import list_ports

        list_ports.list_ports()

    elif push:
        from xcontroller import xcontroller

        xcontroller.single_btn_press(push)

    elif autopilot:
        print("WIP feature")

    elif gui:
        from xcv.gui import mainGUI

        mainGUI()

    else:
        click.echo(
            f"{Settings.debug_indent}{hazard}No options passed. Try --help or --gui\n"
        )

    return 0  # indicates finished without error


def countdown(secs):

    if secs is 0:  # In case we pass in a 0 from CLI
        logger.info(rocketLaunchList[3])
    else:
        logger.info(launch)

    # for i in range(secs + 1):
    #     sleep(1)

    #     if i == (secs - 3):
    #         print(rocketLaunchList[0])

    #     elif i == (secs - 2):
    #         print(rocketLaunchList[1])

    #     elif i == (secs - 1):
    #         print(rocketLaunchList[2])

    #     elif i == (secs):
    #         print(rocketLaunchList[3])

    #     else:
    #         print(f"\t    🔥 ... {secs - i}")


if __name__ == "__main__":
    main_input()
