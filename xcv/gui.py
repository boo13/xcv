# TODO: Improve GUI layout
# TODO: Get the xbox buttons sending serial commands
# TODO: Implement switch for `cap = cv2.VideoCapture(0)` and `streamlink` stream from twitch, mixer, etc.

#          Import libraries      ______________________________________________

import sys
# import datetime

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

# from xcv.game.Templates import TemplateMatcher, ROI
# _________________ From 'pip' install _____________________________________
import PySimpleGUIQt as sg  # GUIs made simple
import cv2  # Opencv
# import imutils  # Opencv utils (pyimagesearch.com)
import numpy as np
from loguru import logger

from fps import fps
import xcv.xcontroller
# from settings import serial_session

from base64_btns import (
    xb_a,
    xb_a_null,
)


@logger.catch
class GUI:
    # _output_console = [
    #     sg.Output(size=(640, 100), background_color="#16161F", text_color="#A6A4AF")
    # ]


    def __init__(self):
        # Global GUI settings
        sg.SetOptions(
            font="Helvetica 10",
            element_padding=(5, 5),
            scrollbar_color=None,
            background_color="#16161F",
            text_color="#A6A4AF",
        )

        self._btnA = {"btn_name": "_btnA_", "state": None, "on_image": xb_a, "off_image": xb_a_null}
        # self._btnB = {"btn_name": "_btnB_", "state": None, "on_image": xb_b, "off_image": xb_b_null}
        # self._btnX = {"btn_name": "_btnX_", "state": None, "on_image": xb_x, "off_image": xb_x_null}
        # self._btnY = {"btn_name": "_btnY_", "state": None, "on_image": xb_y, "off_image": xb_y_null}
        # self._btnStart = {
        #     "btn_name": "_btnStart_",
        #     "state": None,
        #     "on_image": xb_start,
        #     "off_image": xb_start_null,
        # }
        # self._btnSelect = {
        #     "btn_name": "_btnSelect_",
        #     "state": None,
        #     "on_image": xb_select,
        #     "off_image": xb_select_null,
        # }
        # # self._btnXbox = {"btn_name": "_btnY_", "on_image": xb_y, "off_image": xb_y_null}
        # self._btnLB = {
        #     "btn_name": "_btnLB_",
        #     "state": None,
        #     "on_image": xb_lb,
        #     "off_image": xb_lb_null,
        # }
        # self._btnRB = {
        #     "btn_name": "_btnRB_",
        #     "state": None,
        #     "on_image": xb_rb,
        #     "off_image": xb_rb_null,
        # }
        # #TODO: Fix the `on image` for both LT and RT (size is off)
        # self._btnLT = {
        #     "btn_name": "_btnLT_",
        #     "state": None,
        #     "on_image": xb_lt,
        #     "off_image": xb_lt_null,
        # }
        # self._btnRT = {
        #     "btn_name": "_btnRT_",
        #     "state": None,
        #     "on_image": xb_rt,
        #     "off_image": xb_rt_null,
        # }
        #
        self._all_buttons = [
            self._btnA,
        #     self._btnB,
        #     self._btnX,
        #     self._btnY,
        #     self._btnStart,
        #     self._btnSelect,
        #     self._btnLB,
        #     self._btnRB,
        #     self._btnLT,
        #     self._btnRT,
        ]

        # Style settings
        self._text_color = "#A6A4AF"
        self._btn_text_color = "#16161F"
        self._background_color = "#16161F"

        # create the window and show it
        from xcv.version import XCV_VERSION
        self.window = sg.Window(f"XCV - {XCV_VERSION}", location=(800, 200))
        self.window.Layout(self._layout()).Finalize()

        # OpenCV
        self.cap = cv2.VideoCapture(0)

        # Check if video stream was found
        if not self.cap.isOpened():
            logger.debug("Unable to read camera feed")
        else:
            # Default capture frame width and height (comes as float)
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.debug(
                f"Video Captured - Size: {self.frame_width} x {self.frame_height}\n"
            )

            fps.start()

            self.event_loop()

    def _event_checker(self, _event):
        if _event == "Exit" or _event is None:
            self.close_all(self.window)
            sys.exit(0)

        if _event != "timeout":
            logger.debug(_event)

        # for b in self._all_buttons:
        #     if _event == b["btn_name"]:
        #         self.window.FindElement(b["btn_name"]).Update(data_base64=b["on_image"])
        #         xcv.xcontroller.single_btn_press(b["btn_name"])
        #         print(_event)

        if _event == "_check_serial_":
            print("Check Serial pressed!")

        # if not being pressed: reset the button image
        # for b in self._all_buttons:
        #     if _event != b["btn_name"]:
        #         self.window.FindElement(b["btn_name"]).Update(data_base64=b["off_image"])

    def _values_checker(self, _values, frame):
        if _values["thresh"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
            _, frame = cv2.threshold(
                frame, _values["thresh_slider"], 255, cv2.THRESH_BINARY
            )

        if _values["canny"]:
            frame = cv2.Canny(
                frame, _values["canny_slider_a"], _values["canny_slider_b"]
            )

        if _values["blur"]:
            frame = cv2.GaussianBlur(frame, (21, 21), _values["blur_slider"])

        if _values["hue"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += _values["hue_slider"]
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

        if _values["enhance"]:
            enh_val = _values["enhance_slider"] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        if _values["contour"]:
            hue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hue = cv2.GaussianBlur(hue, (21, 21), 1)
            hue = cv2.inRange(
                hue,
                np.array([_values["contour_slider"], _values["base_slider"], 40]),
                np.array([_values["contour_slider"] + 30, 255, 220]),
            )
            _, cnts, _ = cv2.findContours(
                hue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if cnts:
                cv2.drawContours(frame, cnts, -1, (0, 0, 255), 2)
        return _values, frame

    def event_loop(self):
        while True:
            fps.update()

            _event, _values = self.window.Read(timeout=10, timeout_key="timeout")

            ret, frame = self.cap.read()

            self._event_checker(_event)
            _, frame = self._values_checker(_values, frame)

            draw_HUD_FPS(frame, 7)
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()  # ditto

            self._gui_variable_updates()
            self.window.FindElement("_video_frame_").Update(data=imgbytes)
            # self.window.FindElement("imagetab_image").Update(data=imgbytes)

    def _gui_variable_updates(self):
        """"Where I put the ``FindElement` commands."""

        self.window.FindElement("_elapsed_").Update(fps.elapsed)
        self.window.FindElement("_fps_").Update(fps.fps)

    def _layout(self):

        _row_gui_commands = [
                sg.Button(
                    "Check Serial",
                    size=(10, 1),
                    button_color=("#16161F", "#007339"),
                    key="_check_serial_",
                ),
                sg.Button(
                    "Stop",
                    button_color=(self._btn_text_color, "#B36C42"),
                    size=(10, 1),
                    key="_stop_",
                ),
                sg.Button(
                    "Record",
                    size=(10, 1),
                    button_color=(self._btn_text_color, "#BD3138"),
                    key="_record_",
                ),
                sg.Button(
                    "Screenshot",
                    button_color=(self._btn_text_color, "#1749BF"),
                    size=(10, 1),
                    key="_screenshot_",
                ),
            ]


        _row_buttons_col_main_buttons = [
                # sg.Image(
                #     data_base64=xb_lt_null,
                #     key="_btnLT_",
                #     enable_events=True,
                #     pad=((10, 0), (0, 0)),
                # ),
                # sg.Image(data_base64=xb_lb_null, key="_btnLB_", enable_events=True),
                # sg.Image(
                #     data_base64=xb_select_null, key="_btnSelect_", enable_events=True
                # ),
                # sg.Image(
                #     data_base64=xb_start_null, key="_btnStart_", enable_events=True
                # ),
                # sg.Image(data_base64=xb_x_null, key="_btnX_", enable_events=True),
                # sg.Image(data_base64=xb_y_null, key="_btnY_", enable_events=True),
                sg.Image(data_base64=xb_a_null, key="_btnA_", enable_events=True),
                # sg.Image(data_base64=xb_b_null, key="_btnB_", enable_events=True),
                # sg.Image(data_base64=xb_rb_null, key="_btnRB_", enable_events=True),
                # sg.Image(data_base64=xb_rt_null, key="_btnRT_", enable_events=True),
            ]

        _gui_commands_row_4 = [
            sg.Button("Exit", size=(10, 1), button_color=("#A6A4AF", "#BD3138")),
            sg.Text("Vers:", text_color="#A6A4AF"),
            sg.Text("", key="_elapsed_", text_color="#A6A4AF"),
            sg.Text("FPS:", text_color="#A6A4AF"),
            sg.Text("", key="_fps_", text_color="#A6A4AF"),
        ]


        maintab_layout = [
            [sg.T("XCV", font=("Helvetica", 16), justification="center")],
            [sg.Image(filename="", size=(640, 480), key="_video_frame_")],

            _row_gui_commands,
            _row_buttons_col_main_buttons,
            _gui_commands_row_4
        ]

        imagetab_layout = [
            [sg.T("Image Controls", font=("Helvetica", 16), justification="center")],
            [sg.Image(filename="", size=(40, 15), key="imagetab_image")],
            [sg.Checkbox("None", default=True, size=(10, 1))],
            [
                sg.Checkbox("threshold", size=(10, 1), key="thresh"),
                sg.Slider(
                    (0, 255),
                    128,
                    1,
                    orientation="h",
                    size=(40, 15),
                    key="thresh_slider",
                ),
            ],
            [
                sg.Checkbox("canny", size=(10, 1), key="canny"),
                sg.Slider(
                    (0, 255),
                    128,
                    1,
                    orientation="h",
                    size=(20, 15),
                    key="canny_slider_a",
                ),
                sg.Slider(
                    (0, 255),
                    128,
                    1,
                    orientation="h",
                    size=(20, 15),
                    key="canny_slider_b",
                ),
            ],
            [
                sg.Checkbox("contour", size=(10, 1), key="contour"),
                sg.Slider(
                    (0, 255),
                    128,
                    1,
                    orientation="h",
                    size=(20, 15),
                    key="contour_slider",
                ),
                sg.Slider(
                    (0, 255), 80, 1, orientation="h", size=(20, 15), key="base_slider"
                ),
            ],
            [
                sg.Checkbox("blur", size=(10, 1), key="blur"),
                sg.Slider(
                    (1, 11), 1, 1, orientation="h", size=(40, 15), key="blur_slider"
                ),
            ],
            [
                sg.Checkbox("hue", size=(10, 1), key="hue"),
                sg.Slider(
                    (0, 225), 0, 1, orientation="h", size=(40, 15), key="hue_slider"
                ),
            ],
            [
                sg.Checkbox("enhance", size=(10, 1), key="enhance"),
                sg.Slider(
                    (1, 255),
                    128,
                    1,
                    orientation="h",
                    size=(40, 15),
                    key="enhance_slider",
                ),
            ],
        ]

        return [
            [
                sg.TabGroup(
                    [
                        [
                            sg.Tab("Main", maintab_layout, tooltip="Main Menu"),
                            sg.Tab(
                                "Image Controls",
                                imagetab_layout,
                            ),
                        ]
                    ]
                )
            ]
        ]

    def close_all(self, window) -> None:
        """Release the camera feed, close all OpenCV windows and close all pysimpleGUI windows"""
        fps.stop()
        logger.debug(f"fps: {fps.fps}  elapsed: {fps.elapsed}")
        self.cap.release()
        cv2.destroyAllWindows()
        window.Close()
        logger.debug("Nice! You closed the windows on exit.")


if __name__ == "__main__":
    gui = GUI()
