import os
import sys
import subprocess

# --- পাথ কনফিগারেশন ---
# সরাসরি তোমার বর্তমান প্রজেক্ট ফোল্ডারকে টার্গেট করা
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
        print(f"⏱️ মোট সময়: {duration:.2f} সেকেন্ড")
        
        num_slices = input(f"\033[1;36m[?] কয়টি ভাগে ভাগ করতে চান? (উদা: ৩): \033[0m")
        
        if not num_slices.isdigit():
            print("\033[1;31m[!] ভুল ইনপুট! শুধু সংখ্যা দিন।\033[0m")
            return

        num_slices = int(num_slices)
        slice_duration = duration / num_slices
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        for i in range(num_slices):
            start_time = i * slice_duration
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_part_{i+1}.mp4")
            
            # মোবাইল অপ্টিমাইজড FFmpeg কমান্ড
            ffmpeg_cmd = (
                f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
                f'-c:v libx264 -preset superfast -crf 24 -pix_fmt yuv420p '
                f'-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '
                f'-c:a aac -b:a 128k -movflags +faststart "{output_file}" -loglevel error'
            )
            
            print(f"[>] স্লাইস {i+1}/{num_slices} তৈরি হচ্ছে...")
            subprocess.run(ffmpeg_cmd, shell=True)
            
        print(f"\n\033[1;32m[✓] সফলভাবে সম্পন্ন হয়েছে!\033[0m")
        print(f"\033[1;32m📂 ফাইলগুলো এখানে আছে: {OUTPUT_DIR}\033[0m")

    except Exception as e:
        print(f"\033[1;31m[X] এরর: {str(e)}\033[0m")

if __name__ == "__main__":
    # clips ফোল্ডার চেক করা
    if not os.path.exists(CLIPS_DIR):
        print(f"\n\033[1;31m[!] এরর: '{CLIPS_DIR}' ফোল্ডারটি পাওয়া যায়নি!\033[0m")
        sys.exit()
        
    # ভিডিও ফাইলগুলো খুঁজে বের করা
    vids = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))]
    
    if not vids:
        print(f"\n\033[1;31m[!] এই ফোল্ডারে কোনো ভিডিও ফাইল নেই!\033[0m")
        print(f"📁 লোকেশন চেক করুন: {CLIPS_DIR}")
        sys.exit()

    print("\n\033[1;34m========================================\033[0m")
    print("\033[1;32m       অটো ভিডিও স্লাইসার (বাংলা)       \033[0m")
    print("\033[1;34m========================================\033[0m")
    
    for idx, vid in enumerate(vids, 1):
        print(f"{idx}. {vid}")

    choice = input("\n[?] ভিডিওর নম্বর লিখুন (একাধিক হলে কমা দিন, উদা: ১,২): ")
    try:
        selected_indices = [int(i.strip()) for i in choice.split(',')]
        for index in selected_indices:
            if 1 <= index <= len(vids):
                target_video = os.path.join(CLIPS_DIR, vids[index-1])
                slice_video(target_video)
            else:
                print(f"\033[1;31m[!] {index} নম্বর ভিডিওটি তালিকায় নেই।\033[0m")
    except ValueError:
        print("\n\033[1;31m[X] দয়া করে সঠিক নম্বর দিন!\033[0m")
