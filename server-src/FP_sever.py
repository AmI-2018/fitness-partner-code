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
from config_operation import config_write, config_read, reset_config
from get_restHBR_from_cloud import get_averange_hbt_from_server


# INITIALIZE MODULE


def initialize_server():
    global converter, lights_url, all_the_lights, \
           host, port
    # Read configurations
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize Hue Bridge information and RGB_to_XY converter
    if config['LIGHT BRIDGE']['converter'] == "GamutA":
        converter = Converter(GamutA)
    elif config['LIGHT BRIDGE']['converter'] == "GamutB":
        converter = Converter(GamutB)
    elif config['LIGHT BRIDGE']['converter'] == "GamutC":
        converter = Converter(GamutC)

    base_url = config['LIGHT BRIDGE']['base_url']
    username = config['LIGHT BRIDGE']['username']

    lights_url = base_url + '/api/' + username + '/lights/'
    all_the_lights = rest.send(url=lights_url)

    # Initialize Server information
    host = config['SERVER']['host']
    port = int(config['SERVER']['port'])


def initialize_sport_settings(rest_heartbeat_rate):
    global warm_up_time, rest_time, \
        default_color, anaerobic_color, maximum_color, aerobic_color_range, anaerobic_color_range, \
        aerobic_start, anaerobic_start, maximum_heart_beat, aerobic_range, anaerobic_range, \
        demo_mode

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
    maximum_heart_beat = eval(config['BODY INFO']['maximum_heart_beat'])
    aerobic_start = eval(config['BODY INFO']['aerobic_start'])

    heart_beat_storage = maximum_heart_beat - rest_heartbeat_rate
    anaerobic_start = rest_heartbeat_rate + 0.8 * heart_beat_storage

    aerobic_range = anaerobic_start - aerobic_start
    anaerobic_range = maximum_heart_beat - anaerobic_start

    # Initialize demo settings
    demo_mode = False

    print(rest_time, warm_up_time)
    print(default_color, anaerobic_color, maximum_color, aerobic_color_range, anaerobic_color_range)
    print(maximum_heart_beat, aerobic_start, anaerobic_start, aerobic_range, anaerobic_range)


# HEART BEAT RATE DETECTION MODULE


def detect_hbr_data():
    global queue_lock, heart_beat_queue, demo_mode, rest_time

    # Judge whether start the module by demo mode
    if demo_mode:
        print("\033[33mStart heart beat rate detection demo module!\033[0m")
        heart_beat = 130
        while events.get_value("Detect_on"):
            queue_lock.acquire()
            if len(heart_beat_queue) >= rest_time:
                heart_beat_queue.pop(0)

            if random.randint(0, 1):
                heart_beat += random.randint(0, 10)
            else:
                heart_beat -= random.randint(0, 10)

            if heart_beat < 70:
                heart_beat_queue.append(heart_beat + random.randint(10, 20))
            elif heart_beat > 200:
                heart_beat_queue.append(heart_beat - random.randint(10, 20))
            else:
                heart_beat_queue.append(heart_beat)
            queue_lock.release()

            outMessage["command"] = "Heartbeat rate"
            outMessage["data"] = heart_beat
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])

            time.sleep(1)
        print("\033[31mHeart beat rate detection demo module stopped!\033[0m")

    # Start with real module
    # TODO: Implement heart beat sense module
    else:
        print("\033[33mStart heart beat rate detection module!\033[0m")
        time.sleep(1)
        print("\033[31mHeart beat rate detection module stopped!\033[0m")


def get_highest_averange_hbr_data():
    global queue_lock, heart_beat_queue, rest_time

    queue_lock.acquire()
    temp = heart_beat_queue
    queue_lock.release()

    numbers = heapq.nlargest(5, temp)
    averange = numpy.mean(numbers)

    print("Highest 5 HBR in last %s seconds is:" % rest_time, numbers, ", Averange is:", averange)

    return averange


# MUSIC MODULE


