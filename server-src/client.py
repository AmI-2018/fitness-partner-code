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
            outMessage["command"] = "Start sport music"

        elif command == "2":
            outMessage["command"] = "Change music"

        elif command == "3":
            outMessage["command"] = "Pause"

        elif command == "4":
            outMessage["command"] = "unPause"

        elif command == "5":
            outMessage["command"] = "Stop music module"

        elif command == "6":
            outMessage["command"] = "Start light module"

        elif command == "7":
            outMessage["command"] = "Stop light module"

        elif command == "8":
            outMessage["command"] = "Start heartbeat detection"

        elif command == "9":
            outMessage["command"] = "Stop heartbeat detection"

        elif command == "initial":
            outMessage["command"] = "Initialize"
            outMessage["data"] = {"age": 23,
                                  "rest_time": 60,
                                  "warm_ip_time": 15,
                                  "fitbit_user_secret": "90dca659ed79208397b8cb3f3682f4f4",
                                  "fitbit_user_id": "22CTVH",
                                  "default_color": (255, 255, 255),
                                  "anaerobic_color": (153, 204, 51),
                                  "maximum_color": (255, 68, 0)
                                  }
        elif command == "isInitial":
            outMessage["command"] = "isInitialized"

        elif command == "getRHBR":
            outMessage["command"] = "Get rest heartbeat rate"

        elif command == "quit":
            outMessage["command"] = "Quit client"

        elif command == "setDemo":
            outMessage["command"] = "Set demo module"

        elif command == "reset":
            outMessage["command"] = "Reset server"

        elif command == "updateMusicDB":
            outMessage["command"] = "Update music database"

        else:
            outMessage["command"] = command

        data = simplejson.dumps(outMessage).encode()

        sock.send(data)
        if command == "quit":
            break

    print("Send module stopped!")


def client_receive(sock):
    print("Start receive module!")
    global inMessage, running

    while running:
        inMessage = simplejson.loads(sock.recv(1024).decode())

        if inMessage["command"] == "Quit client":
            break

        print(str(inMessage["command"]))

    sock.close()

    print("Receive module stopped!")


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 8888
    sock = socket.socket()
    sock.connect((ip, port))

    thread_send = threading.Thread(target=client_send, args=(sock,))
    thread_receive = threading.Thread(target=client_receive, args=(sock,))

    thread_send.start()
    thread_receive.start()

