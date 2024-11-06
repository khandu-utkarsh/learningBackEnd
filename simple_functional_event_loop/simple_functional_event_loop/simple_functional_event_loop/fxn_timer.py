from execution_context import ExecutionContext  # Assuming ExecutionContext is the correct import
from event_loop import EventLoop
from typing import Callable

class SetTimeout(ExecutionContext):
    """
    A class that sets a timeout to execute a callback after a specified duration.
    
    Inherits from ExecutionContext to access the shared event loop and set timers.

    Attributes:
        duration (int): The duration in microseconds to wait before executing the callback.
        callback (Callable): The callback function to execute when the timer expires.
        callback_args (tuple): The arguments to pass to the callback function.
    """

    def __init__(self, duration: int, callback: Callable[..., None], callback_args: tuple):
        """
        Initializes a SetTimeout instance and sets a timer in the event loop.

        Args:
            duration (int): Duration in microseconds before the callback is triggered.
            callback (Callable): The callback function to call when the timer expires.
            callback_args (tuple): Arguments to pass to the callback function.
        """
        # Access the event loop via the parent class (ExecutionContext)
        self.evloop.set_timer(duration, callback, *callback_args)
