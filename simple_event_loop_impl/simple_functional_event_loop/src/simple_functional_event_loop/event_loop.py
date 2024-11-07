from .event_loop_impl_deque import EventLoopDequeImpl
import time  # Import time to handle time-related operations
from typing import Callable, Any

class EventLoop:
    """
    A simple event loop implementation to manage callbacks and timers.

    The EventLoop class manages the execution of registered callbacks and
    handles file object events. It processes a queue of events and invokes
    corresponding callbacks in the order they are registered.

    Attributes:
        _queue (Queue): The queue to hold events and callbacks.
        _time (float): The current time in high-resolution format.
    """

    def __init__(self):
        """Initialize the event loop with an empty EventLoopDequeImpl instance."""
        self._queue = EventLoopDequeImpl()
        self._time = time.perf_counter() * 1_000_000 # Use high-resolution counter


    def run(self, entry_point: Callable[..., None], *args: Any):
        """
        Run the event loop starting from the entry point callback.

        Args:
            entry_point (callable): The initial callback to execute.
            *args: Arguments to pass to the entry point callback.
        """
        self._execute(entry_point, *args)

        while not self._queue.is_empty():
            fn, args_fxn, mask = self._queue.pop(self._time)  # Adjusted to unpack `pop` result correctly
            self._execute(fn, *args_fxn)

        self._queue.close()

    def register_fileobj(self, fileobj: Any, callback: Callable[..., None], *args: Any):
        """
        Register a file object with a callback for events.

        Args:
            fileobj: The file object to monitor.
            callback (callable): The function to call when the file object is ready.
            *args: Arguments to pass to the callback.
        """
        self._queue.register_file_obj(fileobj, callback, args)  # Use `register_file_obj` from EventLoopDequeImpl

    def unregister_fileobj(self, fileobj: Any):
        """
        Unregister a file object.

        Args:
            fileobj: The file object to stop monitoring.
        """
        self._queue.unregister_file_obj(fileobj)

    def set_timer(self, duration: float, callback: Callable[..., None], *callback_args: Any):
        """
        Set a timer that triggers a callback after a specified duration.

        Args:
            duration (float): Duration in microseconds before the callback is invoked.
            callback (Callable[..., None]): The function to call when the timer expires.
            *callback_args (Any): Additional arguments to pass to the callback.
        """
        self._time = time.perf_counter() * 1_000_000 # Convert it into microseconds
        tick_time = int((self._time + duration))
        self._queue.register_fxn_timer(tick_time, callback, callback_args)


    def _execute(self, callback: Callable[..., None], *args: Any):
        """
        Execute a callback function with the provided arguments.

        Args:
            callback (callable): The function to execute.
            *args: Arguments to pass to the callback.
        """
        self._time = time.perf_counter() * 1_000_000 # Use high-resolution counter for time
        try:
            callback(*args)  # Execute the callback with the provided arguments
        except Exception as err:
            print('Uncaught exception:', err)
        self._time = time.perf_counter() * 1_000_000 # Use high-resolution counter for time