import pytest
import cv2
import streamlink

@pytest.fixture(scope='session')
def hardware_VidCapture(tmpdir_factory):
    # Setup the video stream before running tests
    cap = cv2.VideoCapture(0)
    ok, frame = cap.read()

    # Checks the BOOLEAN is not false
    if ok:

        # ========================================
        yield frame         # this is where the testing happens
        # ========================================
    else:
        return

    # Teardown
    cap.release()
    cv2.destroyAllWindows()


@pytest.fixture(scope='session')
def streamlink_VidCapture(tmpdir_factory):
    url = "https://www.twitch.tv/overwatchleague"
    quality = "best"
    fps = 30.0

    streams = streamlink.streams(url)

    if streams:
        stream_url = streams[quality].to_url()
    else:
        raise ValueError("No streams were available")

    cap = cv2.VideoCapture(stream_url)

    ok, frame = cap.read()

    if ok:

        yield frame

    else:
        return


    # Teardown
    cap.release()
    cv2.destroyAllWindows()
