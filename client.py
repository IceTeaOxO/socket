import socket
import threading
import time


# 設定要連接的伺服器IP以及接口
pars = ('127.0.0.1', 8888) 
fileName = "good.html"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 連接伺服器
s.connect(pars)
print("Connect:", str(pars))

#要求good.html檔案
s.send(str(fileName).encode())
data =  s.recv(1024).decode()
print("From server:",data)
# while True:
    
#     # 送出第一則訊息
#     s.send(b'request')
    
#     # 等待伺服器回應
#     data = s.recv(1024)
#     # 印出伺服器回應訊息
#     if data:
#         print("data from server:", data)

#     # 結束連接
#     s.send(b'close')
#     break


print("Receiving " + str(fileName), end ="...")
time.sleep(3)
s.send("<EXIT>".encode())

s.send(b'close')
# 關閉socket
s.close()