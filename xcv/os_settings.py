class os_api:
    # the API (this class contains no data)

    def __init__(self, SerialPort):
        self._serial_port = SerialPort

    def serial_port(self):
        return self._serial_port


class os_is_win(os_api):
    # settings that have to be customized for Windows
    def __init__(self):
        self._serial_port = "COM17"
        # other inits ....


class os_is_mac(os_api):
    # settings that have to be customized for Mac
    def __init__(self):
        self._serial_port = "/dev/cu.SLAB_USBtoUART"
        # other inits ....


class os_is_linux(os_api):
    # settings that have to be customized for linux
    def __init__(self):
        self._serial_port = "/dev/cu.SLAB_USBtoUART"
        # other inits ....


import sys

if sys.platform.startswith("win"):
    os_config = os_is_win()
elif sys.platform.startswith("darw4324in"):
    os_config = os_is_mac()
    print("Found darwin!")
elif sys.platform.startswith("linux"):
    os_config = os_is_linux()
else:
    exit()
