"""
Camera operator program v0.0.1 
"""
import os
import requests
import time
import threading
from functools import partial

def get_video(IP, OUTPUT_PATH):
    os.system(f'ffmpeg -i "{IP}:81/stream" -t 20 -c copy "{OUTPUT_PATH}.mkv"')

def change_quality(IP):
    time.sleep(5)
    print('hesdddddddddddddd')
    requests.get(f"{IP}/control?var=framesize&val=11")

VERSION = "0.0.1"
print("ControlEye cam operator")
print(f"Version:{VERSION}")
IP = "http://192.168.19.131"
print("Please enter path for video output")
OUTPUT_PATH = input()
requests.get(f"{IP}/control?var=framesize&val=2")

chore1 = threading.Thread(target=partial(get_video, IP, OUTPUT_PATH))
chore2 = threading.Thread(target=partial(change_quality, IP))
chore2.start()
chore1.start()
#os.system(f'ffmpeg -i "{IP}:81/stream" -t 20 -c copy "{OUTPUT_PATH}2.mkv"')
