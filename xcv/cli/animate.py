""" Add some animated dots to CLI via contextmanager.

All thanks to Pipx, lifted directly from their source code - https://github.com/pipxproject/pipx/blob/master/pipx/animate.py

"""

from contextlib import contextmanager
import sys
from typing import Dict
from threading import Thread
from time import sleep


@contextmanager
def animate(message: str, do_animation: bool):
    animate = {"do_animation": do_animation, "message": message}
    t = Thread(target=print_animation, args=(animate,))
    t.start()
    try:
        yield
    finally:
        animate["do_animation"] = False
        t.join(0)


def print_animation(meta: Dict[str, bool]):
    if not sys.stdout.isatty():
        return

    cur = "."
    longest_len = 0
    sleep(1)
    while meta["do_animation"]:
        if cur == "":
            cur = "."
        elif cur == ".":
            cur = ".."
        elif cur == "..":
            cur = "..."
        else:
            cur = ""
        message = f"{meta['message']}{cur}"
        longest_len = max(len(message), longest_len)
        sys.stdout.write(" " * longest_len)
        sys.stdout.write("\r")
        sys.stdout.write(message)
        sys.stdout.write("\r")
        sleep(0.5)
    sys.stdout.write(" " * longest_len)
    sys.stdout.write("\r")


if __name__ == "__main__":
    print(__doc__)
    print("Testing the animation a loop for 10 seconds.")

    with animate(f"Animation here: ", True):
        sleep(10)
