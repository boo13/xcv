#          Import libraries      _________________________________________________________________
try:
    # From the Internet___________________________________________________________________________
    from loguru import logger  # Logging made simple
    import cv2  # Opencv

    logger.debug("OpenCV Version: " + str(cv2.__version__))
    import pytz
    import numpy as np  # Handles arrays, makes images into numbers
    import serial
    # import inputs

    # Built-in____________________________________________________________________________________
    from time import sleep
    import datetime
    from dataclasses import dataclass, field
    import multiprocessing

    # Local_______________________________________________________________________________________
    # from config import config
    from Templates import ROI, TemplateMatcher
    from fps import FPS
    from FifaFlags import FifaFlags, defending, homeaway, scoreCheck
    from HUD import HUD
    from controller.serialSend import serialSend

except ImportError:
    logger.exception(" | ERROR | Modules missing ")
    raise


class Game:
    buttons = {'A': 0,
               'B': 0,
               'X': 0,
               'Y': 0,
               'Lb': 0,
               'Rb': 0,
               'Lpb': 0,
               'Rpb': 0,
               'Select': 0,
               'Start': 0,
               'Xbox': 0,
               'LSx': 0,
               'LSy': 0,
               'RSx': 0,
               'RSy': 0,
               'LT': 0,
               'RT': 0,
               }

    frameWidth = None
    frameHeight = None
    frameCounter = 0
    countSinceLastKnownState = 0
    debug = False

    def __init__(self, timezone="US/Eastern", debug=False):
        """
        Instantiate an object of the class Game

        :param timezone: A String known by pytz
        :param debug: Boolean (print debug messages)
        """
        self.timezone = timezone
        self.debug = debug
        datetime.datetime.now(tz=pytz.UTC).astimezone(pytz.timezone(self.timezone))

        self.hud = HUD()

        # Setup the button press functions to send the serial commands
        self.pressX = serialSend('x\n')
        self.pressB = serialSend('b\n')
        self.pressY = serialSend('y\n')
        self.pressDU = serialSend('8\n')
        self.pressDD = serialSend('2\n')
        self.pressDL = serialSend('4\n')
        self.pressDR = serialSend('6\n')
        self.pressLB = serialSend('7\n')
        self.pressSelect = serialSend('1\n')
        self.pressRB = serialSend('9\n')
        self.pressStart = serialSend('3\n')
        self.pressA = serialSend('a\n')

        self.btnList = [
            self.pressX,
            self.pressB,
            self.pressY,
            self.pressDU,
            self.pressDD,
            self.pressDL,
            self.pressDR,
            self.pressLB,
            self.pressSelect,
            self.pressRB,
            self.pressStart,
            self.pressA,
        ]

        self.defN = defending(0)
        self.defL = defending(1)
        self.defR = defending(2)

        self.homeN = homeaway(0)
        self.homeH = homeaway(1)
        self.homeA = homeaway(2)

        # pads = inputs.devices.gamepads
        # if len(pads) == 0:
        #     raise Exception("Couldn't find any Gamepads!")
        # elif len(pads) > 1:
        #     raise Exception("Multiple Gamepads found!")
        # else:
        #     logger.info(f"Controller found at:\n{pads}")

        self.defN()
        self.pressStart()

    def connect(self, startTime: datetime, camPort=0, url=None):
        """

        :param startTime: Originally from __main__.py
        :param url: Uses Streamlink (supports Twitch, Mixer, etc.)
        :return: None
        """

        if not url:

            cap = cv2.VideoCapture(camPort)

            if Game.debug:
                Game.frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                Game.frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                logger.debug(f"Video Captured - Frame size: w{Game.frameWidth} h{Game.frameHeight}\n")

            self.vidCapture(cap, startTime)

        # if we did enter a URL then stream it
        else:
            exit()

    def clock(self, startTime: datetime):
        """
        Make the human-readable clock to display it.

        :param startTime: Originally passed in from __main__.py
        :return: Elapsed Time and the Frames Per Second (FPS)
        """

        current_time = datetime.datetime.now(tz=pytz.UTC).astimezone(pytz.timezone(self.timezone))
        elapsedTime = (current_time - startTime)
        secs = round(elapsedTime.total_seconds())

        if elapsedTime is not 0:
            fps = round(Game.frameCounter / secs)
        else:
            fps = 0

        hrs = int(secs / 3600)
        mins = int((secs % 3600) / 60)
        secs = int(secs % 60)

        elapsedTime = f'{hrs:02}:{mins:02}:{secs:02}'

        return elapsedTime, fps

    def scoreboard(self, cvFrame, ogFrame):

        for i in range(12):
            TemplateMatcher(cv2.imread(f'./templates/HomeScore/{i}.png', 0),
                            ROI.HomeTeamScore, cvFrame, ogFrame,
                            func=scoreCheck([i]),
                            state=7)
        # return score

    # @classmethod
    # def set_game_state(cls, stateChange):
    #     cls.buttons = stateChange

    def vidCapture(self, cap: object, startTime: datetime):

        # While the Stream is Open... Keep processing the image
        while True:




            # The CV2 capture comes back as a tuple - bool flag, then the frame
            ok, og_frame = cap.read()

            if ok:
                assert og_frame is not None
                
                # Update the clock
                elapsed, fps = self.clock(startTime)

                cv_frame = cv2.cvtColor(og_frame.copy(), cv2.COLOR_BGR2GRAY)

                # events = inputs.get_gamepad()
                # for event in events:
                #     print(event.ev_type, event.code, event.state)

                if Game.countSinceLastKnownState > 30:

                    # if FifaFlags.State == 7:
                    #     self.scoreboard(cvFrame, ogFrame)
                    TemplateMatcher(cv2.imread('./templates/myTeamBadge.jpg', 0),
                                    ROI.TeamBadgeLeft, cv_frame, og_frame,
                                    func=self.defL,
                                    state=7)
                    TemplateMatcher(cv2.imread('./templates/myTeamBadge.jpg', 0),
                                    ROI.TeamBadgeRight, cv_frame, og_frame,
                                    func=self.defR,
                                    state=7)
                    TemplateMatcher(cv2.imread('./templates/myTeamScoreboardName.png', 0),
                                    ROI.HomeTeamName, cv_frame, og_frame,
                                    func=self.homeH,
                                    state=7)
                    TemplateMatcher(cv2.imread('./templates/myTeamScoreboardName.png', 0),
                                    ROI.AwayTeamName, cv_frame, og_frame,
                                    func=self.homeA,
                                    state=7)
                    TemplateMatcher(cv2.imread('./templates/Menu/Menu_SinglePlayerSeason_Start_No.png', 0),
                                    ROI.SinglePlayerSeason_AreYouSure, cv_frame, og_frame,
                                    func=self.pressDD, state=4)
                    TemplateMatcher(cv2.imread('./templates/StartBtn.png', 0),
                                    ROI.btnStrip, cv_frame, og_frame,
                                    func=self.pressStart,
                                    state=5)
                    TemplateMatcher(cv2.imread('./templates/Menu/InGameMenu_ResumeMatch_On.png', 0),
                                    ROI.InGameMenu_Resume, cv_frame, og_frame,
                                    func=self.pressA,
                                    state=14)
                    TemplateMatcher(cv2.imread('./templates/Menu/InGameMenu_ResumeMatch_Off.png', 0),
                                    ROI.InGameMenu_Resume, cv_frame, og_frame,
                                    state=14)
                    TemplateMatcher(cv2.imread('./templates/SquadManagement.png', 0),
                                    ROI.SquadManage, cv_frame, og_frame,
                                    state=2)

                    if FifaFlags.inGame or FifaFlags.Unknown:
                        # self.pressA()
                        # og_frame = self.hud.draw(og_frame, press='a')

                        for b in self.btnList:
                            b()
                            sleep(0.1)


                    Game.countSinceLastKnownState = 0
                    Game.State = 15

                og_frame = self.hud.draw(og_frame, fps=fps, elapsedTime=elapsed)

                Game.frameCounter += 1
                Game.countSinceLastKnownState += 1

                #   Display Original frame
                cv2.imshow("Original", og_frame)

                # #################################################
                #   Quit                     Keyboard key 'q' quits
                # #################################################
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    if Game.debug:
                        logger.critical("USER: QUIT\n")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

            else:
                logger.critical(" | QUIT | No video found")
                cap.release()
                cv2.destroyAllWindows()
                exit()

    def singleBtnPress(self, btn: str):
        for key, value in Game.buttons.items():
            if key == btn:
                value = True
            else:
                value = False
            print(key, value)


