import xcv
import xcv.base64_icons as b64
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
                )
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
                sg.Image(
                    data_base64=b64.DL_WHITE,
                    key="_dl_",
                    enable_events=True,
                    pad=(50, 0, 0, 0),
                ),
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
                sg.Image(
                    data_base64=self.button_lt["off_image"],
                    key="_lt_",
                    enable_events=True,
                ),
                sg.Image(
                    data_base64=b64.XBOX_LOADING,
                    key="_xbox_",
                    enable_events=True,
                    pad=(16, 16, 0, 0),
                ),
                sg.Image(
                    data_base64=self.button_rt["off_image"],
                    key="_rt_",
                    enable_events=True,
                ),
            ],
            [
                sg.Image(
                    data_base64=self.button_lb["off_image"],
                    key="_lb_",
                    enable_events=True,
                ),
                sg.Image(
                    data_base64=self.button_start["off_image"],
                    key="_start_",
                    enable_events=True,
                ),
                sg.Image(
                    data_base64=self.button_select["off_image"],
                    key="_select_",
                    enable_events=True,
                ),
                sg.Image(
                    data_base64=self.button_rb["off_image"],
                    key="_rb_",
                    enable_events=True,
                ),
            ],
            [
                sg.Image(data_base64=b64.JOYSTICK_GIF),
                sg.Text("LSX 188\nLSY 1289"),
                sg.Image(data_base64=b64.JOYSTICK_GIF),
                sg.Text("RSX 178\nRSY 179"),
            ],
        ]

        roi_column = [
            [
                sg.Text("Clock:"),
                sg.Image(filename="", key="_output_frame_"),
                sg.Image(filename="", key="_output_frame2_"),
                sg.Image(filename="", key="_output_frame3_"),
                sg.Image(filename="", key="_output_frame4_"),
            ],
            [
                sg.Text("Score:"),
                sg.Image(filename="", key="_output_frame5_"),
                sg.Image(filename="", key="_output_frame6_"),
            ],
        ]

        return [
            sg.Column(roi_column),
            sg.Column(_row3_xcontroller_dpad),
            sg.Column(_row3_xcontroller_other),
            sg.Column(_row3_xcontroller_action_buttons),
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
            sg.Text(
                f"{Scoreboard.home_score} - {Scoreboard.away_score}",
                key="_score_",
                text_color=self.GREEN,
                font="Helvetica-Bold 16",
            ),
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

