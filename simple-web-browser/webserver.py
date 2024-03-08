from socket import *

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        serversocket.bind(('localhost', 9000))  #Binding it to port and ip. There could only be one program listenting to one port. 
        #So, on running this application on two terminals, one will popup error message.
        serversocket.listen(5) # It tells the operating system to queue up to 5 total connect requests. If server is working on one, it will queue up 4 more.
        #If this is not specified, os will drop any request if server is busy.
        while(1):
            (clientsocket, address) = serversocket.accept()
            rd = clientsocket.recv(5000).decode()   #Limiting the number of character in the message
            pieces = rd.split("\n")
            if (len(pieces) > 0) :print(pieces[0])
            #print(rd) For seeing what is sent by the browser
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += "<html><body>Hello World </body></html>\r\n\r\n"
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        print("\nShutting down the server because of keyboard interrupt\n")
    except Exception as exc:
        print("Error: \n")
        print(exc)

    serversocket.close()
print("Access http://localhost:9000")
createServer()