class GameClock(Game):
    def __init__(self, timezone="US/Eastern", debug=False, gameStart=None, gameEnd=None):
        super.__init__(timezone, debug)
        self.gameStart = gameStart
        self.gameEnd = gameEnd

        logger.info("Game Start")
        gameStart = datetime.datetime.now(tz=pytz.UTC).astimezone(pytz.timezone(timezone))

    @property
    def elapsed(self):
        return

    def update(self, elapsed):

        # self.elapsed =

        if self.gameEnd:
            logger.info("Game End")

class Controller(Game):

    def __init__(self, timezone="US/Eastern", debug=False, conType="xBox"):
        super.__init__(timezone, debug)
        self.conType = conType

    def send(self, buttons=None, pots=None):
        # btns = dict{}

        return

    # # Create controller properties
    # @property
    # def LTHUMBX(self):
    #     return self.controlValues[self.XboxControls.LTHUMBX]
    #
    # @property
    # def LTHUMBY(self):
    #     return self.controlValues[self.XboxControls.LTHUMBY]
    #
    # @property
    # def RTHUMBX(self):
    #     return self.controlValues[self.XboxControls.RTHUMBX]
    #
    # @property
    # def RTHUMBY(self):
    #     return self.controlValues[self.XboxControls.RTHUMBY]
    #
    # @property
    # def RTRIGGER(self):
    #     return self.controlValues[self.XboxControls.RTRIGGER]
    #
    # @property
    # def LTRIGGER(self):
    #     return self.controlValues[self.XboxControls.LTRIGGER]
    #
    # @property
    # def A(self):
    #     return self.controlValues[self.XboxControls.A]
    #
    # @property
    # def B(self):
    #     return self.controlValues[self.XboxControls.B]
    #
    # @property
    # def X(self):
    #     return self.controlValues[self.XboxControls.X]
    #
    # @property
    # def Y(self):
    #     return self.controlValues[self.XboxControls.Y]
    #
    # @property
    # def LB(self):
    #     return self.controlValues[self.XboxControls.LB]
    #
    # @property
    # def RB(self):
    #     return self.controlValues[self.XboxControls.RB]
    #
    # @property
    # def BACK(self):
    #     return self.controlValues[self.XboxControls.BACK]
    #
    # @property
    # def START(self):
    #     return self.controlValues[self.XboxControls.START]
    #
    # @property
    # def XBOX(self):
    #     return self.controlValues[self.XboxControls.XBOX]
    #
    # @property
    # def LEFTTHUMB(self):
    #     return self.controlValues[self.XboxControls.LEFTTHUMB]
    #
    # @property
    # def RIGHTTHUMB(self):
    #     return self.controlValues[self.XboxControls.RIGHTTHUMB]
    #
    # @property
    # def DPAD(self):
    #     return self.controlValues[self.XboxControls.DPAD]

@logger.catch
def main(startTime: datetime, url: str = None):
    session = Game()
    session.connect(startTime)
