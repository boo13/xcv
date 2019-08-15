import PySimpleGUIQt as sg
# import cv2

"""
"""
_row0_video_frame = [
    [
        sg.Image(filename='', key='_IMAGE_')
    ]
]

"""
"""
_row1_detected_state = [
    [
        sg.Text('', key='_detected_state_')
    ]
]


""" --------------------------------------------------------------------------
Game Stats - Example Display: 

0 - 0  Home    Defending Left  BALL    Offensive - Shooting - InsideBox

_tactic_ = Our AI's current gameplan/status
"""
_row2_game_stats = [
    [
        sg.Text('', key='_score_'), sg.Text('', key='_home_away_'), sg.Text(
            '', key='_defending_side_'), sg.Text('', key='_possession_'), sg.Text('', key='_tactic_'),
    ]
]

"""
"""
_row3_xcontroller_action_buttons = [
    [
        sg.Image(filename='', key='_a_'), sg.Image(filename='', key='_b_'), sg.Image(
            filename='', key='_x_'), sg.Image(filename='', key='_y_')
    ]
]


_row3_xcontroller_dpad = [
    [
        sg.Image(filename='', key='_a_'), sg.Image(
            filename='', key='_b_'), sg.Image(filename='', key='_x_'), sg.Image(filename='', key='_y_')
    ]
]

"""
"""
_row4_connection_status = [
    [
        sg.Text('', key='_detected_state_')
    ]
]


"""
"""
_row5_gui_menu_buttons = [
    [
        sg.Image(filename='', key='_save_logs_'), sg.Image(filename='', key='_save_screenshot_'), sg.Image(
            filename='', key='_start_record_'), sg.Image(filename='', key='_EXIT_')
    ]
]
