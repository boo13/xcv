# TODO: Improve GUI layout
# TODO: Get the xbox buttons sending serial commands
# TODO: Implement switch for `cap = cv2.VideoCapture(0)` and `streamlink` stream from twitch, mixer, etc.

#          Import libraries      ______________________________________________

import sys
import datetime

# Local
# from xcv.commands import XcvError
from hud import (
    draw_HUD_FPS,
    #     draw_HUD_controller,
    #     draw_HUD_HomeAway,
    #     draw_HUD_DefendingSide,
    #     draw_HUD_elapsedTime,
    draw_HUD_elapsedGameTime,
)


from tools import checkSerial

from gui_layout import layout

# from xcv.game.Templates import TemplateMatcher, ROI
# _________________ From 'pip' install _____________________________________
import PySimpleGUIQt as sg  # GUIs made simple
import cv2  # Opencv
import imutils  # Opencv utils (pyimagesearch.com)
import numpy as np
from loguru import logger
import xcontroller


@logger.catch
def mainGUI():

    # create the window and show it without the plot
    window = sg.Window("XCV", location=(800, 200))
    window.Layout(layout).Finalize()

    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Unable to read camera feed")
    else:
        # Default capture frame width and height, comes as float, converted to
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        logger.debug(f"Video Captured - Frame size: {frame_width} x {frame_height}\n")

    while True:
        event, values = window.Read(timeout=0, timeout_key="timeout")

        if event == "Exit" or event is None:
            close_all(cap, window)
            sys.exit(0)

        if event != "timeout":
            logger.debug(event)

        if event == "_btnA_":
            xcontroller.single_btn_press("A")
            print("A - pressed!")

        if event == "_btnB_":
            xcontroller.single_btn_press("B")
            print("B - pressed!")

        if event == "_btnX_":
            xcontroller.single_btn_press("X")
            print("X - pressed!")

        if event == "_btnY_":
            xcontroller.single_btn_press("Y")
            print("Y - pressed!")

        if event == "_btnLB_":
            xcontroller.single_btn_press("l")
            print("LB - pressed!")

        if event == "_btnRB_":
            xcontroller.single_btn_press("r")
            print("RB - pressed!")

        if event == "_btnStart_":
            xcontroller.single_btn_press("S")
            print("Start - pressed!")

        if event == "_btnSelect_":
            print("This button is NOT yet setup... sorry!")

        if event == "_check_serial_":
            checkSerial()
            print("Check Serial pressed!")

        ret, frame = cap.read()

        if values["thresh"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
            _, frame = cv2.threshold(
                frame, values["thresh_slider"], 255, cv2.THRESH_BINARY
            )

        if values["canny"]:
            frame = cv2.Canny(frame, values["canny_slider_a"], values["canny_slider_b"])

        if values["blur"]:
            frame = cv2.GaussianBlur(frame, (21, 21), values["blur_slider"])

        if values["hue"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += values["hue_slider"]
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

        if values["enhance"]:
            enh_val = values["enhance_slider"] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        if values["contour"]:
            hue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hue = cv2.GaussianBlur(hue, (21, 21), 1)
            hue = cv2.inRange(
                hue,
                np.array([values["contour_slider"], values["base_slider"], 40]),
                np.array([values["contour_slider"] + 30, 255, 220]),
            )
            _, cnts, _ = cv2.findContours(
                hue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if cnts:
                cv2.drawContours(frame, cnts, -1, (0, 0, 255), 2)

        draw_HUD_FPS(frame, 7)

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()  # ditto
        window.FindElement("main_image").Update(data=imgbytes)
        window.FindElement("imagetab_image").Update(data=imgbytes)


def close_all(cap, window) -> None:
    """Release the camera feed, close all OpenCV windows and close all pysimpleGUI windows"""
    cap.release()
    cv2.destroyAllWindows()
    window.Close()
    logger.debug("Nice! You closed the windows on exit.")


if __name__ == "__main__":
    mainGUI()
