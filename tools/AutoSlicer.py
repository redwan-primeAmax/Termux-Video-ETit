import os
import sys
import subprocess

# Always connect to Path 1
BASE_DIR = os.path.expanduser("~/Termux-Video-ETit")
CLIPS_DIR = os.path.join(BASE_DIR, 'clips')
OUTPUT_DIR = os.path.join(BASE_DIR, 'ready_video')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def slice_video(input_file):
    try:
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        duration = float(subprocess.check_output(cmd, shell=True))
        
        print(f"\n[🎞️] Processing: {os.path.basename(input_file)}")
        num_slices = input(f"[?] How many slices? (e.g. 3): ")
        
        if not num_slices.isdigit():
            print("[!] Invalid input!")
            return

        num_slices = int(num_slices)
        slice_duration = duration / num_slices
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        for i in range(num_slices):
            start_time = i * slice_duration
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_part_{i+1}.mp4")
            
            # Optimized for mobile to prevent crashing
            ffmpeg_cmd = (
                f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
                f'-c:v libx264 -preset superfast -crf 24 -pix_fmt yuv420p '
                f'-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '
                f'-c:a aac -b:a 128k -movflags +faststart "{output_file}" -loglevel error'
            )
            print(f"[>] Creating slice {i+1}/{num_slices}...")
            subprocess.run(ffmpeg_cmd, shell=True)
            
        print(f"\n[✓] Done! Files saved in: {OUTPUT_DIR}")

    except Exception as e:
        print(f"[X] Error: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(CLIPS_DIR):
        print(f"[!] Error: {CLIPS_DIR} not found!")
        sys.exit()
        
    vids = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))]
    
    if not vids:
        print(f"[!] No videos found in: {CLIPS_DIR}")
        sys.exit()

    print("\n--- Auto Slicer (English Mode) ---")
    for idx, vid in enumerate(vids, 1):
        print(f"{idx}. {vid}")

    choice = input("\nEnter video number(s): ")
    try:
        indices = [int(i.strip()) for i in choice.split(',')]
        for index in indices:
            if 1 <= index <= len(vids):
                slice_video(os.path.join(CLIPS_DIR, vids[index-1]))
    except ValueError:
        print("[X] Please enter valid numbers!")
