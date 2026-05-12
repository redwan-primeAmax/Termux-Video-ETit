#!/bin/bash

clear
echo "=========================================="
echo "   Termux Video Editor - Clean Setup    "
echo "=========================================="

# রেন্ডম ফোল্ডার তৈরি
RANDOM_NAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1)
INTERNAL_DIR="$HOME/$RANDOM_NAME"

# প্রয়োজনীয় ফোল্ডার তৈরি (এখানেই সব ফ্রন্ট-এন্ড ফাইল থাকবে)
mkdir -p "$INTERNAL_DIR/app"
mkdir -p "$INTERNAL_DIR/tools"
mkdir -p "$INTERNAL_DIR/clips"

CURRENT_PATH=$(pwd)

# ফাইলগুলো সঠিক জায়গায় কপি করা
echo "[+] ফাইলগুলো গোছানো হচ্ছে..."

# ১. মেইন কন্ট্রোল ফাইল
cp "$CURRENT_PATH/sc.py" "$INTERNAL_DIR/"

# ২. ফ্রন্ট-এন্ড ফাইলগুলো শুধু app/ ফোল্ডারে যাবে
cp "$CURRENT_PATH/index.html" "$INTERNAL_DIR/app/"
cp "$CURRENT_PATH/index.css" "$INTERNAL_DIR/app/"
cp "$CURRENT_PATH/index.js" "$INTERNAL_DIR/app/"

# ৩. টুলস কপি করা
if [ -d "$CURRENT_PATH/tools" ]; then
    cp -r "$CURRENT_PATH/tools"/* "$INTERNAL_DIR/tools/"
fi

# প্রজেক্ট রান করা
cd "$INTERNAL_DIR"
python sc.py
