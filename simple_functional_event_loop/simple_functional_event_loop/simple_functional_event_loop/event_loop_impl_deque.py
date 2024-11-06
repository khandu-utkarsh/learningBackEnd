from collections import deque  #For dobule ended queue
import heapq
import selectors    #For IO Multiplexing
import time
from typing import Callable, Any, Tuple, List

class EventLoopDequeImpl:
    """
    A class that implements an event loop using a deque for scheduling functions 
    and a heap for managing timers.

    Attributes:
        _selector (selectors.BaseSelector): The selector for I/O events.
        _timers (List[Tuple[int, int, Callable[..., None], Tuple[Any]]]): A list of timers, 
            where each timer is a tuple containing the tick time, timer ID, callback function, 
            and its arguments.
        _timer_no (int): Counter for the next timer's identifier.
        _ready (deque): A deque holding functions ready to be executed.
    """
    
    def __init__(self) -> None:
        self._selector: selectors.BaseSelector = selectors.DefaultSelector()
        self._timers: List[Tuple[int, int, Callable[..., None], Tuple[Any]]] = []
        self._timer_no: int = 0  # Counter for the next timer information
        self._ready: deque[Tuple[Callable[..., None], Tuple[Any, ...], Optional[int]]] = deque()

    
    def register_fxn_timer(self, curr_tick: int, callback: Callable[..., None], 
                           callback_args: Tuple[Any, ...]) -> None:
        """
        Register a timer with the event loop.

        Args:
            curr_tick (int): The current tick time for the timer.
            callback (Callable[..., None]): The function to be called when the timer expires.
            callback_args (Tuple[Any, ...]): The arguments to pass to the callback function.

        Returns:
            None
        """
        timer = (curr_tick, self._timer_no, callback, callback_args)
        heapq.heappush(self._timers, timer)  # By default min heap, so the first one ticking out would be at the top
        self._timer_no += 1

    def register_file_obj(self, file_obj: Any, callback: Callable[..., None], 
                           callback_args: Tuple[Any, ...]) -> None:
        """
        Register a file object with the event loop for read/write events.

        Args:
            file_obj (Any): The file object to register.
            callback (Callable[..., None]): The function to call when the event occurs.
            callback_args (Tuple[Any, ...]): The arguments to pass to the callback function.

        Returns:
            None
        """
        self._selector.register(file_obj, selectors.EVENT_READ | selectors.EVENT_WRITE, (callback, callback_args))


    def unregister_file_obj(self, file_obj: Any) -> None:
        """
        Unregister a file object from the event loop.

        Args:
            file_obj (Any): The file object to unregister.

        Returns:
            None
        """
        self._selector.unregister(file_obj)

    def pop(self, tick: int) -> Optional[Tuple[Callable[..., None], Optional[int]]]:
        """
        Retrieve the next callback to execute.

        This function checks for any ready callbacks. If none are ready, it waits for events 
        that can be added to the list of callbacks to execute.

        Args:
            tick (int): The current tick time.

        Returns:
            Optional[Tuple[Callable[..., None], Optional[int]]]: The next callback to execute 
            and its mask, or None if there are no callbacks ready.
        """
        if self._ready:
            return self._ready.popleft()

        timeout = None  # Determine how long to wait before the next function is ready to execute.
        if self._timers:
            timeout = (self._timers[0][0] - tick) / 1_000_000  # Convert microseconds to seconds

        events = self._selector.select(timeout)  # Wait for events until the timeout
        for key, mask in events:
            callback, callback_args = key.data
            self._ready.append((callback, callback_args, mask))  # Add all callbacks ready to be executed.

        if not self._ready and self._timers:  # If no events occurred in the given time
            idle = (self._timers[0][0] - tick)
            if idle > 0:
                time.sleep(idle / 1_000_000)  # Sleep for the remaining idle time
                return self.pop(tick + idle)

        while self._timers and self._timers[0][0] <= tick:  # Check for expired timers
            _, _, callback, callback_args = heapq.heappop(self._timers)
            self._ready.append((callback, callback_args, None))  # Add timer callbacks to ready list

        return self._ready.popleft()  # Return the next function to execute.

    def is_empty(self) -> bool:
        """
        Check if the event loop is empty.

        Returns:
            bool: True if there are no ready callbacks, timers, or registered file objects; False otherwise.
        """
        return not (self._ready or self._timers or self._selector.get_map())

    def close(self) -> None:
        """
        Close the event loop and clean up resources.

        Returns:
            None
        """
        self._selector.close()




