import http.client
from urllib.parse import urlsplit
import io
from PIL import Image, ImageTk
import tkinter

#server connection setting
ENCODING = 'UTF-8' #use as codec format
MISSION_HEADER = "2018008940/JAEMYEONG LEE/WEBCLIENT/COMPUTERNETWORK"

#GET /test/index.html
#POST /test/result.html stuAnswer=1&sno1=2018008940
#POST /test/postHandleTest
#GET /test/366140.jpg

TK_IMG = None

#show data in window
def show_result(data):
    global TK_IMG
    try:
        #text case
        txt_box.delete(1.0,"end")
        txt_box.insert(1.0, data.decode(ENCODING))
    except:
        #img case
        try:
            data = io.BytesIO(data)
            img = Image.open(data)
            TK_IMG = ImageTk.PhotoImage(image=img)
            txt_box.image_create(1.0,image=TK_IMG)
        except:
            #other case
            print("Error: Can't render data in window")


#send message to server
def send_message(conn, message):
    #message format: "METHOD URL BODY"
    message = message.split(' ')
    print(*message)
    
    responded = False
    retry_cnt = 0

    #request max 10 times
    while not responded and retry_cnt < 10:
        try:
            #request
            conn.request(*message, headers = {"User-Agent" : MISSION_HEADER})
            response = conn.getresponse()
            data = response.read()
            responded = True
            
        except:
            #request failed
            print("Request Failed: Try to reconnect...")
            conn.connect()
            retry_cnt += 1
            
    if not responded:
        #fail case
        print("Connection Failed")
        return False

    #show data
    return show_result(data)

#handle url request to make message
def handle_request(query):
    
    print("Query:", query)
    
    #split query
    query = query.strip().split(' ')

    #parse url
    url = urlsplit(query[0])
    host = url.netloc
    
    if not host:
        #add url scheme
        url = urlsplit("http://" + query[0])
        host = url.netloc
    
    print("HOST: ", host)
    
    if url.scheme == 'https':
        #HTTPS case
        conn = http.client.HTTPSConnection(host)
    else:
        #HTTP case
        conn = http.client.HTTPConnection(host)
        
    if len(query) == 1:
        #GET case
        return send_message(conn, "GET " + url.path)
    else:
        #POST case
        return send_message(conn, "POST "+ url.path + ' ' + query[1])

#GUI part

#make window
win = tkinter.Tk()

#config window
win.title("WebClient")
win.geometry("600x400")
win.resizable(width=False, height=False)

#url input box
entry = tkinter.Entry(win, width = 40)
entry.bind("<Return>",lambda x : handle_request(entry.get()))

#send button
send_button = tkinter.Button(win, text="OK", overrelief="solid", command=lambda : handle_request(entry.get()))

#text box to show web page and image
txt_box = tkinter.Text(win, width=80, height=20)

#scrollbar for textbox
ys = tkinter.Scrollbar(win, orient = 'vertical', command = txt_box.yview)
txt_box['yscrollcommand'] = ys.set

#logo image
logoObj = tkinter.PhotoImage(file="icon.gif")
img_label = tkinter.Label(win, relief="solid", image=logoObj)

#pack widget to window
ys.pack(side='right', fill='y')
entry.pack(pady = 10)
send_button.pack()
txt_box.pack(pady = 5)
img_label.pack(pady = 10)

win.mainloop()
