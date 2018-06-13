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

        if command == "1":
            outMessage["command"] = "Start warm up music"

        elif command == "2":
            outMessage["command"] = "Start sport music"

        elif command == "3":
            outMessage["command"] = "Change music"

        elif command == "4":
            outMessage["command"] = "Pause"

        elif command == "5":
            outMessage["command"] = "unPause"

        elif command == "6":
            outMessage["command"] = "Stop music module"

        elif command == "7":
            outMessage["command"] = "Start light module"

        elif command == "8":
            outMessage["command"] = "Stop light module"

        elif command == "9":
            outMessage["command"] = "Start heartbeat detection"

        elif command == "10":
            outMessage["command"] = "Stop heartbeat detection"

        elif command == "11":
            outMessage["command"] = "Initialize"
            outMessage["data"] = {"age": 23,
                                  "rest_time": 60,
                                  "warm_up_time": 15,
                                  "rest_heartbeat_rate": 65,
                                  # "fitbit_user_secret": "90dca659ed79208397b8cb3f3682f4f4",
                                  # "fitbit_user_id": "22CTVH",
                                  "fitbit_user_id": '',
                                  "fitbit_user_secret": '',
                                  "default_color": [255, 255, 255],
                                  "anaerobic_color": [153, 204, 51],
                                  "maximum_color": [255, 68, 0]
                                  }
        elif command == "12":
            outMessage["command"] = "isInitialized"

        elif command == "13":
            outMessage["command"] = "Get rest heartbeat rate"

        elif command == "14":
            outMessage["command"] = "Set demo module"

        elif command == "15":
            outMessage["command"] = "Reset server"

        elif command == "16":
            outMessage["command"] = "Update music database"

        elif command == "17":
            outMessage["command"] = "Update light color"

            outMessage["data"] = {"default_color": [255, 255, 0],
                                  "anaerobic_color": [153, 204, 0],
                                  "maximum_color": [255, 0, 0]
                                  }

        elif command == "quit":
            outMessage["command"] = "Quit client"

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

        print("Command: ", str(inMessage["command"]))
        if "data" in inMessage:
            print("Data is:", inMessage["data"])

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
