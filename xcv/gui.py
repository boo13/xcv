# TODO: Implement switch for `cap = cv2.VideoCapture(0)` and `streamlink` stream from twitch, mixer, etc.
import os
import sys
import random
import string
from pathlib import Path

# _________________ Local
import xcv
from xcv.template_matcher import TemplateMatcher
import xcv.xcontroller
from xcv.fps import fps
import xcv.base64_icons as b64
from xcv.version import XCV_VERSION
from xcv.hud import draw_HUD_FPS
from xcv.stats import GameSession, FifaSession, FifaMatch
from xcv.event_loop import EventLoop
from xcv.gui_layout import GUILayout

# _________________ `pip install` _________________
import PySimpleGUIQt as sg
import cv2
import numpy as np
from loguru import logger


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


@logger.catch()
class VideoCapture:
    def __init__(self, gui=True):
        self.game_session = GameSession()

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
            self.button_rt,
        ]

        if gui:
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

            _gui_layout = GUILayout()

            self.window = sg.Window(
                f"XCV - {XCV_VERSION}",
                layout=_gui_layout.full_layout(),
                location=(600, 200),
                icon=b64.Microsoft_Xbox_Emoji_Icon,
                border_depth=0,
            )

        self.cap = cv2.VideoCapture(0)
        self.game_session.check_video_source_size(self.cap)
        fps.start()
        _loop = EventLoop(self.cap)
        _loop.event_loop(gui_window=self.window)

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
            filename = random_string() + ".png"

            cv2.imwrite(
                os.path.join(self.clock_image_path, filename), roi_game_clock_digit1
            )
            cv2.imwrite(
                os.path.join(self.clock_image_path, filename), roi_game_clock_digit2
            )
            cv2.imwrite(
                os.path.join(self.clock_image_path, filename), roi_game_clock_digit3
            )
            cv2.imwrite(
                os.path.join(self.clock_image_path, filename), roi_game_clock_digit4
            )

            cv2.imwrite(
                os.path.join(self.score_image_path, filename), roi_game_score1_digit1
            )
            cv2.imwrite(
                os.path.join(self.score_image_path, filename), roi_game_score2_digit1
            )

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


if __name__ == "__main__":
    video_capture = VideoCapture()
