import json
import random
import sys
from socketserver import BaseRequestHandler, TCPServer
from uuid import uuid4
from typing import Dict, Any, Tuple


class Handler(BaseRequestHandler):
    """
    A request handler for managing user and account data over TCP.

    This handler supports GET requests for retrieving `user` or `account`
    data. If a user or account doesn't exist, it creates default entries
    with randomized or default values.
    """

    # Shared dictionaries to store user and account information
    users: Dict[str, Dict[str, Any]] = {}
    accounts: Dict[str, Dict[str, Any]] = {}

    def handle(self) -> None:
        """
        Handles incoming TCP requests from the client. 
        Parses the request, retrieves or creates user or account data, 
        and sends the response back to the client.
        """
        client = f'client {self.client_address}'
        try:
            # Receive the request from the client
            request_data = self.request.recv(1024)
            if not request_data:
                print(f'{client} unexpectedly disconnected')
                return

            print(f'{client} < {request_data}')
            request_text = request_data.decode('utf8').strip()
            if not request_text:
                raise ValueError('Empty request received')

            # Parse and validate the request format
            method, entity_kind, entity_id = self.parse_request(request_text)
            
            # Process the request based on entity type
            if entity_kind == 'user':
                response_data = self.get_or_create_user(entity_id)
            elif entity_kind == 'account':
                response_data = self.get_account(entity_id)
            else:
                raise ValueError('Unknown entity kind')

            # Send the response
            self.send_response(response_data)

        except Exception as e:
            print(f'{client} error: {e}')
            self.send_response({'error': str(e)})

    def parse_request(self, request_text: str) -> Tuple[str, str, str]:
        """
        Parses and validates the request format.

        Args:
            request_text (str): The received request text.

        Returns:
            tuple: (method, entity_kind, entity_id)

        Raises:
            ValueError: If the request format is invalid.
        """
        parts = request_text.split()
        if len(parts) != 3:
            raise ValueError('Invalid request format')
        
        method, entity_kind, entity_id = parts
        if method != 'GET':
            raise ValueError('Only GET requests are supported')
        if entity_kind not in ('user', 'account'):
            raise ValueError('Invalid entity kind')
        if not entity_id.isdigit():
            raise ValueError('Entity ID must be numeric')

        return method, entity_kind, entity_id

    def get_or_create_user(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieves an existing user or creates a new one if not found.

        Args:
            user_id (str): The user ID.

        Returns:
            dict: The user data with an associated account.
        """
        # Fetch or create user
        user = self.users.setdefault(user_id, {'id': user_id})

        # Assign a unique name if it doesn't exist
        if 'name' not in user:
            user['name'] = str(uuid4()).split('-')[0]

        # Assign an account to the user if not already assigned
        if 'account_id' not in user:
            account_id = str(len(self.accounts) + 1)
            account = {'id': account_id, 'balance': random.randint(0, 100)}
            self.accounts[account_id] = account
            user['account_id'] = account_id

        return user

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        Retrieves an existing account based on account ID.

        Args:
            account_id (str): The account ID.

        Returns:
            dict: The account data.

        Raises:
            KeyError: If the account ID does not exist.
        """
        if account_id not in self.accounts:
            raise KeyError(f'Account ID {account_id} not found')
        return self.accounts[account_id]

    def send_response(self, data: Dict[str, Any]) -> None:
        """
        Sends a JSON-encoded response to the client.

        Args:
            data (dict): The response data to send.
        """
        response = json.dumps(data).encode('utf8')
        print(f'client {self.client_address} > {response}')
        self.request.sendall(response)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
        
    port = int(sys.argv[1])
    with TCPServer(('127.0.0.1', port), Handler) as server:
        print(f'Server started on port {port}')
        server.serve_forever()

