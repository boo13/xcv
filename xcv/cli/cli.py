from time import sleep
from dataclasses import dataclass
import click
import xcv.constants
from xcv.util import WINDOWS


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
def main_input(
    verbose=False, port=None, autopilot=False, push=None, count=None, dryrun=None
):
    """🕹 XCV uses 👾OpenCV for 🐍Python to 👷‍operate a ✨magic 🤖robot 🎮controller
    \n\n
    The project's goal is to make OpenCV experiments easier, by avoiding controller-driver 
    nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. 
    On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals
    to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.

    \n
    \n\t\t____________________ Xbox Commands ____________________                               
    \n\t\t                 ⒮ tart   ⒳ box    s⒠ lect               
    \n\t\t                    Ⓐ =A Ⓑ =B Ⓧ =X Ⓨ =Y                               
    \n\t\t      𝗗⬆ =w   
    \n\t\t𝗗⬅ =a      𝗗➡ =d   Ⓛ Stick          Ⓡ Stick
    \n\t\t      𝗗⬇ =s 
    \n\t\t_____________________________________________________  """

    if verbose:
        # click.echo(f"Successfully connected to port: {port}"))
        click.echo(
            f"{stars}{gamerobot}XCV go...{gamesnake}Try to do things...\n"
        )

    # local imports
    from xcontroller import xcontroller

    if dryrun:
        click.echo(
            f"{exiting}{debug_indent}{hazard}Sorry! - This is actually a WIP Feature. {suggest}Try usinsg --help to find something that actually works, or make it work by contributing on github! \n"
        )

    elif push:
        xcontroller.single_btn_press(push)

    elif autopilot:
        print("WIP feature")
        xcontroller.start_btn_press_sequence()
    
    else:
        click.echo(
            f"{exiting}{debug_indent}You need to choose an option. ⚠️ Try using --help \n"
        )

    
    return 0    # indicates function finished without error


def countdown(secs):

    if secs is 0:   # In case we pass in a 0 from CLI
        print(rocketLaunchList[3])
    else:
        print(launch)

        for i in range(secs + 1):
            sleep(1)

            if i == (secs - 3):
                print(rocketLaunchList[0])

            elif i == (secs - 2):
                print(rocketLaunchList[1])

            elif i == (secs - 1):
                print(rocketLaunchList[2])

            elif i == (secs):
                print(rocketLaunchList[3])

            else:
                print(f"\t    🔥 ... {secs - i}")




if __name__ == "__main__":
    print(f"{debug_indent}{exiting}{debug_indent}{hazard}Not an entry point! {suggest}Use main xcv module")
