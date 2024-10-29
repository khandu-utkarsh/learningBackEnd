#


import collections
import heapq
import selectors
import time

class Queue:
    def __init__(self):
        self._selector = selectors.DefaultSelector()
        self._timers = []
        self._timer_no = 0
        self._ready = collections.deque()

    def register_timer(self, tick, callback):
        timer = (tick, self._timer_no, callback)
        heapq.heappush(self._timers, timer) #By default min heap, so so first one ticking out would be at top
        self._timer_no += 1

    def register_fileobj(self, fileobj, callback):
        self._selector.register(fileobj,
                selectors.EVENT_READ | selectors.EVENT_WRITE,
                callback)

    def unregister_fileobj(self, fileobj):
        self._selector.unregister(fileobj)

    def pop(self, tick):
        if self._ready:
            return self._ready.popleft()

        timeout = None
        if self._timers:
            timeout = (self._timers[0][0] - tick) / 10e6

        events = self._selector.select(timeout)
        for key, mask in events:
            callback = key.data
            self._ready.append((callback, mask))

        if not self._ready and self._timers:
            idle = (self._timers[0][0] - tick)
            if idle > 0:
                time.sleep(idle / 10e6)
                return self.pop(tick + idle)

        while self._timers and self._timers[0][0] <= tick:
            _, _, callback = heapq.heappop(self._timers)
            self._ready.append((callback, None))

        return self._ready.popleft()

    def is_empty(self):
        return not (self._ready or self._timers or self._selector.get_map())

    def close(self):
        self._selector.close()

