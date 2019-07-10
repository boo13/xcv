from time import sleep
from dataclasses import dataclass
import click


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Display debug information")
@click.option(
    "--port",
    default="/dev/cu.usbmodem58290301",
    help="Controller port, default is /dev/cu.usbmodem58290301",
)
@click.option("--autopilot", "-auto", is_flag=True, help="Initiate xcv sequence")
@click.option(
    "--push",
    type=click.Choice(
        ["A", "B", "X", "Y", "S", "l", "r", "w", "a", "s", "d", "o", "p"]
    ),
    help="Enter button to push",
)
@click.option("--count", type=int, default=3, help="Time in seconds before commands")
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
    
    \n\n\tThe project's goal is to make OpenCV experiments easier, by avoiding controller-driver nonsense and just hacking intro controllers and connecting the buttons to an arduino/teensy/whatever. On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.

    \n\n\t\t( - - - - - - - | _ _Xbox Commands_ _ | - - - - - - - -)
      \n\t\t                     ⒳ box                       
      \n\t\t              ⒮ tart      s⒠ lect               

    \n\n\t\tⒶ =A Ⓑ =B Ⓧ =X Ⓨ =Y 
    
    \n\n\t\tⓁ Stick Ⓡ Stick
    
    \n\n\t\t𝗗⬆ =w  𝗗⬇ =s  𝗗⬅ =a  𝗗➡ =d
    
    \n\n\t\t( - - - - - - -  - - - - - - - - - - - - - - - - - - - -)"""

    if verbose:
        click.echo(f"Successfully connected to port: {port}")
        click.echo("\n\t\t👾 🕹 🎮 XCV is about to do things... ✨ 💫 🐍 \n\n \n")

    # local imports
    import __main__
    from settings import Settings

    # Set our CLI dataclass to match the input parameters
    Settings.verbose = verbose
    Settings.port = port
    Settings.timerFlag = count

    if dryrun:
        print("WIP feature")
    elif push:
        __main__.single_btn_press(push)
    elif autopilot:
        __main__.start_btn_press_sequence()
    else:
        click.echo(
            "\n\t\t 👟 ️Exiting... 🥵 \n\t\t You need to choose an option. ⚠️ Try using --help \n"
        )

    # return 0 indicates function finished without error
    return 0


def countdown(secs):

    if secs is 0:
        print("🚀")
    else:
        print("  🧨  Starting in...")

        for i in range(secs + 1):
            sleep(1)
            if i == (secs):
                print("........💨 XCV Go! 🚀\n")
            else:
                print(f"\t🔥...{secs - i}...")
