# TODO: Implement switch for `cap = cv2.VideoCapture(0)` and `streamlink` stream from twitch, mixer, etc.

#          Import libraries      ______________________________________________

import sys

# import datetime

from xcv.template_matcher import TemplateMatcher

# _________________ From 'pip' install _____________________________________
import PySimpleGUIQt as sg
import cv2
import imutils
import numpy as np
from loguru import logger

from xcv.fps import fps
import xcontroller
from settings import serial_session
import xcv.base64_icons as b64


@logger.catch
class GUI:
    """
    Build the GUI layout, display it, check for events and act accordingly.
    """

    def __init__(self):
        # Style settings
        self.FONT = "Helvetica 8"
        self.TEXT_COLOR = "#A6A4AF"
        self.BKG_COLOR = "#0a0a0f"
        
        self._build_window()


    def _build_window(self):

        from xcv.version import XCV_VERSION

        self.window = sg.Window(
            f"XCV - {XCV_VERSION}",
            layout=self._lay_it_out(),
            location=(600, 200),
            background_color=self.BKG_COLOR,
        )

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


    def _layout_maintab(self):

        # Global GUI settings
        sg.SetOptions(
            font=self.FONT, element_padding=(0, 0), scrollbar_color=None, text_color=self.TEXT_COLOR
        )

        """
        """
        _row0_video_frame = [sg.Image(filename="", key="_video_frame_")]

        """
        """
        _row1_detected_state = [sg.Text("", key="_detected_state_")]

        """ --------------------------------------------------------------------------
        Game Stats - Example Display: 

        0 - 0  Home    Defending Left  BALL    Offensive - Shooting - InsideBox

        _tactic_ = Our AI's current gameplan/status
        """
        _row2_game_stats = [
            sg.Text("", key="_score_"),
            sg.Text("", key="_home_away_"),
            sg.Text("", key="_defending_side_"),
            sg.Text("", key="_possession_"),
            sg.Text("", key="_tactic_"),
        ]

        """
        Action Buttons - Example Display: 

            Y
          X   B
            A
        """
        _row3_xcontroller_action_buttons = [
            sg.Image(filename="", key="_a_", enable_events=True),
            sg.Image(filename="", key="_b_", enable_events=True),
            sg.Image(filename="", key="_x_", enable_events=True),
            sg.Image(filename="", key="_y_", enable_events=True),
        ]

        """
        DPad Buttons - Example Display: 

            ^
          <   >
            v
        """
        _row3_xcontroller_dpad = [
            sg.Image(data_base64=b64.DU_WHITE, key="_du_", enable_events=True),
            # sg.Image(data_base64=b64.DD_WHITE, key="_dd_", enable_events=True),
            sg.Image(data_base64=b64.DL_WHITE, key="_dl_", enable_events=True),
            sg.Image(data_base64=b64.DR_WHITE, key="_dr_", enable_events=True),
        ]

        """
        """
        _row4_connection_status = [
            sg.Image(data_base64=b64.GAMEPAD_NULL, key="_gamepad_connection_status_"),
            sg.Text("", key="_gamepad_usb_port_"),
            sg.Image(data_base64=b64.FILM_NULL, key="_opencv_fps_icon_"),
            sg.Text("", key="_opencv_fps_"),
        ]

        """
        """
        _row5_gui_menu_buttons = [
            sg.Image(data_base64="", key="_save_logs_"),
            sg.Image(data_base64=b64.SAVE_NULL, key="_save_screenshot_"),
            sg.Image(data_base64="", key="_start_record_"),
            sg.Image(data_base64=b64.POWER_NULL, key="_EXIT_"),
        ]
        _output_console = [
            sg.Output(size=(640, 100), background_color="#16161F", text_color="#A6A4AF")
        ]

        # define the window layout
        full_layout = [
            _row0_video_frame,
            _row1_detected_state,
            _row2_game_stats,
            _row3_xcontroller_action_buttons,
            _row3_xcontroller_dpad,
            _row4_connection_status,
            _row5_gui_menu_buttons,
            _output_console,
        ]
        return full_layout


    def _lay_it_out(self):
        maintab_layout = self._layout_maintab()

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
                            sg.Tab("Main", maintab_layout),
                            sg.Tab("Image Controls", imagetab_layout),
                        ]
                    ]
                )
            ]
        ]

    def _event_checker(self, _event):
        if _event == "Exit" or _event is None:
            self.close_all(self.window)
            sys.exit(0)

        if _event != "timeout":
            logger.debug(_event)

        # for b in self._all_buttons:
        #     if _event == b["btn_name"]:
        #         self.window.FindElement(b["btn_name"]).Update(
        #             data_base64=b["on_image"])
        #         xcontroller.single_btn_press(b["btn_name"])
        #         print(_event)

        if _event == "_check_serial_":
            print("Check Serial pressed!")

        # if not being pressed: reset the button image
        # for b in self._all_buttons:
        #     if _event != b["btn_name"]:
        #         self.window.FindElement(b["btn_name"]).Update(
        #             data_base64=b["off_image"])

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

            ok, frame = self.cap.read()

            if ok:
                self._event_checker(_event)
                # _, frame = self._values_checker(_values, frame)

                # draw_HUD_FPS(frame, 7)

            imgbytes = cv2.imencode(".png", frame)[1].tobytes()  # ditto
            # self.window.FindElement("_elapsed_").Update(fps.elapsed)
            # self.window.FindElement("_fps_").Update(fps.fps)
            self.window.FindElement("_video_frame_").Update(data=imgbytes)
            # self.window.FindElement("imagetab_image").Update(data=imgbytes)

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
