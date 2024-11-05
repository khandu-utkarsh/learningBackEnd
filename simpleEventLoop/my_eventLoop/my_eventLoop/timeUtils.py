
import time
from context import Context


def hrtime():
    """ returns time in microseconds """
    return int(time.time() * 10e6)

class set_timer(Context):
    def __init__(self, duration, callback):
        """ duration is in microseconds """
        self.evloop.set_timer(duration, callback)
