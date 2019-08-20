# TODO: Implement switch for `cap = cv2.VideoCapture(0)` and `streamlink` stream from twitch, mixer, etc.
import os
import sys

# import datetime
from xcv.template_matcher import TemplateMatcher
import xcv.xcontroller
from xcv.fps import fps
import xcv.base64_icons as b64
import xcv.version
from xcv.hud import draw_HUD_FPS

# _________________ `pip install` _________________
import PySimpleGUIQt as sg
import cv2
import numpy as np
from loguru import logger

import random
import string
from pathlib import Path

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@logger.catch()
class VideoCapture:

    def __init__(self, gui=True):
        path = Path(__file__).resolve().parent
        self.clock_image_path = path / "output/scoreboard/clock"
        self.score_image_path = path / "output/scoreboard/score"

        # Style settings
        self.FONT = "Helvetica 8"
        self.TEXT_COLOR = "#A6A4AF"
        self.BKG_COLOR = "#0a0a0f"

        self.button_a = {
            "key": "_a_",
            "name": "A",
            "on_image": b64.BTN_A_ON,
            "off_image": b64.BTN_A_OFF,
        }
        self.button_b = {
            "key": "_b_",
            "name": "B",
            "on_image": b64.BTN_B_ON,
            "off_image": b64.BTN_B_OFF,
        }
        self.button_x = {
            "key": "_x_",
            "name": "X",
            "on_image": b64.BTN_X_ON,
            "off_image": b64.BTN_X_OFF,
        }
        self.button_y = {
            "key": "_y_",
            "name": "Y",
            "on_image": b64.BTN_Y_ON,
            "off_image": b64.BTN_Y_OFF,
        }
        self.button_start = {
            "key": "_start_",
            "name": "Start",
            "on_image": b64.START_ON,
            "off_image": b64.START_OFF,
        }
        self.button_select = {
            "key": "_select_",
            "name": "Select",
            "on_image": b64.SELECT_ON,
            "off_image": b64.SELECT_OFF,
        }
        self.button_lb = {
            "key": "_lb_",
            "name": "L Bumper",
            "on_image": b64.BTN_LB_ON,
            "off_image": b64.BTN_LB_OFF,
        }
        self.button_lt = {
            "key": "_lt_",
            "name": "L Trigger",
            "on_image": b64.BTN_LT_ON,
            "off_image": b64.BTN_LT_OFF,
        }
        self.button_rb = {
            "key": "_rb_",
            "name": "R Bumper",
            "on_image": b64.BTN_RB_ON,
            "off_image": b64.BTN_RB_OFF,
        }
        self.button_rt = {
            "key": "_rt_",
            "name": "R Trigger",
            "on_image": b64.BTN_RT_ON,
            "off_image": b64.BTN_RT_OFF,
        }
        self._all_buttons = [
            self.button_a,
            self.button_b,
            self.button_x,
            self.button_y,
            self.button_select,
            self.button_start,
            self.button_lb,
            self.button_lt,
            self.button_rb,
            self.button_rt
        ]

        self.gui_switch = gui

        if self.gui_switch:
            sg.SetOptions(
                scrollbar_color=None,
                text_color=self.TEXT_COLOR,
                font=self.FONT,
                element_padding=(0, 0),
                background_color=self.BKG_COLOR,
                message_box_line_width=0,
                text_justification="left",
                margins=(0, 0),
                border_width=0,
            )

            from xcv.version import XCV_VERSION
            _gui_layout = GUILayout()

            self.window = sg.Window(
                f"XCV - {XCV_VERSION}",
                layout=_gui_layout.full_layout(),
                location=(600, 200),
                icon=b64.Microsoft_Xbox_Emoji_Icon,
                border_depth=0,
            )

        self.cap = cv2.VideoCapture(0)
        self.check_video_stream()
        fps.start()
        self.event_loop()


    def check_video_stream(self):
        """Check if video stream was found"""
        if not self.cap.isOpened():
            logger.warning("Unable to read camera feed")
        else:
            # Default capture frame width and height (comes as float)
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.debug(
                f"Video Captured - Size: {self.frame_width} x {self.frame_height}\n"
            )
            if self.frame_width >= 641:
                logger.warning(
                    "OpenCV values are currently hard-coded for a 640x480 frame."
                )

    def scoreboard_processor(self, gray_frame, save=False):
        _clock_y1 = 92
        _clock_y2 = 100

        _digit1_x1 = 36
        _digit1_x2 = 41
        _digit2_x1 = 41
        _digit2_x2 = 46
        _digit3_x1 = 49
        _digit3_x2 = 54
        _digit4_x1 = 54
        _digit4_x2 = 59

        _score_y1 = 92
        _score_y2 = 101

        _score1_x1 = 117
        _score1_x2 = 123

        _score2_x1 = 128
        _score2_x2 = 134
        roi_game_clock_digit1 = gray_frame[_clock_y1:_clock_y2, _digit1_x1:_digit1_x2]

        roi_game_clock_digit2 = gray_frame[_clock_y1:_clock_y2, _digit2_x1:_digit2_x2]

        roi_game_clock_digit3 = gray_frame[_clock_y1:_clock_y2, _digit3_x1:_digit3_x2]
        roi_game_clock_digit4 = gray_frame[_clock_y1:_clock_y2, _digit4_x1:_digit4_x2]

        roi_game_score1_digit1 = gray_frame[_score_y1:_score_y2, _score1_x1:_score1_x2]
        roi_game_score2_digit1 = gray_frame[_score_y1:_score_y2, _score2_x1:_score2_x2]

        if save:
            filename = randomString() + ".png"

            cv2.imwrite(os.path.join(self.clock_image_path, filename), roi_game_clock_digit1)
            cv2.imwrite(os.path.join(self.clock_image_path, filename), roi_game_clock_digit2)
            cv2.imwrite(os.path.join(self.clock_image_path, filename), roi_game_clock_digit3)
            cv2.imwrite(os.path.join(self.clock_image_path, filename), roi_game_clock_digit4)

            cv2.imwrite(os.path.join(self.score_image_path, filename), roi_game_score1_digit1)
            cv2.imwrite(os.path.join(self.score_image_path, filename), roi_game_score2_digit1)

        cropped_imgbytes = cv2.imencode(".png", roi_game_clock_digit1)[1].tobytes()
        cropped_imgbytes2 = cv2.imencode(".png", roi_game_clock_digit2)[1].tobytes()
        cropped_imgbytes3 = cv2.imencode(".png", roi_game_clock_digit3)[1].tobytes()
        cropped_imgbytes4 = cv2.imencode(".png", roi_game_clock_digit4)[1].tobytes()
        cropped_imgbytes5 = cv2.imencode(".png", roi_game_score1_digit1)[1].tobytes()
        cropped_imgbytes6 = cv2.imencode(".png", roi_game_score2_digit1)[1].tobytes()

        self.window.Element("_output_frame_").Update(data=cropped_imgbytes)
        self.window.Element("_output_frame2_").Update(data=cropped_imgbytes2)
        self.window.Element("_output_frame3_").Update(data=cropped_imgbytes3)
        self.window.Element("_output_frame4_").Update(data=cropped_imgbytes4)
        self.window.Element("_output_frame5_").Update(data=cropped_imgbytes5)
        self.window.Element("_output_frame6_").Update(data=cropped_imgbytes6)

    def event_loop(self):
        while True:
            fps.update()

            _event, _values = self.window.Read(timeout=20, timeout_key="timeout")

            ok, frame = self.cap.read()


            if ok:

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                self.scoreboard_processor(gray_frame)

                self._event_checker(_event)

                #
                if self.gui_switch:
                    _, frame = self._values_checker(_values, frame)

                    TemplateMatcher(frame).find_all()

                    mins, secs = divmod(fps.elapsed, 60)
                    str_elapsed = '{:02d}:{:02d}'.format(mins, secs)
                    # draw_HUD_FPS(frame, fps.fps)
                    imgbytes = cv2.imencode(".png", frame)[1].tobytes()

                    _event, _values = self.window.Read(timeout=10, timeout_key="timeout")
                    self.window.Element("_video_frame_").Update(data=imgbytes)
                    self.window.Element("_elapsed_").Update(str_elapsed)
                    self.window.Element("_opencv_fps_").Update(fps.fps)
                    self.window.Element("imagetab_image").Update(data=imgbytes)


    def _event_checker(self, _event):
        if _event == "_EXIT_" or _event is None:
            self.close_all(self.window)
            sys.exit(0)

        if _event != "timeout":
            logger.debug(_event)

        for b in self._all_buttons:
            if _event == b["key"]:
                print(f"{b['name']} pressed!")
                self.window.FindElement(b["key"]).Update(data_base64=b["on_image"])
                # xcv.xcontroller.single_btn_press(btn["key"])

        # if not being pressed: reset the button image
        for b in self._all_buttons:
            if _event != b["key"]:
                self.window.FindElement(b["key"]).Update(data_base64=b["off_image"])

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



    def close_all(self, window):
        """Release the camera feed, close all OpenCV windows and close all pysimpleGUI windows"""
        fps.stop()
        logger.debug(f"fps: {fps.fps}  elapsed: {fps.elapsed}")
        self.cap.release()
        cv2.destroyAllWindows()
        window.Close()
        logger.debug("Nice! You closed the windows on exit.")


