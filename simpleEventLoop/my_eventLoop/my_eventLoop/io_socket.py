import socket as _socket
from context import Context
import selectors
import errno
import IOError

'''
Class providing non blocking socket with all the basic functionalities.
'''
class socket(Context):
    def __init__(self, *args):
        self._sock = _socket.socket(*args)  #Mostly tcp socket for networking
        self._sock.setblocking(False)   #Making it non blocking.
        self.evloop.register_fileobj(self._sock, self._on_event)    #Adding the socket to the event loop to monitor it using IO Multiplexing
        # 0 - initial
        # 1 - connecting
        # 2 - connected
        # 3 - closed
        self._state = 0
        self._callbacks = {}

    def connect(self, addr, callback):
        assert self._state == 0
        self._state = 1
        self._callbacks['conn'] = callback
        err = self._sock.connect_ex(addr)
        assert errno.errorcode[err] == 'EINPROGRESS'

    def recv(self, n, callback):
        assert self._state == 2
        assert 'recv' not in self._callbacks

        def _on_read_ready(err):
            if err:
                return callback(err)
            data = self._sock.recv(n)
            callback(None, data)

        self._callbacks['recv'] = _on_read_ready

    def sendall(self, data, callback):
        assert self._state == 2
        assert 'sent' not in self._callbacks

        def _on_write_ready(err):
            nonlocal data
            if err:
                return callback(err)

            n = self._sock.send(data)
            if n < len(data):
                data = data[n:]
                self._callbacks['sent'] = _on_write_ready
            else:
                callback(None)

        self._callbacks['sent'] = _on_write_ready

    def close(self):
        self.evloop.unregister_fileobj(self._sock)  #Closing the socket, removing it from the event loop
        self._callbacks.clear() #Socket has been closed, clear all the callbacks, even if they remained, since can't help
        self._state = 3
        self._sock.close()

    def _on_event(self, mask):  #Defining what to do on following events. Fetching the appropriate callback and calling them.
        if self._state == 1:
            assert mask == selectors.EVENT_WRITE
            cb = self._callbacks.pop('conn')
            err = self._get_sock_error()
            if err:
                self.close()
            else:
                self._state = 2
            cb(err)

        if mask & selectors.EVENT_READ:
            cb = self._callbacks.get('recv')
            if cb:
                del self._callbacks['recv']
                err = self._get_sock_error()
                cb(err)

        if mask & selectors.EVENT_WRITE:
            cb = self._callbacks.get('sent')
            if cb:
                del self._callbacks['sent']
                err = self._get_sock_error()
                cb(err)

    def _get_sock_error(self):
        err = self._sock.getsockopt(_socket.SOL_SOCKET,
                                    _socket.SO_ERROR)
        if not err:
            return None
        return IOError('connection failed',
                       err, errno.errorcode[err])