
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

