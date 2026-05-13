import os
import sys
import subprocess
import time

# --- Path Configuration ---
BASE_DIR = os.path.expanduser("~/Termux-Video-ETit")
CLIPS_DIR = os.path.join(BASE_DIR, 'clips')
OUTPUT_DIR = os.path.join(BASE_DIR, 'ready_video')

os.makedirs(OUTPUT_DIR, exist_ok=True)

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
    print(f"\033[1;33m📦 Slices : \033[1;32m{num_slices}\033[0m")
    
    for i in range(num_slices):
        start_time = i * slice_duration
        output_file = os.path.join(OUTPUT_DIR, f"{base_name}_part_{i+1}.mp4")
        
        # Stream Copy (Bullet Speed)
        ffmpeg_cmd = (
            f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
            f'-c copy -avoid_negative_ts make_zero -map_metadata 0 '
            f'-movflags +faststart "{output_file}" -loglevel error'
        )
        
        print(f"\033[1;34m[⚡] Part {i+1} of {num_slices}...\033[0m")
        subprocess.run(ffmpeg_cmd, shell=True)

if __name__ == "__main__":
    os.system('clear')
    print("\033[1;35m" + "╔═══════════════════════════════════════════╗")
    print("║        BULLET SLICER (Queue Mode)         ║")
    print("╚═══════════════════════════════════════════╝\033[0m")
    
    if not os.path.exists(CLIPS_DIR):
        print(f"\033[1;31m[!] Error: {CLIPS_DIR} not found!\033[0m")
        sys.exit()

    vids = sorted([f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))])
    
    if not vids:
        print("\033[1;31m[!] No videos found in clips/ folder!\033[0m")
        sys.exit()

    for idx, vid in enumerate(vids, 1):
        print(f"\033[1;37m {idx:02d}. \033[0m{vid}")

    choice = input("\n\033[1;36mSelect video number(s) (e.g. 1,4,6): \033[0m")
    
    try:
        selected_indices = [int(i.strip()) for i in choice.split(',')]
        queue = []

        for index in selected_indices:
            idx = index - 1
            if 0 <= idx < len(vids):
                video_path = os.path.join(CLIPS_DIR, vids[idx])
                duration = get_duration(video_path)
                
                print("\n" + "─"*45)
                print(f"\033[1;33m🎬 Video   : \033[1;37m{vids[idx]}\033[0m")
                print(f"\033[1;33m⏱️  Duration: \033[1;32m{format_time(duration)}\033[0m")
                print("─"*45)
                
                # ইনপুট নেওয়ার সময় শুধু প্রথম সংখ্যাটি নেওয়ার ব্যবস্থা
                slice_input = input(f"\033[1;36m[?] How many slices for this video?: \033[0m").strip()
                if slice_input.isdigit():
                    queue.append({
                        'path': video_path,
                        'duration': duration,
                        'slices': int(slice_input)
                    })
                else:
                    print("\033[1;31m[!] Invalid number. Skipping this video.\033[0m")
        
        if queue:
            print(f"\n\033[1;32m🚀 Starting Queue Processing ({len(queue)} videos)...\033[0m")
            start_total = time.time()
            
            for item in queue:
                process_slicing(item)
                
            end_total = time.time()
            print(f"\n\033[1;32m✅ ALL DONE! Total Time: {int(end_total - start_total)}s\033[0m")
            print(f"\033[1;37m📂 Output: ready_video/\033[0m")
        else:
            print("\033[1;31m[!] Queue is empty.\033[0m")

    except Exception as e:
        print(f"\033[1;31m[X] Error: {str(e)}\033[0m")
