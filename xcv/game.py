try:
    from loguru import logger
    import pytz
    from time import sleep
    from datetime import datetime

    # Local_____________________________________
    # from xcv.fps import fps
    # from xcv.template_matcher import TemplateMatcher
    # from xcv.settings import UserSettings
    # from xcv.gui import GUI

except ImportError:
    logger.exception("ERROR | Modules missing ")
    raise


class GameError(Exception):
    pass


class MenuManager:

    _detected_menu = "unknown"

    def __init__(self):
        self.menu_states = {
            "unknown": 0,
            "blank_screen": 0,
            "xbox_startup": 0,
            "xbox_home": 0,
            "fifa_home": 0,
            "fut": self.fut_menu_states,
        }

        self.fut_menu_states = {
            "fut_loading": 0,
            "fut_central_tab_selected": 0,
            "fut_single_player_tab_slected": 0,
            "fut_single_player_squad_battle_slected": 0,
            "fut_single_player_season_slected": 0,
            "fut_single_player_tow_selected": 0,
            "fut_single_player_draft_selected": 0,
            "fut_single_player_squad_build_selected": 0,
            "fut_onine_tab_selected": 0,
            "fut_squads_tab_selected": 0,
            "fut_transfers_tab_selected": 0,
            "fut_store_tab_selected": 0,
            "fut_my_club_tab_selected": 0,
            "continue_screen_press_a": 0,
            "continue_screen_press_down_and_a": 0,
            "continue_screen_press_start": 0,
        }

    @classmethod
    def menu_state(cls):
        return cls._detected_menu


class Game:

    is_alive = False
    is_in_game = False
    _num_games_started = 0
    _num_games_completed = 0
    _wins = 0
    _losses = 0
    _ties = 0
    frame_counter = 0

    def __init__(self):
        Game._num_of_games += 1

        self.game_start_time = self.stopwatch_start()

        # stats
        self.home_score = 0
        self.away_score = 0
        self.game_state = 0

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

    def __str__(self):
        """Class holds all detected stats for Fifa games, based on OpenCV detections and basic logic.
        """

    @classmethod
    def num_games_started(cls):
        return Game._num_games_completed

    @classmethod
    def num_games_completed(cls):
        return Game._num_games_completed

    @classmethod
    def wins(cls):
        return Game._wins

    @classmethod
    def losses(cls):
        return Game._losses

    @classmethod
    def ties(cls):
        return Game._ties

    @classmethod
    def record(cls):
        return f"W{str(Game._wins)} - L{str(Game._losses)} - T{str(Game._ties)}"

    def set_game_state(self, new_state):
        self.game_state = new_state

    def status(self):
        if Game.is_alive and Game.is_in_game:
            return
        else:
            return

    def set_detected_score(self, home_away, new_score):
        if home_away:
            return
        else:
            return

    def detected_score(self):
        return

    def stopwatch_start(self):
        return datetime.now(tz=pytz.UTC).astimezone(pytz.timezone("US/Eastern"))

    def timer(self):
        """
        Make the human-readable clock to display it.

        :param startTime: Originally passed in from __main__.py
        :return: Elapsed Time and the Frames Per Second (FPS)
        """

        _now = datetime.now(tz=pytz.UTC).astimezone(pytz.timezone("US/Eastern"))
        elapsedTime = _now - self.game_start_time
        secs = round(elapsedTime.total_seconds())

        if elapsedTime is not 0:
            fps = round(Game.frame_counter / secs)
        else:
            fps = 0

        hrs = int(secs / 3600)
        mins = int((secs % 3600) / 60)
        secs = int(secs % 60)

        elapsedTime = f"{hrs:02}:{mins:02}:{secs:02}"

        return elapsedTime, fps

    def detected_match_clock(self):
        return


if __name__ == "__main__":
    g = Game()
