from xcv.clock import Clock

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

    # def find_if_in_fifa(self):
    #     return

    # def find_if_in_menu(self):
    #     return

    def state(self):
        if True:
            return
        else:
            return

    def clock(self, print_it=False):
        if print_it:
            print(f"Game Session Elapsed: {self.game_session_clock.elapsed()}")
        else:
            return self.game_session_clock.elapsed()

    def reset_clock(self):
        self.game_session_clock.reset()


# ======================
class FifaSession:
    def __init__(self, game_session):
        self.fifa_session_clock = Clock()

        self.menu_states = {"fut": self.fut_menu_states}

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

    def state(self):
        if True:
            return
        else:
            return

    def clock(self, print_it=False):
        if print_it:
            print(f"Fifa Session Elapsed: {self.fifa_session_clock.elapsed()}")
        else:
            return self.fifa_session_clock.elapsed()

    def reset_clock(self):
        self.fifa_session_clock.reset()


# ======================
class FifaMatch:
    def __init__(self, game_session, fifa_session):
        self.fifa_match_clock = Clock()

        self.home = False
        self.away = False
        self.side_left = False
        self.side_right = False
        self.known_state = False

        # stats
        self.home_score = 0
        self.away_score = 0
        self.game_state = 0

    def state(self):
        if self.known_state:
            return self.known_state
        else:
            return

    def check_loop(self):
        return

    def clock(self, print_it=False):
        if print_it:
            print(f"Fifa Match Elapsed: {self.fifa_match_clock.elapsed()}")
        else:
            return self.fifa_match_clock.elapsed()

    def reset_clock(self):
        self.fifa_match_clock.reset()


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


# ======================
class Scoreboard:
    def find_score(self, fifa_session, fifa_match):
        return

    def last_known_score(self, fifa_match):
        return

    def find_clock(self, fifa_match):
        return

    def last_known_clock(self, fifa_match):
        return

    def home_away(self, fifa_match):
        return


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
