from socket import socket, AF_INET, SOCK_STREAM
import time

if __name__ == '__main__':
    serverPort = 1234

    serverSocket = socket(AF_INET,SOCK_STREAM) ## LISTENING SOCKET!!!
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept() ## RETURNS CONNECTION SOCKET!!!
        print('accept')
        sentence = connectionSocket.recv(2048) 
        print('recv')
        # Processing
        capitalizedSentence = sentence.upper()

        connectionSocket.send(capitalizedSentence)
        print ("server handled: " + str(addr) + " with message: " + sentence.decode('utf-8'))
        connectionSocket.close()
