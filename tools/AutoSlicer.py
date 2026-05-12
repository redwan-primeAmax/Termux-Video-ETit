import os
import sys
import subprocess

# পাথ কনফিগারেশন
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS_DIR = os.path.join(BASE_DIR, 'clips')
OUTPUT_DIR = '/sdcard/Ready_Video'

# আউটপুট ফোল্ডার নিশ্চিত করা
if not os.path.exists(OUTPUT_DIR):
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except:
        OUTPUT_DIR = os.path.join(BASE_DIR, 'ready_video')
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def slice_video(input_file):
    try:
        # ভিডিওর ডিউরেশন বের করা
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        duration = float(subprocess.check_output(cmd, shell=True))
        
        print(f"\n\033[1;33m[🎞️] বর্তমান ভিডিও: {os.path.basename(input_file)}\033[0m")
        print(f"⏱️ দৈর্ঘ্য: {duration:.2f} সেকেন্ড")
        
        num_slices = input(f"\033[1;36m[?] এই ভিডিওটি কয়টি ভাগে ভাগ করতে চান? (উদা: ৩): \033[0m")
        if not num_slices.isdigit():
            print("[!] ভুল ইনপুট, স্কিপ করা হলো।")
            return

        num_slices = int(num_slices)
        slice_duration = duration / num_slices
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        print(f"[>] {num_slices}টি স্লাইস তৈরি হচ্ছে (High Quality)...")
        for i in range(num_slices):
            start_time = i * slice_duration
            output_file = os.path.join(OUTPUT_DIR, f"{base_name}_part_{i+1}.mp4")
            
            # এখানে -c copy বদলে রেন্ডারিং এবং সঠিক বিটরেট দেওয়া হয়েছে যাতে ভিডিও ফ্রিজ না হয়
            ffmpeg_cmd = (
                f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
                f'-c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p '
                f'-c:a aac -b:a 128k "{output_file}" -loglevel error'
            )
            subprocess.run(ffmpeg_cmd, shell=True)
            
        print(f"\033[1;32m[✓] {os.path.basename(input_file)} সম্পন্ন!\033[0m")

    except Exception as e:
        print(f"[X] এরর: {str(e)}")

if __name__ == "__main__":
    # বাকি অংশ আগের মতোই থাকবে...
    vids = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))]
    if not vids:
        print("\n[!] কোনো ভিডিও পাওয়া যায়নি!")
        sys.exit()

    print("\nউপলব্ধ ভিডিওগুলো:")
    for idx, vid in enumerate(vids, 1):
        print(f"{idx}. {vid}")

    choice = input("\nকোন ভিডিওগুলো প্রসেস করবেন? নম্বর লিখুন: ")
    try:
        selected_indices = [int(i.strip()) for i in choice.split(',')]
        for index in selected_indices:
            if 1 <= index <= len(vids):
                target_video = os.path.join(CLIPS_DIR, vids[index-1])
                slice_video(target_video)
        print(f"\n\033[1;32m[🎉] সব কাজ শেষ! লোকেশন: {OUTPUT_DIR}\033[0m")
    except ValueError:
        print("\n[X] শুধু নম্বর দিন!")
