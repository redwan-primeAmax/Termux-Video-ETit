import json
import os
import subprocess
import math
import sys

def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

def get_duration(file_path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    return float(result)

def process_video(input_file, start, duration, output_name):
    cmd = (
        f'ffmpeg -y -ss {start} -t {duration} -i "{input_file}" '
        f'-c:v libx264 -preset ultrafast -crf 22 -pix_fmt yuv420p '
        f'-c:a aac -b:a 128k "{output_name}"'
    )
    run_cmd(cmd)

def list_and_select_files(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    if not files:
        print(f"\n[!] Error: '{folder_path}' fouldere kono video nai.")
        return []

    print("\n--- Available Videos ---")
    for i, file in enumerate(files):
        print(f"[{i+1}] {file}")

    try:
        user_input = input("\nFile number(s) likhun (Ex: 1,3,4): ")
        indices = [int(x.strip()) - 1 for x in user_input.split(',')]
        return [files[i] for i in indices if 0 <= i < len(files)]
    except:
        return []

def mode_custom_cutter():
    info_path, clips_dir = 'Custom_Cutter/info.json', 'Custom_Cutter/clips'
    output_dir = 'ready_video/Custom_Cutter'
    
    selected_files = list_and_select_files(clips_dir)
    if not selected_files or not os.path.exists(info_path):
        print("[!] Info.json missing ba file select hoyni.")
        return

    with open(info_path, 'r') as f:
        video_list = json.load(f)

    for video_name in selected_files:
        video_data = next((item for item in video_list if item["video_file"] == video_name), None)
        if video_data:
            print(f"\n>> Processing: {video_name}")
            video_in = os.path.join(clips_dir, video_name)
            temp_files = []
            for i, seg in enumerate(video_data['segments']):
                tmp = f"part_{i}_{video_name}"; process_video(video_in, seg['start'], seg['end']-seg['start'], tmp); temp_files.append(tmp)
            
            with open('list.txt', 'w') as f:
                for t in temp_files: f.write(f"file '{t}'\n")
            
            run_cmd(f'ffmpeg -y -f concat -safe 0 -i list.txt -c copy "{os.path.join(output_dir, video_name)}"')
            for t in temp_files: os.remove(t)
            os.remove('list.txt')

def mode_duration_cutter():
    clips_dir, output_dir = 'Cut_by_Duration/clips', 'ready_video/Cut_by_Duration'
    selected_files = list_and_select_files(clips_dir)
    if not selected_files: return

    try:
        mins = int(input("Minute: ")); secs = input("Second (skip korte 1): ")
        target = (mins * 60) + (0 if secs=='1' else int(secs))
        adj = input("Smart Adjust? (y/n): ").lower()
    except: return

    for video_name in selected_files:
        video_in = os.path.join(clips_dir, video_name)
        total = get_duration(video_in)
        dur = total / math.ceil(total/target) if adj == 'y' else target
        
        curr, p = 0, 1
        while curr < total:
            rem = total - curr
            if rem < 1: break
            clip_dur = min(dur, rem)
            process_video(video_in, curr, clip_dur, os.path.join(output_dir, f"part_{p}_{video_name}"))
            curr += clip_dur; p += 1

def main():
    try:
        print("\n=== Video Editor Pro ===\n1. Custom Cutter\n2. Duration Cutter")
        c = input("\nChoice (1/2): ")
        if c == '1': mode_custom_cutter()
        elif c == '2': mode_duration_cutter()
    except KeyboardInterrupt: sys.exit()

if __name__ == "__main__":
    main()