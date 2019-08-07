# TODO: Improve GUI layout
# TODO: Get the xbox buttons sending serial commands
# TODO: Implement switch for `cap = cv2.VideoCapture(0)` and `streamlink` stream from twitch, mixer, etc.

#          Import libraries      ______________________________________________

import sys
import datetime

# Local
from xcv.commands import XcvError
from xcv.hud import (
    draw_HUD_FPS,
    #     draw_HUD_controller,
    #     draw_HUD_HomeAway,
    #     draw_HUD_DefendingSide,
    #     draw_HUD_elapsedTime,
    draw_HUD_elapsedGameTime,
)
from xcv.settings import Settings
from xcv.tools import checkSerial

# from xcv.game.Templates import TemplateMatcher, ROI
# _________________ From 'pip' install _____________________________________
import PySimpleGUIQt as sg  # GUIs made simple
import cv2  # Opencv
import imutils  # Opencv utils (pyimagesearch.com)
import numpy as np
from loguru import logger
from xcv.xcontroller import xcontroller

from xcv.base64_btns import (
    xb_a,
    xb_b,
    xb_x,
    xb_y,
    xb_a_null,
    xb_b_null,
    xb_x_null,
    xb_y_null,
    xb_select,
    xb_select_null,
    xb_start,
    xb_start_null,
    xb_lb,
    xb_lb_null,
    xb_rb,
    xb_rb_null,
    xb_lt,
    xb_lt_null,
    xb_rt,
    xb_rt_null,
    stick_inner_ring,
    stick_outer_ring,
)


