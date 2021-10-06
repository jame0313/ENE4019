import socket
import threading
import httprequest

#server setting
HOST = ''
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

print('tcpServer listen at: %s:%s\r\n' % sock.getsockname() )

while True:

    #accept client's access
    client_sock, client_addr = sock.accept()
    
    print('%s:%s connected' % client_addr)

    #make deamon thread and run
    th = threading.Thread(target = httprequest.handle_request, args = (client_sock, client_addr))
    th.daemon = True
    th.start()
        

#close socket before termination
sock.close()
