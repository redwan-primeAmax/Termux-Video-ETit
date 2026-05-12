import os
import threading
import sys
import subprocess
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# পাথ কনফিগারেশন
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'app')
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'clips')

app = Flask(__name__, 
            template_folder=APP_DIR, 
            static_folder=APP_DIR, 
            static_url_path='')

# আনলিমিটেড ফাইল সাইজ সাপোর্ট
app.config['MAX_CONTENT_LENGTH'] = None 

# প্রয়োজনীয় ফোল্ডার নিশ্চিত করা
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TOOLS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"status": "error", "message": "কোনো ফাইল পাওয়া যায়নি"}), 400
    
    files = request.files.getlist('files')
    uploaded_count = 0

    for file in files:
        if file.filename != '':
            filename = secure_filename(file.filename)
            # দ্রুত লোকাল ট্রান্সফার
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            uploaded_count += 1
    
    return jsonify({"status": "success", "message": f"{uploaded_count}টি ফাইল দ্রুত আপলোড হয়েছে!"})

def run_tool(filename):
    path = os.path.join(TOOLS_DIR, filename)
    if not os.path.exists(path):
        print(f"\n\033[1;31m[X] এরর: tools/{filename} পাওয়া যায়নি!\033[0m")
        return
    try:
        print(f"\n\033[1;32m[🚀] {filename} রান হচ্ছে...\033[0m\n")
        subprocess.run([sys.executable, path])
    except Exception as e:
        print(f"\033[1;31m[!] এরর: {str(e)}\033[0m")

def start_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)

if __name__ == '__main__':
    threading.Thread(target=start_flask, daemon=True).start()
    
    print("\n" + "="*40)
    print("🚀 এডিটর কন্ট্রোল প্যানেল সচল!")
    print(f"🔗 লিঙ্ক: http://127.0.0.1:5000")
    print("="*40)

    try:
        while True:
            print("\n--- মেনু ---")
            print("১. Mode 1 (Custom Cutter)")
            print("২. Mode 2 (Auto Slicer)")
            print("০. বন্ধ করুন")
            choice = input("\nআপনার পছন্দ লিখুন: ")
            
            if choice == '1': run_tool('CustomCutter.py')
            elif choice == '2': run_tool('AutoSlicer.py')
            elif choice in ['0', 'o', '০']: os._exit(0)
            else: print("\033[1;31m[X] ভুল ইনপুট!\033[0m")
    except KeyboardInterrupt:
        os._exit(0)
