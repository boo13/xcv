import sys
import cv2
from loguru import logger

from xcv.video_stream import VideoStream
from xcv.print_info import print_package_info
import xcv.base64_icons as b64
from xcv.fps import fps
from xcv.template_matcher import TemplateMatcher
from xcv.stats import GameSession, FifaSession, FifaMatch, Scoreboard

from time import sleep

class EventLoopError(Exception):
    pass

class GuiButtonEventChecker:
    def __init__(self):
        pass

    def make(self):
        return

class GuiFindAndUpdate:
    pass

class EventLoop:
    """Take video frames from xcv.VideoStream, initiate opencv processing, then send resulting commands to xcv.Controller.


    If the GUI is enabled, we also display it and handle those button command, speficially, updating the current data to the GUI.

    Arguments:
            gui_window  --  PySimpleGUI window object (optional)


    FIXME: Clock processing and resulting FPS problem
    TODO: Add video source switching to streamlink
    """

    def __init__(self):
        # Create instances of the game sessions
        self.game_session = GameSession()
        self.fifa_session = FifaSession(self.game_session)
        self.fifa_match = FifaMatch(self.fifa_session)
        self.scoreboard = Scoreboard(self.fifa_match)
        
        # Initialize main frame var
        self.frame = None

        # Initialize default GUI values (all false, except show_video and use_cv)
        self.use_cv = True
        self.show_video = True
        self.show_menu = False
        self.show_game_stats = False
        self.show_gui_buttons = False
        self.show_output_console = False
        self.show_about_info = False
        
        # Give the camera et al time to warm up
        fps.start()
        sleep(1)
        self.vs = VideoStream().start()
        sleep(1)

    def event_loop(self, gui_window=None):

        while True:
            self.frame = self.vs.read()
            # key = cv2.waitKey(1) & 0xFF
            fps.update()

            if self.use_cv:
                TemplateMatcher(self.vs).find_all(self.fifa_match, self.scoreboard)

            # # self._event_checker(_event)
            if gui_window is not None:
                _event, _values = gui_window.Read(timeout=20, timeout_key="timeout")
                self._event_checker(_event, gui_window)
                self._update_gui(gui_window)
        fps.stop()
        cv2.destroyAllWindows()
        vs.stop()

    def _update_gui(self, gui_window):

        mins, secs = divmod(fps.elapsed, 60)
        str_elapsed = "{:02d}:{:02d}".format(mins, secs)
        # draw_HUD_FPS(frame, fps.fps)

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
        self._update_fps_icon(gui_window)

    def _update_fps_icon(self, gui_window):
        if fps.fps > 19:
            gui_window.Element("_fps_icon_").Update(data_base64=b64.FILM_NULL)
        elif fps.fps > 15:
            gui_window.Element("_fps_icon_").Update(data_base64=b64.FILM_GREEN)
        elif fps.fps > 7:
            gui_window.Element("_fps_icon_").Update(data_base64=b64.FILM_YELLOW)
        else:
            gui_window.Element("_fps_icon_").Update(data_base64=b64.FILM_RED)

    def _event_checker(self, _event, gui_window):
        if _event == "_EXIT_" or _event is None:
            self.close_all(gui_window)
            sys.exit(0)

        if self.show_video:
            gui_window.Element("_cctv_").Update(data_base64=b64.CCTV_ON)
            imgbytes = cv2.imencode(".png", self.frame)[1].tobytes()
            # imgbytes = cv2.imencode(".png", UnthreadedVideoStream()
            #                         )[1].tobytes()
            gui_window.Element("_video_frame_").Update(data=imgbytes)
        else:
            gui_window.Element("_cctv_").Update(data_base64=b64.CCTV_OFF)

        if _event == "_use_cv_":
            self.use_cv = not self.use_cv
            if self.use_cv:
                gui_window.Element("_use_cv_").Update(data_base64=b64.POWER_ON)
            else:
                gui_window.Element("_use_cv_").Update(data_base64=b64.POWER_OFF)

        if _event == "_trophy_icon_":
            self.show_game_stats = not self.show_game_stats
            if self.show_game_stats:
                gui_window.Element("_use_cv_").Update(data_base64=b64.TROPHY_ON)
            else:
                gui_window.Element("_use_cv_").Update(data_base64=b64.TROPHY_OFF)

        if _event == "_menu_icon_":
            self.show_menu = not self.show_menu
            if self.show_menu:
                gui_window.Element("_menu_icon_").Update(data_base64=b64.MENU_ON)
            else:
                gui_window.Element("_menu_icon_").Update(data_base64=b64.MENU_OFF)

            gui_window.Element("_info_icon_").Update(visible=self.show_menu)
            gui_window.Element("_cctv_").Update(visible=self.show_menu)
            gui_window.Element("_gamepad_connection_status_").Update(
                visible=self.show_menu
            )
            gui_window.Element("_trophy_icon_").Update(visible=self.show_menu)
            gui_window.Element("_use_cv_").Update(visible=self.show_menu)
            gui_window.Element("_pie_chart_icon_").Update(visible=self.show_menu)
            gui_window.Element("_EXIT_").Update(visible=self.show_menu)

        if _event == "_info_icon_":
            self.show_output_console = not self.show_output_console

            if self.show_output_console:
                gui_window.Element("_info_icon_").Update(data_base64=b64.INFO_ON)
            else:
                gui_window.Element("_info_icon_").Update(data_base64=b64.INFO_OFF)

            gui_window.Element("_output_console_").Update(
                visible=self.show_output_console
            )
            print_package_info()

        if _event == "_cctv_":
            self.show_video = not self.show_video
            gui_window.Element("_video_frame_").Update(visible=self.show_video)

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
        """Release the camera feed, close all OpenCV windows and close all pysimpleGUI windows."""
        fps.stop()
        logger.debug(f"fps: {fps.fps}  elapsed: {fps.elapsed}")
        # self.cap.release()
        cv2.destroyAllWindows()
        window.Close()
        logger.debug("Nice! You closed the windows on exit.")
