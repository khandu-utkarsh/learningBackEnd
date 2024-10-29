# import socket as _socket

# class socket:
#     def __init__(self, *args):
#         slef._sock =_socket.socket(*args)
#         self._sock.setblocking(False)
#         self.evloop.register_fileobj(self._sock, self._on_event)
        

# ## This function is basically tring to connect to a sever at the given address and then
# #  sending message to the socket. It then waits and recive message from the client
# #  and print it on the screen.
# def main():
#     sock = socket(_._socket.AF_INET, _socket.SOCK_STREAM)

#     def on_timer():

#         def on_conn(err):
#             if err:
#                 raise err
        
#             def on_sent(err):
#                 if err:
#                     sock.close()
#                     raise err
        
#                 def on_read(err, data=None):
#                     sock.close()
#                     if err:
#                         raise err
#                     print(data)
        
#                 sock.recv(1024, on_read)

#             sock.sendall(b'foobar', on_sent)

#         sock.connect(('127.0.0.1', 53210), on_conn)
    
#     set_timer(1000, on_timer)   #Time is in microseconds hence this is 1 second.

# #Defining the event loop and passing the main function to execute it.
# event_loop = EventLoop()
# Context.set_event_loop(event_loop)
# event_loop.run(main)


# class set_timer(Context):
#     def __init__(self, duration, callback):
#         """ duration in microseconds """
#         self.evloop.set_timer(duration, callback)

# class Context:
#     _event_loop = None

#     @classmethod
#     def set_event_loop(cls, event_loop):
#         cls._event_loop = event_loop


#     @property
#     def evloop(self):
#         return self._event_loop

class EventLoop:
    def __init__(self):
        self._queue = Queue()
        self._time = None

    def run(self, entry_point, *args):
        self._execute(entry_point, *args)

        while not self._queue.is_empty():
            fn, mask = self._queue.pop(self._time)
            self._execute(fn, mask)

        self._queue.close()

    def register_fileobj(self, fileobj, callback):
        self._queue.register_fileobj(fileobj, callback)

    def unregister_fileobj(self, fileobj):
        self._queue.unregister_fileobj(fileobj)

    def set_timer(self, duration, callback):
        self._time = hrtime()
        self._queue.register_timer(self._time + duration,
                                   lambda _: callback())

    def _execute(self, callback, *args):
        self._time = hrtime()
        try:
            callback(*args)  # new callstack starts
        except Exception as err:
            print('Uncaught exception:', err)
        self._time = hrtime()
