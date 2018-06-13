import socket
import threading
import simplejson
import random
import time

outMessage = {}
inMessage = {}

send_event = threading.Event()
run_lock = threading.Lock()

hbr_running = False
music_running = False


def server_send(sock, address):
    global outMessage, send_event, inMessage

    print("\033[33mStart send module!\033[0m")

    while True:
        # 通过全局变量 outMessage 储存待发数据， 用 event 暂停和触发
        send_event.wait()

        if inMessage["command"] == "Quit client":
            sock.send(simplejson.dumps(inMessage).encode())
            break

        data = simplejson.dumps(outMessage).encode()
        sock.send(data)
        send_event.clear()

    send_event.clear()

    print("\033[31mSend module stopped!\033[0m")
    print("\033[31mDisconnected with:\033[0m", address[0] + ":" + str(address[1]))


def server_receive(sock):
    global inMessage, outMessage, send_event, hbr_running, run_lock, music_running

    print("\033[33mStart receive module!\033[0m")

    while True:
        inMessage = simplejson.loads(sock.recv(1024).decode())

        print("\033[34mRECEIVE MESSAGE:\033[0m", inMessage["command"])

        # 1.客户端发送 "Quit client" 退出运行，服务器会发送 "Quit client" 帮助客户端退出运行
        if inMessage["command"] == "Quit client":
            outMessage["command"] = "Quit client"
            hbr_running = False
            music_running = False
            send_event.set()
            break

        # 2.客户端请求服务器是否初始化过
        elif inMessage["command"] == "isInitialized":
            # 通过改变switch改变服务器是否初始化过
            switch = True

            # 如果初始化过会发送给客户端"Server is initialized"
            if switch:
                outMessage["command"] = "Server is initialized"

                # 必要的启动数据，保存在字典 outMessage["data"] 中
                outMessage["data"] = {"warm_up_time": 15,
                                      "default_color": [255, 255, 255],
                                      "anaerobic_color": [153, 204, 51],
                                      "maximum_color": [255, 68, 0]
                                      }

            # 如果没有初始化过会发送给客户端 "Server isn't initialized"
            else:
                outMessage["command"] = "Server isn't initialized"

            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", str(outMessage["command"]))

        # 3.服务器接收客户端初始化数据
        elif inMessage["command"] == "Initialize":
            print("\033[35mInitialized with:\033[0m")

            # 打印客户端发送的初始化数据
            for (key, value) in inMessage["data"].items():
                print(key, ":", value, "-", type(value))

                # if key == "default_color":
                #     for i in value:
                #         print(i, type(i))

            # 会向客户端发送字符串 "Initialized successfully"
            outMessage["command"] = "Initialized successfully"
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        # 4.客户端向服务器请求静息心率数据
        elif inMessage["command"] == "Get rest heartbeat rate":

            # 服务端会向客户端发送15个有效的心率数据
            for i in range(0, 15):
                outMessage["command"] = "Heartbeat rate"
                outMessage["data"] = random.randint(70, 80)
                send_event.set()
                print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])
                time.sleep(0.1)

        # 5.客户端向服务器请求开始热身音乐
        elif inMessage["command"] == "Start warm up music":
            music_running = True

            send_musicname_demo = threading.Thread(target=send_music_name_demo)
            send_musicname_demo.start()

            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 6.客户端向服务器请求开始健身音乐
        elif inMessage["command"] == "Start sport music":
            music_running = True

            if not hbr_running:
                hbr_running = True
                thread_hbrdemo = threading.Thread(target=heart_beat_demo)
                thread_hbrdemo.start()

            send_musicname_demo = threading.Thread(target=send_music_name_demo)
            send_musicname_demo.start()

            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 7.客户端向服务器请求随机更换音乐
        elif inMessage["command"] == "Change music":
            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

            playlist = ("Crazy All My Life",
                        "Love Me Again",
                        "Celebrate",
                        "Wrecking Ball")

            outMessage["command"] = "Music name"
            outMessage["data"] = random.choice(playlist)
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])

        # 8.客户端向服务器请求暂停音乐
        elif inMessage["command"] == "Pause":
            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 9.客户端向服务器请求继续播放音乐
        elif inMessage["command"] == "unPause":
            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 10.客户端向服务器请求停止音乐
        elif inMessage["command"] == "Stop music module":
            music_running = False

            # 音乐停止后向客户端发送音乐停止命令。
            outMessage["command"] = "Music stopped"
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 11.客户端向服务器请求打开灯光
        elif inMessage["command"] == "Start light module":
            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 12.客户端向服务器请求关闭灯光
        elif inMessage["command"] == "Stop light module":
            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 13.客户端向服务器请求打开心率检测
        elif inMessage["command"] == "Start heartbeat detection":
            hbr_running = True
            # 启动心率检测demo线程，每一秒会向服务端发送一个心率数据
            thread_hbr_demo = threading.Thread(target=heart_beat_demo)
            thread_hbr_demo.start()

        # 14.客户端向服务器请求关闭心率检测
        elif inMessage["command"] == "Stop heartbeat detection":
            hbr_running = False
            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 15.客户端向服务器请求设置demo模式
        elif inMessage["command"] == "Set demo module":
            print("\033[36mEXECUTED COMMAND:\033[0m", inMessage["command"])

        # 16.客户端请求重置服务器配置
        elif inMessage["command"] == "Reset server":

            # 服务器回复重设成功
            outMessage["command"] = "Reset successfully"
            send_event.set()

            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        # 17.客户端向服务器请求更新音乐数据库
        elif inMessage["command"] == "Update music database":

            # 服务器回复更新成功
            outMessage["command"] = "Update MDB successfully"
            send_event.set()

            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        # 18.客户端向服务器更新灯光颜色
        elif inMessage["command"] == "Update light color":

            # 打印客户端发送的灯光颜色数据
            for (key, value) in inMessage["data"].items():
                print(key, ":", value)

            # 服务器回复更新成功
            outMessage["command"] = "Update color successfully"
            send_event.set()

            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        else:
            pass

    print("\033[31mReceive module stopped!\033[0m")


def heart_beat_demo():
    global hbr_running, run_lock

    while hbr_running:
        for i in range(random.randint(0, 5), random.randint(5, 10)):
            if not hbr_running:
                break

            time.sleep(1)
            outMessage["command"] = "Heartbeat rate"
            outMessage["data"] = random.randint(120, 160)
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])



        for i in range(random.randint(0, 5), random.randint(5, 10)):

            if not hbr_running:
                break

            time.sleep(1)
            outMessage["command"] = "Heartbeat rate"
            outMessage["data"] = random.randint(160, 190)
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])



def send_music_name_demo():
    global music_running

    playlist = ("Even Heaven",
                "Separation",
                "Shangri-La",
                "Wake Me Up")

    while True:
        if not music_running:
            break
        outMessage["command"] = "Music name"
        outMessage["data"] = random.choice(playlist)
        send_event.set()
        print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])
        time.sleep(5)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888

    s = socket.socket()
    print("\033[33mSocket created\033[0m")

    s.bind((host, port))
    s.listen(5)
    print("\033[33mSocket new listening\033[0m")

    while True:
        conn, addr = s.accept()
        send_event.clear()
        inMessage.clear()
        outMessage.clear()
        print("\033[34mConnect with: \033[0m" + addr[0] + ":" + str(addr[1]))

        thread_send = threading.Thread(target=server_send, args=(conn, addr))
        thread_receive = threading.Thread(target=server_receive, args=(conn,))

        thread_send.start()
        thread_receive.start()
