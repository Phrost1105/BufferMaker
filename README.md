# Video Buffer Generator

A small python utility that stitches an mp4 file to a short glitch clip (glitch.mp4) with ffmpeg so you get a clean buffer between scenes. No re-encode, just a straight stream copy, so it’s fast and keeps the quality.

## What it does

- Tkinter gui – drag, click, done  
- Concatenates your clip with RawBuffer/glitch.mp4  
- Lets you pick the output name and folder  
- Adds a one-line credit + description you can edit  

## Before you start

You’ll need:

- Python 3.8 or newer  
- ffmpeg in your path (windows build or brew install ffmpeg)

## Quick setup (windows)

1. Grab python from python.org and tick “add to PATH” during install.  
2. Download a static ffmpeg build, unzip, and drop the bin folder into PATH.  
3. Clone or unzip this repo, open cmd inside the folder and run:

```bash
python app.py
```

Pick your video, hit “create buffer”, and the new file lands where you chose.

---

**Note:** *This script was created for educational purposes. I am not responsible for the use of this script.*
