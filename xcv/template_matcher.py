import numpy as np
import cv2
from loguru import logger
from xcv.game import Game, Match
from xcv.stats import GameSession, FifaSession, FifaMatch
from xcv.video_stream import VideoStream


# class ROI:
#     def __init__(self, x1, y1, x2, y2):
#         return np.array([[(30, 400), (60, 400), (60, 375), (30, 375)]])

class TemplateMatcher:
    """Take in an OpenCV frame, process it, find templates a pop it out again.

        :param template: template image we're going to search for
        :param ROI: region-of-interest to search for that template in
        :param cvFrame: the maluable computer vision frame
        :param ogFrame: the original frame, we use it to display information back to the user
        :option func: a function to run if we do find that template (e.g. we are defending the left side of the screen)
        :param threshold (float): opencv param for template threshold
        :option state (int): an optional flag that will be switched if we found our template (a simplified version of `func`)
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

        # Clock
        self.clock_nums = [
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAOUlEQVQIHWMUtHI5t53RomF2+FLGSOeUYkbGWNuMfFbGeKusfBbGwNCM+tuMwjWi37sY+VkEPv8CAGXPD2mT02KCAAAAAElFTkSuQmCC',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAO0lEQVQIHQEwAM//AREGW83XAQ1zTpOzAREkTOGyART5d+CvARjyf9uvARf1etuxARH8buG5ART+C/z9zyEVqporuAUAAAAASUVORK5CYII=',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAO0lEQVQIHQEwAM//ARf9+gIEAQ8eVf6mARWN0wgYARcozjJjARj9BIi8ARb+fO+QAQ5hMnn4ASGY9O7piMYSfAip4t4AAAAASUVORK5CYII=',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAO0lEQVQIHQEwAM//ARFDPMa8AUNupF+WAR8O1pPFART4X1VnARb5E3XMAVEkmHXzASd5Af+IAQwJE+36pSUR9lJH9DoAAAAASUVORK5CYII=',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAOUlEQVQIHWMU/WkqsoNRkHHSugOMnK6huayMfJO2fbzI6BtT213GWOL7yHwmozg/Z0k3owjLb97PAIBCEDJBbsgFAAAAAElFTkSuQmCC',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAOUlEQVQIHWNUjuVi2cRoVLqC/SqjXs629+cYDZuO2U5kFGF9lSHCaOE2pfQNo3iN0J8ORj5Wwc8/AIPbEPJEsQY/AAAAAElFTkSuQmCC',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAOUlEQVQIHWMU/+z24zSjANfkrgeMnPHKDRyM0ovePZjKGBhVXniVMTgwq/IFo3i1yK82Rj5WoY8/AbngEnJZg+6XAAAAAElFTkSuQmCC',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAOUlEQVQIHWM0C/v37zRjTNSUuMuMqpIXFrYxCjOYR6czSn5rO7OBUVS8I+8bI0+IWqsAoxD377/MAMNREXTtZknXAAAAAElFTkSuQmCC',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAOUlEQVQIHWMUtLM/t5vRvnJ2xArGkIDk+meMsjPeKmUyBgW3pt9mTLAryGNlVC7l/dfJKMQg/PEHAJ7XETPQ/VwfAAAAAElFTkSuQmCC',
            b'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAAAAAAUmmrnAAAAOUlEQVQIHWMUtHE7t5XRtnJeyBrGKMfUAi5G7dZrNq2MQsKxmqmM4t/7t+5nFNOKrWRiFGNm/sEGAHQaDodzWupNAAAAAElFTkSuQmCC',
        ]

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
        # _score2_x2 = 134

        self.roi_game_clock_digit1 = np.array(
            [[(_digit1_x1, _clock_y1), (_digit1_x2, _clock_y1), (_digit1_x2, _clock_y2), (_digit1_x1, _clock_y2)]])
        self.roi_game_clock_digit2 = np.array(
            [[(_digit2_x1, _clock_y1), (_digit2_x2, _clock_y1), (_digit2_x2, _clock_y2), (_digit2_x1, _clock_y2)]])
        self.roi_game_clock_digit3 = np.array(
            [[(_digit3_x1, _clock_y1), (_digit3_x2, _clock_y1), (_digit3_x2, _clock_y2), (_digit3_x1, _clock_y2)]])
        self.roi_game_clock_digit4 = np.array(
            [[(_digit4_x1, _clock_y1), (_digit4_x2, _clock_y1), (_digit4_x2, _clock_y2), (_digit4_x1, _clock_y2)]])

        # roi_game_score1_digit1 = gray_frame[_score_y1:_score_y2, _score1_x1:_score1_x2]
        # roi_game_score2_digit1 = gray_frame[_score_y1:_score_y2, _score2_x1:_score2_x2]
        # Hard-coded ROI values
        self.ROI_SquadManage = np.array([[(0, 0), (640, 0), (640, 400), (0, 500)]])
        self.ROI_SinglePlayerSeason_AreYouSure = np.array(
            [[(170, 232), (200, 232), (200, 272), (170, 272)]]
        )
        self.ROI_InGameMenu_Resume = np.array(
            [[(420, 172), (454, 172), (454, 206), (420, 206)]]
        )
        self.ROI_InGameMenu_Time = np.array(
            [[(305, 110), (335, 110), (335, 100), (305, 100)]]
        )
        self.ROI_btnStrip = np.array([[(610, 384), (30, 384), (30, 365), (610, 365)]])
        self.ROI_AwayTeamScore = np.array(
            [[(126, 101), (138, 101), (138, 92), (126, 92)]]
        )
        self.ROI_HomeTeamScore = np.array(
            [[(110, 101), (123, 101), (123, 92), (110, 92)]]
        )
        self.ROI_HomeTeamName = np.array([[(80, 101), (108, 101), (108, 92), (80, 92)]])
        self.ROI_AwayTeamName = np.array(
            [[(142, 101), (168, 101), (168, 92), (142, 92)]]
        )
        self.ROI_TeamBadgeLeft = np.array(
            [[(30, 400), (60, 400), (60, 375), (30, 375)]]
        )
        self.ROI_TeamBadgeRight = np.array(
            [[(610, 400), (580, 400), (580, 375), (610, 375)]]
        )
        self.ROI_halftimeMarker = np.array(
            [[(305, 110), (335, 110), (335, 100), (305, 100)]]
        )
        self.ROI_mainMenuCart = np.array(
            [[(560, 100), (580, 100), (580, 88), (560, 88)]]
        )
        self.ROI_Menu_StartGame_PlayMatch = np.array(
            [[(97, 337), (117, 337), (117, 357), (97, 357)]]
        )
        self.ROI_Menu_Squad = np.array([[(484, 81), (506, 81), (506, 94), (484, 94)]])

        self.clock = np.array([[(484, 81), (506, 81), (506, 94), (484, 94)]])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.template}), {self.ROI}, {self.cvFrame}, {self.ogFrame}, threshold={self.threshold}, state={self.state}, func={self.func})"

    def __str__(self):
        return f"""
                Matching `template` in `ROI` of `cvFrame`, beyond the chosen `threshold`: {self.threshold}.
                We ouput the visual information to `ogFrame`.
                If we found our template we use `state`({self.state}) or `func`({self.func}) to set the appropriate `game_state` flags."""

    def useless_function(self, num):
        self.game_clock_secs_ones = num
        print(f"Found # {num}")

    def find_all(self, fifa_match, scoreboard):
        self.frame = self.video_stream.read()
        self.find(cv2.imread("./templates/myTeamBadge.jpg", 0), self.ROI_TeamBadgeLeft, fifa_match.set_side_left)
        self.find(cv2.imread("./templates/myTeamBadge.jpg", 0), self.ROI_TeamBadgeRight, fifa_match.set_side_right)
        self.find(cv2.imread("./templates/myTeamScoreboardName.png", 0), self.ROI_AwayTeamName,
                  fifa_match.set_away_team)
        self.find(cv2.imread("./templates/myTeamScoreboardName.png", 0), self.ROI_HomeTeamName,
                  fifa_match.set_home_team)
        self.find(cv2.imread("./templates/SquadManage.png", 0), self.ROI_SquadManage, fifa_match.set_in_squad_menu)

        for n in range(10):
            self.find(cv2.imread(f"./templates/clock/{n}.png", 0), self.roi_game_clock_digit1, scoreboard.found_digit,
                      (n, 1))

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
