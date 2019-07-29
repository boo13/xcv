from dataclasses import dataclass
from typing import List, Any


def defending(side: int = 0):

    assert side < 4

    def currentSide():
        FifaFlags.Defending = side

    return currentSide


def homeaway(side: int = 0):

    assert side < 4

    def currentHomeAway():
        FifaFlags.HomeAway = side

    return currentHomeAway


def scoreCheck(homeS: int = None, awayS: int = None):
    def currentScores():
        if homeS is not None:
            FifaFlags.Match_HomeScore = homeS
        if awayS is not None:
            FifaFlags.Match_AwayScore = awayS

    return currentScores


@dataclass
class FifaFlags:
    frameW: int = 0
    frameH: int = 0

    State: int = 0
    gameStates: List[Any] = (
        "Xbox Home",
        "Fifa Main Menu",
        "Squad Edit",
        "Side Select",
        "PreGame Menus",
        "Start Game",
        "Kickoff",
        "Game",
        "CutScene",
        "CornerKick",
        "GoalKick",
        "Halftime",
        "FullTime",
        "GameStats",
        "InGame Menu",
        "???",
    )

    inGame: bool = False
    inMenu: bool = True
    Unknown: bool = True

    Match_NumPlayed: int = 0
    Match_HomeScore: int = 0
    Match_AwayScore: int = 0

    Defending: int = 0
    Defense_States: tuple = (None, "Left", "Right")

    HomeAway: int = 0
    HomeAway_States: tuple = (None, "Home", "Away")


@dataclass
class MenuFlags(FifaFlags):

    Menu_FifaHome: bool = False
    Menu_FUTHome: bool = False
    Menu_SquadBattles: bool = False
    Menu_SinglePlayerSeason: bool = False
    Menu_AcceptMatch: bool = False
    Menu_ManageSquad: bool = False
    Menu_SquadEligibleToPlay: bool = False
    Menu_SideSelect: bool = False
    Menu_JerseySelect: bool = False
    Menu_StartGame_PlayMatch: bool = False
    Menu_GameLoading: bool = False
    Menu_PracticeDuringLoading: bool = False
    Menu_PreGame: bool = False
    Menu_ZeroMark: bool = False
    Menu_KickOff: bool = False
    Menu_HalfTime: bool = False
    Menu_FullTime: bool = False
    Menu_GameOver: bool = False
