STARS = "✨ ✨ ✨"
ROBOT: "🤖"
BOO = "👻"
HAZARD: "\n\t⚠️"
GENERIC_CONTROLLER = "🕹"
XBOX_CONTROLLER = "🎮"
PYTHON = "🐍"
WORK = ""
MAGIC = "✨"
OPENCV = "👾"

import sys

if sys.platform.startswith("win"):
    STARS = "Yay!"
    ROBOT = ""
    BOO = "Boo!"
    HAZARD = "\n\t!"
    GENERIC_CONTROLLER = ""
    XBOX_CONTROLLER = ""
    PYTHON = ""
    WORK = ""
    MAGIC = ""
    OPENCV = ""
