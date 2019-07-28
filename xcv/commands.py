"""The implementation of xcv commands"""

import datetime
import time
import serial


from xcv.constants import (
    SERIAL_BAUD, 
    SERIAL_PORT,
    print_all_constants,
)
from xcv.cli.cli import hazard, sleep, stars
from xcv.util import (
    WINDOWS,
    XcvError,
    print_version,
    print_info
)

class HUD:
    from collections import namedtuple

    # ========================================
    # Color Stuff
    Color = namedtuple('Color', ['r', 'g', 'b'])
    GREEN = Color(0, 255, 0)
    RED = Color(0, 0, 255)
    BLUE = Color(255, 75, 0)
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    YELLOW = Color(0, 255, 255)
    TEAL = Color(255, 255, 0)
    PINK = Color(255, 0, 255)
    ORANGE = Color(0, 130, 255)

    GRAY1 = Color(20, 20, 20)
    GRAY2 = Color(50, 50, 50)
    GRAY4 = Color(200, 200, 200)

    #
    # ========================================

    def __init__(self):
        pass

    def draw(self, frame, press=None, fps=0, elapsedTime=0):
        import cv2
        from Game import Game
        from FifaFlags import FifaFlags

        font = cv2.FONT_HERSHEY_SIMPLEX

        if fps is not 0:
            cv2.putText(frame, "FPS", (5, 15), font, 0.25, HUD.GRAY2, 1)
            cv2.putText(frame, str(fps), (25, 15), font, 0.5, HUD.GRAY4, 1)

        if elapsedTime is not 0:
            cv2.putText(frame, "Elapsed", (530, 20), font, 0.25, HUD.GRAY2, 1)
            cv2.putText(frame, str(elapsedTime), (530, 35), font, 0.5, HUD.GRAY2, 1)

        if elapsedTime is not 0:
            cv2.putText(frame, "Game", (410, 20), font, 0.25, HUD.GRAY2, 1)
            cv2.putText(frame, str(elapsedTime), (410, 35), font, 0.5, HUD.GREEN, 1)


        # Home Away
        if FifaFlags.HomeAway == 1:
            cv2.putText(frame, "Home", (275, 25), font, 0.5, HUD.GREEN, 1)
        elif FifaFlags.HomeAway == 2:
            cv2.putText(frame, "Away", (275, 25), font, 0.5, HUD.GREEN, 1)

        # Defense
        if FifaFlags.Defending == 1:
            cv2.putText(frame, "Defend Left", (275, 50), font, 0.5, HUD.GREEN, 1)
        elif FifaFlags.Defending == 2:
            cv2.putText(frame, "Defend Right", (275, 50), font, 0.5, HUD.GREEN, 1)

        # A
        if press == 'a':
            cv2.putText(frame, "A", (480, 470), font, 0.5, HUD.GREEN, 2)
            cv2.circle(frame, (485, 465), 9, HUD.GREEN, 2)
        else:
            cv2.putText(frame, "A", (480, 470), font, 0.5, HUD.GRAY2, 2)
            cv2.circle(frame, (485, 465), 9, HUD.GRAY2, 1)

        # B
        if press == 'b':
            cv2.putText(frame, "B", (495, 455), font, 0.5, HUD.RED, 2)
            cv2.circle(frame, (500, 450), 9, HUD.RED, 2)
        else:
            cv2.putText(frame, "B", (495, 455), font, 0.5, HUD.GRAY2, 2)
            cv2.circle(frame, (500, 450), 9, HUD.GRAY2, 1)

        # X
        if press == 'x':
            cv2.putText(frame, "X", (465, 455), font, 0.5, HUD.BLUE, 2)
            cv2.circle(frame, (470, 450), 9, HUD.BLUE, 2)
        else:
            cv2.putText(frame, "X", (465, 455), font, 0.5, HUD.GRAY2, 2)
            cv2.circle(frame, (470, 450), 9, HUD.GRAY2, 1)

        # Y
        if press == 'y':
            cv2.putText(frame, "Y", (480, 440), font, 0.5, HUD.YELLOW, 2)
            cv2.circle(frame, (485, 435), 9, HUD.YELLOW, 1)
        else:
            cv2.putText(frame, "Y", (480, 440), font, 0.5, HUD.GRAY2, 2)
            cv2.circle(frame, (485, 435), 9, HUD.GRAY2, 1)

        cv2.putText(frame, "Xbox", (270, 435), font, 0.5, HUD.GRAY2, 1)

        if press == '3':
            cv2.putText(frame, "Start", (270, 455), font, 0.5, HUD.YELLOW, 1)
        else:
            cv2.putText(frame, "Start", (270, 455), font, 0.5, HUD.GRAY2, 1)

        cv2.putText(frame, "Select", (270, 475), font, 0.5, HUD.GRAY2, 1)

        # ==========================================================================================
        #  Controller
        # ___________________________

        # D-Pad Display

        #   D Up
        if press == '8':
            cv2.rectangle(frame, (390, 440), (380, 450), HUD.YELLOW, 1)
        else:
            cv2.rectangle(frame, (390, 440), (380, 450), HUD.GRAY2, 1)

        #   D L
        if press == '4':
            cv2.rectangle(frame, (370, 450), (380, 460), HUD.YELLOW, 1)
        else:
            cv2.rectangle(frame, (370, 450), (380, 460), HUD.GRAY2, 1)

        #   D Dn
        if press == '2':
            cv2.rectangle(frame, (390, 460), (380, 470), HUD.YELLOW, 1)
        else:
            cv2.rectangle(frame, (390, 460), (380, 470), HUD.GRAY2, 1)

        #   D R
        if press == '6':
            cv2.rectangle(frame, (390, 450), (400, 460), HUD.YELLOW, 1)
        else:
            cv2.rectangle(frame, (390, 450), (400, 460), HUD.GRAY2, 1)

        # LS Display
        cv2.circle(frame, (350, 440), 1, HUD.YELLOW, 1)
        cv2.circle(frame, (350, 440), 15, HUD.GRAY2, 1)

        # RS Display
        cv2.circle(frame, (440, 460), 1, HUD.YELLOW, 1)
        cv2.circle(frame, (440, 460), 15, HUD.GRAY2, 1)

        # Display the detected game state
        cv2.putText(frame, "Game State", (10, 435), font, 0.5, HUD.GRAY2, 1)
        cv2.putText(frame, FifaFlags.gameStates[FifaFlags.State], (10, 470), font, 1, HUD.TEAL, 2)

        return frame

if __name__ == "__main__":
    print_all_constants()