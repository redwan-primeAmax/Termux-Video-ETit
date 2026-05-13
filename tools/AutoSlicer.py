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

def slice_video(input_file):
    try:
        # Duration বের করা
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        duration = float(subprocess.check_output(cmd, shell=True))
        
        print("\n" + "─"*45)
        print(f"\033[1;33m🎬 File      : \033[1;37m{os.path.basename(input_file)}\033[0m")
        print(f"\033[1;33m⏱️  Duration  : \033[1;32m{format_time(duration)}\033[0m")
        print("─"*45)
        
        num_slices = input(f"\n\033[1;36m[?] How many slices? (e.g. 3): \033[0m")
        if not num_slices.isdigit(): return

        num_slices = int(num_slices)
        slice_duration = duration / num_slices
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        start_total = time.time() # টাইমার শুরু

        for i in range(num_slices):
            start_time = i * slice_duration
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_part_{i+1}.mp4")
            
            # --- বুলেট স্পিড সলিউশন ---
            # -c copy ব্যবহার করলে রি-এনকোডিং হবে না, সরাসরি ফাইল কাটবে।
            # -avoid_negative_ts make_zero ভিডিও প্লেয়ারে ল্যাগ হওয়া আটকাবে।
            ffmpeg_cmd = (
                f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
                f'-c copy -avoid_negative_ts make_zero -map_metadata 0 '
                f'-movflags +faststart "{output_file}" -loglevel error'
            )
            
            print(f"\033[1;34m[⚡] Slicing part {i+1}...\033[0m")
            subprocess.run(ffmpeg_cmd, shell=True)
            
        end_total = time.time()
        print(f"\n\033[1;32m✅ DONE! Total Time: {int(end_total - start_total)}s\033[0m")
        print(f"\033[1;37m📂 Saved in: ready_video\033[0m")

    except Exception as e:
        print(f"\033[1;31m[X] Error: {str(e)}\033[0m")

if __name__ == "__main__":
    os.system('clear')
    print("\033[1;35m" + "╔═══════════════════════════════════════════╗")
    print("║        BULLET SLICER (Low-End Fix)        ║")
    print("╚═══════════════════════════════════════════╝\033[0m")
    
    vids = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov'))]
    if not vids: sys.exit()

    for idx, vid in enumerate(vids, 1):
        print(f"\033[1;37m {idx}. \033[0m{vid}")

    choice = input("\n\033[1;36mSelect video number: \033[0m")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(vids):
            slice_video(os.path.join(CLIPS_DIR, vids[idx]))
    except: pass
