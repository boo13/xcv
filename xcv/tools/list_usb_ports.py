def list_usb_ports():
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()

    print("\n-------------------------- Serial Ports --------------------------")

    for port, desc, hwid in sorted(ports):
        if desc != "n/a":
            print(f"\n\t{port}\n\t  DESC: {desc}\n\t  HWID: {hwid}")
        else:
            if not port.startswith("/dev/cu.Bluetooth") and not port.startswith(
                "/dev/cu.rara"
            ):
                print("\t", port)

    print("\n------------------------------------------------------------------")


if __name__ == "__main__":
    list_usb_ports()
