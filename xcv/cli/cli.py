from time import sleep
from dataclasses import dataclass
import click
import xcv.constants
from xcv.constants import WINDOWS


# Emoji handling
debug_indent = "\n\t\t"
centered_indent = "\n\t\t\t\t"

if WINDOWS:
    stars = f"{centered_indent}✨ ✨ ✨\n\n"
    hazard = f"{debug_indent}⚠️  "
    sleep = f"{debug_indent}😴 "
    suggest = f"{debug_indent}✏️  "
    gamerobot = ""
    gamesnake = ""
    launch = f"{debug_indent}LAUNCHING"
    warning = f"{debug_indent}🥵 WARNING"
    exiting = f"{debug_indent}👟 ️ EXITING"
    rocketLaunchList = [
        f"{debug_indent}... ",
        f"{debug_indent} .. ",
        f"{debug_indent}  . ",
        f"{debug_indent}XCV!\n",
        f"{debug_indent}XCV!\n",
    ]
else:
    stars = f"{centered_indent}✨ 🌟 ✨\n\n"
    hazard = f"{debug_indent}⚠️  "
    sleep = f"{debug_indent}😴 "
    suggest = f"{debug_indent}✏️  "
    gamerobot = f"{debug_indent}👾 🕹  "
    gamesnake = f"{debug_indent}🎮 🐍  "
    launch = f"{debug_indent}🧨  LAUNCHING"
    warning = f"{debug_indent}🥵 WARNING"
    exiting = f"{debug_indent}👟 ️ EXITING"
    rocketLaunchList = [
        f"{debug_indent}🔥 ... ",
        f"{debug_indent} 🔥 .. ",
        f"{debug_indent}  🔥 . ",
        f"{debug_indent}    💨  XCV 🚀\n",
        "🚀",
    ]

# Main CLI 
_btnList = ["A", "B", "X", "Y", "S", "l", "r", "w", "a", "s", "d", "o", "p"]
_defaultUSBport = "/dev/cu.SLAB_USBtoUART"

_docstring = f""

@click.command()
@click.option(
    "--verbose", 
    "-v", 
    is_flag=True, 
    help="Display debug information")
@click.option(
    "--port",
    default=_defaultUSBport,
    help=f"Controller port, default is {_defaultUSBport}",
)
@click.option(
    "--autopilot", 
    "-auto", 
    is_flag=True, 
    help="Initiate xcv sequence")
@click.option(
    "--push", 
    type=click.Choice(_btnList), 
    help="Enter button to push")
@click.option(
    "--count", 
    type=int, 
    default=3, 
    help="Time in seconds before commands")
@click.option(
    "--dryrun",
    "-dry",
    is_flag=True,
    help="For testing without xbox controller connected",
)
@click.option(
    "--debug",
    is_flag=True,
    help="List USB ports and check the serial connection",
)
def main_input(
    verbose=False, port=None, autopilot=False, push=None, count=None, dryrun=None, debug=None
):
    """The project's goal is to make OpenCV experiments easier, by avoiding controller-driver 
    nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. 
    On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals
    to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.

    \n
    \n\t____________________ Xbox Commands ____________________                               
    \n\t                 ⒮ tart   ⒳ box    s⒠ lect               
    \n\t                    Ⓐ =A Ⓑ =B Ⓧ =X Ⓨ =Y                               
    \n\t      𝗗⬆ =w   
    \n\t𝗗⬅ =a      𝗗➡ =d   Ⓛ Stick          Ⓡ Stick
    \n\t      𝗗⬇ =s 
    \n\t_____________________________________________________  """

    if not WINDOWS:
        print("🕹 XCV uses 👾OpenCV for 🐍Python to 👷‍operate a ✨magic 🤖robot 🎮controller")

    if verbose:
        # click.echo(f"Successfully connected to port: {port}"))
        click.echo(
            f"{stars}{gamerobot}XCV go...{gamesnake}Try to do things...\n"
        )


    if dryrun:
        click.echo(
            f"{exiting}{debug_indent}{hazard}Sorry! - This is actually a WIP Feature. {suggest}Try usinsg --help to find something that actually works, or make it work by contributing on github! \n"
        )

    elif debug:
        from xcv.tools import list_ports
        list_ports.list_ports()
        # checkSerial.checkSerial()

    elif push:
        from xcontroller import xcontroller
        xcontroller.single_btn_press(push)

    elif autopilot:
        print("WIP feature")
    
    else:
        click.echo(
            f"{debug_indent}{hazard}No options passed - Opening GUI\n"
        )
        from xcv.gui import mainGUI
        mainGUI()

    
    return 0    # indicates function finished without error


def countdown(secs):

    if secs is 0:   # In case we pass in a 0 from CLI
        print(rocketLaunchList[3])
    else:
        print(launch)

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
