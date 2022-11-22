import socket
import threading

# 創建socket實例，設定L3 L4 protocol(IP/TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pars = ('127.0.0.1', 8888)


# 設定伺服器IP以及接口，讓server run 在 post=8888 IP=127.0.0.1上
s.bind(pars)
# 設定連接上限
s.listen(5)

#html = "<html><head><link href=”style.css” rel=”stylesheet” type=”text/css”></head><body>good</body></html>"
html = '<html><head><link href="style.css" rel="stylesheet" type = "text/css"></head><body>good</body></html>'
css = 'Body {color: red;}'

# 伺服器傳送給客戶端的資料
def resM(code,obj):
    resH=""
    if str(code)=="200":
        resH += "HTTP/1.1 "+"200 OK"+" \r\n"
    elif str(code)=="301":
        resH += "HTTP/1.1 "+"301 Moved Permanently\r\nLocation: http://127.0.0.1:8888/good.html"+"\r\n\r\n"
    elif str(code)=="404":
        resH = "HTTP/1.1 "+"404 NotFound"+" \r\n"
    resH += "Content-Type: text/html; charset=UTF-8\r\n"
    resH += "\r\n"
    
    if obj:    
        resH += str(obj)

    print(resH)
    return resH



# 當有客戶端連接時，執行下列方法
def serveClient(clientsocket, address):
    
    # 持續接收客戶端的訊息
    while True:
        # 設定一次可接收資料的大小
        data = clientsocket.recv(1024)
        #print("from client", data)
        
        # 如果有收到資料，則回送
        if data:
            cData = data.decode("utf-8").split(' ')
            print((cData))
            method = cData[0]
            url = cData[1]

            if url=="/":
                res = resM(200,html)
                print(200)
                clientsocket.send(bytes(res,"UTF-8"))

            if url=="/good.html":
                
                res = resM(200,html)
                print(200)
                #print(res)
                clientsocket.send(bytes(res,"UTF-8"))
            
            if url=="/style.css":
                res = resM(200,css)
                print(css)
                clientsocket.send(bytes(res,"UTF-8"))
            if url=="/redirect.html":
                res = resM(301,"redirect")
                print(301)
                #print(res)
                clientsocket.send(bytes(res,"UTF-8"))

                clientsocket.close()
                break
            if url=="/notfound":
                res = resM(404,'notfound')
                print(404)
                #print(res)
                clientsocket.send(bytes(res,"UTF-8"))
            #clientsocket.send(b'response')
            clientsocket.close()
            break
        # 如果客戶端送出結束訊息，則關閉連線，跳出迴圈
        if data == b'close':
            clientsocket.close()
            break




# 使用(src IP, dst IP, src port, dst port)分辨不同使用者
while True:
    # accept a new client and get it's information
    
    (clientsocket, address) = s.accept()
    # print(clientsocket)
    # print(address)
    
    
    # 當有新客戶端連上，則為他多開一個線程，開啟線程後執行target
    
    threading.Thread(target = serveClient, args = (clientsocket, address)).start()


    



