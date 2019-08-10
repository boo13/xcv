import sys

STARS = "✨ ✨ ✨"
ROBOT: "🤖"
BOO = "👻"
HAZARD: "⚠️"


if sys.platform.startswith("win"):
    STARS = "Yay!"
    ROBOT = ""
    BOO = "Boo!"
    HAZARD = "!"
