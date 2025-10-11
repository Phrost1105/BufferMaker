#!/usr/bin/env python3
"""
Video Buffer and Merge Generator
--------------------------------
Features:
1. Generate Buffer: Converts input, then merges with glitch.mp4 (fast copy mode).
2. Merge Two Videos: Converts both user inputs, then merges them with glitch.mp4 
    (V1 -> Glitch -> V2) using fast copy mode.

Dependencies:
- Python 3.x
- ffmpeg (must be installed and accessible from PATH)
"""

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# === CONFIGURABLE UI TEXT ===
APP_TITLE = "Video Buffer Generator"
APP_DESCRIPTION = (
    "Select an operation below. All merging/concatenation is preceded by an \n"
    "automatic H.264 conversion to ensure fast, reliable output."
)
APP_CREDIT = "Concept by 4est__"

# === MAIN APPLICATION CLASS ===
class VideoBufferGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("650x580")  # Increased size for new widgets
        self.configure(bg="#1e1e1e")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", background="#2b2b2b", foreground="#ffffff", borderwidth=0, padding=6)
        self.style.map("TButton", background=[("active", "#3c3c3c")])
        self.style.configure("TLabel", background="#1e1e1e", foreground="#e0e0e0", wraplength=600)

        # File paths for Buffer functionality (original)
        self.buffer_video_path = None
        # File paths for Merge functionality (new)
        self.merge_video1_path = None
        self.merge_video2_path = None

        self.create_widgets()

    def create_widgets(self):
        # Title and Description
        title = tk.Label(self, text=APP_TITLE, font=("Segoe UI", 18, "bold"), fg="#00C853", bg="#1e1e1e")
        title.pack(pady=(20, 5))
        desc = tk.Label(self, text=APP_DESCRIPTION, font=("Segoe UI", 10), fg="#ffffff", bg="#1e1e1e", justify="center")
        desc.pack(pady=(0, 20))

        # --- FRAME 1: VIDEO BUFFER FUNCTIONALITY ---
        buffer_frame = tk.LabelFrame(self, text=" 1. Generate Buffer (Video + Glitch) ", fg="#00C853", bg="#1e1e1e", padx=10, pady=10)
        buffer_frame.pack(pady=10, padx=20, fill="x")

        ttk.Button(buffer_frame, text="Select Input MP4", command=lambda: self.select_video("buffer")).pack(pady=5)
        self.buffer_file_label = tk.Label(buffer_frame, text="Buffer Input: No file selected", fg="#888", bg="#1e1e1e")
        self.buffer_file_label.pack(pady=(0, 10))

        self.generate_btn = ttk.Button(buffer_frame, text="Generate Video Buffer", command=lambda: self.generate_output(mode="buffer"), state="disabled")
        self.generate_btn.pack(pady=5)

        # --- FRAME 2: MERGE TWO VIDEOS FUNCTIONALITY ---
        merge_frame = tk.LabelFrame(self, text=" 2. Merge Two Videos (V1 + Glitch + V2) ", fg="#00C853", bg="#1e1e1e", padx=10, pady=10)
        merge_frame.pack(pady=10, padx=20, fill="x")

        # Video 1 Selector (the "other button")
        ttk.Button(merge_frame, text="Select Video 1 (First Segment)", command=lambda: self.select_video("merge1")).pack(pady=5)
        self.merge1_file_label = tk.Label(merge_frame, text="Video 1: No file selected", fg="#888", bg="#1e1e1e")
        self.merge1_file_label.pack(pady=(0, 5))

        # Video 2 Selector (the "third button")
        ttk.Button(merge_frame, text="Select Video 2 (Last Segment)", command=lambda: self.select_video("merge2")).pack(pady=5)
        self.merge2_file_label = tk.Label(merge_frame, text="Video 2: No file selected", fg="#888", bg="#1e1e1e")
        self.merge2_file_label.pack(pady=(0, 10))

        self.merge_btn = ttk.Button(merge_frame, text="Merge V1, Glitch, and V2", command=lambda: self.generate_output(mode="merge"), state="disabled")
        self.merge_btn.pack(pady=5)

        # Credit
        credit = tk.Label(self, text=f"Credit: {APP_CREDIT}", font=("Segoe UI", 8), fg="#aaa", bg="#1e1e1e")
        credit.pack(side="bottom", pady=10)

    def select_video(self, target):
        file_path = filedialog.askopenfilename(
            title="Select MP4 Video",
            filetypes=[("MP4 Files", "*.mp4")]
        )
        if not file_path:
            return
            
        filename = os.path.basename(file_path)

        if target == "buffer":
            self.buffer_video_path = file_path
            self.buffer_file_label.config(text=f"Buffer Input: {filename}")
            self.generate_btn.config(state="normal")
        elif target == "merge1":
            self.merge_video1_path = file_path
            self.merge1_file_label.config(text=f"Video 1: {filename}")
        elif target == "merge2":
            self.merge_video2_path = file_path
            self.merge2_file_label.config(text=f"Video 2: {filename}")

        # Check merge button state
        if self.merge_video1_path and self.merge_video2_path:
            self.merge_btn.config(state="normal")
        else:
            self.merge_btn.config(state="disabled")

    def run_ffmpeg_conversion(self, input_path, output_path):
        """Converts an input file to H.264/AAC for compatibility."""
        conversion_cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            output_path
        ]
        
        subprocess.run(
            conversion_cmd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )

    def run_ffmpeg_concat(self, concat_list_path, output_path):
        """Runs the fast copy concatenation."""
        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list_path,
            "-c", "copy",  
            output_path
        ]
        
        subprocess.run(
            concat_cmd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )

    def generate_output(self, mode):
        # --- PATH VALIDATION AND SETUP ---
        files_to_process = []
        glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")

        if mode == "buffer":
            if not self.buffer_video_path: return
            files_to_process.append(self.buffer_video_path)
            # Check for glitch file
            if not os.path.exists(glitch_path):
                messagebox.showerror("Error", f"Missing required file:\n{glitch_path}")
                return
            
        elif mode == "merge":
            if not self.merge_video1_path or not self.merge_video2_path: return
            files_to_process.extend([self.merge_video1_path, self.merge_video2_path])
            # Check for glitch file (needed for merging with buffer)
            if not os.path.exists(glitch_path):
                messagebox.showerror("Error", f"Missing required file:\n{glitch_path}")
                return
            
        output_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4")],
            title="Save Output As"
        )
        if not output_path: return

        # Define temporary files
        temp_dir = os.path.dirname(output_path)
        concat_list = os.path.join(temp_dir, "temp_list.txt")
        temp_files_created = []

        try:
            # 1. CONVERSION STEP: Convert all user-selected files to H.264/AAC
            converted_paths = {}
            if files_to_process:
                messagebox.showinfo("Processing", f"Starting automatic conversion of {len(files_to_process)} user file(s). This may take a moment...")
            
            for i, input_path in enumerate(files_to_process):
                # Use a unique identifier for the temporary file
                temp_output_path = os.path.join(temp_dir, f"temp_compatible_{i}.mp4")
                self.run_ffmpeg_conversion(input_path, temp_output_path)
                
                # Map original path to converted path
                converted_paths[input_path] = temp_output_path
                temp_files_created.append(temp_output_path)
            
            # --- Determine Final List for Concatenation ---
            files_for_concat = []
            if mode == "buffer":
                # V_converted, Glitch_original
                files_for_concat = [converted_paths[self.buffer_video_path], glitch_path]
            elif mode == "merge":
                # V1_converted, Glitch_original, V2_converted
                files_for_concat = [
                    converted_paths[self.merge_video1_path], 
                    glitch_path, 
                    converted_paths[self.merge_video2_path]
                ]

            # 2. CONCAT LIST: Write the list of compatible files
            with open(concat_list, "w", encoding="utf-8") as f:
                for path in files_for_concat:
                    safe_path = path.replace("\\", "/")
                    f.write(f"file '{safe_path}'\n")
            temp_files_created.append(concat_list)

            # 3. CONCATENATION STEP: Use the fast, original '-c copy' command
            messagebox.showinfo("Processing", "Concatenating files using fast copy mode...")
            self.run_ffmpeg_concat(concat_list, output_path)

            messagebox.showinfo("Success", f"Operation completed successfully!\nSaved to:\n{output_path}")

        except subprocess.CalledProcessError as e:
            # Display detailed error if conversion or concat fails
            full_output = f"STDOUT:\n{e.stdout.strip()}\n\nSTDERR:\n{e.stderr.strip()}"
            messagebox.showerror(
                "FFmpeg Failed (Detailed Error)",
                f"A step in the process failed. Check FFmpeg logs.\n\n"
                f"--- FFmpeg Output ---\n"
                f"{full_output}"
            )
        
        except Exception as e:
            messagebox.showerror("General Error", str(e))
        
        finally:
            # 4. CLEANUP: Delete all temporary files
            for temp_file in temp_files_created:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except OSError:
                        pass # Ignore cleanup errors

# === MAIN ENTRYPOINT ===
if __name__ == "__main__":
    app = VideoBufferGenerator()
    app.mainloop()