class GUILayout:

    def __init__(self):
        # Style settings
        self.FONT = "Helvetica 8"
        self.TEXT_COLOR = "#A6A4AF"
        self.BKG_COLOR = "#0a0a0f"
        self.GREEN = "#4e8827"
        self.YELLOW = "#a68c27"
        self.RED = "#7e2c2c"
        self.GREY = "#a6a6a6"
        self.GREY2 = "#2b2b2e"

        self.button_a = {
            "key": "_a_",
            "name": "A",
            "on_image": b64.BTN_A_ON,
            "off_image": b64.BTN_A_OFF,
        }
        self.button_b = {
            "key": "_b_",
            "name": "B",
            "on_image": b64.BTN_B_ON,
            "off_image": b64.BTN_B_OFF,
        }
        self.button_x = {
            "key": "_x_",
            "name": "X",
            "on_image": b64.BTN_X_ON,
            "off_image": b64.BTN_X_OFF,
        }
        self.button_y = {
            "key": "_y_",
            "name": "Y",
            "on_image": b64.BTN_Y_ON,
            "off_image": b64.BTN_Y_OFF,
        }
        self.button_start = {
            "key": "_start_",
            "name": "Start",
            "on_image": b64.START_ON,
            "off_image": b64.START_OFF,
        }
        self.button_select = {
            "key": "_select_",
            "name": "Select",
            "on_image": b64.SELECT_ON,
            "off_image": b64.SELECT_OFF,
        }
        self.button_lb = {
            "key": "_lb_",
            "name": "L Bumper",
            "on_image": b64.BTN_LB_ON,
            "off_image": b64.BTN_LB_OFF,
        }
        self.button_lt = {
            "key": "_lt_",
            "name": "L Trigger",
            "on_image": b64.BTN_LT_ON,
            "off_image": b64.BTN_LT_OFF,
        }
        self.button_rb = {
            "key": "_rb_",
            "name": "R Bumper",
            "on_image": b64.BTN_RB_ON,
            "off_image": b64.BTN_RB_OFF,
        }
        self.button_rt = {
            "key": "_rt_",
            "name": "R Trigger",
            "on_image": b64.BTN_RT_ON,
            "off_image": b64.BTN_RT_OFF,
        }
        self._all_buttons = [
            self.button_a,
            self.button_b,
            self.button_x,
            self.button_y,
            self.button_select,
            self.button_start,
            self.button_lb,
            self.button_lt,
            self.button_rb,
            self.button_rt
        ]



    def _layout_mainttab_row3_buttons(self):
        """
                Action Buttons - Example Display:

                    Y
                  X   B
                    A
                """
        _row3_xcontroller_action_buttons = [
            [
                sg.Image(
                    data_base64=self.button_y["off_image"],
                    key="_y_",
                    enable_events=True,
                    pad=(35, 0, 0, 0),
                )
            ],
            [
                sg.Image(
                    data_base64=self.button_x["off_image"],
                    key="_x_",
                    enable_events=True,
                    pad=(5, 0, 0, 0),
                ),
                sg.Image(
                    data_base64=self.button_b["off_image"],
                    key="_b_",
                    enable_events=True,
                    pad=(0, 0, 0, 0),
                ),
            ],
            [
                sg.Image(
                    data_base64=self.button_a["off_image"],
                    key="_a_",
                    enable_events=True,
                    pad=(35, 0, 0, 0),
                ),

            ],
        ]

        """
        DPad Buttons - Example Display: 

            ^
          <   >
            v
        """
        _row3_xcontroller_dpad = [
            [
                sg.Image(
                    data_base64=b64.DU_WHITE,
                    key="_du_",
                    enable_events=True,
                    pad=(80, 0, 0, 0),
                )
            ],
            [
                sg.Image(data_base64=b64.DL_WHITE, key="_dl_", enable_events=True, pad=(50, 0, 0, 0)),
                sg.Image(
                    data_base64=b64.DR_WHITE,
                    key="_dr_",
                    enable_events=True,
                    pad=(0, 0, 0, 0),
                ),
            ],
            [
                sg.Image(
                    data_base64=b64.DU_WHITE,
                    key="_left_stick_gif_",
                    enable_events=True,
                    pad=(80, 0, 0, 0),
                )
            ],
        ]

        _row3_xcontroller_other = [
            [
                sg.Image(data_base64=self.button_lt["off_image"], key="_lt_", enable_events=True),
                sg.Image(
                    data_base64=b64.XBOX_LOADING,
                    key="_xbox_",
                    enable_events=True,
                    pad=(16, 16, 0, 0),
                ),
                sg.Image(data_base64=self.button_rt["off_image"], key="_rt_", enable_events=True),
            ],
            [
                sg.Image(data_base64=self.button_lb["off_image"], key="_lb_", enable_events=True),
                sg.Image(data_base64=self.button_start["off_image"], key="_start_", enable_events=True),
                sg.Image(data_base64=self.button_select["off_image"], key="_select_", enable_events=True),
                sg.Image(data_base64=self.button_rb["off_image"], key="_rb_", enable_events=True),
            ],
            [
                sg.Image(data_base64=b64.JOYSTICK_GIF),
                sg.Text("LSX 188\nLSY 1289"),
                sg.Image(data_base64=b64.JOYSTICK_GIF),
                sg.Text("RSX 178\nRSY 179"),
            ]
        ]

        roi_column = [[sg.Text("Clock:"),
                      sg.Image(filename="", key="_output_frame_"),
                      sg.Image(filename="", key="_output_frame2_"),
                      sg.Image(filename="", key="_output_frame3_"),
                      sg.Image(filename="", key="_output_frame4_")],
                      [sg.Text("Score:"),
                      sg.Image(filename="", key="_output_frame5_"),
                      sg.Image(filename="", key="_output_frame6_"),
                      ]]

        return [
            sg.Column(roi_column),
            sg.Column(_row3_xcontroller_dpad),
            sg.Column(_row3_xcontroller_other),
            sg.Column(_row3_xcontroller_action_buttons),
        ]

    def _layout_maintab_row4_connection_status(self):
        """
        """
        return [
            sg.Image(data_base64=b64.GAMEPAD_GREY, key="_gamepad_connection_status_"),
            sg.Text(
                "No Connection",
                key="_gamepad_usb_port_",
                text_color=self.TEXT_COLOR,
                justification="left",
            ),
            sg.Image(data_base64=b64.FILM_GREY, key="_opencv_fps_icon_"),
            sg.Text("FPS:"),
            sg.Text("", key="_opencv_fps_", text_color=self.TEXT_COLOR),
            # sg.Image(data_base64=b64.FILM_YELLOW, key="_elapsed_icon_"),
            sg.Text("Elapsed:"),
            sg.Text("", key="_elapsed_"),
        ]

    def _output_console(selfs):
        return [
            sg.Output(size=(640, 50), background_color="#16161F", text_color="#A6A4AF")
        ]

    def _row0_video_frame(self):
        return [sg.Image(filename="", key="_video_frame_")]

    def _row2_game_stats(self):
        """ --------------------------------------------------------------------------
                Game Stats - Example Display:

                0 - 0  Home    Defending Left  BALL    Offensive - Shooting - InsideBox

                _tactic_ = Our AI's current gameplan/status
        """
        return [
            sg.Text("\n\t"),
            sg.Text("0 - 0", key="_score_", text_color=self.GREEN, font="Helvetica-Bold 16"),
            sg.Text("Home", key="_home_away_"),
            # sg.Text("Defending", key="_defending_side_", text_color=self.YELLOW),
            sg.Image(data_base64=b64.goal),
            sg.Text("", key="_possession_"),
            sg.Text("No Tactic", key="_tactic_"),
            sg.Text("\n"),
        ]

    def _row1_detected_state(self):
        return [
            sg.Text("\n"),
            sg.Text(
                "Unknown State",
                key="_detected_state_",
                font="Helvetica 16",
                justification="center",
            ),
            sg.Text("\n"),
        ]

    def _row5_gui_menu_buttons(self):
        return [
            sg.Text("\n"),
            sg.Image(
                data_base64=b64.CHECK_SERIAL_OFF,
                key="_check_serial_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=b64.SCREENSHOT_OFF,
                key="_save_screenshot_",
                enable_events=True,
            ),
            sg.Image(
                data_base64=b64.RECORD_OFF, key="_start_record_", enable_events=True
            ),
            sg.Image(data_base64=b64.EXIT_OFF, key="_EXIT_", enable_events=True),
            sg.Text("\n"),
        ]

    def _layout_maintab(self):

        # define the window layout
        _full_layout = [
            self._row0_video_frame(),
            self._row1_detected_state(),
            self._row2_game_stats(),
            self._layout_mainttab_row3_buttons(),
            self._layout_maintab_row4_connection_status(),
            self._output_console(),
            self._row5_gui_menu_buttons(),
        ]
        return _full_layout

    def _layout_imagetab(self):
        _imagetab_layout = [
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
        return _imagetab_layout

    def _layout_about_tab(self):
        return [
            [sg.Text("")],
            [sg.Image(data_base64=b64.BOO, pad=(240, 0))],
            [sg.Text(f"{xcv.__author__}\n", justification="center")],
            [sg.Text(f"{xcv.__email__}\n", justification="center")],
            [
                sg.Text(
                    f"XCV VERSION: {xcv.version.XCV_VERSION}\n", justification="center"
                )
            ],
            [
                sg.Text(
                    "\n\n\tSPECIAL THANKS TO\n",
                    font=("Helvetica", 16),
                    justification="left",
                )
            ],
            [sg.Text(f"\tIcons from: https://www.flaticon.com/authors/freepik \n")],
            [sg.Text(f"\thttps://github.com/PySimpleGUI/PySimpleGUI\n")],
            [sg.Text(f"\thttps://www.youtube.com/user/sentdexv\n")],
        ]

    def full_layout(self):
        return [
            [
                sg.TabGroup(
                    [
                        [
                            sg.Tab("Main", layout=self._layout_maintab()),
                            sg.Tab("Image Controls", layout=self._layout_imagetab()),
                            sg.Tab("About", layout=self._layout_about_tab()),
                        ]
                    ],
                    background_color=self.BKG_COLOR,
                    title_color=self.TEXT_COLOR,
                    selected_title_color=self.GREY2,
                    border_width=0,
                )
            ]
        ]


if __name__ == "__main__":
    video_capture = VideoCapture()
    # gui = GUI()
