import os
import threading
import sys
import subprocess
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# --- Path Configuration ---
BASE_DIR = os.path.expanduser("~/Termux-Video-ETit")
APP_DIR = os.path.join(BASE_DIR, 'app')
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'clips')

app = Flask(__name__, 
            template_folder=APP_DIR, 
            static_folder=APP_DIR, 
            static_url_path='')

app.config['MAX_CONTENT_LENGTH'] = None 

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TOOLS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"status": "error", "message": "No files found"}), 400
    
    files = request.files.getlist('files')
    uploaded_count = 0
    for file in files:
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            uploaded_count += 1
    return jsonify({"status": "success", "message": f"{uploaded_count} files uploaded!"})

def run_tool(filename):
    path = os.path.join(TOOLS_DIR, filename)
    if not os.path.exists(path):
        print(f"\n\033[1;31m[X] Error: {path} not found!\033[0m")
        return
    try:
        print(f"\n\033[1;32m[🚀] Running {filename}...\033[0m\n")
        subprocess.run([sys.executable, path])
    except Exception as e:
        print(f"\033[1;31m[!] Error: {str(e)}\033[0m")

def start_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)

if __name__ == '__main__':
    # --- STEP 1: GitHub Auto-Update ---
    try:
        print("\n\033[1;34m[🔄] Checking for updates from GitHub...\033[0m")
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=BASE_DIR)
        print("\033[1;32m[✓] Repository is up to date.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Update failed: {str(e)}\033[0m")

    # --- STEP 2: Start Flask Thread ---
    threading.Thread(target=start_flask, daemon=True).start()
    
    print("\n" + "="*45)
    print("🚀 EDITOR CONTROL PANEL ACTIVE")
    print(f"🔗 URL: http://127.0.0.1:5000")
    print("="*45)

    # --- STEP 3: Control Menu ---
    try:
        while True:
            print("\n--- MENU ---")
            print("1. Mode 1 (Custom Cutter)")
            print("2. Mode 2 (Auto Slicer)")
            print("0. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == '1':
                run_tool("QuickSplit.py")
            elif choice == '2':
                run_tool("AutoSlicer.py")
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")
    except KeyboardInterrupt:
        print("\nStopping...")
        sys.exit()
