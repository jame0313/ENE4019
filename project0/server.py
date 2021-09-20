import socket


#server setting
HOST = '127.0.0.1'
PORT = 54321
BUFFER = 4096
ENCODING = 'UTF-8' #use as codec format

#make socket object
#type of protocol(ipv4 internet address family, tcp)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding socket with ip and port
sock.bind((HOST, PORT))
#start listening
sock.listen(0)

print('tcpServer listen at: %s:%s\n\r' % (HOST, PORT) )

while True:
    #Echo server(echo capitalized client's message)
    
    #accept client's access
    client_sock, client_addr = sock.accept()
    print('%s:%s connected' % client_addr)

    while True:

        #get client's message in bytes format (max size: BUFFER)
        recv = client_sock.recv(BUFFER)

        if not recv:
            #no message from client (disconnected)
            print('%s:%s disconnected' % client_addr)
            client_sock.close()
            break

        print('[Client %s:%s said]: %s' % (client_addr[0], client_addr[1], recv.decode('UTF-8')))

        #send result message to client
        client_sock.send(recv.decode(ENCODING).upper().encode(ENCODING))

#close socket before termination
sock.close()
