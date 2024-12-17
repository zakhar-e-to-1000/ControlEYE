"""
Camera operator program v0.0.1 
"""
import os
import threading
import time
from tkinter import *
from tkinter import messagebox
import requests
tasks = []
#jobs
jobs = []
job_canvases = []
#/jobs
qualities = []
durations = []
OUTPUT_PATH = ""
VERSION = "0.0.1"
STARTBUTTON_EXISTS = False
IP = "http://192.168.0.101"
print()
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
    global STARTBUTTON_EXISTS
    _input = quality_textbox_text.get()
    try:
        _input = int(_input)
    except ValueError:
        msg = messagebox.showerror("Error", "Quality must be a number between 1 and 13")
        return
    if _input < 1 or _input > 13:
        msg = messagebox.showerror("Error", "Quality is not in valid range")
        return
    qualities.append(_input)
    _input = duration_textbox_text.get()
    try:
        _input = int(_input)
    except ValueError:
        msg = messagebox.showerror("Error", "Duration must be a number")
        return
    durations.append(int(_input))
    if STARTBUTTON_EXISTS is False:
        recording_start_button["state"] = "active"
        STARTBUTTON_EXISTS = True
    job = Label(jobs_frame, text=f"Job {len(durations)}: Quality: {qualities[-1]}, Duration: {durations[-1]}")
    job.grid(row=len(durations), column=0)
    jobs.append(job)
    job_canv = Canvas(jobs_frame, width=50, height=10)
    job_canv.grid(row=len(durations), column=1)
    job_canvases.append(job_canv)
    progress_bg = job_canv.create_rectangle(0, 0, 50, 10, fill="black")


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

def start_chores():
    """
    Innitiates ffmmeg and quality changing chores on new threads
    """
    create_chores()
    video_chore = threading.Thread(target=get_video_from_stream, args=(IP, OUTPUT_PATH, sum(durations)))
    for ch in tasks:
        ch.start()
    video_chore.start()

#window initialisations
app_window = Tk()
tkinterthread = threading.Thread(target=app_window.mainloop)

app_window.title("ControlEye camera operator")
app_window.geometry("500x200")

main_frame = Frame(app_window)
main_frame.grid(row=0, column=0)
second_frame = Frame(app_window)
second_frame.grid(row=0, column=1)
jobs_frame = Frame(app_window)
jobs_frame.grid(row=0, column=2)

label_jobs = Label(jobs_frame, text="Jobs:")
label_jobs.grid(row=0, column=0)


label_qual = Label(main_frame, text="Fragment quality")
label_qual.grid(row=0, column=0)
quality_textbox_text = StringVar(main_frame)
quality_textbox = Entry(main_frame, width=10, textvariable=quality_textbox_text)
quality_textbox.grid(row=1, column=0)

label_dur = Label(main_frame, text="Fragment duration")
label_dur.grid(row=2, column=0)

duration_textbox_text = StringVar(main_frame)
duration_textbox = Entry(main_frame, width=10, textvariable=duration_textbox_text)
duration_textbox.grid(row=3, column=0)

create_job_button = Button(main_frame, text="Add job", fg="black", padx=20, pady=10, command=user_input_handling)
create_job_button.grid(row=4, column=0)

recording_start_button = Button(second_frame, text="Start recording", command=start_chores)
recording_start_button["state"] = "disabled"
recording_start_button.grid(row=0, column=0)
tkinterthread.start()
#end of window initialisation

while True:
    _input = input()
    if _input == "exit":
        break


#get_video_from_stream(IP, OUTPUT_PATH, sum(durations))
