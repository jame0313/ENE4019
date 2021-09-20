import socket

#server connection setting
HOST = '127.0.0.1'
PORT = 54321
BUFFER = 4096
ENCODING = 'UTF-8' #use as codec format

#make socket object
#type of protocol(ipv4 internet address family, tcp)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect socket with ip and port
sock.connect((HOST, PORT))

print('tcpClient connect at: %s:%s\n\r' % (HOST, PORT) )

#get message which wanted to send and send it to server
message = input('send message: ')
sock.send(message.encode(ENCODING))

#get server's response in bytes format (max size: BUFFER)
recv = sock.recv(BUFFER)

#print server's response
print('[tcpServer said]: %s' % recv.decode(ENCODING))

#close socket(connection) before termination
sock.close()
print('connection closed')
