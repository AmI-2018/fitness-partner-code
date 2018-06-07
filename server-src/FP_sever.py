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
import simplejson
import configparser

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
    global outMessage
    pygame.mixer.init()

    if events.get_value("Warming_up"):
        music_location, music_name = musicDB.select_music(random.randint(90, 109))
        events.set_value("Music_location", str(music_location))
        events.set_value("Music_name", str(music_name))
    else:
        music_location, music_name = musicDB.select_music(get_highest_averange_hbr_data())
        events.set_value("Music_location", str(music_location))
        events.set_value("Music_name", str(music_name))

    # events.to_string()

    outMessage = "Playing: " + music_name
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
    for light in all_the_lights:
        url_to_call = lights_url + light + '/state'
        body = '{"on":true, "transitiontime": 10,"xy":[%f, %f]}' % converter.rgb_to_xy(rgb[0], rgb[1], rgb[2])
        rest.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})


# Turn off lights
def turn_off_light():
    time.sleep(1)
    for light in all_the_lights:
        url_to_call = lights_url + light + '/state'
        body = '{ "on" : false }'
        rest.send('PUT', url_to_call, body, {'Content-Type': 'application/json'})


# Change color lights color by real time heart beat rate
def change_light_color_by_hbr():
    global queue_lock, heart_beat_queue

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


# Server send message
def server_send(sock, address):
    global outMessage, send_event, inMessage

    print("\033[33mStart send module!\033[0m")

    while True:
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


# Server receive message
def server_receive(sock):
    global outMessage, send_event, inMessage
    global command_event, music_start_event, send_event

    print("\033[33mStart receive module!\033[0m")

    while True:
        inMessage = simplejson.loads(sock.recv(1024).decode())

        print("\033[34mRECEIVE MESSAGE:\033[0m", inMessage["command"])

        if inMessage["command"] == "Quit client":
            events.set_value("Music_player_state", "QUIT")
            events.set_value("Lights_on", False)
            command_event.set()
            print("Music STOPPED.")

            outMessage["command"] = "Quit client"
            send_event.set()
            break

        elif inMessage["command"] == "Start warm up music":
            music = MusicModule("Music model")
            detection = MusicPlaying("Music playing")
            events.set_value("Warming_up", True)

            music.start()
            detection.start()

        elif inMessage["command"] == "Start sport music":
            music = MusicModule("Music model")
            detection = MusicPlaying("Music playing")
            events.set_value("Warming_up", False)

            initial_hbr = random.randint(aerobic_start, anaerobic_start)
            for i in range(60):
                heart_beat_queue.append(initial_hbr)

            music.start()
            detection.start()

        elif inMessage["command"] == "1":
            events.set_value("Music_player_state", "CHANGE")
            command_event.set()
            print("Changing song......")

        elif inMessage["command"] == "2":
            events.set_value("Music_player_state", "PAUSE")
            command_event.set()
            print("Music paused......")

        elif inMessage["command"] == "3":
            events.set_value("Music_player_state", "PLAYING")
            command_event.set()
            print("Music continued......")

        elif inMessage["command"] == "4":
            events.set_value("Music_player_state", "QUIT")
            command_event.set()
            print("Music STOPPED.")

        elif inMessage["command"] == "6":
            thread_detect_hbr_data = threading.Thread(target=detect_hbr_data_demo)
            thread_light = threading.Thread(target=change_light_color_by_hbr)
            events.set_value("Lights_on", True)

            thread_detect_hbr_data.start()
            thread_light.start()

    print("\033[31mReceive module stopped!\033[0m")


def initialize_server():
    global converter, lights_url, all_the_lights, \
           host, port, is_initialized
    # Read configurations
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize Hue Bridge information and RGB_to_XY converter
    converter = Converter(config['LIGHT BRIDGE']['converter'])

    base_url = config['LIGHT BRIDGE']['base_url']
    username = config['LIGHT BRIDGE']['username']

    lights_url = base_url + '/api/' + username + '/lights/'
    all_the_lights = rest.send(url=lights_url)

    # Initialize Server information
    host = config['SERVER']['host']
    port = int(config['SERVER']['port'])
    is_initialized = eval(config['SERVER']['is_initialized'])


def initialize_sport_settings():
    global warm_up_time, rest_time, \
        default_color, anaerobic_color, maximum_color, aerobic_color_range, anaerobic_color_range, \
        aerobic_start, anaerobic_start, maximum_heart_beat, aerobic_range, anaerobic_range

    # Read configurations
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize sport information
    warm_up_time = int(config['SPORT INFO']['warm_up_time'])
    rest_time = int(config['SPORT INFO']['rest_time'])

    # Initialize light color terminal and range information
    default_color = eval(config['LIGHT COLOR']['default_color'])
    anaerobic_color = eval(config['LIGHT COLOR']['anaerobic_color'])
    maximum_color = eval(config['LIGHT COLOR']['maximum_color'])

    aerobic_color_range = eval(config['LIGHT COLOR']['aerobic_color_range'])
    anaerobic_color_range = eval(config['LIGHT COLOR']['anaerobic_color_range'])

    # Initialize sport type terminal and range information
    aerobic_start = int(config['BODY INFO']['aerobic_start'])
    anaerobic_start = int(config['BODY INFO']['anaerobic_start'])
    maximum_heart_beat = int(config['BODY INFO']['maximum_heart_beat'])

    aerobic_range = int(config['BODY INFO']['aerobic_range'])
    anaerobic_range = int(config['BODY INFO']['anaerobic_range'])


if __name__ == "__main__":

    # Initialize Global events
    events.init()
    initialize_server()

    print("\033[36mServer initialize state:\033[0m", is_initialized)

    # If server is initialized, load the saved information
    if is_initialized:
        initialize_sport_settings()
        print("\033[36mSport settings loaded.\033[0m")

    # Initialize hear beat queue and lock for it
    queue_lock = threading.Lock()
    heart_beat_queue = []

    # # Initialize light color terminal and range information
    # default_color = (255, 255, 255)
    # anaerobic_color = (153, 204, 51)
    # maximum_color = (255, 68, 0)
    #
    # aerobic_color_range = range_minus(default_color, anaerobic_color)
    # anaerobic_color_range = range_minus(anaerobic_color, maximum_color)
    #
    # # Initialize sport type terminal and range information
    # aerobic_start = 114
    # anaerobic_start = 160
    # maximum_heart_beat = 191
    #
    # aerobic_range = anaerobic_start - aerobic_start
    # anaerobic_range = maximum_heart_beat - anaerobic_start

    # Initialize Events
    command_event = threading.Event()
    music_start_event = threading.Event()
    send_event = threading.Event()

    # Initialize Socket and begin to listen
    s = socket.socket()
    print("\033[33mSocket created\033[0m")

    s.bind((host, port))
    s.listen(5)
    print("\033[33mSocket new listening\033[0m")

    # Waiting for client connection......
    while True:
        conn, addr = s.accept()

        # Initialize input and output cache
        inMessage = {}
        outMessage = {}
        print("\033[34mConnect with: \033[0m" + addr[0] + ":" + str(addr[1]))

        # Set and start main threads
        thread_send = threading.Thread(target=server_send, args=(conn, addr))
        thread_receive = threading.Thread(target=server_receive, args=(conn,))

        thread_send.start()
        thread_receive.start()
