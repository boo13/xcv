import PySimpleGUIQt as sg
import cv2

# define the window layout
layout = [[sg.Image(filename='', key='_IMAGE_')], ]

# create the window and show it without the plot
window = sg.Window('Demo Application - OpenCV Integration',
                   layout, location=(800, 400))

# ---===--- Event LOOP Read and display frames, operate the GUI --- #
# Setup the OpenCV capture device (webcam)
cap = cv2.VideoCapture(0)
while True:
    event, values = window.Read(timeout=20, timeout_key='timeout')
    if event in ('Exit', None):
        break
    # Read image from capture device (camera)
    ret, frame = cap.read()
    # Convert the image to PNG Bytes
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window.FindElement('_IMAGE_').Update(data=imgbytes)   # Chang
