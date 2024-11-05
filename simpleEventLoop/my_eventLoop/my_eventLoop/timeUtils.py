
import time
from context import Context


def hrtime():
    """ returns time in microseconds """
    return int(time.time() * 10e6)

