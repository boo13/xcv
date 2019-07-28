import pytest
import cv2
import streamlink

@pytest.fixture(scope='session')
def hardware_VidCapture(tmpdir_factory):
    # Setup the video stream before running tests
    cap = cv2.VideoCapture(0)
    ok, frame = cap.read()

    # Checks the BOOLEAN is not false
    assert ok

    # ========================================
    yield frame         # this is where the testing happens
    # ========================================

    # Teardown
    cap.release()
    cv2.destroyAllWindows()
