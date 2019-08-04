from dataclasses import dataclass


# Settings - we use these to set (and mostly forget) the config
@dataclass
class Settings:
    # __slots__ = ["TIMEZONE", "timer", "verbose", "PACKAGE_NAME", "SERIAL_BAUD", "WINDOWS", "SERIAL_PORT"]
    # ====================================
    #   User Settings
    # ====================================
    TIMEZONE: str = "US/Eastern"
    timer: int = 10
    verbose: bool = False

    # ====================================
    #   Package Info
    # ====================================
    from xcv import __version__, __author__, __email__

    PACKAGE_NAME: str = "xcv"
    XCV_VERSION: str = __version__
    XCV_AUTHOR: str = __author__
    XCV_EMAIL: str = __email__
    XCV_DESCRIPTION: str = f"""
        The project's goal is to make game-based OpenCV experiments easier.

        By avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. 
        On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins
        (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.
    """

    # ====================================
    #   Serial
    # ====================================
    SERIAL_BAUD: int = 115200

    # ====================================
    #   CLI Styling
    # ====================================
    debug_indent: str = "\n\t\t"
    centered_indent: str = "\n\t\t\t\t"
    WARNING = f"{debug_indent}🥵  WARNING"
    LAUNCHING = f"{debug_indent}🧨  LAUNCHING"

    # ====================================
    #   Paths
    # ====================================
    from pathlib import Path

    HOME_PATH: Path = Path.home()
    ABSPATH: str = Path(__file__).resolve().parent

    @property
    def WINDOWS(self) -> bool:
        import platform

        if platform.system() == "Windows":
            _w = True
        else:
            _w = False

        return _w

    @property
    def SERIAL_PORT(self) -> str:
        if self.WINDOWS:
            _sp: str = "COM17"
        else:
            _sp: str = "/dev/cu.SLAB_USBtoUART"

        return _sp


if __name__ == "__main__":
    s = Settings()
    print(s.SERIAL_PORT)
    print(s.WINDOWS)
    print(s.HOME_PATH)
