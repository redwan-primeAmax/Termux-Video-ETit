import json
import os
import subprocess
import math
import sys

# ১. ফোল্ডারগুলো চেক এবং তৈরি করার ফাংশন
def check_folders():
    dirs = [
        'Custom_Cutter/clips',
        'Cut_by_Duration/clips',
        'ready_video/Custom_Cutter',
        'ready_video/Cut_by_Duration'
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

# ২. কমান্ড রান করার ফাংশন
def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

# ৩. ভিডিওর ডিউরেশন বের করার ফাংশন
def get_duration(file_path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    return float(result)

# ৪. ভিডিও প্রসেসিং (FFmpeg সেটিংস)
def process_video(input_file, start, duration, output_name):
    cmd = (
        f'ffmpeg -y -ss {start} -t {duration} -i "{input_file}" '
        f'-c:v libx264 -preset ultrafast -crf 22 -pix_fmt yuv420p '
        f'-c:a aac -b:a 128k "{output_name}"'
    )
    run_cmd(cmd)

# ৫. ফাইল লিস্ট করা এবং ইউজারকে সিলেক্ট করতে দেওয়া
def list_and_select_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    if not files:
        print(f"\n[!] Error: '{folder_path}' ফোল্ডারে কোনো ভিডিও পাওয়া যায়নি।")
        return []

    print("\n--- Available Videos ---")
    for i, file in enumerate(files):
        print(f"[{i+1}] {file}")

    try:
        user_input = input("\nভিডিওর নাম্বারগুলো লিখুন (যেমন: 1,3,4): ")
        indices = [int(x.strip()) - 1 for x in user_input.split(',')]
        return [files[i] for i in indices if 0 <= i < len(files)]
    except (ValueError, IndexError):
        print("ভুল নাম্বার দিয়েছেন!")
        return []

# --- মোড ১: Custom Cutter ---
def mode_custom_cutter():
    info_path = os.path.join('Custom_Cutter', 'info.json')
    clips_dir = os.path.join('Custom_Cutter', 'clips')
    output_dir = os.path.join('ready_video', 'Custom_Cutter')

    selected_files = list_and_select_files(clips_dir)
    if not selected_files: return

    if not os.path.exists(info_path):
        print(f"[!] Error: {info_path} ফাইলটি পাওয়া যায়নি!")
        return

    with open(info_path, 'r') as f:
        video_list = json.load(f)

    for video_name in selected_files:
        video_data = next((item for item in video_list if item["video_file"] == video_name), None)
        if not video_data:
            print(f"Skipping: {video_name} এর তথ্য info.json এ নেই।")
            continue

        video_input_path = os.path.join(clips_dir, video_name)
        segments, temp_files = video_data['segments'], []
        
        print(f"\n>> প্রসেসিং কাস্টম কাটার: {video_name}")
        for i, seg in enumerate(segments):
            start, duration = seg['start'], seg['end'] - seg['start']
            temp_name = f"part_{i}_{video_name}"
            process_video(video_input_path, start, duration, temp_name)
            temp_files.append(temp_name)

        list_file = f"list_{video_name}.txt"
        with open(list_file, 'w') as f:
            for name in temp_files: f.write(f"file '{name}'\n")

        final_output = os.path.join(output_dir, f"final_{video_name}")
        run_cmd(f'ffmpeg -y -f concat -safe 0 -i {list_file} -c copy "{final_output}"')
        
        for name in temp_files: os.remove(name)
        os.remove(list_file)
    print(f"\nকাজ শেষ! আউটপুট পাবেন: {output_dir}")

# --- মোড ২: Duration Cutter ---
def mode_duration_cutter():
    clips_dir = os.path.join('Cut_by_Duration', 'clips')
    output_dir = os.path.join('ready_video', 'Cut_by_Duration')

    selected_files = list_and_select_files(clips_dir)
    if not selected_files: return

    try:
        minutes = int(input("কত মিনিট পর পর কাটবেন? (মিনিট): "))
        sec_input = input("কত সেকেন্ড? (না থাকলে 1 লিখুন): ")
        seconds = 0 if sec_input == '1' else int(sec_input)
        target_duration = (minutes * 60) + seconds
        adjust_choice = input("স্মার্ট এডজাস্ট (Smart Adjust) করবেন? (y/n): ").lower()
    except ValueError: return

    for video_name in selected_files:
        video_input_path = os.path.join(clips_dir, video_name)
        total_duration = get_duration(video_input_path)
        
        if adjust_choice == 'y':
            num_parts = math.ceil(total_duration / target_duration)
            seg_duration = total_duration / num_parts
        else:
            seg_duration = target_duration

        print(f"\n>> স্প্লিট করা হচ্ছে: {video_name}")
        current_start, part_num = 0, 1
        while current_start < total_duration:
            remaining = total_duration - current_start
            if remaining < 1: break
            clip_duration = min(seg_duration, remaining)
            output_name = os.path.join(output_dir, f"part_{part_num}_{video_name}")
            process_video(video_input_path, current_start, clip_duration, output_name)
            current_start += clip_duration
            part_num += 1
    print(f"\nকাজ শেষ! আউটপুট পাবেন: {output_dir}")

# --- মেইন ফাংশন ---
def main():
    check_folders()
    try:
        print("\n=== Smart Video Editor Pro ===")
        print("1. কাস্টম কাটার (Mode 1)")
        print("2. ডিউরেশন অনুযায়ী কাটা (Mode 2)")
        choice = input("\nঅপশন সিলেক্ট করুন (1/2): ")
        if choice == '1': mode_custom_cutter()
        elif choice == '2': mode_duration_cutter()
        else: print("ভুল অপশন সিলেক্ট করেছেন।")
    except KeyboardInterrupt:
        print("\n\nস্ক্রিপ্ট বন্ধ করা হয়েছে। আল্লাহ হাফেজ!")
        sys.exit()

if __name__ == "__main__":
    main()