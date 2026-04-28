# 🎬 Smart Video Editor Pro 🚀
**The Ultimate Video Splitting & Joining Tool for Creators!**  
এটি একটি শক্তিশালী ভিডিও এডিটিং টুল যা আপনার বড় ভিডিওগুলোকে সোশ্যাল মিডিয়া (TikTok, CapCut, Reels) এর জন্য একদম নিখুঁতভাবে তৈরি করে দেয়।

---

## ✨ বিশেষ ফিচারসমূহ (Key Features):

✅ **Mode 1: Custom Cutter (JSON Based)**  
একটি ভিডিওর একাধিক নির্দিষ্ট অংশ (`start` এবং `end` টাইম অনুযায়ী) কাটবে এবং সবগুলোকে অটোমেটিক জোড়া দিয়ে একটি ফাইনাল আউটপুট দিবে।

✅ **Mode 2: Smart Duration Cutter**  
আপনার বড় ভিডিওকে নির্দিষ্ট মিনিট বা সেকেন্ডে ভাগ করবে। এতে **'Smart Adjust'** ফিচার আছে, যা ক্লিপগুলোকে এমনভাবে ব্যালেন্স করে যাতে শেষ ক্লিপটি অযথা ছোট না হয়।

✅ **Optimized for Apps**  
সবগুলো ক্লিপ `libx264` ভিডিও কোডেক এবং `aac` অডিওতে প্রসেস হয়, যা **CapCut, TikTok, InShot** এবং যেকোনো এডিটিং অ্যাপে কালার বা অডিওর কোনো সমস্যা ছাড়াই কাজ করবে।

✅ **One-Click Setup**  
আপনার পিসি বা Termux-এ কোনো ঝামেলা ছাড়াই সব ডিরেক্টরি এবং ডিপেন্ডেন্সি অটোমেটিক সেটআপ করে দেয়।

---

## 🛠 কিভাবে ইন্সটল করবেন (Installation Guide):

আপনার টার্মিনালে বা Termux-এ নিচের ধাপগুলো অনুসরণ করুন:
মেইন: **pkg install git -y** এটা দিয়ে বাকি কাজ করো।

### ১. রিপোজিটরি ক্লোন করুন
প্রথমে GitHub-এর সবুজ রঙের **"<> Code"** বাটনে ক্লিক করে প্রোজেক্টের লিঙ্কটি কপি করে নিন। তারপর আপনার টার্মিনালে নিচের কমান্ডটি লিখুন:
```bash
git clone https://github.com/redwan-primeAmax/Termux-Video-ETit.git
```

### ২. ফোল্ডারে প্রবেশ করুন
```bash
cd /sdcard/আপনার ফোল্ডার নাম
```

### ৩. অটো-সেটআপ রান করুন
এখন শুধু নিচের কমান্ডটি দিন। এটি আপনাকে একটি নতুন ফোল্ডার নাম জিজ্ঞেস করবে এবং সব ফাইল গুছিয়ে দিবে:
```bash
bash setup.sh
```
*(সেটআপ শেষ হলে `setup.sh` ফাইলটি অটোমেটিক রিমুভ হয়ে যাবে।)*

---

## 🎮 কিভাবে ব্যবহার করবেন (How to Use):

সেটআপ শেষ হলে আপনার নতুন প্রজেক্ট ফোল্ডারে গিয়ে কমান্ড দিন:
```bash
python sc.py
```

### 🔹 Mode 1: Custom Cutter
- আপনার ভিডিও ফাইলটি `Custom_Cutter/clips` ফোল্ডারে রাখুন।
- `Custom_Cutter/info.json` ফাইলে ভিডিওর নাম এবং কোন কোন অংশ কাটতে চান তা লিখে দিন।
- টুলটি রান করে অপশন **1** সিলেক্ট করুন।

### 🔹 Mode 2: Duration Cutter
- আপনার ভিডিও ফাইলটি `Cut_by_Duration/clips` ফোল্ডারে রাখুন।
- টুলটি রান করে অপশন **2** সিলেক্ট করুন।
- কত মিনিট বা সেকেন্ডের ক্লিপ চান তা দিন। ব্যস! সব ক্লিপ `ready_video/` ফোল্ডারে পেয়ে যাবেন।

---

## 📁 ফোল্ডার স্ট্রাকচার (Folder Structure):
```text
📂 Project_Folder/
├── 📄 sc.py (Main Script)
├── 📂 Custom_Cutter/
│   ├── 📄 info.json
│   └── 📂 clips/ (Input Videos Here)
└── 📂 Cut_by_Duration/
    └── 📂 clips/ (Input Videos Here)
└── 📂 ready_video/ (Output Folders)
```

---

## 🛡 সিকিউরিটি এবং কোয়ালিটি:
- **No Quality Loss:** প্রতিটি ক্লিপ CRF 22 ব্যবহার করে প্রসেস করা হয়, যা হাই কোয়ালিটি নিশ্চিত করে।
- **Clean Environment:** কোনো টেম্পোরারি ফাইল আপনার স্টোরেজে জমা থাকবে না, কাজ শেষে সব অটো ডিলিট হয়ে যাবে।

---
*Developed with "Redwan" for Content Creators.*  
🌟 **Star this repo if you like it!**
