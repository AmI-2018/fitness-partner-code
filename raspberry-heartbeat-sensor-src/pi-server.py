from pulsesensor import Pulsesensor
import time
import socket
import threading
import simplejson

p = Pulsesensor()

host = "192.168.137.61"
port = 6666
send_event = threading.Event()


def detection_module():
    global detection_running, send_event
    p.BPM = 0
    p.startAsyncBPM()

    print("\033[33mStart detecting module!\033[0m")

    while True:
        if not detection_running:
            p.stopAsyncBPM()
            break

        bpm = p.BPM

        if 0 < bpm < 220:
            outMessage["command"] = "Heartbeat rate"
            outMessage["data"] = bpm
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])
        else:
            print("\033[36mNo Heartbeat found\033[0m")

        time.sleep(1)

    print("\033[31mDetecting module stopped!\033[0m")


def server_send(sock, address):
    global outMessage, send_event, inMessage

    print("\033[33mStart send module!\033[0m")

    # Reset send event
    send_event.clear()

    while True:
        send_event.wait()

        if inMessage["command"] == "Quit client":
            # sock.send(simplejson.dumps(inMessage).encode())
            break

        data = simplejson.dumps(outMessage).encode()
        sock.send(data)

        send_event.clear()

    print("\033[31mSend module stopped!\033[0m")
    print("\033[31mDisconnected with:\033[0m", address[0] + ":" + str(address[1]))


# Server receive message
def server_receive(sock):
    global outMessage, inMessage, send_event, detection_running

    print("\033[33mStart receive module!\033[0m")

    while True:
        inMessage = simplejson.loads(sock.recv(1024).decode())

        print("\033[34mRECEIVE MESSAGE:\033[0m", inMessage["command"])

        # 1. If client send "Quit client", server will reply to help client quit
        if inMessage["command"] == "Quit client":
            detection_running = False
            outMessage["command"] = "Quit client"
            send_event.set()
            break

        # 2. If client send "Start detecting", server will begin to reply heart beat rate
        elif inMessage["command"] == "Start detecting":
            detection_running = True
            detection_thread = threading.Thread(target=detection_module)
            detection_thread.start()

    print("\033[31mReceive module stopped!\033[0m")


s = socket.socket()
print("\033[33mSocket created\033[0m")

s.bind((host, port))
s.listen(5)
print("\033[33mSocket new listening\033[0m")

while True:
    conn, addr = s.accept()

    # Initialize input and output cache
    inMessage = {}
    outMessage = {}
    detection_running = False
    print("\033[34mConnect with: \033[0m" + addr[0] + ":" + str(addr[1]))

    # Set and start main threads
    thread_send = threading.Thread(target=server_send, args=(conn, addr))
    thread_receive = threading.Thread(target=server_receive, args=(conn,))
    thread_receive.setDaemon(True)
    thread_send.setDaemon(True)
    thread_send.start()
    thread_receive.start()

    thread_send.join()
    thread_receive.join()
