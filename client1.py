import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


pars = ('127.0.0.1', 8888) # 設定要連接的伺服器IP以及接口
# 連接伺服器
s.connect(pars)

while True:
    for i in range(4):
        # 送出第一則訊息
        s.send(b'request')
        # s.send(b'second obj')
        
        # 等待伺服器回應
        data = s.recv(1024)
        # 印出伺服器回應訊息
        if data:
            print("data from server:", data)

    # 結束連接
    s.send(b'close')
    break
    
# 關閉socket
s.close()