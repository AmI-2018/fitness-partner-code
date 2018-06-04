import socket
import threading

outString = ""
inString = ""
running = True


def client_send(sock):
    global outString, running
    print("Start send module!")
    while True:
        data = input()
        if data == "7":
            data = "Start sport music"
        elif data == "0":
            data = "Start warm up music"
        outString = data.encode()
        sock.send(outString)
        if data == "5":
            break
    print("Send module stopped!")


def client_receive(sock):
    print("Start receive module!")
    global inString, running
    while running:
        inString = sock.recv(1024).decode()
        if inString == "5":
            break
        print(inString)
    sock.close()
    print("Receive module stopped!")


ip = "127.0.0.1"
port = 8888
sock = socket.socket()
sock.connect((ip, port))


thread_send = threading.Thread(target=client_send, args=(sock,))
thread_receive = threading.Thread(target=client_receive, args=(sock,))

thread_send.start()
thread_receive.start()
