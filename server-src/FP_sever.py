import socket
import threading
import global_events as events
import time
import random
import pygame
import musicDB
from rgbxy import Converter
from rgbxy import GamutA, GamutB, GamutC
import rest
import heapq
import numpy


# HEART BEAT RATE DETECTION MODULE


def detect_hbr_data_demo():
    global queue_lock, heart_beat_queue
    print("Start heart beat rate detection demo module!")
    heart_beat = 130

    while events.get_value("Lights_on"):
        queue_lock.acquire()
        if len(heart_beat_queue) >= 60:
            heart_beat_queue.pop(0)
        if heart_beat < 70:
            heart_beat_queue.append(heart_beat + random.randint(10, 20))
        elif heart_beat > 200:
            heart_beat_queue.append(heart_beat - random.randint(10, 20))
        else:
            heart_beat_queue.append(heart_beat)
        queue_lock.release()

        print(heart_beat)
        if random.randint(0, 1):
            heart_beat += random.randint(0, 10)
        else:
            heart_beat -= random.randint(0, 10)

        time.sleep(1)

    print("Heart beat rate detection demo module! stopped!")


def get_highest_averange_hbr_data():
    global queue_lock, heart_beat_queue

    queue_lock.acquire()
    temp = heart_beat_queue
    queue_lock.release()

    numbers = heapq.nlargest(5, temp)
    averange = numpy.mean(numbers)

    print("Highest 5 HBR in last one minute is:", numbers, ", Averange is:", averange)

    return averange


# MUSIC MODULE


class MusicPlaying(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Music detection started.")
        # Wait the music start.
        music_start_event.wait()

        # Start detecting weather the music is playing.
        while events.get_value("Music player running"):
            # Wait the music start.
            music_start_event.wait()
            # Detected the music ended and change to another one.
            if not pygame.mixer.music.get_busy():
                # Start playing a new music.
                music_start_event.clear()
                music_play()
            time.sleep(0.01)

        music_start_event.clear()
        print("Music detection stopped.")


class MusicModule(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Start music module!")

        music_play()

        while events.get_value("Music player running"):
            # Wait for command.
            command_event.wait()

            # Get command and perform operation.
            current_state = events.get_value("Music_player_state")
            if current_state == "PAUSE":
                music_pause()

            if current_state == "PLAYING":
                music_unpause()

            if current_state == "CHANGE":
                music_stop()

            if current_state == "QUIT":
                # Stop the player.
                events.set_value("Music player running", False)
                music_stop()

            command_event.clear()
        print("Music module stopped!")


# Play the music.
def music_play():
    global outString
    pygame.mixer.init()

    # TODO: get implementation of select new song.
    if events.get_value("Warming_up"):
        music_location, music_name = musicDB.select_music(random.randint(90, 109))
        events.set_value("Music_location", str(music_location))
        events.set_value("Music_name", str(music_name))
    else:
        music_location, music_name = musicDB.select_music(get_highest_averange_hbr_data())
        events.set_value("Music_location", str(music_location))
        events.set_value("Music_name", str(music_name))

    # events.to_string()

    outString = "Playing: " + music_name
    send_event.set()

    pygame.mixer.music.load(music_location)
    pygame.mixer.music.play()

    events.set_value("Music player running", True)
    music_start_event.set()

    # print("Playing music @%s" % music_location)


# Music paused.
def music_pause():
    # print("Music paused.")
    pygame.mixer.music.pause()


# Music unpaused.
def music_unpause():
    # print("Music unpaused.")
    pygame.mixer.music.unpause()


# Stop or Change the playing music.
def music_stop():
    pygame.mixer.music.fadeout(1000)


# LIGHT MODULE


# Get two RGB color minus
def range_minus(start, end):
    result = []
    for i in range(3):
        result.append(start[i] - end[i])
    return result


# Get the change lights change data
def range_multiply(color, percent):
    result = []
    for i in range(3):
        result.append(color[i] * percent)
    return result


# Send http requests to change lights color
def change_light_color(rgb):
    global all_the_lights, lights_url
    for light in all_the_lights:
        url_to_call = lights_url + light + '/state'
        body = '{"on":true, "transitiontime": 5,"xy":[%f, %f]}' % converter.rgb_to_xy(rgb[0], rgb[1], rgb[2])
        rest.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})


# Turn off lights
def turn_off_light():
    global all_the_lights, lights_url
    time.sleep(1)
    for light in all_the_lights:
        url_to_call = lights_url + light + '/state'
        body = '{ "on" : false }'
        rest.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})


