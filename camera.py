"""
Camera operator program v0.0.1 
"""
import os
import threading
import time
import requests
tasks = []
qualities = []
durations = []
OUTPUT_PATH = ""
def get_video_from_stream(ip, output_path, t):
    """
    Connects to videostream and writes into .mkv file 
    """
    #added the ability to input final video time from keyboard
    os.system(f'ffmpeg -use_wallclock_as_timestamps 1 -i "{ip}:81/stream" -t {t} -c copy "{output_path}.mp4"')

def change_quality(ip, qual, waittime):
    """
    Sends a signal to change video quality
    """
    time.sleep(waittime)
    #pylint says i need to write timeout=10 in case of no response, so i did
    requests.get(f"{ip}/control?var=framesize&val={qual}", timeout=10)

def user_input_handling():
    """
    User input is now processed here, User now inputs certain amount 
    of video intervals vith certain quality and duration
    """
    while True:
        print("Please enter fragment quality ('done' to finish)")
        _input = input()
        if _input == "done":
            break
        if _input < 1 or _input > 13:
            print("quality is not in valid range")
            continue
        qualities.append(_input)
        print("Please enter fragment duration (in seconds)")
        _input = input()
        if not _input.isnumeric:
            print("Please enter a number (in seconds)")
            qualities.pop(-1)
            continue
        durations.append(_input)

def create_chores():
    """
    For each interval this creates a chore that waits and swaps quality when needed
    """
    _moment = 0
    _i = 0
    for quality in qualities:
        chore = threading.Thread(target=change_quality, args=(IP, quality, _moment))
        tasks.append(chore)
        _moment += durations[_i]

VERSION = "0.0.1"
print("ControlEye cam operator")
print(f"Version:{VERSION}")

IP = "http://192.168.19.131"

#now user inputs multiple video fragments with various quality
print("Please enter path for video output")
OUTPUT_PATH = input()
user_input_handling()

for ch in tasks:
    ch.start()

get_video_from_stream(IP, OUTPUT_PATH, sum(durations))
