##Above lines are temporary to debug and look into pacakage.

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'simple_functional_event_loop', 'src'))

#
import simple_functional_event_loop
import client
# def main2(*args):
#   sock = socket(_socket.AF_INET, _socket.SOCK_STREAM)

#   def on_conn(err):
#     if err:
#       return print(err)

#     def on_sent(err):
#       if err:
#         sock.close()
#         return print(err)

#       def on_resp(err, resp=None):
#         sock.close()
#         if err:
#           return print(err)
#         print(resp)

#       sock.recv(1024, on_resp)

#     sock.sendall(b'GET / HTTP/1.1\r\nHost: t.co\r\n\r\n', on_sent)

#   sock.connect(('t.co', 80), on_conn)


# if __name__ == '__main__':
print("Running the first function...")

#Creating the event loop
event_loop = simple_functional_event_loop.EventLoop()
#Setting the execution context
simple_functional_event_loop.ExecutionContext.set_event_loop(event_loop)

serv_addr = ('127.0.0.1', 53210)
event_loop.run(client.main_fxn_1, serv_addr)

    # print('\nRun main2()')
    # event_loop = EventLoop()
    # Context.set_event_loop(event_loop)
    # event_loop.run(main2)