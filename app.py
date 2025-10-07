#!/usr/bin/env python3
"""
Video Buffer Generator
-----------------------
Join a selected MP4 video with a glitch transition clip using FFmpeg.

Author: 4est__ (concept)
GUI/Implementation: You

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
    "This tool takes an MP4 video and seamlessly joins it with a 'glitch' buffer \n\n"
    "video, found at ./RawBuffer/glitch.mp4. The resulting file is exported to "
    "a user-specified location.\n\n"
    "Educational Purposes Only."
)
APP_CREDIT = "Concept by 4est__"

# === MAIN APPLICATION CLASS ===
class VideoBufferGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("600x400")
        self.configure(bg="#1e1e1e")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", background="#2b2b2b", foreground="#ffffff", borderwidth=0, padding=6)
        self.style.map("TButton", background=[("active", "#3c3c3c")])
        self.style.configure("TLabel", background="#1e1e1e", foreground="#e0e0e0", wraplength=550)

        self.video_path = None

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self, text=APP_TITLE, font=("Segoe UI", 18, "bold"), fg="#00C853", bg="#1e1e1e")
        title.pack(pady=(20, 10))

        # Description
        desc = tk.Label(self, text=APP_DESCRIPTION, font=("Segoe UI", 10), fg="#ffffff", bg="#1e1e1e", justify="center")
        desc.pack(pady=(0, 15))

        # Input selector
        ttk.Button(self, text="Select Input MP4", command=self.select_video).pack(pady=10)
        self.file_label = tk.Label(self, text="No file selected", fg="#888", bg="#1e1e1e")
        self.file_label.pack(pady=(0, 10))

        # Process button
        self.generate_btn = ttk.Button(self, text="Generate Video Buffer", command=self.generate_output, state="disabled")
        self.generate_btn.pack(pady=15)

        # Credit
        credit = tk.Label(self, text=f"Credit: {APP_CREDIT}", font=("Segoe UI", 8), fg="#aaa", bg="#1e1e1e")
        credit.pack(side="bottom", pady=10)

    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="Select MP4 Video",
            filetypes=[("MP4 Files", "*.mp4")]
        )
        if file_path:
            self.video_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"Selected: {filename}")
            self.generate_btn.config(state="normal")

    def generate_output(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please select an input video first.")
            return

        glitch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RawBuffer", "glitch.mp4")
        if not os.path.exists(glitch_path):
            messagebox.showerror("Error", f"Missing required file:\n{glitch_path}")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4")],
            title="Save Output As"
        )
        if not output_path:
            return  # User canceled save

        try:
            concat_list = os.path.join(os.path.dirname(output_path), "temp_list.txt")

            # Sanitize paths for FFmpeg (must use forward slashes)
            safe_input = self.video_path.replace("\\", "/")
            safe_glitch = glitch_path.replace("\\", "/")

            with open(concat_list, "w", encoding="utf-8") as f:
                f.write(f"file '{safe_input}'\n")
                f.write(f"file '{safe_glitch}'\n")

            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_list,
                "-c", "copy",
                output_path
            ]

            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.remove(concat_list)
            messagebox.showinfo("Success", f"Video buffer created successfully!\nSaved to:\n{output_path}")

        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "FFmpeg failed to generate video.\nCheck if FFmpeg is installed correctly.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# === MAIN ENTRYPOINT ===
if __name__ == "__main__":
    app = VideoBufferGenerator()
    app.mainloop()