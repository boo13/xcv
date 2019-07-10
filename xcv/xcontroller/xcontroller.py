from dataclasses import dataclass


@dataclass(order=True)
class Buttons:
    aBtn: bytes = 48
    bBtn: bytes = 48
    xBtn: bytes = 48
    yBtn: bytes = 48
    lbBtn: bytes = 48
    rbBtn: bytes = 48
    duBtn: bytes = 48
    ddBtn: bytes = 48
    dlBtn: bytes = 48
    drBtn: bytes = 48
    ltBtn: bytes = 48
    rtBtn: bytes = 48
    lsx: bytes = 53
    lsy: bytes = 53
    rsx: bytes = 53
    rsy: bytes = 53
    startBtn: bytes = 48
    selectBtn: bytes = 48
    xboxBtn: bytes = 48

    def show(self):
        for k, v in self.__dict__.items():
            print(k, v)


def serial_send(buttonSet):
    """ ⚠️ Order matters! ⚠️ This is an order that is parsed out in a hardcoded way in the arduino script. """

    import serial
    from settings import Settings  # Local

    if Settings.verbose:
        buttonSet.show()

    # ASCII lookup table
    on = 49  # '1'
    off = 48  # '0'
    startMarker = 60  # '<'
    endMarker = 62  # '>'
    comma = 44  # ','

    # Be safe kids - use a Context Manager
    with serial.Serial(Settings.serialPort, Settings.serialBaud) as ser:
        # START MARKER
        ser.write(chr(startMarker).encode())

        # A
        ser.write(chr(buttonSet.aBtn).encode())
        ser.write(chr(comma).encode())

        # B
        ser.write(chr(buttonSet.bBtn).encode())
        ser.write(chr(comma).encode())

        # X
        ser.write(chr(buttonSet.xBtn).encode())
        ser.write(chr(comma).encode())

        # Y
        ser.write(chr(buttonSet.yBtn).encode())
        ser.write(chr(comma).encode())

        # Left Bumper
        ser.write(chr(buttonSet.lbBtn).encode())
        ser.write(chr(comma).encode())

        # Right Bumper
        ser.write(chr(buttonSet.rbBtn).encode())
        ser.write(chr(comma).encode())

        # D - Up
        ser.write(chr(buttonSet.duBtn).encode())
        ser.write(chr(comma).encode())

        # D - Down
        ser.write(chr(buttonSet.ddBtn).encode())
        ser.write(chr(comma).encode())

        # D - Left
        ser.write(chr(buttonSet.dlBtn).encode())
        ser.write(chr(comma).encode())

        # D - Right
        ser.write(chr(buttonSet.drBtn).encode())
        ser.write(chr(comma).encode())

        # Left Trigger
        ser.write(chr(buttonSet.ltBtn).encode())
        ser.write(chr(comma).encode())

        # Right Trigger
        ser.write(chr(buttonSet.rtBtn).encode())
        ser.write(chr(comma).encode())

        # Left Stick - X
        ser.write(chr(buttonSet.lsx).encode())
        ser.write(chr(comma).encode())

        # Left Stick - Y
        ser.write(chr(buttonSet.lsy).encode())
        ser.write(chr(comma).encode())

        # Right Stick - X
        ser.write(chr(buttonSet.rsx).encode())
        ser.write(chr(comma).encode())

        # Right Stick - Y
        ser.write(chr(buttonSet.rsy).encode())
        ser.write(chr(comma).encode())

        # Start Button
        ser.write(chr(buttonSet.startBtn).encode())
        ser.write(chr(comma).encode())

        # Select Button
        ser.write(chr(buttonSet.selectBtn).encode())
        ser.write(chr(comma).encode())

        # Xbox Button
        ser.write(chr(buttonSet.xboxBtn).encode())
        ser.write(chr(comma).encode())

        # Button Press Time (* currently unused)
        ser.write(chr(on).encode())

        # END MARKER
        ser.write(chr(endMarker).encode())


# In case we're just testing the controller...
if __name__ == "__main__":
    btns = Buttons()
    btns.aBtn = 49
    serial_send(btns)
