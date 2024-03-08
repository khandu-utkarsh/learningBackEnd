#Higher level over socket
#So we are operating at higher level or socket


import urllib.request

fhand  = urllib.request.urlopen('http://127.0.0.1:9000/romeo.txt')
for line in fhand:
    print(line.decode().strip())