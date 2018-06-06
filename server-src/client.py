import socket
import threading
import simplejson

outMessage = {}
inMessage = {}
running = True


def client_send(sock):
    global outMessage, running
    print("Start send module!")
    while running:
        command = input()

        if command == "0":
            outMessage["command"] = "Start warm up music"

        elif command == "1":
            outMessage["command"] = "Change music"

        elif command == "2":
            outMessage["command"] = "Pause"

        elif command == "3":
            outMessage["command"] = "unPause"

        elif command == "4":
            outMessage["command"] = "Stop music module"

        elif command == "5":
            outMessage["command"] = "Quit client"

        elif command == "6":
            outMessage["command"] = "Start light module"

        elif command == "7":
            outMessage["command"] = "Start sport music"

        elif command == "initial":
            outMessage["command"] = "Initialize"
            outMessage["data"] = {"isInitialized": True,
                                  "Age": 23,
                                  "Rest_time": 60,
                                  "fitbit_user_id": "6NQLSZ",
                                  "default_color": (255, 255, 255),
                                  "anaerobic_color": (153, 204, 51),
                                  "maximum_color": (255, 68, 0)
                                  }

        else:
            outMessage["command"] = command

        data = simplejson.dumps(outMessage).encode()

        sock.send(data)
        if command == "5":
            break

    print("Send module stopped!")


def client_receive(sock):
    print("Start receive module!")
    global inMessage, running

    while running:
        inMessage = simplejson.loads(sock.recv(1024).decode())

        if inMessage["command"] == "Quit client":
            break

        print(inMessage["command"])
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
