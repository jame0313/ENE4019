import socket
import os

BUFFER = 4096
ENCODING = 'UTF-8' #use as codec format
#use for get response phrase
RESPONSE_CODE_MAP = {200: "OK", 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
HTTP_VERSION = "HTTP/1.1"
CRLF = "\r\n"
DEFAULT_HOMEPAGE = "index.html" #set your homepage file

#get content type by extension
def get_content_type(ex):
    if ex == '.jpg':
        return "image/jpeg"
    elif ex == '.html':
        return "text/html"
    else:
        return "application/octet-stream"

#make response line given code number
def make_response_line(code):
    return HTTP_VERSION + ' ' + str(code) + ' ' + RESPONSE_CODE_MAP[code] + CRLF
        

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
        request_header = recv.split(CRLF)
        request_line = request_header[0]
        method, URL, version = request_line.split(' ')

        #set default homepage
        if URL == '/':
            URL += DEFAULT_HOMEPAGE
        
        print('[Client %s:%s request]: %s' % (client_addr[0], client_addr[1], request_line))
        #implement GET method
        if method == 'GET':
            
            #find requested file path
            basedir = os.getcwd()
            filepath = os.path.realpath(os.path.join(basedir + URL))

            #not server file case(forbidden)
            if basedir != os.path.commonpath((basedir, filepath)):
                ret = make_response_line(403) + CRLF
                client_sock.send(ret.encode(ENCODING))
                break
            
            elif os.path.isfile(filepath):
                #http 1.0 request case(bad request)
                if version != HTTP_VERSION:
                    ret = make_response_line(400) + CRLF
                    client_sock.send(ret.encode(ENCODING))
                    break

                #correct URL case(OK)
                else:
                    ex = os.path.splitext(filepath)[1] #extension
                    siz = os.path.getsize(filepath) #size of file
                    
                    #make response header
                    ret = make_response_line(200)
                    ret += "Connection: closed" + CRLF
                    ret += "Content-Type: " + get_content_type(ex) + CRLF
                    ret += "Content-Length: " + str(siz) + CRLF
                    ret += CRLF
                    
                    #encoding first before append entity body
                    ret = ret.encode(ENCODING) 

                    #append entity body
                    with open(filepath, 'rb') as f:
                        ret += f.read()
                    client_sock.send(ret)
                    break
                
            #can't find requested file(Not found)
            else:
                ret = make_response_line(404) + CRLF
                client_sock.send(ret.encode(ENCODING))
                break
        elif method == 'POST':
            #make response header
            ex = os.path.splitext(URL)[1] #extension
            pos_msg = "You posted " + URL + "\n"
            ret = make_response_line(200)
            ret += "Connection: closed" + CRLF
            ret += "Content-Type: " + get_content_type(ex) + CRLF
            ret += "Content-Length: " + str(len(pos_msg)) + CRLF
            ret += CRLF
            ret += pos_msg
                    
            #encoding first before append entity body
            ret = ret.encode(ENCODING) 

            client_sock.send(ret)
            break
            
    #close socket before return
    print('%s:%s disconnected' % client_addr)
    client_sock.close()
    return
