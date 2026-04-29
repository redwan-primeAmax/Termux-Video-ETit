#!/bin/bash

clear
echo "=========================================="
echo "   Advanced Video Editor Auto Setup"
echo "=========================================="

# ১. স্টোরেজ পারমিশন
echo "[+] Requesting Storage Access..."
termux-setup-storage
sleep 2

# ২. পাথ/ফোল্ডার নাম ইনপুট
echo "Apni project-ti kothay rakhte chan?"
echo "Example: 'MyVideos' (Termux-e thakbe) ba '/sdcard/MyVideos' (Phone-e thakbe)"
read -p "[?] Path ba Folder er naam likhun: " TARGET_PATH

if [ -z "$TARGET_PATH" ]; then
    TARGET_PATH="$HOME/VideoEditorProject"
fi

# ৩. সিস্টেম আপডেট ও ডিপেন্ডেন্সি
echo "[+] Installing Python & FFmpeg..."
pkg update && pkg upgrade -y
pkg install python ffmpeg -y

# ৪. ডিরেক্টরি স্ট্রাকচার তৈরি (Absolute Path Handling)
echo "[+] Creating Directories at $TARGET_PATH..."
mkdir -p "$TARGET_PATH/Custom_Cutter/clips"
mkdir -p "$TARGET_PATH/Cut_by_Duration/clips"
mkdir -p "$TARGET_PATH/ready_video/Custom_Cutter"
mkdir -p "$TARGET_PATH/ready_video/Cut_by_Duration"

# ৫. ফাইল মাইগ্রেশন (sc.py কে টার্গেট ফোল্ডারে পাঠানো)
if [ -f "sc.py" ]; then
    cp sc.py "$TARGET_PATH/"
    echo "[+] sc.py moved to $TARGET_PATH"
else
    echo "[!] Error: sc.py not found in current folder!"
    exit 1
fi

# ৬. ফিনিশিং এবং ক্লোন ফোল্ডার ক্লিনআপ গাইড
REPO_DIR=$(pwd)
echo "------------------------------------------"
echo "Setup Complete!"
echo "Apnar project ekhon eikhane: $TARGET_PATH"
echo "------------------------------------------"
echo "Ekhon nicher command-ti diye kaj shuru korun:"
echo "cd $TARGET_PATH && python sc.py"
echo "------------------------------------------"

# বর্তমান স্ক্রিপ্ট ডিলিট করা
rm -- "$0"

# ইউজারকে ক্লোন ফোল্ডার ডিলিট করতে সাজেস্ট করা (নিরাপত্তার খাতিরে অটো ডিলিট এড়ানো হয়েছে)
echo "[Tip] Kaj sheshe 'rm -rf $REPO_DIR' diye clone folder-ti muche felte paren."