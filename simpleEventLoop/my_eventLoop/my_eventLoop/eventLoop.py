from Queue import Queue
from timeUtils import hrtime

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
        """Initialize the event loop with an empty queue and time set to None."""
        self._queue = Queue()
        self._time = None

    def run(self, entry_point, *args):
        """
        Run the event loop starting from the entry point callback.

        Args:
            entry_point (callable): The initial callback to execute.
            *args: Arguments to pass to the entry point callback.
        """
        self._execute(entry_point, *args)

        while not self._queue.is_empty():
            fn, mask = self._queue.pop(self._time)
            self._execute(fn, mask)

        self._queue.close()

    def register_fileobj(self, fileobj, callback):
        """
        Register a file object with a callback for events.

        Args:
            fileobj: The file object to monitor.
            callback (callable): The function to call when the file object is ready.
        """
        self._queue.register_fileobj(fileobj, callback)

    def unregister_fileobj(self, fileobj):
        """
        Unregister a file object.

        Args:
            fileobj: The file object to stop monitoring.
        """
        self._queue.unregister_fileobj(fileobj)

    def set_timer(self, duration, callback):
        """
        Set a timer that triggers a callback after a specified duration.

        Args:
            duration (float): Duration in seconds before the callback is invoked.
            callback (callable): The function to call when the timer expires.
        """
        self._time = hrtime()
        self._queue.register_timer(self._time + duration,
                                   lambda _: callback())

    def _execute(self, callback, *args):
        """
        Execute a callback function with the provided arguments.

        Args:
            callback (callable): The function to execute.
            *args: Arguments to pass to the callback.
        """
        self._time = hrtime()
        try:
            callback(*args)  # new callstack starts
        except Exception as err:
            print('Uncaught exception:', err)
        self._time = hrtime()