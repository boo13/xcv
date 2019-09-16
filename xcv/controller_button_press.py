from loguru import logger
import time
from functools import wraps

# def button_timer(original_function):
#     def wrapper_function(*args, **kwargs):
#         logger.debug("Wrapper executed this before {}".format(original_function.__name__))
#         return original_function(*args, **kwargs)
#     return wrapper_function

class button_timer:
    def __init__(self, original_function):
        self.original_function = original_function
        self.t1 = time.time()

    def __call__(self, *args, **kwargs):
        logger.debug(f"Button Timer: {self.t1 - time.time()}")
        logger.debug("Call method executed this before {}".format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)


# class button_timer:
#     def __init__(self, original_function):
#         self.original_function = original_function
#
#     def __call__(self, *args, **kwargs):
#         logger.debug("Call method executed this before {}".format(self.original_function.__name__))
#         return self.original_function(*args, **kwargs)

def controller_pots(*args):

    return

@button_timer
def press_button(*args, **kwargs):
    logger.info("press_button ran with argument {}".format(args))
    _parsed = parse_button_press_input(*args, **kwargs)
    time.sleep(2)
    return _parsed

def parse_button_press_input(*args, **kwargs):
    """Clean the incoming arguments, return expected dictionary.

    :param *args:
    :param **kwargs:
    :return button_dict: The expected dictionary of all button states
    """

    button_dict = {
        "A": 0,
        "B": 0,
        "X": 0,
        "Y": 0,
        "LB": 0,
        "RB": 0,
        "LPB": 0,
        "RPB": 0,
        "START": 0,
        "SELECT": 0,
        "XBOX": 0,
    }

    for kwarg in kwargs:
        kwarg = kwarg.upper()
        if kwarg in button_dict.keys():
            button_dict[kwarg] = 1

    for arg in args:
        arg = str(arg).upper()

        if arg.startswith('ST'):
            button_dict["START"] = 1
            logger.info("Pressing Start")
        elif arg.startswith('SE'):
           button_dict["SELECT"] = 1
           logger.info("Pressing Select")
        elif arg.startswith('XB'):
           button_dict["XBOX"] = 1
           logger.info("Pressing Xbox")
        elif arg in button_dict:
            button_dict[arg] = 1
            logger.info(f"Pressing {arg}")
        else:
            logger.warning("Unknown Command passed to press_button function")

    logger.debug(f"Button dictionary being sent: {button_dict}")
    return button_dict

if __name__ == "__main__":
    # press_button(A=123, j=12, b=1, x=0)
    press_button("a")
