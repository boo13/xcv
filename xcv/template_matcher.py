import numpy as np
import cv2
from loguru import logger
from xcv.game import Game, Match
from xcv.stats import GameSession, FifaSession, FifaMatch
from xcv.video_stream import VideoStream
from xcv.roi import ROI

class TemplateMatcher:
    """Take in an OpenCV frame, process it, find templates a pop it out again.

        Parameters:
            template: template image we're going to search for
            ROI: region-of-interest to search for that template in
            cvFrame: the maluable computer vision frame
            ogFrame: the original frame, we use it to display information back to the user
            threshold (float): opencv param for template threshold (default=0.8)

        Options:
            func: a function to run if we do find that template (e.g. we are defending the left side of the screen)

        """

    def __init__(self, video_stream) -> None:
        self.threshold = 0.8
        self.state = 0
        self.template = None
        self.ROI = None
        self.if_is_found = None
        self.video_stream = video_stream
        self.frame = None

        # Where we store the detected values for the In-Game Clock
        self.game_clock_hour_ones = None
        self.game_clock_mins_tens = None
        self.game_clock_mins_ones = None
        self.game_clock_secs_tens = None
        self.game_clock_secs_ones = None

    def __repr__(self):
        return f"{self.__class__.__name__}(self.template), {self.ROI}, self.cvFrame, self.ogFrame, threshold={self.threshold}, state={self.state}, func={self.func})"

    def __str__(self):
        return f"""
                Matching `template` in `ROI` of `cvFrame`, beyond the chosen `threshold`: {self.threshold}.
                We ouput the visual information to `ogFrame`.
                
                If we found our template we use `state`({self.state})
                or `func`({self.func}) to set the appropriate `game_state` flags."""

    def useless_function(self, num):
        self.game_clock_secs_ones = num
        print(f"Found # {num}")

    def find_all(self, fifa_match, scoreboard):
        self.frame = self.video_stream.read()
        # self.find(cv2.imread("./templates/myTeamBadge.jpg", 0), self.ROI_TeamBadgeLeft, fifa_match.set_side_left)
        # self.find(cv2.imread("./templates/myTeamBadge.jpg", 0), self.ROI_TeamBadgeRight, fifa_match.set_side_right)
        # self.find(cv2.imread("./templates/myTeamScoreboardName.png", 0), self.ROI_AwayTeamName,
        #           fifa_match.set_away_team)
        # self.find(cv2.imread("./templates/myTeamScoreboardName.png", 0), self.ROI_HomeTeamName,
        #           fifa_match.set_home_team)
        # self.find(cv2.imread("./templates/SquadManage.png", 0), self.ROI_SquadManage, fifa_match.set_in_squad_menu)

        # for n in range(10):
        #     self.find(cv2.imread(f"./templates/clock/{n}.png", 0), self.roi_game_clock_digit1, scoreboard.found_digit,
        #               (n, 1))

    def find_pending_game(self, fifa_session, fifa_match):
        self.find(cv2.imread("./templates/SquadManage.png", 0), self.ROI_SquadManage, fifa_match.set_in_squad_menu)

    def find_scoreboard_team_badge(self, fifa_session, fifa_match):
        self.find(cv2.imread("./templates/myTeamBadge.jpg", 0), self.ROI_TeamBadgeLeft, fifa_match.set_side_left)
        self.find(cv2.imread("./templates/myTeamBadge.jpg", 0), self.ROI_TeamBadgeRight, fifa_match.set_side_right)

    def find(self, template, roi, if_is_found=None, value_if_found=None):

        if template is not None:
            # Get the template dimensions (used to draw the label)
            _tplateH, _tplateW = template.shape[:2]
        else:
            logger.debug("Missing template - pass in a numpy image")
            return self.frame

        if self.frame is not None:
            _find_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # Make a numpy array the same size as the cvFrame
            _mask = np.zeros_like(_find_frame)

            # Take the ROI and make that section white
            cv2.fillPoly(_mask, roi, 255)

            # Combine the mask and cvFrame to make a masked_image
            masked_image = cv2.bitwise_and(_find_frame, _mask)
        else:
            logger.debug("Missing cvFrame - pass in a numpy image")
            return

        # Use CV2's Template Matching to get our result
        res = cv2.matchTemplate(masked_image, template, cv2.TM_CCOEFF_NORMED)

        # Capture results over a defined threshold
        loc = np.where(res >= self.threshold)

        for pt in zip(*loc[::-1]):
            # Draw a red box around any matching template results
            # cv2.rectangle(
            #     self.frame,
            #     pt,
            #     (pt[0] + _tplateW, pt[1] + _tplateH),
            #     (0, 0, 0),
            #     -1,
            # )

            # If we have one - execute the function (typically sets a game_state_change).
            if if_is_found:
                if value_if_found is not None:
                    if_is_found(value_if_found)
                else:
                    if_is_found()

        return _find_frame
