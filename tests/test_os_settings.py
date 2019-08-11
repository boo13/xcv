def test_emojis():
    from xcv import emojis
    import sys

    if sys.platform.startswith("win"):
        assert emojis.STARS == "Yay!"
        assert emojis.ROBOT == ""
        assert emojis.BOO == "Boo!"
        assert emojis.HAZARD == "\n\t!"
        assert emojis.JOYSTICK == ""
        assert emojis.XBOX_CONTROLLER == ""
        assert emojis.PYTHON == ""
        assert emojis.WORK == ""
        assert emojis.MAGIC == ""
        assert emojis.OPENCV == ""

    else:
        assert emojis.STARS == "✨ ✨ ✨"
        assert emojis.ROBOT == "🤖"
        assert emojis.BOO == "👻"
        assert emojis.HAZARD == "\n\t⚠️"
        assert emojis.JOYSTICK == "🕹"
        assert emojis.XBOX_CONTROLLER == "🎮"
        assert emojis.PYTHON == "🐍"
        assert emojis.WORK == ""
        assert emojis.MAGIC == "✨"
        assert emojis.OPENCV == "👾"

