from socket import socket,AF_INET,SOCK_STREAM

import pymongo 
import json

if __name__ == "__main__":
    serverPort = 8080
    serverSocket= socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print("listening")

    while True:
        cl,addr = serverSocket.accept()
        request = cl.recv(2048)
        request = str(request)
        print(request)


        response = "HTTP/1.1 200 OK\n\n"
        cl.send(response.encode('utf-8'))
        cl.close()

    
