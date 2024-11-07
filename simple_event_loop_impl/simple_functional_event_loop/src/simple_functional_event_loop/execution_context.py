from .event_loop import EventLoop  # Assuming EventLoop is the class type for the event loop

class ExecutionContext:
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
    
    _event_loop: EventLoop = None  # Class-level attribute for event loop

    @classmethod
    def set_event_loop(cls, event_loop: EventLoop) -> None:
        """
        Set the event loop instance.

        Args:
            event_loop (EventLoop): An instance of the EventLoop class to be set.

        Returns:
            None
        """
        cls._event_loop = event_loop

    @property
    #@classmethod
    def evloop(cls) -> EventLoop:
        """
        Get the current event loop instance.

        Returns:
            EventLoop: The current event loop instance that was set using set_event_loop.
        """
        return cls._event_loop
