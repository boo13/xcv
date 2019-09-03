from xcv.clock import Clock
from loguru import logger
import cv2
from datetime import datetime, timedelta

# ======================
class GameSession:
    def __init__(self):
        self.game_session_clock = Clock()

        self.menu_states = {
            "unknown": 0,
            "blank_screen": 0,
            "xbox_startup": 0,
            "xbox_home": 0,
            "fifa_home": 0,
        }

    def check_video_source_size(self, cap):

        _width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        _height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if not cap.isOpened():
            logger.warning("Unable to read camera feed")
        elif _width >= 641 or _height >= 481:
            logger.warning(
                f"OpenCV values are currently hard-coded for a 640x480 frame, but your frame is {_width}x{_height}"
            )
        else:
            logger.debug(f"Frame {_width}x{_height}")

    def state(self):
        if True:
            return
        else:
            return

    def clock(self, print_it=False, as_string=False):
        if print_it:
            print(f"Game Session Elapsed: {self.game_session_clock.elapsed_no_microseconds()}")
        else:
            return self.game_session_clock.elapsed_no_microseconds()

    def reset_clock(self):
        self.game_session_clock.reset()


# ======================
class FifaSession:
    def __init__(self, game_session):
        # Session clock does not start until we have detected a known GUI flag (such as scoreboard)
        self.fifa_session_clock = None
        self.clock_is_started = False

        self.in_game = False
        self.in_menu = False
        # self.in_pre_game_menu = False
        # self.in_in_game_menu = False
        # self.in_post_game_menu = False

        self.fut_menu_states = {
            "fut_loading": 0,
            "fut_central_tab_selected": 0,
            "fut_single_player_tab_selected": 0,
            "fut_single_player_squad_battle_selected": 0,
            "fut_single_player_season_selected": 0,
            "fut_single_player_tow_selected": 0,
            "fut_single_player_draft_selected": 0,
            "fut_single_player_squad_build_selected": 0,
            "fut_online_tab_selected": 0,
            "fut_squads_tab_selected": 0,
            "fut_transfers_tab_selected": 0,
            "fut_store_tab_selected": 0,
            "fut_my_club_tab_selected": 0,
            "continue_screen_press_a": 0,
            "continue_screen_press_down_and_a": 0,
            "continue_screen_press_start": 0,
        }

        self.menu_states = {"fut": self.fut_menu_states}

    def set_in_game(self):
        self.in_game = True
        self.in_menu = False
        self.start_clock()

    def set_in_menu(self):
        self.in_game = False
        self.in_menu = True
        self.start_clock()

    def display_status(self):
        if self.in_game:
            return "FIFA Match"
        elif self.in_menu:
            return "FIFA Menu"
        else:
            return ""

    def state(self):
        if True:
            return
        else:
            return

    def start_clock(self):
        if not self.clock_is_started:
            if self.in_game or self.in_menu:
                self.fifa_session_clock = Clock()
                self.clock_is_started = True

    def clock(self, print_it=False):
        if print_it:
            print(f"Fifa Session Elapsed: {self.fifa_session_clock.elapsed_no_microseconds()}")
        else:
            if self.fifa_session_clock is not None:
                return self.fifa_session_clock.elapsed_no_microseconds()

    def reset_clock(self):
        self.fifa_session_clock.reset()


# ======================
class FifaMatch:
    def __init__(self, fifa_session):
        self.fifa_match_clock = Clock()
        self.fifa_session = fifa_session

        self.is_alive = False

        self.home = False
        self.away = False
        self.side_left = False
        self.side_right = False
        self.known_state = False

        # stats
        self.home_score = 0
        self.away_score = 0
        self.game_state = 0

    @classmethod
    def make_fifa_match(cls):
        FifaMatch()

    def state(self):
        if self.known_state:
            return self.known_state
        else:
            return

    def check_loop(self):
        return

    def show_screen_side(self):
        if self.side_left:
            return "Defending Left"
        elif self.side_right:
            return "Defending Right"
        else:
            return ""

    def set_side_left(self):
        self.fifa_session.set_in_game()
        self.side_left = True
        self.side_right = False

    def set_side_right(self):
        self.fifa_session.set_in_game()
        self.side_left = False
        self.side_right = True

    def show_home_or_away(self):
        if self.home:
            return "Home"
        elif self.away:
            return "Away"
        else:
            return ""

    def set_away_team(self):
        self.home = False
        self.away = True

    def set_home_team(self):
        self.home = True
        self.away = False

    def set_in_squad_menu(self):
        self.fifa_session.set_in_menu()

    def set_found_zero(self):
        print("Found a 0!")

    def clock(self, print_it=False):
        if print_it:
            print(f"Fifa Match Elapsed: {self.fifa_match_clock.elapsed_no_microseconds()}")
        else:
            return self.fifa_match_clock.elapsed_no_microseconds()

    def reset_clock(self):
        self.fifa_match_clock.reset()

    def detected_clock(self):
        return

    def last_detected_clock(self):
        return


# ======================


class FifaPlayer:
    def __init__(self):
        self.controled_player_possession_states = {
            "passing_basic": 0,
            "passing_throughball": 0,
            "shooting_basic": 0,
            "shooting_timed": 0,
            "shooting_finesse": 0,
            "shooting_low_driven": 0,
            "shooting_chip": 0,
            "chipping_basic": 0,
            "chipping_low_driven": 0,
        }

        self.controlled_player_off_ball_states = {
            "defensive_marking": 0,
            "defensive_lane_cutting": 0,
            "offensive_run": 0,
        }

        self.controlled_player_state = {
            "sprinting": 0,
            "possesion": 0,
            "kick_off": 0,
            "offense": 0,
            "defense": 0,
            "loose_ball": 0,
            "air_ball": 0,
            "goal_kick": 0,
            "corner_kick": 0,
            "half_time_kick_off": 0,
            "extra_time_kick_off": 0,
            "second_extra_time_kick_off": 0,
            "penalty_kicker": 0,
            "penalty_goalie": 0,
        }

    # def clock(self, print_it=False):
    #     if print_it:
    #         print(f"Command Countdown: {self.fifa_match_clock.elapsed_no_microseconds()}")
    #     else:
    #         return self.fifa_match_clock.elapsed_no_microseconds()
    #
    # def reset_clock(self):
    #     self.fifa_match_clock.reset()


# ======================
class Scoreboard:
    home_score = 0
    away_score = 0

    def __init__(self, fifa_match):
        self.fifa_match = fifa_match

    def find_score(self):
        return

    def last_known_score(self):
        return

    def find_clock(self):
        return

    def last_known_clock(self):
        return

    def home_away(self):
        return

    def found_digit(self, found):
        num, pos = found
        print(f"num {num} at {pos}")

# ======================
class WinLossRecord:
    def __init__(self, game_session):
        self._wins = 0
        self._losses = 0
        self._ties = 0

    def add_win(self):
        _wins += 1

    def add_loss(self):
        _losses += 1

    def add_ties(self):
        _ties += 1

    def as_string(self):
        return f"{self._wins}/{self._losses}/{self._ties}"


# ======================
# ======================
# ======================
if __name__ == "__main__":
    from time import sleep

    game_session = GameSession()
    fifa_session = FifaSession(game_session)
    fifa_match = FifaMatch(game_session, fifa_session)
    sleep(1)

    fifa_session.clock(print_it=True)
    fifa_match.clock(print_it=True)
    sleep(2)
    fifa_match.clock(print_it=True)
    sleep(1)
    fifa_match.reset_clock()
    print(fifa_match.clock())

    #
    record = WinLossRecord(game_session)
    print(record.as_string())
