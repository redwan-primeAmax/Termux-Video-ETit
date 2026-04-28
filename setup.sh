#!/bin/bash

clear
echo "------------------------------------------"
echo "   Video Editor - 1 Click Setup"
echo "------------------------------------------"

# ১. ফোল্ডারের নাম জিজ্ঞেস করা
read -p "[?] Apnar project folder er naam ki rakhte chan? " FOLDER_NAME

if [ -z "$FOLDER_NAME" ]; then
    FOLDER_NAME="MyVideoEditor"
fi

# ২. ফোল্ডার এবং সাব-ফোল্ডার তৈরি
echo "[+] Creating structure in '$FOLDER_NAME'..."
mkdir -p "$FOLDER_NAME/Custom_Cutter/clips"
mkdir -p "$FOLDER_NAME/Cut_by_Duration/clips"
mkdir -p "$FOLDER_NAME/ready_video/Custom_Cutter"
mkdir -p "$FOLDER_NAME/ready_video/Cut_by_Duration"

# ৩. পাইথন স্ক্রিপ্টটি নতুন ফোল্ডারে মুভ করা
if [ -f "sc.py" ]; then
    mv sc.py "$FOLDER_NAME/"
else
    echo "[!] Error: sc.py khuje paoya jayni!"
    exit 1
fi

# ৪. সিস্টেম ডিপেন্ডেন্সি ইন্সটল করা
echo "[+] Installing Dependencies (Python & FFmpeg)..."
if [ -x "$(command -v pkg)" ]; then
    pkg update && pkg upgrade -y
    pkg install python ffmpeg -y
elif [ -x "$(command -v apt)" ]; then
    sudo apt update
    sudo apt install python3 ffmpeg -y
fi

echo "------------------------------------------"
echo "Success! Shob kichu '$FOLDER_NAME' folder e setup hoyeche."
echo "Ekhon bhetore jete likhun: cd $FOLDER_NAME"
echo "Tarpor run korun: python sc.py"
echo "------------------------------------------"

# ৫. নিজেকে ডিলিট করে দেওয়া
rm -- "$0"