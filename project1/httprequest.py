import socket
import os

BUFFER = 4096
ENCODING = 'UTF-8' #use as codec format

def get_content_type(ex):
    if ex == '.jpg':
        return "image/jpeg"
        ret += "Content-Type: " + "" + "\r\n"
    elif ex == '.html':
        return "text/html"
    else:
        return "application/octet-stream"

#handle http requset
def handle_request(client_sock, client_addr):
    while True:
        #get client's request in bytes format (max size: BUFFER)
        recv = client_sock.recv(BUFFER)
        
        if not recv:
            #no message from client (disconnected)
            print('%s:%s disconnected' % client_addr)
            client_sock.close()
            return
        
        #decode request to string
        recv = recv.decode(ENCODING)

        #get header info        
        request_header = recv.split('\r\n')
        request_line = request_header[0]
        method, URL, version = request_line.split(' ')
        
        print('[Client %s:%s request]: %s' % (client_addr[0], client_addr[1], request_line))

        #implement GET method
        if method == 'GET':
            
            #find requested file path
            basedir = os.getcwd()
            filepath = os.path.realpath(os.path.join(basedir + URL))

            #not server file case(forbidden)
            if basedir != os.path.commonpath((basedir, filepath)):
                ret = "HTTP/1.1 403 Forbidden\r\n\r\n"
                client_sock.send(ret.encode(ENCODING))
                break
            
            elif os.path.isfile(filepath):
                #http 1.0 request case(bad request)
                if version != 'HTTP/1.1':
                    ret = "HTTP/1.1 400 Bad Request\r\n\r\n"
                    client_sock.send(ret.encode(ENCODING))
                    break

                #correct URL case(OK)
                else:
                    ex = os.path.splitext(filepath)[1] #extension
                    siz = os.path.getsize(filepath) #size of file
                    
                    #make response header
                    ret = "HTTP/1.1 200 OK\r\n" + "Connection: closed\r\n"
                    ret += "Content-Type: " + get_content_type(ex) + "\r\n"
                    ret += "Content-Length: " + str(siz) + "\r\n"
                    ret += "\r\n"
                    
                    #encoding first before append entity body
                    ret = ret.encode(ENCODING) 

                    #append entity body
                    with open(filepath, 'rb') as f:
                        ret += f.read()
                        
                    client_sock.send(ret)
                    break
            #can't find requested file(Not found)
            else:
                ret = "HTTP/1.1 404 Not Found\r\n"
                client_sock.send(ret.encode(ENCODING))
                break
    #close socket before return
    print('%s:%s disconnected' % client_addr)
    client_sock.close()
    return
