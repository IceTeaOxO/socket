import socket
import threading

#file area
html = '<html><head><link href="style.css" rel="stylesheet" type = "text/css"></head><body>good</body></html>'
css = 'Body{color:red;}'

#response message area, when server receive different type of request, it will call
#this funciton to create the respectively message to client
def respM(number,obj):
    message = 'HTTP/1.1 '+ str(number)
    if number == 200:
        message += ' OK\n '
        if obj == 'html':
            message += 'Content-Type: text/html;\r\n\r\n' + html
        if obj == 'css':
            message += 'Context-Type: text/css;\r\n\r\n' + css
    elif number == 301:
        message += ' Moved Permanently\r\nLocation: http://127.0.0.1:8888/good.html\r\n\r\n'
    elif number == 404:
        message += ' Not Found\r\n\r\n'
    return message

# create socket and set port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pars = ('127.0.0.1', 8888) # you can change the server port to whatever you want
s.bind(pars)
s.listen(5)

# a thread serve the client
def serveClient(clientsocket, address):
    
    # we need a loop to continuously receive messages from the client
    while True:
        data = clientsocket.recv(1024)
        print("from client", data)
        
        # if the received data is not empty, then we send something back by using send() function
        if data:
            # change the byte-like data to string first, and use str.split to identify the 
            # messenge of the user
            newData = data.decode("utf-8").split(' ')
            method = newData[0]
            url = newData[1]
            # check what user want to get, and create the respective response message to client
            # by resM function, and turn it to byte-like data and send to client
            if url == '/good.html':
                resp = respM(200,'html')
                clientsocket.send(bytes(resp,'UTF-8'))
            elif url == '/style.css':
                resp = respM(200,'css')
                clientsocket.send(bytes(resp,'UTF-8'))
            elif url == '/redirect.html':
                resp = respM(301,'0')
                clientsocket.send(bytes(resp,'UTF-8'))
            elif url == '/notfound.html':
                resp = respM(404,'0')
                clientsocket.send(bytes(resp,'UTF-8'))
            else:
               resp = respM(404,'0')
               clientsocket.send(bytes(resp,'UTF-8')) 
            # after send the data, close the socket
            clientsocket.close()
            break
        

while True:
    (clientsocket, address) = s.accept()
    threading.Thread(target = serveClient, args = (clientsocket, address)).start()