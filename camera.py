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
    progressbar_chore = threading.Thread(target=progressbar_tick)
    progressbar_chore.start()
    #pylint says i need to write timeout=10 in case of no response, so i did
    requests.get(f"{ip}/control?var=framesize&val={qual}", timeout=10)
    time.sleep(durations[0])
    jobs[0].destroy()
    jobs.pop(0)
    job_canvases[0].destroy()
    job_canvases.pop(0)
    qualities.pop(0)
    if len(qualities) == 0:
        recording_start_button["state"] = "active"

def progressbar_tick():
    """
    Makes progressbars work
    """
    jobtime = durations[0]
    dupercent = jobtime / 50
    progress = 0
    while dupercent / jobtime * progress < 0.95:
        progress += 1
        time.sleep(dupercent)
        try:
            progress_rect = job_canvases[0].create_rectangle(0, 0, int(dupercent / jobtime * progress * 50), 10, fill="green")
            print(dupercent / jobtime * progress)
        except IndexError:
            return

def user_input_handling():
    """
    User input is now processed here, User now inputs certain amount 
    of video intervals vith certain quality and duration
    """
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
    if recording_start_button["state"] == "disabled":
        recording_start_button["state"] = "active"
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
        _i += 1

def start_chores():
    """
    Innitiates ffmmeg and quality changing chores on new threads
    """
    recording_start_button["state"] = "disabled"
    create_chores()
    video_chore = threading.Thread(target=get_video_from_stream, args=(IP, path_textbox_text.get(), sum(durations)))
    for ch in tasks:
        ch.start()
    video_chore.start()

#window initialisations
app_window = Tk()
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

label_path = Label(main_frame, text="Output path:")
label_path.grid(row=6, column=0)

path_textbox_text = StringVar(main_frame)
path_textbox = Entry(main_frame, width=10, textvariable=path_textbox_text)
path_textbox.grid(row=7, column=0)

create_job_button = Button(main_frame, text="Add job", fg="black", padx=20, pady=10, command=user_input_handling)
create_job_button.grid(row=4, column=0)

recording_start_button = Button(second_frame, text="Start recording", command=start_chores)
recording_start_button["state"] = "disabled"
recording_start_button.grid(row=0, column=0)
app_window.mainloop()
#end of window initialisation
