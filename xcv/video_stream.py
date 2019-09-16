# Based on code from the excellent: PyImageSearch.com
from threading import Thread, Lock
import cv2
from loguru import logger

class VideoStreamError(Exception):
    pass

@logger.catch
class VideoStream:
    """Create a thread and read frames from video source.

    Keyword arguments:
        src -- a camera or video, defaults to hardware-connected webcam (default 0)
    """

    def __init__(self, src=0):
        """Initialize the video camera stream and read the first frame from the stream."""
        logger.debug(f"Setting VideoStream to: {src}")

        self.stream = cv2.VideoCapture(src)
        (_ok, self.frame) = self.stream.read()

        if not _ok:
            raise VideoStreamError("No video input found using source")

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


if __name__ == "__main__":
    vs = VideoStream().start()
    while True:
        frame = vs.read()
        cv2.imshow('Example Frame', frame)
        if cv2.waitKey(1) == 27:
            break

    vs.stop()
    cv2.destroyAllWindows()
