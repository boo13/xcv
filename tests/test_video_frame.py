import numpy as np


def test_frame_exists(hardware_VidCapture):
    frame = hardware_VidCapture
    h, w = frame.shape[:2]

    assert w > 0
    assert w > h


def test_frame_size(hardware_VidCapture):
    """Check it is of the expected dimensions.
    This is  due to the amount of hardcoded values currently used in the package"""
    frame = hardware_VidCapture
    h, w = frame.shape[:2]
    assert h == 480
    assert w == 640


def test_numpy_mask(hardware_VidCapture):
    """Check that a numpy mask works as expected"""
    frame = hardware_VidCapture
    h, w = frame.shape[:2]

    mask = np.zeros_like(frame)
    expectedH, expectedW = mask.shape[:2]

    assert expectedH == h
    assert expectedW == w


def test_streamlink_exists(streamlink_VidCapture):
    frame = streamlink_VidCapture
    h, w = frame.shape[:2]

    assert w > 0
    assert w > h
