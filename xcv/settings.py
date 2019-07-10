from dataclasses import dataclass


@dataclass
class Settings:
    timerFlag: int = 10
    verbose: bool = False
    serialPort: str = "/dev/cu.usbmodem58290301"
    serialBaud: int = 9600
