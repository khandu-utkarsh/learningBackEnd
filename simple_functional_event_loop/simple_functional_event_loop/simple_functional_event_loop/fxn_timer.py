from context import Context

class SetTimeout(Context):

    def __init__(self, duration, callback):
        

class set_timeout(Context):
    def __init__(self, duration, callback):
        """ duration is in microseconds """
        self.evloop.set_timer(duration, callback)
