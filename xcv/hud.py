"""This is for drawing game/debug info on the OpenCV output frame.

See gui.py for displaying information within the GUI Window.

"""
from collections import namedtuple
import cv2

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
font = cv2.FONT_HERSHEY_SIMPLEX

elapsedTime = 666


# HUD functions
def draw_HUD_FPS(frame, fps: int=0) -> None:
    if fps is not 0:
        cv2.putText(frame, "FPS", (5, 15), font, 0.25, GRAY4, 1)
        cv2.putText(frame, str(fps), (25, 15), font, 0.5, GRAY4, 1)

def draw_HUD_elapsedTime(frame) -> None:
    if elapsedTime is not 0:
        cv2.putText(frame, "Elapsed", (530, 20), font, 0.25, HUD.GRAY2, 1)
        cv2.putText(frame, str(elapsedTime), (530, 35), font, 0.5, GRAY2, 1)

def draw_HUD_elapsedGameTime(frame) -> None:
    if elapsedTime is not 0:
        cv2.putText(frame, "Game", (410, 20), font, 0.25, GRAY2, 1)
        cv2.putText(frame, str(elapsedTime), (410, 35), font, 0.5, GREEN, 1)

def draw_HUD_HomeAway(frame) -> None:
    if FifaFlags.HomeAway == 1:
        cv2.putText(frame, "Home", (275, 25), font, 0.5, GREEN, 1)
    elif FifaFlags.HomeAway == 2:
        cv2.putText(frame, "Away", (275, 25), font, 0.5, GREEN, 1)

def draw_HUD_DefendingSide(frame):
    # # Display the detected game state
    # cv2.putText(frame, "Game State", (10, 435), font, 0.5, GRAY2, 1)
    # cv2.putText(frame, FifaFlags.gameStates[FifaFlags.State], (10, 470), font, 1, TEAL, 2)
    
#         # Defense
#         if FifaFlags.Defending == 1:
#             cv2.putText(frame, "Defend Left", (275, 50), font, 0.5, GREEN, 1)
#         elif FifaFlags.Defending == 2:
#             cv2.putText(frame, "Defend Right", (275, 50), font, 0.5, GREEN, 1)
    return


# # ===========================================================================
# #  Controller
# # ===========================================================================

def draw_HUD_controller(frame, press:str=None) -> None:
    # A
    if press == 'a':
        cv2.putText(frame, "A", (480, 470), font, 0.5, GREEN, 2)
        cv2.circle(frame, (485, 465), 9, GREEN, 2)
    else:
        cv2.putText(frame, "A", (480, 470), font, 0.5, GRAY2, 2)
        cv2.circle(frame, (485, 465), 9, GRAY2, 1)
    # B
    if press == 'b':
        cv2.putText(frame, "B", (495, 455), font, 0.5, RED, 2)
        cv2.circle(frame, (500, 450), 9, RED, 2)
    else:
        cv2.putText(frame, "B", (495, 455), font, 0.5, GRAY2, 2)
        cv2.circle(frame, (500, 450), 9, GRAY2, 1)
    # X
    if press == 'x':
        cv2.putText(frame, "X", (465, 455), font, 0.5, BLUE, 2)
        cv2.circle(frame, (470, 450), 9, BLUE, 2)
    else:
        cv2.putText(frame, "X", (465, 455), font, 0.5, GRAY2, 2)
        cv2.circle(frame, (470, 450), 9, GRAY2, 1)
    # Y
    if press == 'y':
        cv2.putText(frame, "Y", (480, 440), font, 0.5, YELLOW, 2)
        cv2.circle(frame, (485, 435), 9, YELLOW, 1)
    else:
        cv2.putText(frame, "Y", (480, 440), font, 0.5, GRAY2, 2)
        cv2.circle(frame, (485, 435), 9, GRAY2, 1)

    cv2.putText(frame, "Xbox", (270, 435), font, 0.5, GRAY2, 1)


    # # D-Pad Display
    #   D Up
    if press == '8':
        cv2.rectangle(frame, (390, 440), (380, 450), YELLOW, 1)
    else:
        cv2.rectangle(frame, (390, 440), (380, 450), GRAY2, 1)

    #   D L
    if press == '4':
        cv2.rectangle(frame, (370, 450), (380, 460), YELLOW, 1)
    else:
        cv2.rectangle(frame, (370, 450), (380, 460), GRAY2, 1)

    #   D Dn
    if press == '2':
        cv2.rectangle(frame, (390, 460), (380, 470), YELLOW, 1)
    else:
        cv2.rectangle(frame, (390, 460), (380, 470), GRAY2, 1)

    #   D R
    if press == '6':
        cv2.rectangle(frame, (390, 450), (400, 460), YELLOW, 1)
    else:
        cv2.rectangle(frame, (390, 450), (400, 460), GRAY2, 1)

    # LS Display
    cv2.circle(frame, (350, 440), 1, YELLOW, 1)
    cv2.circle(frame, (350, 440), 15, GRAY2, 1)

    # RS Display
    cv2.circle(frame, (440, 460), 1, YELLOW, 1)
    cv2.circle(frame, (440, 460), 15, GRAY2, 1)

    cv2.putText(frame, "Select", (270, 475), font, 0.5, GRAY2, 1)

    if press == '3':
            cv2.putText(frame, "Start", (270, 455), font, 0.5, YELLOW, 1)
    else:
        cv2.putText(frame, "Start", (270, 455), font, 0.5, GRAY2, 1)




