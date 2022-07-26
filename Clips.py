import moviepy.editor as mpy
import time
import datetime
import json
import os
import tkinter as tk
from tkinter import filedialog
import shutil
import subprocess


print('Starting Clips Creator')


def get_settings():
    with open('config.json', 'r') as file:
        data = json.load(file)
    return data


settings = get_settings()

root = tk.Tk()
root.withdraw()

print('Select The Path To The Video File')
time.sleep(1)
video_file_path = filedialog.askopenfilename()
print(f'Video File Path Set To {video_file_path}')

print('Select The Path To The Text File With The Saved Time Stamps')
time.sleep(1)
text_file_path = filedialog.askopenfilename()
print(f'Video File Path Set To {text_file_path}')

# save_dir = r'C:\Users\baile\Desktop\Clips'
save_dir = settings['directory']


def get_len():
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_file_path)
    duration       = clip.duration
    return int(duration)

today = datetime.date.today()
folder= f'{today} - Clips'


def get_cuts():
    cuts = []
    with open(text_file_path, 'r') as file:
        data = file.readlines()
        for lines in data:
            line = lines.split(',')
            hour = 0
            min = 0
            sec = 0
            for i in line:
                if "hours" in i:
                    hour += int(i.split()[0])
                if "minutes" in i:
                    min += int(i.split()[0])
                if "seconds" in i:
                    sec += int(i.split()[0])
            cuts.append(f'{hour:02d}:{min:02d}:{sec:02d}')
    return cuts



def cut_video(clip_num, start, end):
    #loads the file
    video = mpy.VideoFileClip(video_file_path)

    
    clip = video.subclip(t_start = start,t_end = end)
    file_name = f'Clip - {clip_num}.mp4'
    file_path = f'{save_dir}/{folder}/{file_name}'
    clip.write_videofile(f'{file_path}', fps = settings['fps'], codec = settings['vcodec'], preset = settings['compression'], threads = settings['threads'])
    time.sleep(2)
    video.reader.close()
    video.audio.reader.close_proc() 
    clip.close()


def start():
    # try:
    #     os.mkdir(os.path.join('Clips'))
    # except:
    #     pass
    try:
        print('Creating Directory')
        os.mkdir(os.path.join(f'{save_dir}/{folder}'))
        print('Created Directory')
    except:
        pass
    total_clips = len(get_cuts())
    print(f'Creating {total_clips} clips')
    x = 1
    for cut in get_cuts():
        print(f'{datetime.datetime.now()} Creating Clip {x} of {total_clips} at {cut}')
        time_cut = 0
        data = cut.split(':')
        hour = data[0]
        min = data[1]
        seconds = data[2]
        if int(hour) > 0:
            time_cut += (int(hour) *3600)
        if int(min) > 0:
            time_cut += (int(min) *60)
        time_cut += int(seconds)
        total_lenth = int(settings['clip length'])
        beginning = time_cut-(int(total_lenth-10))
        end = time_cut+10
        if beginning <= 0:
            cut_video(x, (beginning + 1), end)
        elif end >= get_len():
            cut_video(x, beginning, (end - 1))
        else:
            cut_video(x, beginning, end)
        x += 1
    target_dir = f'{save_dir}/{folder}'
    shutil.move('Clips',target_dir)
    print('The script finished and succesfully created clips!')




start()