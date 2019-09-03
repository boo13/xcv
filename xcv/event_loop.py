import sys
import cv2
from loguru import logger

from xcv.video_stream import VideoStream
from xcv.print_info import print_package_info
import xcv.base64_icons as b64
from xcv.fps import fps
from xcv.template_matcher import TemplateMatcher
from xcv.stats import GameSession, FifaSession, FifaMatch
from xcv.version import XCV_VERSION

from time import sleep


class EventLoopError(Exception):
    pass


class EventLoop:
    def __init__(self):
        self.game_session = GameSession()
        self.fifa_session = FifaSession(self.game_session)
        self.fifa_match = FifaMatch(self.fifa_session)
        self.frame = None
        self.show_menu = False
        self.show_gui_buttons = False
        self.show_output_console = False
        self.show_video = True
        self.show_about_info = False
        sleep(1)

    def event_loop(self, gui_window=None):
        vs = VideoStream(src=0).start()
        fps.start()

        while True:
            self.frame = vs.read()
            key = cv2.waitKey(1) & 0xFF
            fps.update()

            # self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            TemplateMatcher(self.frame).find_all(self.fifa_match)

            # # self.scoreboard_processor(gray_frame)

            # # self._event_checker(_event)
            if gui_window is not None:
                _event, _values = gui_window.Read(timeout=20, timeout_key="timeout")
                self._event_checker(_event, gui_window)
                self.gui_returns(gui_window)
        fps.stop()
        cv2.destroyAllWindows()
        vs.stop()

    def gui_returns(self, gui_window):

        mins, secs = divmod(fps.elapsed, 60)
        str_elapsed = "{:02d}:{:02d}".format(mins, secs)
        # draw_HUD_FPS(frame, fps.fps)

        imgbytes = cv2.imencode(".png", self.frame)[1].tobytes()

        gui_window.Element("_video_frame_").Update(data=imgbytes)
        gui_window.Element("_screen_side_").Update(self.fifa_match.show_screen_side())
        # gui_window.Element("_fifa_match_clock_").Update(self.fifa_match.clock())
        # gui_window.Element("_fifa_session_clock_").Update(self.fifa_session.clock())
        # gui_window.Element("_game_session_clock_").Update(self.game_session.clock())
        # gui_window.Element("_command_countdown_").Update(self.game_session.clock())

        gui_window.Element("_detected_state_").Update(
            self.fifa_session.display_status()
        )
        gui_window.Element("_home_away_").Update(self.fifa_match.show_home_or_away())
        # gui_window.Element("_elapsed_").Update(str_elapsed)
        gui_window.Element("_opencv_fps_").Update(fps.fps)
        gui_window.Element("_opencv_fps_").Update(visible=self.show_output_console)
        if fps.fps <= 6:
            gui_window.Element("_fps_icon_").Update(data_base64=b64.FILM_RED)
        elif 6 < fps.fps < 10:
            gui_window.Element("_fps_icon_").Update(data_base64=b64.FILM_YELLOW)
        else:
            gui_window.Element("_fps_icon_").Update(data_base64=b64.FILM_GREEN)

        # self.window.Element("imagetab_image").Update(data=imgbytes)

    def _event_checker(self, _event, gui_window):
        if _event == "_EXIT_" or _event is None:
            self.close_all(gui_window)
            sys.exit(0)

        if _event == "_menu_icon_":
            self.show_menu = not self.show_menu
            gui_window.Element("_info_icon_").Update(visible=self.show_menu)
            gui_window.Element("_cctv_").Update(visible=self.show_menu)
            gui_window.Element("_gamepad_connection_status_").Update(
                visible=self.show_menu
            )
            gui_window.Element("_trophy_icon_").Update(visible=self.show_menu)
            gui_window.Element("_pie_chart_icon_").Update(visible=self.show_menu)
            gui_window.Element("_EXIT_").Update(visible=self.show_menu)

        if _event == "_info_icon_":
            self.show_output_console = not self.show_output_console
            gui_window.Element("_output_console_").Update(
                visible=self.show_output_console
            )
            print_package_info()

        if _event == "_cctv_":
            self.show_video = not self.show_video
            gui_window.Element("_video_frame_").Update(visible=self.show_video)

            if self.show_video:
                gui_window.Element("_cctv_").Update(data_base64=b64.CCTV_ON)
            else:
                gui_window.Element("_cctv_").Update(data_base64=b64.CCTV_OFF)

        # Display the GUI controller buttons if we press the Game Controller Icon
        if _event == "_gamepad_connection_status_":
            self.show_gui_buttons = not self.show_gui_buttons
            gui_window.Element("_du_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_dd_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_dl_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_dr_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_a_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_b_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_x_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_y_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_start_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_select_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_xbox_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_lt_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_rt_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_lb_").Update(visible=self.show_gui_buttons)
            gui_window.Element("_rb_").Update(visible=self.show_gui_buttons)
            if self.show_gui_buttons:
                gui_window.Element("_gamepad_connection_status_").Update(
                    data_base64=b64.CONTROLLER_ON
                )
            else:
                gui_window.Element("_gamepad_connection_status_").Update(
                    data_base64=b64.CONTROLLER_OFF
                )

        if _event != "timeout":
            logger.debug(_event)

        # for b in self._all_buttons:
        #     if _event == b["key"]:
        #         print(f"{b['name']} pressed!")
        #         self.window.FindElement(b["key"]).Update(data_base64=b["on_image"])
        #         xcv.xcontroller.single_btn_press(btn["key"])

        # if not being pressed: reset the button image
        # for b in self._all_buttons:
        #     if _event != b["key"]:
        #         self.window.FindElement(b["key"]).Update(data_base64=b["off_image"])

    def _values_checker(self, _values, frame):
        return _values, frame

    def close_all(self, window):
        """Release the camera feed, close all OpenCV windows and close all pysimpleGUI windows"""
        fps.stop()
        logger.debug(f"fps: {fps.fps}  elapsed: {fps.elapsed}")
        # self.cap.release()
        cv2.destroyAllWindows()
        window.Close()
        logger.debug("Nice! You closed the windows on exit.")

