import socket
import threading
import time

clients = set()

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7002  # Port範圍介於1024~65535，其中0~1023為系統保留不可使用
ADDR = (SERVER, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
s.setblocking(False)  # 將此socket設成非阻塞

def hello():
    time.sleep(1)
    print("Nobody is connecting!")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connect = True
    while connect:
        try:
            msg = conn.recv(1024).decode("utf-8")
            print(f"{addr} says: " + msg)
            for client in clients:
                if client is not conn:
                    client.send((f"{addr} says: " + msg).encode("utf-8"))

        except BlockingIOError:
            # No data available to read, continue or perform other tasks
            pass

        except ConnectionResetError:
            print(f"Connection with {addr} was forcibly closed.")
            clients.remove(conn)
            connect = False

    conn.close()




def start():
    s.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        try:
            conn, addr = s.accept()
            conn.setblocking(False)
            clients.add(conn)
            print(f"Connection established with: {addr}")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

        except:
            pass  # 不理會錯誤
        # print("hi")
        if not clients:
            hello()

print("[STARTING] Server is starting...")

start()