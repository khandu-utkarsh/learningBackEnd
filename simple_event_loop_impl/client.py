from simple_functional_event_loop import Socket as socket, SetTimeout as set_timer
import json
import random
from typing import Callable, Optional, Tuple, Dict, Any

class Client:
    """
    A simple client for interacting with a server over a socket connection to fetch user and account data.

    Attributes:
        addr (tuple): Address of the server in the form (host, port).
    """

    def __init__(self, addr: Tuple[str, int]):
        """
        Initialize the Client with a server address.

        Args:
            addr (tuple): Server address as a (host, port) tuple.
        """
        self.addr = addr

    def get_user(self, user_id: int, callback: Callable[[Optional[Exception], Optional[Dict[str, Any]]], None]) -> None:
        """
        Request user details by user ID from the server.

        Args:
            user_id (int): The ID of the user to retrieve.
            callback (function): A callback function to handle the response. 
                                 It accepts two arguments: an error and user data (if successful).
        """
        self._get(f'GET user {user_id}\n', callback)

    def get_balance(self, account_id: int, callback: Callable[[Optional[Exception], Optional[Dict[str, Any]]], None]) -> None:
        """
        Request account balance by account ID from the server.

        Args:
            account_id (int): The ID of the account to retrieve.
            callback (function): A callback function to handle the response. 
                                 It accepts two arguments: an error and account data (if successful).
        """
        self._get(f'GET account {account_id}\n', callback)

    def _get(self, req: str, callback: Callable[[Optional[Exception], Optional[Dict[str, Any]]], None]) -> None:
        """
        Send a request to the server and handle the response.

        Args:
            req (str): The request string to send.
            callback (function): A callback function to handle the response. 
                                 It accepts two arguments: an error and parsed data (if successful).
        """
        sock = socket(socket.AF_INET, socket.SOCK_STREAM)

        def _on_conn(err: Optional[Exception]) -> None:
            if err:
                return callback(err)

            def _on_sent(err: Optional[Exception]) -> None:
                if err:
                    sock.close()
                    return callback(err)

                def _on_resp(err: Optional[Exception], resp: Optional[bytes] = None) -> None:
                    sock.close()
                    if err:
                        return callback(err)
                    try:
                        data = json.loads(resp.decode('utf-8'))
                        callback(None, data)
                    except json.JSONDecodeError as json_err:
                        callback(json_err)

                sock.recv(1024, _on_resp)

            sock.sendall(req.encode('utf-8'), _on_sent)

        sock.connect(self.addr, _on_conn)


def get_user_balance(serv_addr: Tuple[str, int], user_id: int, done: Callable[[Optional[Exception], Optional[str]], None]) -> None:
    """
    Fetch a user's account balance and print a summary.

    Args:
        serv_addr (tuple): Server address as a (host, port) tuple.
        user_id (int): The ID of the user whose balance is requested.
        done (function): A callback function to handle the final response or error. 
                         It accepts two arguments: an error and a summary string (if successful).
    """
    client = Client(serv_addr)

    def on_timer() -> None:
        def on_user(err: Optional[Exception], user: Optional[Dict[str, Any]] = None) -> None:
            if err:
                return done(err)

            def on_account(err: Optional[Exception], acc: Optional[Dict[str, Any]] = None) -> None:
                if err:
                    return done(err)
                done(None, f'User {user["name"]} has {acc["balance"]} USD')

            try:
                if user_id % 5 == 0:
                    raise Exception('Do not throw from callbacks')
                if user:
                    client.get_balance(user['account_id'], on_account)
            except Exception as e:
                done(e)

        client.get_user(user_id, on_user)

    # Set a random delay for the timer
    delay = random.randint(0, int(10e6))
    set_timer(delay, on_timer)

def main_fxn_1(serv_addr):
    def on_balance(err, balance=None):
        if err:
            print('ERROR', err)
        else:
            print(balance)

    for i in range(10):
        get_user_balance(serv_addr, i, on_balance)

