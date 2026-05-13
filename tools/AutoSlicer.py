import os
import sys
import subprocess

# --- পাথ ফিক্স: সরাসরি তোমার বর্তমান প্রজেক্ট ফোল্ডারকে টার্গেট করা ---
# যেহেতু তোমার লোকেশন ~/Termux-Video-ETit
BASE_DIR = os.path.expanduser("~/Termux-Video-ETit")
CLIPS_DIR = os.path.join(BASE_DIR, 'clips')
OUTPUT_DIR = os.path.join(BASE_DIR, 'ready_video')

# আউটপুট ফোল্ডার নিশ্চিত করা
os.makedirs(OUTPUT_DIR, exist_ok=True)

def slice_video(input_file):
    try:
        # ভিডিওর ডিউরেশন বের করা
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        duration = float(subprocess.check_output(cmd, shell=True))
        
        print(f"\n\033[1;33m[🎞️] প্রসেস হচ্ছে: {os.path.basename(input_file)}\033[0m")
        num_slices = input(f"\033[1;36m[?] কয়টি ভাগে ভাগ করতে চান? (উদা: ৩): \033[0m")
        
        if not num_slices.isdigit():
            print("[!] ভুল ইনপুট!")
            return

        num_slices = int(num_slices)
        slice_duration = duration / num_slices
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        for i in range(num_slices):
            start_time = i * slice_duration
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_part_{i+1}.mp4")
            
            # মোবাইল অপ্টিমাইজড কমান্ড
            ffmpeg_cmd = (
                f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
                f'-c:v libx264 -preset superfast -crf 24 -pix_fmt yuv420p '
                f'-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '
                f'-c:a aac -b:a 128k -movflags +faststart "{output_file}" -loglevel error'
            )
            
            print(f"[>] স্লাইস {i+1}/{num_slices} তৈরি হচ্ছে...")
            subprocess.run(ffmpeg_cmd, shell=True)
            
        print(f"\033[1;32m[✓] সম্পন্ন! ফাইলগুলো আছে: {OUTPUT_DIR}\033[0m")

    except Exception as e:
        print(f"[X] এরর: {str(e)}")

if __name__ == "__main__":
    # বর্তমান ডিরেক্টরি চেক করা
    if not os.path.exists(CLIPS_DIR):
        print(f"\n[!] এরর: {CLIPS_DIR} ফোল্ডারটি পাওয়া যায়নি!")
        # যদি না পাওয়া যায়, তবে বর্তমান ডিরেক্টরির clips খোঁজা
        CLIPS_DIR = os.path.join(os.getcwd(), 'clips')
        
    vids = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))]
    
    if not vids:
        print(f"\n[!] চেক করা লোকেশন: {CLIPS_DIR}")
        print("[!] এই ফোল্ডারে কোনো ভিডিও ফাইল নেই!")
        sys.exit()

    print("\n--- Auto Slicer (Final Path Fix) ---")
    for idx, vid in enumerate(vids, 1):
        print(f"{idx}. {vid}")

    choice = input("\nভিডিওর নম্বর দিন: ")
    try:
        selected_indices = [int(i.strip()) for i in choice.split(',')]
        for index in selected_indices:
            if 1 <= index <= len(vids):
                target_video = os.path.join(CLIPS_DIR, vids[index-1])
                slice_video(target_video)
    except ValueError:
        print("\n[X] সঠিক নম্বর দিন!")
