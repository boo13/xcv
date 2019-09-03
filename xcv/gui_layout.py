import xcv
import xcv.base64_icons as b64
from xcv.version import XCV_VERSION
from xcv.stats import (
    GameSession,
    FifaSession,
    FifaMatch,
    FifaPlayer,
    Scoreboard,
    WinLossRecord,
)
import PySimpleGUIQt as sg


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

    def _output_console(self):
        return [
            sg.Output(size=(640, 100), background_color="#16161F", text_color="#A6A4AF", key="_output_console_",
                      visible=False),
        ]

    def _top_status(self):
        _gui_display_info = [

            [
                sg.Text("", key="_home_away_"),
            ],
            [
                sg.Text("", key="_screen_side_")
            ],
            # [
            #     sg.Text("Elapsed: "),
            #     sg.Text("", key="_game_session_clock_")
            # ],
            # [
            #     sg.Text("FIFA Sess: "),
            #     sg.Text("", key="_fifa_session_clock_")
            # ],
            # [
            #     sg.Text("Match: "),
            #     sg.Text("", key="_fifa_match_clock_")
            # ],
            # [
            #     sg.Text("Countdown: "),
            #     sg.Text("", key="_command_countdown_")
            # ],
            # [
            #     sg.Text("", key="_elapsed_", pad=(0, 0), tooltip="Elapsed"),
            # ],
            # [
            #     sg.Text("Clock:"),
            #     sg.Image(filename="", key="_output_frame_"),
            #     sg.Image(filename="", key="_output_frame2_"),
            #     sg.Image(filename="", key="_output_frame3_"),
            #     sg.Image(filename="", key="_output_frame4_"),
            # ],
            # [
            #     sg.Text("Score:"),
            #     sg.Image(filename="", key="_output_frame5_"),
            #     sg.Image(filename="", key="_output_frame6_"),
            # ],
        ]

        _serial_connection_info = [[sg.Text(
                "No Connection",
                key="_gamepad_usb_port_",
                pad=(0, 0),
                text_color=self.TEXT_COLOR,
                justification="left",
            )]]

        return [sg.Column([[sg.Image(data_base64=b64.FILM_GREY, key="_fps_icon_", tooltip="FPS")],
                     [sg.Text("", key="_opencv_fps_", visible=False, justification="left", tooltip="FPS")]]),
                sg.Column(_serial_connection_info),
                sg.Column(_gui_display_info),
                ]

    def _video_frame(self):
        return [sg.Image(filename="", key="_video_frame_")]

    def _detected_state(self):
        return [sg.Text("",
                key="_detected_state_",
                pad=(0, 50),
                font="Helvetica 16",
                justification="center",)
                ]

    def _vert_spacer(self):
        return [sg.Image(data_base64=b64.VERT_SPACER)]

    def _gui_work_area(self):
        _gui_menu = [
                     [sg.Image(data_base64=b64.MENU, key="_menu_icon_", tooltip="Show/Hide Menu", visible=True,
                               pad=((0, 5), 2), enable_events=True)],
                     [sg.Image(data_base64=b64.INFO, key="_info_icon_", visible=False, pad=((0, 5), 2),
                               tooltip="XCV Info", enable_events=True)],
                     [sg.Image(data_base64=b64.CCTV_ON, key="_cctv_", visible=False, pad=((0, 5), 2),
                               enable_events=True, tooltip="Show/Hide Video")],
                     [sg.Image(data_base64=b64.CONTROLLER_GREY, key="_gamepad_connection_status_", visible=False,
                               pad=((0, 5), 2), enable_events=True, tooltip="Controller IO")],
                     [sg.Image(data_base64=b64.TROPHY, key="_trophy_icon_", visible=False, pad=((0, 5), 2),
                               enable_events=True, tooltip="Game Stats")],
                     [sg.Image(data_base64=b64.PIE_CHART, key="_pie_chart_icon_", visible=False, pad=((0, 5), 2),
                               enable_events=True, tooltip="Data Analysis (Long-Term)")],
                     [sg.Image(data_base64=b64.EXIT, key="_EXIT_", visible=False, pad=(0, 0), enable_events=True,
                         tooltip="Close XCV")]
                     ]


        _xcontroller_action_buttons = [
            [
                sg.Image(
                    data_base64=self.button_y["off_image"],
                    key="_y_",
                    enable_events=True,
                    pad=(35, 0, 0, 0),
                    visible=False,
                )
            ],
            [
                sg.Image(
                    data_base64=self.button_x["off_image"],
                    key="_x_",
                    enable_events=True,
                    pad=(5, 0, 0, 0),
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_b["off_image"],
                    key="_b_",
                    enable_events=True,
                    pad=(0, 0, 0, 0),
                    visible=False,
                ),
            ],
            [
                sg.Image(
                    data_base64=self.button_a["off_image"],
                    key="_a_",
                    enable_events=True,
                    pad=(35, 0, 0, 0),
                    visible=False,
                )
            ],
        ]

        _xcontroller_dpad = [
            [
                sg.Image(
                    data_base64=b64.DU_WHITE,
                    key="_du_",
                    enable_events=True,
                    pad=(80, 0, 0, 0),
                    visible=False,
                )
            ],
            [
                sg.Image(
                    data_base64=b64.DL_WHITE,
                    key="_dl_",
                    enable_events=True,
                    pad=(50, 0, 0, 0),
                    visible=False,
                ),
                sg.Image(
                    data_base64=b64.DR_WHITE,
                    key="_dr_",
                    enable_events=True,
                    pad=(0, 0, 0, 0),
                    visible=False,
                ),
            ],
            [
                sg.Image(
                    data_base64=b64.DU_WHITE,
                    key="_dd_",
                    enable_events=True,
                    pad=(80, 0, 0, 0),
                    visible=False,
                )
            ],
        ]

        _xcontroller_other = [
            [
                sg.Image(
                    data_base64=self.button_lt["off_image"],
                    key="_lt_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=b64.XBOX_LOADING,
                    key="_xbox_",
                    enable_events=True,
                    pad=(16, 16, 0, 0),
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_rt["off_image"],
                    key="_rt_",
                    enable_events=True,
                    visible=False,
                ),
            ],
            [
                sg.Image(
                    data_base64=self.button_lb["off_image"],
                    key="_lb_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_start["off_image"],
                    key="_start_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_select["off_image"],
                    key="_select_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_rb["off_image"],
                    key="_rb_",
                    enable_events=True,
                    visible=False,
                ),
            ],
        ]

        return [sg.Column(_gui_menu),
                # sg.Column(_gui_display_info),
                sg.Column(_xcontroller_dpad),
                sg.Column(_xcontroller_other),
                sg.Column(_xcontroller_action_buttons),
                ]

    def _layout(self):
        # define the window layout
        _full_layout = [
            self._top_status(),
            self._vert_spacer(),
            self._video_frame(),
            self._vert_spacer(),
            self._detected_state(),
            self._vert_spacer(),
            self._gui_work_area(),
            self._output_console(),
            self._vert_spacer(),
        ]
        return _full_layout

    def full_layout(self):
        return self._layout()
