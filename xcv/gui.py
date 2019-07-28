try:
    import sys
    import PySimpleGUIQt as sg
    import cv2
    import numpy as np
    from xcv.constants import XCV_VERSION, SERIAL_PORT, SERIAL_BAUD
except:
    raise

"""
Demo program that displays a webcam using OpenCV and applies some very basic image functions

- functions from top to bottom -
none:       no processing
threshold:  simple b/w-threshold on the luma channel, slider sets the threshold value
canny:      edge finding with canny, sliders set the two threshold values for the function => edge sensitivity
contour:    colour finding in the frame, first slider sets the hue for the colour to find, second the minimum saturation
            for the object. Found objects are drawn with a red contour.
blur:       simple Gaussian blur, slider sets the sigma, i.e. the amount of blur smear
hue:        moves the image hue values by the amount selected on the slider
enhance:    applies local contrast enhancement on the luma channel to make the image fancier - slider controls fanciness.
"""


def mainGUI():
    sg.ChangeLookAndFeel('DarkBlue')

    # define the window layout
    layout = [[sg.Text('XCV', font='Helvetica 16', justification='center')],
              [sg.Text( f'Vers: {XCV_VERSION}    USB: {SERIAL_PORT}    Baud: {SERIAL_BAUD}\n', font='Helvetica 10', justification='center')],
              [sg.Image(filename='', key='image')],
              [sg.Radio('Standby', 'GameMode', default=True, key='GM_standby'), sg.Radio('AutoPilot', 'GameMode',key='GM_autoPilot'), sg.Radio('SinglePress', 'GameMode',key='GM_singlePress'),  sg.Radio('Debug', 'GameMode',key='GM_debug')],
              [sg.Checkbox('None', True, size=(10, 1))],
              [sg.Checkbox('threshold', size=(10, 1), key='thresh'),
               sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='thresh_slider')],
              [sg.Checkbox('canny', size=(10, 1), key='canny'),
               sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='canny_slider_a'),
               sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='canny_slider_b')],
              [sg.Checkbox('contour', size=(10, 1), key='contour'),
               sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='contour_slider'),
               sg.Slider((0, 255), 80, 1, orientation='h', size=(20, 15), key='base_slider')],
              [sg.Checkbox('blur', size=(10, 1), key='blur'),
               sg.Slider((1, 11), 1, 1, orientation='h', size=(40, 15), key='blur_slider')],
              [sg.Checkbox('hue', size=(10, 1), key='hue'),
               sg.Slider((0, 225), 0, 1, orientation='h', size=(40, 15), key='hue_slider')],
              [sg.Checkbox('enhance', size=(10, 1), key='enhance'),
               sg.Slider((1, 255), 128, 1, orientation='h', size=(40, 15), key='enhance_slider')],
              [sg.Button('Exit', size=(10, 1))]]

    # create the window and show it without the plot
    window = sg.Window(f'XCV - {XCV_VERSION}',
                       location=(800, 400))
    window.Layout(layout).Finalize()

    cap = cv2.VideoCapture(0)
    while True:
        event, values = window.Read(timeout=0, timeout_key='timeout')
        if event == 'Exit' or event is None:
            sys.exit(0)
        ret, frame = cap.read()

        # if values['GM_debug']:
        #     sg.Print("hello it's me displaying debug info in a window")

        if values['thresh']:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
            _, frame = cv2.threshold(frame, values['thresh_slider'], 255, cv2.THRESH_BINARY)
        if values['canny']:
            frame = cv2.Canny(frame, values['canny_slider_a'], values['canny_slider_b'])
        if values['blur']:
            frame = cv2.GaussianBlur(frame, (21, 21), values['blur_slider'])
        if values['hue']:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += values['hue_slider']
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        if values['enhance']:
            enh_val = values['enhance_slider'] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        if values['contour']:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame = cv2.GaussianBlur(frame, (21, 21), 1)
            frame = cv2.inRange(frame, np.array([values['contour_slider'], values['base_slider'], 40]),
                              np.array([values['contour_slider'] + 30, 255, 220]))
            # _, cnts, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(frame, cnts, -1, (0, 0, 255), 2)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        window.FindElement('image').Update(data=imgbytes)


mainGUI()
