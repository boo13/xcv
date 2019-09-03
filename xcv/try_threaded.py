# import the necessary packages
from xcv.video_stream import VideoStream
from xcv.fps import fps
import argparse
import imutils
import cv2
from time import sleep

num_frames = 1000

# # grab a pointer to the video stream and initialize the FPS counter
# print("[INFO] sampling frames from webcam...")
# stream = cv2.VideoCapture(0)
# fps.start()
# sleep(2)
#
# # loop over some frames
# while fps._numFrames < num_frames:
#     # grab the frame from the stream and resize it to have a maximum
#     # width of 400 pixels
#     (grabbed, frame) = stream.read()
#     # frame = imutils.resize(frame, width=400)
#     display = 1
#
#     # check to see if the frame should be displayed to our screen
#     if display > 0:
#         cv2.imshow("Frame", frame)
#         key = cv2.waitKey(1) & 0xFF
#
#     # update the FPS counter
#     fps.update()
#
# # stop the timer and display FPS information
# fps.stop()
# print(f"[INFO] elasped time: {fps.elapsed}")
# print(f"[INFO] approx. FPS: {fps.fps}")
#
# # do a bit of cleanup
# stream.release()
# cv2.destroyAllWindows()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = VideoStream(src=0).start()
fps.start()
sleep(1)
# loop over some frames...this time using the threaded stream
while fps._numFrames < num_frames:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    # frame = imutils.resize(frame, width=400)
    display = 1

    # check to see if the frame should be displayed to our screen
    if display > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print(f"[INFO] elasped time: {fps.elapsed}")
print(f"[INFO] approx. FPS: {fps.fps}")

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
