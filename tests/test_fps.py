from xcv.fps import fps
from time import sleep

def test_fps_elapsed():
    assert fps.elapsed is 0
    fps.start()
    sleep(1)
    fps.update()
    sleep(1)
    fps.update()
    fps.stop()
    assert fps.elapsed >= 2
    assert fps.fps > 0
    assert type(fps.str_elapsed) is str
