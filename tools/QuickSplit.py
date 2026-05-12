import os
import math
import subprocess

def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

def get_duration(file_path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    return float(subprocess.check_output(cmd, shell=True).decode('utf-8').strip())

def process_video(input_file, start, duration, output_name):
    cmd = (f'ffmpeg -y -ss {start} -t {duration} -i "{input_file}" '
           f'-c:v libx264 -preset ultrafast -crf 22 -pix_fmt yuv420p '
           f'-c:a aac -b:a 128k "{output_name}"')
    run_cmd(cmd)

def start_tool():
    clips_dir = 'Cut_by_Duration/clips'
    output_dir = 'ready_video'
    files = [f for f in os.listdir(clips_dir) if f.lower().endswith(('.mp4', '.mkv'))]
    
    for i, file in enumerate(files): print(f"[{i+1}] {file}")
    idx = [int(x)-1 for x in input("\nFile number(s): ").split(',')]
    target = float(input("Duration in seconds: "))
    
    for i in idx:
        video_name = files[i]
        video_in = os.path.join(clips_dir, video_name)
        total = get_duration(video_in)
        curr, p = 0, 1
        while curr < total:
            clip_dur = min(target, total - curr)
            if clip_dur < 1: break
            process_video(video_in, curr, clip_dur, os.path.join(output_dir, f"part_{p}_{video_name}"))
            curr += clip_dur; p += 1
    print("\n[✓] QuickSplit কাজ শেষ করেছে।")