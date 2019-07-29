from dataclasses import dataclass
import numpy as np
import cv2
from FifaFlags import FifaFlags, defending, homeaway
from HUD import HUD

@dataclass
class ROI:
    SquadManage = np.array([[
        (0, 0), (640, 0),
        (640, 400), (0, 500)
    ]])

    SinglePlayerSeason_AreYouSure = np.array([[
        (170, 232), (200, 232),
        (200, 272), (170, 272)
    ]])

    InGameMenu_Resume = np.array([[
        (420, 172), (454, 172),
        (454, 206), (420, 206)
    ]])

    InGameMenu_Time = np.array([[
        (305, 110), (335, 110),
        (335, 100), (305, 100)
    ]])

    btnStrip = np.array([[
        (610, 384), (30, 384),
        (30, 365), (610, 365)
    ]])

    AwayTeamScore = np.array([[
        (126, 101), (138, 101),
        (138, 92), (126, 92)
    ]])

    HomeTeamScore = np.array([[
        (110, 101), (123, 101),
        (123, 92), (110, 92)
    ]])

    HomeTeamName = np.array([[
        (80, 101), (108, 101),
        (108, 92), (80, 92)
    ]])

    AwayTeamName = np.array([[
        (142, 101), (168, 101),
        (168, 92), (142, 92)
    ]])

    TeamBadgeLeft = np.array([[
        (30, 400), (60, 400),
        (60, 375), (30, 375)
    ]])

    TeamBadgeRight = np.array([[
        (610, 400), (580, 400),
        (580, 375), (610, 375)
    ]])

    halftimeMarker = np.array([[
        (305, 110), (335, 110),
        (335, 100), (305, 100)
    ]])

    mainMenuCart = np.array([[
        (560, 100), (580, 100),
        (580, 88), (560, 88)
    ]])

    Menu_StartGame_PlayMatch = np.array([[
        (97, 337), (117, 337),
        (117, 357), (97, 357)
    ]])

    Menu_SquadROI = np.array([[
        (484, 81), (506, 81),
        (506, 94), (484, 94)
    ]])


class TemplateMatcher():

    def __init__(self, template, ROI, cvFrame, ogFrame, func=None, threshold: float = 0.8, state: int = 0) -> None:
        self.template = template
        self.ROI = ROI
        self.cvFrame = cvFrame
        self.ogFrame = ogFrame
        self.threshold = threshold
        self.state = state
        self.func = func

        self.find(template, ROI, cvFrame, ogFrame, threshold, state)

    def find(self, template, ROI, cvFrame, ogFrame, state: int = 0, threshold: float = 0.8, func=None):
        # Make a numpy array the same size as the cvFrame
        mask = np.zeros_like(cvFrame)

        # Take the ROI and make that section white
        cv2.fillPoly(mask, ROI, 255)

        # Combine the mask and cvFrame to make a masked_image
        masked_image = cv2.bitwise_and(cvFrame, mask)

        # Get the template dimensions (used to draw the label)
        templateH, templateW = template.shape[:2]

        # Use CV2's Template Matching to get our result
        res = cv2.matchTemplate(masked_image, template, cv2.TM_CCOEFF_NORMED)

        # Capture results over a defined threshold
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            # Draw a box around any matching template results
            cv2.rectangle(ogFrame, pt, (pt[0] + templateW, pt[1] + templateH), HUD.RED, 2)

            # Send back the code for what state change this is supposed to indicate
            if state:
                FifaFlags.State = state

            if func:
                func()

        return cvFrame
