STARS = "✨ ✨ ✨"
ROBOT = "🤖"
BOO = "👻"
HAZARD = "\n\t⚠️"
JOYSTICK = "🕹"
XBOX_CONTROLLER = "🎮"
PYTHON = "🐍"
WORK = ""
MAGIC = "✨"
OPENCV = "👾"
SUGGEST = "💡 "

import sys

if sys.platform.startswith("win"):
    STARS = "Yay!"
    ROBOT = ""
    BOO = "Boo!"
    HAZARD = "\n\t!"
    JOYSTICK = ""
    XBOX_CONTROLLER = ""
    PYTHON = ""
    WORK = ""
    MAGIC = ""
    OPENCV = ""
    SUGGEST = ""