class MusicPlaying(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("\033[33mMusic detection started.\033[0m")
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

        # After music stopped send "Music stopped" to client
        outMessage.clear()
        outMessage["command"] = "Music stopped"
        send_event.set()
        print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        print("\033[31mMusic detection stopped!\033[0m")


class MusicModule(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("\033[33mStart music module!\033[0m")
        music_play()

        while events.get_value("Music player running"):
            # Wait for command.
            command_event.wait()
            music = pygame.mixer.music

            # Get command and perform operation.
            current_state = events.get_value("Music_player_state")
            if current_state == "PAUSE":
                music.pause()

            elif current_state == "PLAYING":
                music.unpause()

            elif current_state == "CHANGE-PLAYING":
                music.fadeout(1000)

            elif current_state == "CHANGE-PAUSE":
                music.unpause()
                pygame.mixer.music.stop()

            elif current_state == "QUIT-PLAYING":
                # Stop the player.
                events.set_value("Music player running", False)
                music.fadeout(1000)

            elif current_state == "QUIT-PAUSE":
                events.set_value("Music player running", False)
                music.unpause()
                pygame.mixer.music.stop()

            command_event.clear()
        print("\033[31mMusic module stopped!\033[0m")


# Play the music.
def music_play():
    global outMessage
    pygame.mixer.init()

    # Judge the music playing style
    if events.get_value("Warming_up"):
        music_location, music_name = musicDB.select_music(random.randint(90, 109))
        events.set_value("Music_location", str(music_location))
        events.set_value("Music_name", str(music_name))
    else:
        music_location, music_name = musicDB.select_music(get_highest_averange_hbr_data())
        events.set_value("Music_location", str(music_location))
        events.set_value("Music_name", str(music_name))

    # Send the name of playing music
    outMessage["command"] = "Music name"
    outMessage["data"] = music_name
    send_event.set()
    print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])

    pygame.mixer.music.load(music_location)
    pygame.mixer.music.play()

    events.set_value("Music player running", True)
    music_start_event.set()

    # print("Playing music @%s" % music_location)


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

    print("\033[33mLight module start!\033[0m")
    while events.get_value("Lights_on"):
        time.sleep(1)

        # Lock heart beat queue
        queue_lock.acquire()
        newest_heart_rate = heart_beat_queue[-1]
        # Release heart beat queue
        queue_lock.release()

        # Lock color parameters
        color_lock.acquire()

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

        # Release color lock
        color_lock.release()

    turn_off_light()
    print("\033[31mLight module stopped!\033[0m")


# NETWORK MODEL


# Server send message
def server_send(sock, address):
    global outMessage, send_event, inMessage

    print("\033[33mStart send module!\033[0m")

    # Reset send event
    send_event.clear()

    while True:
        send_event.wait()

        if inMessage["command"] == "Quit client":
            sock.send(simplejson.dumps(inMessage).encode())
            break

        data = simplejson.dumps(outMessage).encode()
        sock.send(data)

        send_event.clear()

    print("\033[31mSend module stopped!\033[0m")
    print("\033[31mDisconnected with:\033[0m", address[0] + ":" + str(address[1]))


