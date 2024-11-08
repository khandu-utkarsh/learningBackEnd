#Below lines are needed till I create a package.
import sys
import os

print("Current working running directory of the script")
cwd = os.getcwd()
print(cwd)
sys.path.append(os.path.join(os.path.dirname(__file__), 'simple_functional_event_loop', 'src'))

import simple_functional_event_loop
import client

if __name__ == '__main__':
  #Creating the event loop
  event_loop = simple_functional_event_loop.EventLoop()
  #Setting the execution context
  simple_functional_event_loop.ExecutionContext.set_event_loop(event_loop)

  serv_addr = ('127.0.0.1', 53210)
  event_loop.run(client.main_fxn_1, serv_addr)