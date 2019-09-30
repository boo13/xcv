import numpy as np
import cv2
import pytesseract
from loguru import logger

from xcv.video_stream import VideoStream
import streamlink
streamlink_quality='480p'
streamlink_url="https://www.twitch.tv/PistolPete2506"

streams = streamlink.streams(streamlink_url)

if streams:
    logger.debug(f"Streamlink found the following streams at {streamlink_url}\n\n{streams}\n")
    stream_url = streams[streamlink_quality].to_url()
else:
    raise VideoStreamError("No streams were available")

stream = cv2.VideoCapture(stream_url)

while True:
    frame = stream.read()
    cv2.imshow(frame, "frame")

cv2.destroyAllWindows()
vs.stop()