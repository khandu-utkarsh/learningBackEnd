class Context:
    """
    A centralized access point for an event loop.

    The Context class provides a singleton-like access point to a shared event loop
    by storing it as a class attribute. This pattern allows various parts of an
    application to access the same event loop without the need to create multiple
    instances or pass the event loop around explicitly.

    Methods:
        set_event_loop(event_loop): Sets the event loop instance.
        
    Properties:
        evloop: Returns the current event loop instance.
    """
    
    _event_loop = None

    @classmethod
    def set_event_loop(cls, event_loop):
        """Set the event loop instance."""
        cls._event_loop = event_loop

    @property
    def evloop(self):
        """Get the current event loop instance."""
        return self._event_loop
