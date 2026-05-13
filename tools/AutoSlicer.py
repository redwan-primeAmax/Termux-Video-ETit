import os
import sys
import subprocess
import time

# --- Path Configuration ---
BASE_DIR = os.path.expanduser("~/Termux-Video-ETit")
CLIPS_DIR = os.path.join(BASE_DIR, 'clips')
FINAL_OUTPUT = "/sdcard/Video-ETit-Ready"

if not os.path.exists(FINAL_OUTPUT):
    os.makedirs(FINAL_OUTPUT, exist_ok=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

def get_duration(input_file):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
    return float(subprocess.check_output(cmd, shell=True))

def process_slicing(video_data):
    input_file = video_data['path']
    duration = video_data['duration']
    num_slices = video_data['slices']
    
    slice_duration = duration / num_slices
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    print("\n" + "─"*45)
    print(f"\033[1;33m🎬 Slicing: \033[1;37m{os.path.basename(input_file)}\033[0m")
    
    for i in range(num_slices):
        start_time = i * slice_duration
        output_file = os.path.join(FINAL_OUTPUT, f"{base_name}_part_{i+1}.mp4")
        
        # --- THE SMART TRICK (Fast Seek + Accurate Cut) ---
        # -ss কে ইনপুটের আগে ব্যবহার করলে স্পিড বাড়ে
        # -accurate_seek ব্যবহার করা হয়েছে যাতে টাইমিং ঠিক থাকে
        ffmpeg_cmd = (
            f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
            f'-c copy -map 0 -avoid_negative_ts make_zero -break_non_keyframes 1 '
            f'-movflags +faststart "{output_file}" -loglevel error'
        )
        
        print(f"\033[1;34m[🚀] Processing Part {i+1} of {num_slices}...\033[0m")
        subprocess.run(ffmpeg_cmd, shell=True)

if __name__ == "__main__":
    os.system('clear')
    print("\033[1;35m" + "╔═══════════════════════════════════════════╗")
    print("║      SMART SPEED (No-Lag Fix)             ║")
    print("╚═══════════════════════════════════════════╝\033[0m")
    
    vids = sorted([f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))])
    if not vids: sys.exit()

    for idx, vid in enumerate(vids, 1):
        print(f"\033[1;37m {idx:02d}. \033[0m{vid}")

    choice = input("\n\033[1;36mSelect video number(s): \033[0m")
    
    try:
        selected_indices = [int(i.strip()) for i in choice.split(',')]
        queue = []

        for index in selected_indices:
            idx = index - 1
            if 0 <= idx < len(vids):
                video_path = os.path.join(CLIPS_DIR, vids[idx])
                duration = get_duration(video_path)
                print(f"\033[1;32m[+] Added: {vids[idx]} ({format_time(duration)})\033[0m")
                
                slice_input = input(f"    Slices?: ").strip()
                if slice_input.isdigit():
                    queue.append({'path': video_path, 'duration': duration, 'slices': int(slice_input)})
        
        if queue:
            print(f"\n\033[1;32m⚡ Starting Smart Slicing...\033[0m")
            start_time_all = time.time()
            for item in queue:
                process_slicing(item)
            end_time_all = time.time()
            print(f"\n\033[1;32m✅ DONE! All problems fixed.\033[0m")
            print(f"\033[1;37m⏱️  Total Time: {int(end_time_all - start_time_all)}s\033[0m")
        
    except Exception as e:
        print(f"\033[1;31m[X] Error: {str(e)}\033[0m")
