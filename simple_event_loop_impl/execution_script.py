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


if __name__ == '__main__':
    print('Run main1()')
    event_loop = EventLoop()
    Context.set_event_loop(event_loop)

    serv_addr = ('127.0.0.1', int(sys.argv[1]))
    event_loop.run(main1, serv_addr)

    # print('\nRun main2()')
    # event_loop = EventLoop()
    # Context.set_event_loop(event_loop)
    # event_loop.run(main2)