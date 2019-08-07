from dataclasses import dataclass


# Settings - we use these to set (and mostly forget) the config
@dataclass
class Settings:
    # __slots__ = [
    #     "TIMEZONE",
    #     "timer",
    #     "verbose",
    #     "PACKAGE_NAME",
    #     "XCV_VERSION",
    #     "XCV_AUTHOR",
    #     "XCV_EMAIL",
    #     "XCV_DESCRIPTION",
    #     "SERIAL_BAUD",
    #     "WINDOWS",
    #     "SERIAL_PORT",
    # ]

    # ====================================
    #   User Settings
    # ====================================
    TIMEZONE: str = "US/Eastern"
    timer: int = 10
    verbose: bool = False

    # ====================================
    #   Package Info
    # ====================================    
    XCV_DESCRIPTION: str = f"""
        The project's goal is to make game-based OpenCV experiments easier.

        By avoiding controller-driver nonsense and just hacking into controllers and connecting the buttons to an arduino/teensy/whatever. 
        On the arduino/teensy side of things, we then just parse out the commands and send some high/low signals to I/O pins
        (other bits and bobs to handle all the I/O) and then a fancy display output to make things more fancy.
    """

    # ====================================
    #   System
    # ====================================
    import sys

    _WINDOWS = sys.platform.startswith("win")

    @property
    def WINDOWS(self) -> bool:
        return self._WINDOWS

    # ====================================
    #   Serial
    # ====================================
    SERIAL_BAUD: int = 115200

    @property
    def SERIAL_PORT(self) -> str:
        if self.WINDOWS:
            return "COM17"
        else:
            return "/dev/cu.SLAB_USBtoUART"

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
    ABSPATH: Path = Path(__file__).resolve().parent


if __name__ == "__main__":
    s = Settings()
    print(s.SERIAL_PORT)
    print(s.WINDOWS)
    print(s.HOME_PATH)
