class Context:
    _event_loop = None

    @classmethod
    def set_event_loop(cls, event_loop):
        cls._event_loop = event_loop

    @property
    def evloop(self):
        return self._event_loop