@logger.catch
def mainGUI():

    _text_color = "#A6A4AF"
    _btn_text_color = "#16161F"
    _background_color = "#16161F"

    # Global GUI settings
    sg.SetOptions(
        element_padding=(5, 5),
        scrollbar_color=None,
        background_color=_background_color,
        text_color="#A6A4AF",
    )

    _exitButton = [
        sg.Button("Exit", size=(10, 1), button_color=("#A6A4AF", "#BD3138")),
        sg.Text(
            f"Vers: {Settings.XCV_VERSION}    USB: {Settings.SERIAL_PORT}    Baud: {Settings.SERIAL_BAUD}    FPS: ? ",
            font="Helvetica 10",
            justification="right",
        ),
    ]

    _outputconsole = [
        sg.Output(size=(640, 100), background_color="#16161F", text_color=_text_color)
    ]

    # define the window layout
    maintab_layout = [
        [sg.T("XCV", font=("Helvetica", 16), justification="center")],
        [sg.Image(filename="", size=(640, 480), key="main_image")],
        [
            sg.Image(
                data_base64=xb_lt_null,
                key="_btnLT_",
                enable_events=True,
                pad=((10, 0), (0, 0)),
            ),
            sg.Image(
                data_base64=xb_lb_null,
                key="_btnLB_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_select_null,
                key="_btnSelect_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_start_null,
                key="_btnStart_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_x_null,
                key="_btnX_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_y_null,
                key="_btnY_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_a_null,
                key="_btnA_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_b_null,
                key="_btnB_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_rb_null,
                key="_btnRB_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=xb_rt_null,
                key="_btnRT_",
                enable_events=True,
            ),
        ],
        # [sg.Image(
        #         data_base64=stick_outer_ring,
        #         key="_LS_",
        #         enable_events=True,
        #         pad=((50, 0), (0, 0)),
        #     ),
        #     sg.Image(
        #         data_base64=stick_outer_ring,
        #         key="_RS_",
        #         enable_events=True,
        #         pad=((50, 0), (0, 0)),
        #     ),
        # ],
        [
            sg.Button(
                "Check Serial",
                size=(10, 1),
                button_color=("#16161F", "#007339"),
                key="_check_serial_",
            ),
            sg.Button("Stop", button_color=(_btn_text_color, "#B36C42"), size=(10, 1)),
            sg.Button(
                "Record", size=(10, 1), button_color=(_btn_text_color, "#BD3138")
            ),
            sg.Button(
                "Screenshot", button_color=(_btn_text_color, "#1749BF"), size=(10, 1)
            ),
        ],
        _outputconsole,
        _exitButton,
    ]

    tab2_layout = [
        [sg.T("Nothing to see here... yet")],
        [
            sg.Text("Send Command:", size=(15, 1), justification="right"),
            sg.InputText("", key="input1", text_color=_text_color, size_px=(420, 35)),
        ],
        _exitButton,
    ]

    """
    Demo program that displays a webcam using OpenCV and applies some very basic image functions

    - functions from top to bottom -
    none:       no processing
    threshold:  simple b/w-threshold on the luma channel, slider sets the threshold value
    canny:      edge finding with canny, sliders set the two threshold values for the function => edge sensitivity
    contour:    colour finding in the frame, first slider sets the hue for the colour to find, second the minimum saturation
                for the object. Found objects are drawn with a red contour.
    blur:       simple Gaussian blur, slider sets the sigma, i.e. the amount of blur smear
    hue:        moves the image hue values by the amount selected on the slider
    enhance:    applies local contrast enhancement on the luma channel to make the image fancier - slider controls fanciness.
    """
    imagetab_layout = [
        [sg.T("Image Controls", font=("Helvetica", 16), justification="center")],
        [sg.Image(filename="", size=(40, 15), key="imagetab_image")],
        [sg.Checkbox("None", default=True, size=(10, 1))],
        [
            sg.Checkbox("threshold", size=(10, 1), key="thresh"),
            sg.Slider(
                (0, 255), 128, 1, orientation="h", size=(40, 15), key="thresh_slider"
            ),
        ],
        [
            sg.Checkbox("canny", size=(10, 1), key="canny"),
            sg.Slider(
                (0, 255), 128, 1, orientation="h", size=(20, 15), key="canny_slider_a"
            ),
            sg.Slider(
                (0, 255), 128, 1, orientation="h", size=(20, 15), key="canny_slider_b"
            ),
        ],
        [
            sg.Checkbox("contour", size=(10, 1), key="contour"),
            sg.Slider(
                (0, 255), 128, 1, orientation="h", size=(20, 15), key="contour_slider"
            ),
            sg.Slider(
                (0, 255), 80, 1, orientation="h", size=(20, 15), key="base_slider"
            ),
        ],
        [
            sg.Checkbox("blur", size=(10, 1), key="blur"),
            sg.Slider((1, 11), 1, 1, orientation="h", size=(40, 15), key="blur_slider"),
        ],
        [
            sg.Checkbox("hue", size=(10, 1), key="hue"),
            sg.Slider((0, 225), 0, 1, orientation="h", size=(40, 15), key="hue_slider"),
        ],
        [
            sg.Checkbox("enhance", size=(10, 1), key="enhance"),
            sg.Slider(
                (1, 255), 128, 1, orientation="h", size=(40, 15), key="enhance_slider"
            ),
        ],
        _exitButton,
    ]

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Main", maintab_layout, tooltip="Main Menu"),
                        sg.Tab(
                            "Image Controls",
                            imagetab_layout,
                            tooltip="For testings CV values",
                        ),
                        # sg.Tab("Output", tab2_layout, tooltip="eSet Output"),
                        # sg.Tab(
                        #     "Autopilot",
                        #     tab2_layout,
                        #     tooltip="Press Buttons Automagically",
                        # ),
                        # sg.Tab(
                        #     "Training", tab2_layout, tooltip="Machine Learning Stuff"
                        # ),
                        # sg.Tab("Debug", tab2_layout, tooltip="Debug"),
                    ]
                ],
                tooltip="TIP2",
            )
        ]
    ]

    # create the window and show it without the plot
    window = sg.Window("XCV", location=(800, 400))
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
