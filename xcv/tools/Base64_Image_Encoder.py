import PySimpleGUIQt as sg
import os
import base64

"""
    Base64 Encoder - encodes a folder of PNG files and creates a .py file with definitions

    This is an unmodified version of the Demo Program from PySimpleGUI
    https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Base64_Image_Encoder.py

"""


def main():
    OUTPUT_FILENAME = "base64_output.py"
    folder = "input"

    try:
        namesonly = [
            f for f in os.listdir(folder) if f.endswith(".png") or f.endswith(".ico")
        ]
    except:
        print("Cancelled - No valid folder entered")
        return

    outfile = open(os.path.join(folder, OUTPUT_FILENAME), "w")

    for i, file in enumerate(namesonly):
        contents = open(os.path.join(folder, file), "rb").read()
        encoded = base64.b64encode(contents)
        outfile.write("\n{} = {}\n\n".format(file[: file.index(".")], encoded))
        sg.OneLineProgressMeter("Base64 Encoding", i + 1, len(namesonly), key="_METER_")

    outfile.close()
    sg.Popup("Completed!", "Encoded %s files" % (i + 1))


if __name__ == "__main__":
    main()
