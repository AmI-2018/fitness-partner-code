import socket
import threading

outString = ""
inString = ""


def client_send(sock):
    global outString
    while True:
        outString = input()
        sock.send(outString.encode())


def client_receive(sock):
    global inString
    while True:
        inString = sock.recv(1024).decode()
        print(inString)


host = "127.0.0.1"
port = 8888

s = socket.socket()
print("Socket created")
s.bind((host, port))
s.listen(5)

print("Socket new listening")

while True:
    conn, addr = s.accept()
    print("Connect with " + addr[0] + ":" + str(addr[1]))

    thread_send = threading.Thread(target=client_send, args=(conn,))
    thread_receive = threading.Thread(target=client_receive, args=(conn,))

    thread_send.start()
    thread_receive.start()
