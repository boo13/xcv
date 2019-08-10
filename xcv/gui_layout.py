import PySimpleGUIQt as sg
from version import XCV_VERSION
from settings import serial_api
from base64_btns import (
    xb_a,
    xb_b,
    xb_x,
    xb_y,
    xb_a_null,
    xb_b_null,
    xb_x_null,
    xb_y_null,
    xb_select,
    xb_select_null,
    xb_start,
    xb_start_null,
    xb_lb,
    xb_lb_null,
    xb_rb,
    xb_rb_null,
    xb_lt,
    xb_lt_null,
    xb_rt,
    xb_rt_null,
    stick_inner_ring,
    stick_outer_ring,
)


_text_color = "#A6A4AF"
_btn_text_color = "#16161F"
_background_color = "#16161F"

# Global GUI settings
sg.SetOptions(
    element_padding=(5, 5),
    scrollbar_color=None,
    background_color=_background_color,
    text_color="#A6A4AF",
)


_exitButton = [
    sg.Button("Exit", size=(10, 1), button_color=("#A6A4AF", "#BD3138")),
    sg.Text(
        f"Vers: {XCV_VERSION}    USB: {serial_api.port}    Baud: {serial_api.BAUD}    FPS: ? ",
        font="Helvetica 10",
        justification="right",
    ),
]

_outputconsole = [
    sg.Output(size=(640, 100), background_color="#16161F", text_color=_text_color)
]


imagetab_layout = [
    [sg.T("Image Controls", font=("Helvetica", 16), justification="center")],
    [sg.Image(filename="", size=(40, 15), key="imagetab_image")],
    [sg.Checkbox("None", default=True, size=(10, 1))],
    [
        sg.Checkbox("threshold", size=(10, 1), key="thresh"),
        sg.Slider(
            (0, 255), 128, 1, orientation="h", size=(40, 15), key="thresh_slider"
        ),
    ],
    [
        sg.Checkbox("canny", size=(10, 1), key="canny"),
        sg.Slider(
            (0, 255), 128, 1, orientation="h", size=(20, 15), key="canny_slider_a"
        ),
        sg.Slider(
            (0, 255), 128, 1, orientation="h", size=(20, 15), key="canny_slider_b"
        ),
    ],
    [
        sg.Checkbox("contour", size=(10, 1), key="contour"),
        sg.Slider(
            (0, 255), 128, 1, orientation="h", size=(20, 15), key="contour_slider"
        ),
        sg.Slider((0, 255), 80, 1, orientation="h", size=(20, 15), key="base_slider"),
    ],
    [
        sg.Checkbox("blur", size=(10, 1), key="blur"),
        sg.Slider((1, 11), 1, 1, orientation="h", size=(40, 15), key="blur_slider"),
    ],
    [
        sg.Checkbox("hue", size=(10, 1), key="hue"),
        sg.Slider((0, 225), 0, 1, orientation="h", size=(40, 15), key="hue_slider"),
    ],
    [
        sg.Checkbox("enhance", size=(10, 1), key="enhance"),
        sg.Slider(
            (1, 255), 128, 1, orientation="h", size=(40, 15), key="enhance_slider"
        ),
    ],
    _exitButton,
]

# define the window layout
maintab_layout = [
    [sg.T("XCV", font=("Helvetica", 16), justification="center")],
    [sg.Image(filename="", size=(640, 480), key="main_image")],
    [
        sg.Image(
            data_base64=xb_lt_null,
            key="_btnLT_",
            enable_events=True,
            pad=((10, 0), (0, 0)),
        ),
        sg.Image(data_base64=xb_lb_null, key="_btnLB_", enable_events=True),
        sg.Image(data_base64=xb_select_null, key="_btnSelect_", enable_events=True),
        sg.Image(data_base64=xb_start_null, key="_btnStart_", enable_events=True),
        sg.Image(data_base64=xb_x_null, key="_btnX_", enable_events=True),
        sg.Image(data_base64=xb_y_null, key="_btnY_", enable_events=True),
        sg.Image(data_base64=xb_a_null, key="_btnA_", enable_events=True),
        sg.Image(data_base64=xb_b_null, key="_btnB_", enable_events=True),
        sg.Image(data_base64=xb_rb_null, key="_btnRB_", enable_events=True),
        sg.Image(data_base64=xb_rt_null, key="_btnRT_", enable_events=True),
    ],
    # [sg.Image(
    #         data_base64=stick_outer_ring,
    #         key="_LS_",
    #         enable_events=True,
    #         pad=((50, 0), (0, 0)),
    #     ),
    #     sg.Image(
    #         data_base64=stick_outer_ring,
    #         key="_RS_",
    #         enable_events=True,
    #         pad=((50, 0), (0, 0)),
    #     ),
    # ],
    [
        sg.Button(
            "Check Serial",
            size=(10, 1),
            button_color=("#16161F", "#007339"),
            key="_check_serial_",
        ),
        sg.Button("Stop", button_color=(_btn_text_color, "#B36C42"), size=(10, 1)),
        sg.Button("Record", size=(10, 1), button_color=(_btn_text_color, "#BD3138")),
        sg.Button(
            "Screenshot", button_color=(_btn_text_color, "#1749BF"), size=(10, 1)
        ),
    ],
    _outputconsole,
    _exitButton,
]

tab2_layout = [
    [sg.T("Nothing to see here... yet")],
    [
        sg.Text("Send Command:", size=(15, 1), justification="right"),
        sg.InputText("", key="input1", text_color=_text_color, size_px=(420, 35)),
    ],
    # _exitButton,
]

layout = [
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Main", maintab_layout, tooltip="Main Menu"),
                    sg.Tab(
                        "Image Controls",
                        imagetab_layout,
                        tooltip="For testings CV values",
                    ),
                    # sg.Tab("Output", tab2_layout, tooltip="eSet Output"),
                    # sg.Tab(
                    #     "Autopilot",
                    #     tab2_layout,
                    #     tooltip="Press Buttons Automagically",
                    # ),
                    # sg.Tab(
                    #     "Training", tab2_layout, tooltip="Machine Learning Stuff"
                    # ),
                    # sg.Tab("Debug", tab2_layout, tooltip="Debug"),
                ]
            ],
            tooltip="TIP2",
        )
    ]
]
