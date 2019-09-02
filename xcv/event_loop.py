import sys
import cv2
from loguru import logger

from xcv.fps import fps
from xcv.template_matcher import TemplateMatcher


class EventLoopError(Exception):
    pass


class EventLoop:
    def event_loop(self, cap, gui_window=None):

        self.cap = cap

        while True:
            fps.update()
            ok, self.frame = self.cap.read()

            if not ok:
                raise EventLoopError("No Video Frame found")

            self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # self.scoreboard_processor(gray_frame)

            # self._event_checker(_event)
            if gui_window is not None:
                _event, _values = gui_window.Read(timeout=20, timeout_key="timeout")
                self._event_checker(_event, gui_window)
                self.gui_returns(gui_window)

    def gui_returns(self, gui_window):
        TemplateMatcher(self.frame).find_all()

        mins, secs = divmod(fps.elapsed, 60)
        str_elapsed = "{:02d}:{:02d}".format(mins, secs)
        # draw_HUD_FPS(frame, fps.fps)

        imgbytes = cv2.imencode(".png", self.frame)[1].tobytes()

        gui_window.Element("_video_frame_").Update(data=imgbytes)
        gui_window.Element("_elapsed_").Update(str_elapsed)
        gui_window.Element("_opencv_fps_").Update(fps.fps)
        # self.window.Element("imagetab_image").Update(data=imgbytes)

    def _event_checker(self, _event, gui_window):
        if _event == "_EXIT_" or _event is None:
            self.close_all(gui_window)
            sys.exit(0)

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
        self.cap.release()
        cv2.destroyAllWindows()
        window.Close()
        logger.debug("Nice! You closed the windows on exit.")

