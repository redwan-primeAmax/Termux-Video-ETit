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
    """সেকেন্ডকে mm:ss ফরম্যাটে কনভার্ট করার ফাংশন"""
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

def animated_loading(text):
    """টার্মিনালে ছোট একটি লোডিং অ্যানিমেশন"""
    chars = "/—\\|"
    for i in range(10):
        sys.stdout.write(f"\r\033[1;36m[{chars[i % len(chars)]}] {text}...\033[0m")
        sys.stdout.flush()
        time.sleep(0.1)
    print()

def slice_video(input_file):
    try:
        # ffprobe দিয়ে ডিউরেশন বের করা
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        duration = float(subprocess.check_output(cmd, shell=True))
        
        # UI ডিজাইন
        print("\n" + "─"*45)
        print(f"\033[1;33m🎬 File      : \033[1;37m{os.path.basename(input_file)}\033[0m")
        print(f"\033[1;33m⏱️  Duration  : \033[1;32m{format_time(duration)}\033[0m") # এখানে mm:ss দেখাবে
        print("─"*45)
        
        num_slices = input(f"\n\033[1;36m[?] How many slices? (e.g. 3): \033[0m")
        
        if not num_slices.isdigit():
            print("\033[1;31m[!] Invalid input! Please enter a number.\033[0m")
            return

        num_slices = int(num_slices)
        slice_duration = duration / num_slices
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        for i in range(num_slices):
            start_time = i * slice_duration
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_part_{i+1}.mp4")
            
            print(f"\n\033[1;34m[➔] Creating part {i+1} of {num_slices}...\033[0m")
            
            ffmpeg_cmd = (
                f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
                f'-c:v libx264 -preset superfast -crf 24 -pix_fmt yuv420p '
                f'-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '
                f'-c:a aac -b:a 128k -movflags +faststart "{output_file}" -loglevel error'
            )
            
            subprocess.run(ffmpeg_cmd, shell=True)
            
        animated_loading("Finalizing all parts")
        print(f"\n\033[1;32m✅ SUCCESS: Files saved in 'ready_video' folder.\033[0m")

    except Exception as e:
        print(f"\033[1;31m[X] Error: {str(e)}\033[0m")

if __name__ == "__main__":
    if not os.path.exists(CLIPS_DIR):
        print(f"\033[1;31m[!] Error: {CLIPS_DIR} not found!\033[0m")
        sys.exit()
        
    vids = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))]
    
    if not vids:
        print(f"\033[1;31m[!] No videos found in 'clips' folder!\033[0m")
        sys.exit()

    # মেইন হেডার ডিজাইন
    os.system('clear')
    print("\033[1;35m" + "╔═══════════════════════════════════════════╗")
    print("║          AUTO VIDEO SLICER PRO            ║")
    print("╚═══════════════════════════════════════════╝\033[0m")
    
    for idx, vid in enumerate(vids, 1):
        print(f"\033[1;37m {idx}. \033[0m{vid}")

    choice = input("\n\033[1;36mSelect video number(s): \033[0m")
    try:
        indices = [int(i.strip()) for i in choice.split(',')]
        for index in indices:
            if 1 <= index <= len(vids):
                slice_video(os.path.join(CLIPS_DIR, vids[index-1]))
    except ValueError:
        print("\033[1;31m[X] Please enter valid numbers!\033[0m")
