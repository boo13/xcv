from xcv.util import WINDOWS

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
