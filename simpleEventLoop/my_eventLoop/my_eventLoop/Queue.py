import collections
import heapq
import selectors
import time


'''
Provinding the queue, where we can use pop method to get the next function to execute.
Below class can be hooked up with event loop to simultaneously keep track of functions with timeout, and changes happening at socket.
'''

class Queue:
    def __init__(self):
        self._selector = selectors.DefaultSelector()
        self._timers = []
        self._timer_no = 0  #Counter for next timer information
        self._ready = collections.deque()   #Double ended queue to fetch information easily

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

    '''
    This functions first checks, if there are already present callbacks on the eventloop.
    If nothing already ready to be executed, it checks for events that can be added to the list of callbacks that we can execute.
    '''
    def pop(self, tick):
        if self._ready:
            return self._ready.popleft()

        timeout = None  #We are getting the time we need to wait before first function with the timer will be ready to be executed.
        if self._timers:
            timeout = (self._timers[0][0] - tick) / 10e6 

        events = self._selector.select(timeout) #Select the events happened till timeout, because once we reached timeout, callback from one of the timers will also be ready
        for key, mask in events:
            callback = key.data
            self._ready.append((callback, mask))    #Adding all the callbacks ready to be executed.

        if not self._ready and self._timers:    #If no event happened in the given time, check the timers and check if we need to wait. Also don't waste the compute and make it sleep and callback again.
            idle = (self._timers[0][0] - tick)
            if idle > 0:
                time.sleep(idle / 10e6)
                return self.pop(tick + idle)

        while self._timers and self._timers[0][0] <= tick:  #Check if we can add any timer function to be executed and add that to ready list.
            _, _, callback = heapq.heappop(self._timers)
            self._ready.append((callback, None))

        return self._ready.popleft()    #At this point, we would have some function to execute.

    def is_empty(self):
        return not (self._ready or self._timers or self._selector.get_map())

    def close(self):
        self._selector.close()