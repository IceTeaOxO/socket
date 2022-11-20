
# 引入需要使用的函式庫
import socket
import threading

#創建socket實例，設定L3 L4 protocol(IP/TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 設定伺服器IP以及接口，讓server run 在 post=8888 IP=127.0.0.1上
pars = ('127.0.0.1', 8888) # you can change the server port to whatever you want
s.bind(pars)

# 設定連接上限
s.listen(5)


# 當有客戶端連接時，執行下列方法
def serveClient(clientsocket, address):
    
    # 持續接收客戶端的訊息
    while True:
        
        # 設定一次可接收資料的大小
        data = clientsocket.recv(1024)
        print("from client", data)
        
        # 如果有收到資料，則回送
        if data:
            clientsocket.send(b'response')
        
        # 如果客戶端送出結束訊息，則關閉連線，跳出迴圈
        if data == b'close':
            clientsocket.close()
            break


# 使用(src IP, dst IP, src port, dst port)分辨不同使用者
while True:
    # accept a new client and get it's information
    (clientsocket, address) = s.accept()
    
    # 當有新客戶端連上，則為他多開一個線程，開啟線程後執行target
    
    threading.Thread(target = serveClient, args = (clientsocket, address)).start()