import numpy as np
from dataclasses import dataclass
import cv2

from loguru import logger


class CVManager:
    # self.original_frame = original_frame

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def _read_captured_frame(self):
        _ok, self.original_frame = self.cap.read()

        if _ok:
            print("yay we're ok")
            cv2.imshow("Original", self.original_frame))


class TemplateMatcher(CVManager):
    """Take in an OpenCV frame, process it, find templates a pop it out again.

        :param template: template image we're going to search for
        :param ROI: region-of-interest to search for that template in
        :param cvFrame: the maluable computer vision frame
        :param ogFrame: the original frame, we use it to display information back to the user
        :option func: a function to run if we do find that template (e.g. we are defending the left side of the screen)
        :param threshold (float): opencv param for template threshold
        :option state (int): an optional flag that will be switched if we found our template (a simplified version of `func`)
        """

    def __init__(self) -> None:
        self.threshold=0.8
        self.state=0
        self.template=None
        self.ROI=None
        self.if_is_found=None

        # Hard-coded ROI values
        self.ROI_SquadManage=np.array(
            [[(0, 0), (640, 0), (640, 400), (0, 500)]])
        self.ROI_SinglePlayerSeason_AreYouSure=np.array(
            [[(170, 232), (200, 232), (200, 272), (170, 272)]]
        )
        self.ROI_InGameMenu_Resume=np.array(
            [[(420, 172), (454, 172), (454, 206), (420, 206)]])
        self.ROI_InGameMenu_Time=np.array(
            [[(305, 110), (335, 110), (335, 100), (305, 100)]])
        self.ROI_btnStrip=np.array(
            [[(610, 384), (30, 384), (30, 365), (610, 365)]])
        self.ROI_AwayTeamScore=np.array(
            [[(126, 101), (138, 101), (138, 92), (126, 92)]])
        self.ROI_HomeTeamScore=np.array(
            [[(110, 101), (123, 101), (123, 92), (110, 92)]])
        self.ROI_HomeTeamName=np.array(
            [[(80, 101), (108, 101), (108, 92), (80, 92)]])
        self.ROI_AwayTeamName=np.array(
            [[(142, 101), (168, 101), (168, 92), (142, 92)]])
        self.ROI_TeamBadgeLeft=np.array(
            [[(30, 400), (60, 400), (60, 375), (30, 375)]])
        self.ROI_TeamBadgeRight=np.array(
            [[(610, 400), (580, 400), (580, 375), (610, 375)]])
        self.ROI_halftimeMarker=np.array(
            [[(305, 110), (335, 110), (335, 100), (305, 100)]])
        self.ROI_mainMenuCart=np.array(
            [[(560, 100), (580, 100), (580, 88), (560, 88)]])
        self.ROI_Menu_StartGame_PlayMatch=np.array(
            [[(97, 337), (117, 337), (117, 357), (97, 357)]]
        )
        self.ROI_Menu_Squad=np.array(
            [[(484, 81), (506, 81), (506, 94), (484, 94)]])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.template}), {self.ROI}, {self.cvFrame}, {self.ogFrame}, threshold={self.threshold}, state={self.state}, func={self.func})"

    def __str__(self):
        return f"""
                Matching `template` in `ROI` of `cvFrame`, beyond the chosen `threshold`: {self.threshold}.
                We ouput the visual information to `ogFrame`.
                If we found our template we use `state`({self.state}) or `func`({self.func}) to set the appropriate `game_state` flags."""

    def find(self):

        if self.template is not None:
            # Get the template dimensions (used to draw the label)
            _tplateH, _tplateW=self.template.shape[:2]
        else:
            logger.debug("Missing template - pass in a numpy image")
            return self.original_frame

        if self.original_frame is not None:
            _find_frame=cv2.cvtColor(self.original_frame, cv2.COLOR_BGR2GRAY)

            # Make a numpy array the same size as the cvFrame
            _mask=np.zeros_like(_find_frame)

            # Take the ROI and make that section white
            cv2.fillPoly(_mask, self.ROI, 255)

            # Combine the mask and cvFrame to make a masked_image
            masked_image=cv2.bitwise_and(_find_frame, _mask)
        else:
            logger.debug("Missing cvFrame - pass in a numpy image")
            return _find_frame

        # Use CV2's Template Matching to get our result
        res=cv2.matchTemplate(
            masked_image, self.template, cv2.TM_CCOEFF_NORMED)

        # Capture results over a defined threshold
        loc=np.where(res >= self.threshold)

        for pt in zip(*loc[::-1]):
            # Draw a red box around any matching template results
            cv2.rectangle(
                self.original_frame, pt, (pt[0] + _tplateW, pt[1] +
                                          _tplateH), (0, 0, 255), 2
            )

            # If we have one - execute the function (typically sets a game_state_change).
            if self.is_found:
                self.is_found()

        return _find_frame

    def _find_which_side_are_we_defending(self):
        self.ROI=self.ROI_TeamBadgeLeft

    def _find_are_we_home_or_away(self):
        return

    def _determine_the_game_score(self):
        return


if __name__ == "__main__":

    # if ok:
    #

    #     # #################################################
    #     #   Quit                     Keyboard key 'q' quits
    #     # #################################################
    #     key = cv2.waitKey(1) & 0xFF
    #     if key == ord("q"):
    #         cap.release()
    #         cv2.destroyAllWindows()
    #         exit()

    t=TemplateMatcher(
        cv2.imread("./templates/Menu/InGameMenu_ResumeMatch_On.png", 0),
        ROI.InGameMenu_Resume,
        cv_frame,
        og_frame,
        func = None,
        state = 14,
    )
    print(repr(t))
