import socket
import threading
import simplejson

outMessage = {}
inMessage = {}


def client_send(sock):
    global outMessage
    while True:
        command = input()
        outMessage["command"] = command
        data = simplejson.dumps(outMessage).encode()
        sock.send(data)


def client_receive(sock):
    global inMessage
    while True:
        inMessage = simplejson.loads(sock.recv(1024).decode())

        if inMessage["command"] == "Quit client":
            outMessage["command"] = "Quit client"
            data = simplejson.dumps(outMessage).encode()
            sock.send(data)

        elif inMessage["command"] == "Initialize":
            print("Initialized with: ", inMessage["data"])

        print(inMessage["command"])


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
