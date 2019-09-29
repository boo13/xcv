# Based on code from the excellent: PyImageSearch.com
from threading import Thread, Lock
import cv2
from loguru import logger

@logger.catch
class VideoStream:
    """Create a thread and read frames from video source.
        
    If we can't find video on the hardware camera, try streamlink.

    Keyword arguments:
        src -- a camera or video, defaults to hardware-connected webcam (default 0)
        fps -- (float) (default 30.0)
        streamlink_url -- (default https://www.mixer.com/)
        streamlink_quality -- useful values include 'audio_only', '480p', 'best', 'worst' (default '480p')

    """

    def __init__(self, src=0, fps=30.0, use_streamlink_backup=True, streamlink_url="https://www.twitch.tv/PistolPete2506", streamlink_quality='480p'):
        """Initialize the video camera stream and read the first frame from the stream to test it."""
        logger.debug(f"Setting VideoStream to: {src}")

        self.stream = cv2.VideoCapture(src)
        (_ok, self.frame) = self.stream.read()

        if not _ok:
            logger.warning("No video input found using source")
            logger.debug("Trying streamlink source...")
            
            import streamlink

            streams = streamlink.streams(streamlink_url)

            if streams:
                logger.debug(f"Streamlink found the following streams at {streamlink_url}\n\n{streams}\n")
                stream_url = streams[streamlink_quality].to_url()
            else:
                raise VideoStreamError("No streams were available")

            self.stream = cv2.VideoCapture(stream_url)

        self.grabbed = None
        self.thread = None
        self.started = False
        self.read_lock = Lock()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()

    def start(self):
        """Start the thread to read frames from the video stream."""
        if self.started:
            logger.warning("Thread already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        """Keep looping infinitely until the thread is stopped."""
        while self.started:
            (grabbed, _frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, _frame
            self.read_lock.release()

    def read(self):
        """Return the most recently read frame."""
        self.read_lock.acquire()
        _frame = self.frame.copy()
        self.read_lock.release()
        return _frame

    def stop(self):
        """Indicate that the thread should be stopped."""
        self.started = False
        self.thread.join()


class VideoStreamError(Exception):
    pass

if __name__ == "__main__":
    vs = VideoStream().start()
    while True:
        frame = vs.read()
        cv2.imshow('Example Frame', frame)
        if cv2.waitKey(1) == 27:
            break

    vs.stop()
    cv2.destroyAllWindows()