# Change color lights color by real time heart beat rate
def change_light_color_by_hbr():
    global queue_lock, heart_beat_queue, \
        aerobic_start, anaerobic_start, maximum_heart_beat, \
        aerobic_color_range, anaerobic_color_range, \
        aerobic_range, anaerobic_range, \
        default_color, anaerobic_color, maximum_color

    print("Light module start!")
    while events.get_value("Lights_on"):
        time.sleep(1)

        queue_lock.acquire()
        newest_heart_rate = heart_beat_queue[-1]
        queue_lock.release()

        if newest_heart_rate < aerobic_start:
            print("newest heart beat rate is:", newest_heart_rate, default_color)
            change_light_color(default_color)

        elif aerobic_start <= newest_heart_rate < anaerobic_start:
            result = range_minus(default_color,
                                 range_multiply(aerobic_color_range,
                                                (newest_heart_rate - aerobic_start) / aerobic_range))
            print("aerobic sport:", newest_heart_rate, result)
            change_light_color(result)

        elif anaerobic_start <= newest_heart_rate < maximum_heart_beat:
            result = range_minus(anaerobic_color,
                                 range_multiply(anaerobic_color_range,
                                                (newest_heart_rate - anaerobic_start) / anaerobic_range))
            print("anaerobic sport:", newest_heart_rate, result)
            change_light_color(result)

        else:
            print("maximum heart beat:", newest_heart_rate, maximum_color)
            change_light_color(maximum_color)

    turn_off_light()
    print("Light module stopped!")


# NETWORK MODEL


# Client send message
def client_send(sock):
    global outString
    print("Start send module!")
    while True:
        send_event.wait()
        if inString == "5":
            sock.send(inString.encode())
            break
        print("Send message:", outString)
        sock.send(outString.encode())
        send_event.clear()
    print("Send module stopped!")


# Client receive message
def client_receive(sock):
    global inString
    global command_event, music_start_event, send_event
    print("Start receive module!")
    while True:
        inString = sock.recv(1024).decode()
        if inString == "Start warm up music":
            music = MusicModule("Music model")
            detection = MusicPlaying("Music playing")
            events.set_value("Warming_up", True)

            music.start()
            detection.start()
        elif inString == "Start sport music":
            music = MusicModule("Music model")
            detection = MusicPlaying("Music playing")
            events.set_value("Warming_up", False)

            initial_hbr = random.randint(aerobic_start, anaerobic_start)
            for i in range(60):
                heart_beat_queue.append(initial_hbr)

            music.start()
            detection.start()
        elif inString == "1":
            events.set_value("Music_player_state", "CHANGE")
            command_event.set()
            print("Changing song......")

        elif inString == "2":
            events.set_value("Music_player_state", "PAUSE")
            command_event.set()
            print("Music paused......")

        elif inString == "3":
            events.set_value("Music_player_state", "PLAYING")
            command_event.set()
            print("Music continued......")

        elif inString == "4":
            events.set_value("Music_player_state", "QUIT")
            command_event.set()
            print("Music STOPPED.")

        elif inString == "5":
            events.set_value("Music_player_state", "QUIT")
            events.set_value("Lights_on", False)
            command_event.set()
            print("Music STOPPED.")
            send_event.set()
            break
        elif inString == "6":
            thread_demo = threading.Thread(target=detect_hbr_data_demo)
            thread_light = threading.Thread(target=change_light_color_by_hbr)
            events.set_value("Lights_on", True)

            thread_demo.start()
            thread_light.start()
    print("Receive module stopped!")


if __name__ == "__main__":
    # Initialize Global events
    events._init()

    # Initialize hear beat queue and lock for it
    queue_lock = threading.Lock()
    heart_beat_queue = []

    # Initialize light color terminal and range information
    default_color = (255, 255, 255)
    anaerobic_color = (153, 204, 51)
    maximum_color = (255, 68, 0)

    aerobic_color_range = range_minus(default_color, anaerobic_color)
    anaerobic_color_range = range_minus(anaerobic_color, maximum_color)

    # Initialize sport type terminal and range information
    aerobic_start = 114
    anaerobic_start = 160
    maximum_heart_beat = 191

    aerobic_range = anaerobic_start - aerobic_start
    anaerobic_range = maximum_heart_beat - anaerobic_start

    # Initialize Events
    command_event = threading.Event()
    music_start_event = threading.Event()
    send_event = threading.Event()

    # Initialize Hue Bridge information and RGB_to_XY converter
    converter = Converter(GamutA)

    base_url = 'http://localhost:8000'
    username = 'newdeveloper'
    lights_url = base_url + '/api/' + username + '/lights/'
    all_the_lights = rest.send(url=lights_url)

    # Initialize Server information
    host = "127.0.0.1"
    port = 8888

    # Initialize Socket and begin to listen
    s = socket.socket()
    print("Socket created")
    s.bind((host, port))
    s.listen(5)
    print("Socket new listening")

    # Waiting for client connection......
    while True:
        conn, addr = s.accept()

        # Initialize input and output cache
        inString = ""
        outString = ""
        print("Connect with " + addr[0] + ":" + str(addr[1]))

        # Set and start main threads
        thread_send = threading.Thread(target=client_send, args=(conn,))
        thread_receive = threading.Thread(target=client_receive, args=(conn,))

        thread_send.start()
        thread_receive.start()