# Server receive message
def server_receive(sock):
    global outMessage, inMessage,\
        command_event, music_start_event, send_event, color_lock
    global warm_up_time, rest_time, \
        default_color, anaerobic_color, maximum_color, aerobic_color_range, anaerobic_color_range, \
        aerobic_start, anaerobic_start, maximum_heart_beat, aerobic_range, anaerobic_range, \
        demo_mode

    print("\033[33mStart receive module!\033[0m")

    while True:
        inMessage = simplejson.loads(sock.recv(1024).decode())

        print("\033[34mRECEIVE MESSAGE:\033[0m", inMessage["command"])

        # 1. If client send "Quit client", server will reply to help client quit
        if inMessage["command"] == "Quit client":
            # Judge whether music is playing
            if events.get_value("Music_player_state") == "PAUSE":
                events.set_value("Music_player_state", "QUIT-PAUSE")
            else:
                events.set_value("Music_player_state", "QUIT-PLAYING")
            events.set_value("Detect_on", False)
            events.set_value("Lights_on", False)
            command_event.set()

            outMessage["command"] = "Quit client"
            send_event.set()
            break

        # 2. Client asks whether server is initialized
        elif inMessage["command"] == "isInitialized":
            # Read configurations
            config = configparser.ConfigParser()
            config.read('config.ini')

            # If it is, server will send "Server is initialized" after initialize
            if eval(config['SERVER']['is_initialized']):

                # Update fitbit account rest heartbeat rate from server
                if eval(config_read('FITBIT ACCOUNT', 'fitbit_is_initialized')):

                    client_id = config_read('FITBIT ACCOUNT', 'fitbit_user_id')
                    client_secret = config_read('FITBIT ACCOUNT', 'fitbit_user_secret')
                    rest_heartbeat_rate = get_averange_hbt_from_server(client_id, client_secret, 7)

                    # Error occurred during fetch data from cloud, use the stored data
                    if not rest_heartbeat_rate:
                        rest_heartbeat_rate = eval(config_read('BODY INFO', 'rest_heartbeat_rate'))
                # Use stored data
                else:
                    rest_heartbeat_rate = eval(config_read('BODY INFO', 'rest_heartbeat_rate'))

                print('rest_heartbeat_rate:', rest_heartbeat_rate)

                # Load the saved information
                initialize_sport_settings(rest_heartbeat_rate)
                print("\033[36mSport settings loaded.\033[0m")

                outMessage["command"] = "Server is initialized"

                # Necessary data will be stored in outMessage["data"]
                outMessage["data"] = {"warm_up_time": warm_up_time,
                                      "default_color": default_color,
                                      "anaerobic_color": anaerobic_color,
                                      "maximum_color": maximum_color,
                                      }

            # If not, will send "Server isn't initialized"
            else:
                outMessage.clear()
                outMessage["command"] = "Server isn't initialized"

            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", str(outMessage["command"]))

        # 3. Client sends initialize information
        elif inMessage["command"] == "Initialize":
            print("\033[35mInitialized with:\033[0m")

            initialize_data = inMessage["data"]

            # Print the client send data
            for (key, value) in initialize_data.items():
                print(key, ":", value)

            # Initialize and save fitbit user information
            client_secret = initialize_data['fitbit_user_secret']
            config_write('FITBIT ACCOUNT', 'fitbit_user_secret', client_secret)
            client_id = initialize_data['fitbit_user_id']
            config_write('FITBIT ACCOUNT', 'fitbit_user_id', client_id)
            fitbit_is_initialized = initialize_data['fitbit_user_id'] != ""
            config_write('FITBIT ACCOUNT', 'fitbit_is_initialized', fitbit_is_initialized)

            # Initialize and save heart beat information
            if fitbit_is_initialized:
                rest_heartbeat_rate = get_averange_hbt_from_server(client_id, client_secret, 7)
                config_write('BODY INFO', 'rest_heartbeat_rate', rest_heartbeat_rate)

                # Error occurred during fetch data from cloud
                if not rest_heartbeat_rate:
                    rest_heartbeat_rate = initialize_data['rest_heartbeat_rate']
                    config_write('BODY INFO', 'rest_heartbeat_rate', rest_heartbeat_rate)
            else:
                rest_heartbeat_rate = initialize_data['rest_heartbeat_rate']
                config_write('BODY INFO', 'rest_heartbeat_rate', rest_heartbeat_rate)

            maximum_heart_beat = 206.9 - (0.67 * initialize_data['age'])
            config_write('BODY INFO', 'maximum_heart_beat', maximum_heart_beat)

            aerobic_start = maximum_heart_beat * 0.6
            config_write('BODY INFO', 'aerobic_start', aerobic_start)

            heart_beat_storage = maximum_heart_beat - rest_heartbeat_rate
            anaerobic_start = rest_heartbeat_rate + 0.8 * heart_beat_storage

            aerobic_range = anaerobic_start - aerobic_start
            anaerobic_range = maximum_heart_beat - anaerobic_start

            # Initialize and save sport information
            warm_up_time = initialize_data['warm_up_time']
            config_write('SPORT INFO', 'warm_up_time', warm_up_time)
            rest_time = initialize_data['rest_time']
            config_write('SPORT INFO', 'rest_time', rest_time)

            # Initialize and save light color
            default_color = initialize_data['default_color']
            config_write('LIGHT COLOR', 'default_color', default_color)
            anaerobic_color = initialize_data['anaerobic_color']
            config_write('LIGHT COLOR', 'anaerobic_color', anaerobic_color)
            maximum_color = initialize_data['maximum_color']
            config_write('LIGHT COLOR', 'maximum_color', maximum_color)

            aerobic_color_range = range_minus(default_color, anaerobic_color)
            config_write('LIGHT COLOR', 'aerobic_color_range', aerobic_color_range)
            anaerobic_color_range = range_minus(anaerobic_color, maximum_color)
            config_write('LIGHT COLOR', 'anaerobic_color_range', anaerobic_color_range)

            # Initialize demo settings
            demo_mode = False

            # Initialize music database
            musicDB.scan_music(config_read('SERVER', 'music_directory'))

            # After initialize will set is_initialized to True and send "Initialized successfully"
            config_write('SERVER', 'is_initialized', True)

            outMessage.clear()
            outMessage["command"] = "Initialized successfully"
            send_event.set()
            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        # 4. Client asks rest heartbeat data
        elif inMessage["command"] == "Get rest heartbeat rate":

            # Server will send 15 valid heart beat data
            # TODO: Implement heart beat sense module
            for i in range(0, 15):
                outMessage["command"] = "Heartbeat rate"
                outMessage["data"] = random.randint(70, 80)
                send_event.set()
                print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"], outMessage["data"])
                time.sleep(0.1)

        # 5. Client asks server to start warm up music
        elif inMessage["command"] == "Start warm up music":
            music = MusicModule("Music model")
            detection = MusicPlaying("Music playing")
            events.set_value("Warming_up", True)

            music.start()
            detection.start()

        # 6. Client asks server to start sport music
        elif inMessage["command"] == "Start sport music":
            music = MusicModule("Music model")
            detection = MusicPlaying("Music playing")
            events.set_value("Warming_up", False)

            # Check whether the detection module is on
            if not events.get_value("Detect_on"):
                thread_detect_hbr_data = threading.Thread(target=detect_hbr_data)
                thread_light = threading.Thread(target=change_light_color_by_hbr)
                events.set_value("Detect_on", True)
                events.set_value("Lights_on", True)

                # Fill the queue with random aerobic sport heart rate
                for i in range(rest_time):
                    heart_beat_queue.append(random.randint(round(aerobic_start), round(anaerobic_start)))

                thread_detect_hbr_data.start()
                thread_light.start()

            music.start()
            detection.start()

        # 7. Client asks server to change music
        elif inMessage["command"] == "Change music":
            if events.get_value("Music_player_state") == "PAUSE":
                events.set_value("Music_player_state", "CHANGE-PAUSE")
            else:
                events.set_value("Music_player_state", "CHANGE-PLAYING")
            command_event.set()
            print("\033[36mChanging song......\033[0m")

        # 8. Client asks server to pause music
        elif inMessage["command"] == "Pause":
            events.set_value("Music_player_state", "PAUSE")
            command_event.set()
            print("\033[36mMusic paused......\033[0m")

        # 9. Client asks server to continue music
        elif inMessage["command"] == "unPause":
            events.set_value("Music_player_state", "PLAYING")
            command_event.set()
            print("\033[36mMusic continued......\033[0m")

        # 10. Client asks server to stop music
        elif inMessage["command"] == "Stop music module":
            if events.get_value("Music_player_state") == "PAUSE":
                events.set_value("Music_player_state", "QUIT-PAUSE")
            else:
                events.set_value("Music_player_state", "QUIT-PLAYING")
            command_event.set()
            print("\033[36mMusic STOPPED.\033[0m")

        # 11. Client asks server to open lights
        elif inMessage["command"] == "Start light module":
            thread_light = threading.Thread(target=change_light_color_by_hbr)
            events.set_value("Lights_on", True)
            thread_light.start()

        # 12. Client asks server to close lights
        elif inMessage["command"] == "Stop light module":
            events.set_value("Lights_on", False)

        # 13. Client asks server to begin heartbeat rate detection
        elif inMessage["command"] == "Start heartbeat detection":
            # Filled the queue with random aerobic sport heart beat rate.
            for i in range(rest_time):
                heart_beat_queue.append(random.randint(round(aerobic_start), round(anaerobic_start)))

            # Start detecting thread, server will send heartbeat data once per second
            thread_detect_hbr_data = threading.Thread(target=detect_hbr_data)
            events.set_value("Detect_on", True)
            thread_detect_hbr_data.start()

        # 14. Client asks server to turn off heartbeat rate detection
        elif inMessage["command"] == "Stop heartbeat detection":
            events.set_value("Detect_on", False)

        # 15. Client asks server to set demo module
        elif inMessage["command"] == "Set demo module":
            if not demo_mode:
                demo_mode = True
                print("\033[36mDemo mode enabled!\033[0m")
            else:
                demo_mode = False
                print("\033[36mDemo mode disabled!\033[0m")

        # 16. Client asks server to reset server
        elif inMessage["command"] == "Reset server":
            # Reset config.ini
            reset_config()
            print("\033[36mConfiguration file reset!\033[0m")

            # Truncate music database
            musicDB.truncate_music_db(config_read('SERVER', 'music_directory'))

            # Set server state to not initialized
            config_write('SERVER', 'is_initialized', False)

            # Server replies rest successfully
            outMessage.clear()
            outMessage["command"] = "Reset successfully"
            send_event.set()

            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        # 17. Client asks server to update music database
        elif inMessage["command"] == "Update music database":
            # Scan the music directories
            musicDB.scan_music(config_read('SERVER', 'music_directory'))

            # Server replies success
            outMessage.clear()
            outMessage["command"] = "Update MDB successfully"
            send_event.set()

            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

        # 18. Client asks server to update light color
        elif inMessage["command"] == "Update light color":

            update_data = inMessage["data"]

            # Print the client sent colors
            for (key, value) in inMessage["data"].items():
                print(key, ":", value)

            # Lock color parameters
            color_lock.acquire()

            # Update and save light color
            default_color = update_data['default_color']
            config_write('LIGHT COLOR', 'default_color', default_color)
            anaerobic_color = update_data['anaerobic_color']
            config_write('LIGHT COLOR', 'anaerobic_color', anaerobic_color)
            maximum_color = update_data['maximum_color']
            config_write('LIGHT COLOR', 'maximum_color', maximum_color)

            aerobic_color_range = range_minus(default_color, anaerobic_color)
            config_write('LIGHT COLOR', 'aerobic_color_range', aerobic_color_range)
            anaerobic_color_range = range_minus(anaerobic_color, maximum_color)
            config_write('LIGHT COLOR', 'anaerobic_color_range', anaerobic_color_range)

            # Release color parameters
            color_lock.release()

            # Server reply update color successfully
            outMessage.clear()
            outMessage["command"] = "Update color successfully"
            send_event.set()

            print("\033[36mSEND MESSAGE:\033[0m", outMessage["command"])

    print("\033[31mReceive module stopped!\033[0m")


if __name__ == "__main__":

    # Initialize server
    initialize_server()

    # Initialize hear beat queue and lock for it
    queue_lock = threading.Lock()
    color_lock = threading.Lock()
    heart_beat_queue = []

    # Initialize Events
    command_event = threading.Event()
    music_start_event = threading.Event()
    send_event = threading.Event()

    # Initialize Socket and begin to listen
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("\033[33mSocket created\033[0m")

    s.bind((host, port))
    s.listen(5)
    print("\033[33mSocket new listening\033[0m")

    # Waiting for client connection......
    while True:
        conn, addr = s.accept()

        # Initialize Global events
        events.init()

        # Initialize input and output cache
        inMessage = {}
        outMessage = {}
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
