class TemplateMatcher:
    """Take in an OpenCV frame, process it, find templates a pop it out again.

        :param template: template image we're going to search for
        :param ROI: region-of-interest to search for that template in
        :param cvFrame: the maluable computer vision frame
        :param ogFrame: the original frame, we use it to display information back to the user
        :option func: a function to run if we do find that template (e.g. we are defending the left side of the screen)
        :paramt hreshold (float): opencv param for template threshold
        :option state (int): an optional flag that will be switched if we found our template (a simplified version of `func`)
        """

    def __init__(
        self,
        template,
        ROI,
        cvFrame,
        ogFrame,
        func=None,
        threshold: float = 0.8,
        state: int = 0,
    ) -> None:
        self.template = template
        self.ROI = ROI
        self.cvFrame = cvFrame
        self.ogFrame = ogFrame
        self.threshold = threshold
        self.state = state
        self.func = func

        self.find(template, ROI, cvFrame, ogFrame, threshold, state)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.template}), {self.ROI}, {self.cvFrame}, {self.ogFrame}, threshold={self.threshold}, state={self.state}, func={self.func})"

    def __str__(self):
        return f"""
                Matching `template` in `ROI` of `cvFrame`, beyond a chosen `threshold`. 
                We ouput the visual information to `ogFrame`. 
                If we found our template we use `state` or `func` to set the appropriate `game_state` flags."""

    def find(
        self,
        template,
        ROI,
        cvFrame,
        ogFrame,
        state: int = 0,
        threshold: float = 0.8,
        func=None,
    ):
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
            # Draw a red box around any matching template results
            cv2.rectangle(
                ogFrame, pt, (pt[0] + templateW, pt[1] + templateH), (0, 0, 255), 2
            )

            # If we have one - set the code for the state change this is supposed to indicate
            if state:
                FifaFlags.State = state

            if func:
                func()

        return cvFrame


from dataclasses import dataclass
import numpy as np


@dataclass
class ROI:
    SquadManage = np.array([[(0, 0), (640, 0), (640, 400), (0, 500)]])

    SinglePlayerSeason_AreYouSure = np.array(
        [[(170, 232), (200, 232), (200, 272), (170, 272)]]
    )

    InGameMenu_Resume = np.array([[(420, 172), (454, 172), (454, 206), (420, 206)]])

    InGameMenu_Time = np.array([[(305, 110), (335, 110), (335, 100), (305, 100)]])

    btnStrip = np.array([[(610, 384), (30, 384), (30, 365), (610, 365)]])

    AwayTeamScore = np.array([[(126, 101), (138, 101), (138, 92), (126, 92)]])

    HomeTeamScore = np.array([[(110, 101), (123, 101), (123, 92), (110, 92)]])

    HomeTeamName = np.array([[(80, 101), (108, 101), (108, 92), (80, 92)]])

    AwayTeamName = np.array([[(142, 101), (168, 101), (168, 92), (142, 92)]])

    TeamBadgeLeft = np.array([[(30, 400), (60, 400), (60, 375), (30, 375)]])

    TeamBadgeRight = np.array([[(610, 400), (580, 400), (580, 375), (610, 375)]])

    halftimeMarker = np.array([[(305, 110), (335, 110), (335, 100), (305, 100)]])

    mainMenuCart = np.array([[(560, 100), (580, 100), (580, 88), (560, 88)]])

    Menu_StartGame_PlayMatch = np.array(
        [[(97, 337), (117, 337), (117, 357), (97, 357)]]
    )

    Menu_SquadROI = np.array([[(484, 81), (506, 81), (506, 94), (484, 94)]])


if __name__ == "__main__":

    import cv2

    cap = cv2.VideoCapture(0)

    ok, og_frame = cap.read()

    cv_frame = cv2.cvtColor(og_frame.copy(), cv2.COLOR_BGR2GRAY)

    # if ok:
    #     cv2.imshow("Original", og_frame)

    #     # #################################################
    #     #   Quit                     Keyboard key 'q' quits
    #     # #################################################
    #     key = cv2.waitKey(1) & 0xFF
    #     if key == ord("q"):
    #         cap.release()
    #         cv2.destroyAllWindows()
    #         exit()

    t = TemplateMatcher(
        cv2.imread("./templates/Menu/InGameMenu_ResumeMatch_On.png", 0),
        ROI.InGameMenu_Resume,
        cv_frame,
        og_frame,
        func=None,
        state=14,
    )
    print(repr(t))
