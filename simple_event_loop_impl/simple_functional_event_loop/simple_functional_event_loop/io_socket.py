import socket as _socket    #Python's scoket clas
from execution_context import ExecutionContext
import selectors
import errno
from typing import Callable, Any

'''
Class providing non blocking socket with all the basic functionalities.
'''
class Socket(ExecutionContext):
    """
    A class providing a non-blocking socket with all the basic functionalities.
    
    This class extends `ExecutionContext` to utilize the event loop for monitoring
    and managing non-blocking socket operations.

    Methods:
        connect(addr, callback): Initiates a non-blocking connection to a given address.
        recv(n, callback): Starts a non-blocking receive operation with a specified number of bytes.
        sendall(data, callback): Sends all data non-blockingly.
        close(): Closes the socket and unregisters it from the event loop.
    """

    def __init__(self, *args: Any) -> None:
        """
        Initializes the socket object.
        
        Sets the socket to non-blocking mode and registers it with the event loop.
        
        Args:
            *args: Arguments to pass to the socket constructor (typically family, type, etc.).
        """
        self._sock = _socket.socket(*args)  # Mostly TCP socket for networking
        self._sock.setblocking(False)  # Making it non-blocking.

        #Register the socket to the event loop, and provide the callback function
        self.evloop.register_fileobj(self._sock, self._on_event)  # Adding the socket to the event loop
        self._state = 0  # 0 - initial, 1 - connecting, 2 - connected, 3 - closed
        self._callbacks = {}    #Dict of callbacks for this socket. 

    def connect(self, addr: tuple[str, int], callback: Callable[[Any], None]) -> None:
        """
        Initiates a non-blocking connection to the specified address.
        
        Args:
            addr (tuple): Address to connect to (host, port).
            callback (callable): A callback to invoke once the connection completes.
        """
        assert self._state == 0
        self._state = 1
        
        def _on_connect_ready(err: Optional[str]) -> None:
            if err:
                return callback(err)  # Invoke the callback with error if there's an issue
            
            # Connection has succeeded, update state and invoke the callback
            self._state = 2
            callback(None)  # Connection successful, pass None as error

        self._callbacks['conn'] = _on_connect_ready
        
        err = self._sock.connect_ex(addr)
        if errno.errorcode[err] == 'EINPROGRESS':
            # Connection is in progress
            return
        else:
            # Handle failure if the connection attempt did not start correctly
            _on_connect_ready(errno.errorcode.get(err, 'Unknown Error'))



    def recv(self, n: int, callback: Callable[[Any, bytes], None]) -> None:
        """
        Starts a non-blocking receive operation with the specified number of bytes.
        
        Args:
            n (int): Number of bytes to receive.
            callback (callable): A callback to invoke with the received data or error.
        """
        assert self._state == 2
        assert 'recv' not in self._callbacks

        def _on_read_ready(err: Optional[str]) -> None:
            if err:
                return callback(err, b'')
            data = self._sock.recv(n)
            callback(None, data)

        self._callbacks['recv'] = _on_read_ready

    def sendall(self, data: bytes, callback: Callable[[Any], None]) -> None:
        """
        Sends all data in a non-blocking manner.
        
        Args:
            data (bytes): Data to send.
            callback (callable): A callback to invoke when sending completes or fails.
        """
        assert self._state == 2
        assert 'sent' not in self._callbacks

        def _on_write_ready(err: Optional[str]) -> None:
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

    def close(self) -> None:
        """
        Closes the socket and unregisters it from the event loop.
        Clears all callbacks and sets the state to closed.
        """
        self.evloop.unregister_fileobj(self._sock)  # Unregistering from event loop
        self._callbacks.clear()  # Clear callbacks
        self._state = 3  # Closed state
        self._sock.close()

    def _on_event(self, mask: int) -> None:
        """
        Defines what to do on various events. Fetches the appropriate callback and calls it.
        
        Args:
            mask (int): A bitmask representing the events triggered on the socket.
        """
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


    def _get_sock_error(self) -> Optional[OSError]:
        """
        Checks if there is any socket error.

        Returns:
            OSError or None: Returns the error if any, otherwise None.
        """
        err = self._sock.getsockopt(_socket.SOL_SOCKET, _socket.SO_ERROR)
        if not err:
            return None
        return OSError('Connection failed', err, errno.errorcode[err])