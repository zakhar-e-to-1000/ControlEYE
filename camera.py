"""
Camera operator program v0.0.1 
"""
import os
import requests
import time

def get_video(IP, OUTPUT_PATH):
    os.system(f'ffmpeg -use_wallclock_as_timestamps 1 -i "{IP}:81/stream" -t 60 -c copy "{OUTPUT_PATH}.mp4"')

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

get_video(IP, OUTPUT_PATH)
