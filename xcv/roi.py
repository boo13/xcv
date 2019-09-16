import numpy as np
# from collections import namedtuple

# ROI = namedtuple('ROI', 'x1 y1 x2 y2')

# home_team_score = ROI(x1=110, y1=101, x2=123, y2=92)


class ROI:

    def __init__(self, frame_w=640, frame_h=480):
        self.frame_w = frame_w
        self.frame_h = frame_h
        #
        self._letterbox()
        self._scoreboard_clock()
        self._scoreboard_score()

    def make(self, x1, y1, x2, y2):
        return np.array([[(x1, y1), (x2, y1), (x2, y2), (x1, y2)]])

    def _letterbox(self, is_letterboxed=True):
        if is_letterboxed:
            self.without_letterbox = self.make(0, 0, self.frame_w, 0)

    def _scoreboard_score(self):
        _score_y1 = 92
        _score_y2 = 101
        self.score_home = self.make(117, _score_y1, 123, _score_y2)
        self.score_away = self.make(128, _score_y1, 138, _score_y2)

    def _scoreboard_clock(self):
        _clock_y1 = 92
        _clock_y2 = 100
        self.clock_digit_hour = self.make(36, _clock_y1, 41, _clock_y2)
        self.clock_mins_tens = self.make(41, _clock_y1, 46, _clock_y2)
        self.clock_mins_ones = self.make(49, _clock_y1, 54, _clock_y2)

    def show_all(self):
        return

    def _WIP_stuff(self):
        # Hard-coded ROI values
        # ROI_SquadManage = np.array([[(0, 0), (640, 0), (640, 400), (0, 500)]])
        # ROI_SinglePlayerSeason_AreYouSure = np.array(
        #     [[(170, 232), (200, 232), (200, 272), (170, 272)]]
        # )
        # ROI_InGameMenu_Resume = np.array(
        #     [[(420, 172), (454, 172), (454, 206), (420, 206)]]
        # )
        # ROI_InGameMenu_Time = np.array(
        #     [[(305, 110), (335, 110), (335, 100), (305, 100)]]
        # )
        # ROI_btnStrip = np.array([[(610, 384), (30, 384), (30, 365), (610, 365)]])
        # ROI_AwayTeamScore = np.array(
        #     [[(126, 101), (138, 101), (138, 92), (126, 92)]]
        # )
        # ROI_HomeTeamScore = np.array(
        #     [[(110, 101), (123, 101), (123, 92), (110, 92)]]
        # )
        # ROI_HomeTeamName = np.array([[(80, 101), (108, 101), (108, 92), (80, 92)]])
        # ROI_AwayTeamName = np.array(
        #     [[(142, 101), (168, 101), (168, 92), (142, 92)]]
        # )
        # ROI_TeamBadgeLeft = np.array(
        #     [[(30, 400), (60, 400), (60, 375), (30, 375)]]
        # )
        # ROI_TeamBadgeRight = np.array(
        #     [[(610, 400), (580, 400), (580, 375), (610, 375)]]
        # )
        # ROI_halftimeMarker = np.array(
        #     [[(305, 110), (335, 110), (335, 100), (305, 100)]]
        # )
        # ROI_mainMenuCart = np.array(
        #     [[(560, 100), (580, 100), (580, 88), (560, 88)]]
        # )
        # ROI_Menu_StartGame_PlayMatch = np.array(
        #     [[(97, 337), (117, 337), (117, 357), (97, 357)]]
        # )
        # ROI_Menu_Squad = np.array([[(484, 81), (506, 81), (506, 94), (484, 94)]])
        return


roi = ROI()

