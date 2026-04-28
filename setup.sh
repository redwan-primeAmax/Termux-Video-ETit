#!/bin/bash

clear
echo "------------------------------------------"
echo "   Video Editor - Auto Setup Started"
echo "------------------------------------------"

# ১. স্টোরেজ পারমিশন রিকোয়েস্ট (নতুন যোগ করা হয়েছে)
echo "[+] Requesting Storage Access... Please click 'Allow' on your phone screen."
termux-setup-storage
sleep 4 # ইউজারকে পারমিশন দেওয়ার জন্য একটু সময় দেওয়া

# ২. ফোল্ডার নাম জিজ্ঞেস করা
read -p "[?] Apnar project folder er naam ki rakhte chan? " FOLDER_NAME

if [ -z "$FOLDER_NAME" ]; then
    FOLDER_NAME="MyVideoEditor"
fi

# ৩. প্রয়োজনীয় ডিরেক্টরি তৈরি
echo "[+] Creating project structure in '$FOLDER_NAME'..."
mkdir -p "$FOLDER_NAME/Custom_Cutter/clips"
mkdir -p "$FOLDER_NAME/Cut_by_Duration/clips"
mkdir -p "$FOLDER_NAME/ready_video/Custom_Cutter"
mkdir -p "$FOLDER_NAME/ready_video/Cut_by_Duration"

# ৪. sc.py মুভ করা
if [ -f "sc.py" ]; then
    mv sc.py "$FOLDER_NAME/"
else
    echo "[!] Error: sc.py khuje paoya jayni! GitHub clone thikmoto hoyeche ki na check korun."
    exit 1
fi

# ৫. FFmpeg & Python ইন্সটল
echo "[+] Installing Dependencies (Python & FFmpeg)..."
if [ -x "$(command -v pkg)" ]; then
    pkg update && pkg upgrade -y
    pkg install python ffmpeg -y
elif [ -x "$(command -v apt)" ]; then
    sudo apt update
    sudo apt install python3 ffmpeg -y
fi

echo "------------------------------------------------"
echo "Setup Complete! Folder Name: $FOLDER_NAME"
echo "Ekhon bhetore jete likhun: cd $FOLDER_NAME"
echo "Tarpor run korun: python sc.py"
echo "------------------------------------------------"

# ৬. নিজেকে ডিলিট করা
rm -- "$0"