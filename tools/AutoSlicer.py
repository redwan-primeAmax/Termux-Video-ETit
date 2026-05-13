import os
import sys
import subprocess
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel

console = Console()

# --- Path Configuration ---
BASE_DIR = os.path.expanduser("~/Termux-Video-ETit")
CLIPS_DIR = os.path.join(BASE_DIR, 'clips')
FINAL_OUTPUT = "/sdcard/Video-ETit-Ready"

if not os.path.exists(FINAL_OUTPUT):
    os.makedirs(FINAL_OUTPUT, exist_ok=True)

def get_duration(input_file):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
    return float(subprocess.check_output(cmd, shell=True))

def process_slicing(video_data, progress, task_id):
    input_file = video_data['path']
    duration = video_data['duration']
    num_slices = video_data['slices']
    
    slice_duration = duration / num_slices
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    for i in range(num_slices):
        start_time = i * slice_duration
        output_file = os.path.join(FINAL_OUTPUT, f"{base_name}_part_{i+1}.mp4")
        
        ffmpeg_cmd = (
            f'ffmpeg -y -ss {start_time} -t {slice_duration} -i "{input_file}" '
            f'-c copy -map 0 -copyts -start_at_zero -avoid_negative_ts make_zero '
            f'-movflags +faststart "{output_file}" -loglevel error'
        )
        
        subprocess.run(ffmpeg_cmd, shell=True)
        # প্রগ্রেস বার আপডেট করা
        progress.update(task_id, advance=1)

if __name__ == "__main__":
    console.clear()
    console.print(Panel.fit("[bold magenta]ETit - ULTRA SYNC SLICER PRO[/bold magenta]\n[cyan]Developed by Redwan[/cyan]", border_style="green"))
    
    vids = sorted([f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mp4', '.mkv', '.mov', '.avi'))])
    if not vids: 
        console.print("[red][!] No videos found![/red]")
        sys.exit()

    # সুন্দর টেবিল তৈরি
    table = Table(title="Available Clips", show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim", width=6)
    table.add_column("File Name", style="white")

    for idx, vid in enumerate(vids, 1):
        table.add_row(f"{idx:02d}", vid)
    
    console.print(table)

    choice = console.input("\n[bold yellow]Select video number(s) (e.g. 1,2): [/bold yellow]")
    
    try:
        selected_indices = [int(i.strip()) for i in choice.split(',')]
        queue = []

        for index in selected_indices:
            idx = index - 1
            if 0 <= idx < len(vids):
                video_path = os.path.join(CLIPS_DIR, vids[idx])
                duration = get_duration(video_path)
                console.print(f"[green][+] Added:[/green] {vids[idx]}")
                
                slice_input = console.input(f"    [cyan]Slices for this video?: [/cyan]").strip()
                if slice_input.isdigit():
                    queue.append({'path': video_path, 'duration': duration, 'slices': int(slice_input), 'name': vids[idx]})
        
        if queue:
            console.print("\n[bold green]⚡ Starting Optimized Slicing...[/bold green]")
            
            # প্রগ্রেস বার সেটআপ
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=None),
                "[progress.percentage]{task.percentage:>3.0f}%",
                TimeElapsedColumn(),
                console=console
            ) as progress:
                
                for item in queue:
                    task = progress.add_task(f"[yellow]Slicing {item['name']}...[/yellow]", total=item['slices'])
                    process_slicing(item, progress, task)
            
            console.print(Panel(f"[bold green]✅ DONE![/bold green]\n[white]Check your SD Card / Gallery.[/white]\n[cyan]Path: {FINAL_OUTPUT}[/cyan]", title="Success"))
        
    except Exception as e:
        console.print(f"[bold red][X] Error: {str(e)}[/bold red]")
