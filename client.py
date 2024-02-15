import socket
import threading
import tkinter
import sys

PORT = 7002
FORMAT = 'utf-8'
SERVER = "192.168.105.1"  # Server IP
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# GUI
window = tkinter.Tk()
window.title("Connected To: " + SERVER + ":" + str(PORT))

txt = tkinter.Text(window, width=100)
txt.grid(row=0, column=0, padx=20, pady=20)

txtYour = tkinter.Entry(window, width=100)
txtYour.insert(0, "Your message")
txtYour.grid(row=1, column=0, padx=20, pady=20)


def send():
    msgtoserver = txtYour.get()
    if msgtoserver == "quit":
        client.close()
        sys.exit(0)
    else:
        txt.insert(tkinter.END, "\n" + "You: " + msgtoserver)
        client.send(msgtoserver.encode("utf-8"))


btnSendMessage = tkinter.Button(window, text="Send", width=20, command=send)
btnSendMessage.grid(row=2, column=0, padx=20, pady=20)


def recvMessage():
    while True:
       try:
            serverMessage = client.recv(1024).decode("utf-8")
            print(serverMessage)
            txt.insert(tkinter.END, "\n" + serverMessage)
            
       except ConnectionAbortedError:
            break


recvThread = threading.Thread(target=recvMessage)  # do func recvMessage
recvThread.daemon = True  # thread will automatically terminate if the main program finishes.
recvThread.start()

print("Client connect to server")

window.mainloop()