#!/bin/bash

# --- কনফিগারেশন ---
# এখানে YOUR_TOKEN এর জায়গায় তোমার গিটহাব টোকেনটি বসাও
TOKEN="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"
USERNAME="redwan-primeAmax"
REPO_NAME="Termux-Video-ETit"

# সঠিক লিঙ্ক সেটআপ (যাতে পাসওয়ার্ড না চায়)
REMOTE_URL="https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"

echo "🚀 প্রোজেক্ট আপডেট শুরু হচ্ছে, রেদওয়ান..."

# ১. গিট কনফিগার করা (যদি আগে না করা থাকে)
git config --global user.email "redwanislam7900@gmail.com"

git config --global user.name "redwan-primeAmax"

# ২. রিমোট ইউআরএল আপডেট করা
git remote set-url origin "$REMOTE_URL" 2>/dev/null || git remote add origin "$REMOTE_URL"

# ৩. ফাইলগুলো অ্যাড করা
git add .

# ৪. কমিট করা (যদি কোনো পরিবর্তন থাকে)
commit_msg="Update by Redwan: $(date +'%d-%m-%Y %H:%M')"
if git commit -m "$commit_msg"; then
    echo "📦 পরিবর্তনগুলো সেভ করা হয়েছে..."
else
    echo "✨ নতুন কোনো পরিবর্তন নেই।"
fi

# ৫. গিটহাবে পুশ করা
echo "📤 ফাইলগুলো পাঠানো হচ্ছে..."
if git push -f origin main; then
    echo "✅ সফলভাবে গিটহাবে আপডেট হয়েছে!"
else
    echo "⚠️ সমস্যা হয়েছে, আবার চেষ্টা করা হচ্ছে..."
    git push -f origin master
fi
