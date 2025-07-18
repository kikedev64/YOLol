# 🎞️ Frame Extractor for .MKV Videos

This utility extracts image frames from `.mkv` video files at fixed time intervals. It is especially designed for **League of Legends match videos**, enabling frame-level extraction to generate datasets for training computer vision models or AI-based systems.

## 📂 Directory Structure

Place your `.mkv` video files in a folder named `video/` in the same directory as the script:

```
project_root/
├── video/
│   ├── game1.mkv
│   ├── game2.mkv
├── extract_frames.py
```

After execution, extracted frames are saved to:

```
project_root/
└── frames/
    ├── game1/
    │   ├── game1_0000.png
    │   ├── game1_0030.png
    ├── game2/
        ├── game2_0000.png
        ├── game2_0030.png
```

## ⚙️ How It Works

1. Iterates through all `.mkv` files in `video/`.
2. For each video:
   - Opens it using OpenCV.
   - Calculates duration and total frames.
   - Extracts one frame every **30 seconds** (by default).
   - Saves each frame as PNG with **no compression**.

## 🧪 Usage

Run directly:

```bash
python extract_frames.py
```

You can adjust the interval (in seconds) for frame extraction by editing this line:

```python
extract_frames_instant(path_to_video, interval_s=30)
```

## 🔍 Notes

- Requires **OpenCV** and **tqdm**:

```bash
pip install opencv-python tqdm
```

- If `video/` folder or `.mkv` files are missing, the script will notify and exit gracefully.
- Extracted frames are saved in organized subfolders named after each video file.

## ✅ Output Example

```
🎬 2 .mkv en 'video/'.
📸 game1: 120 frames cada 30s
✅ Guardados en: ./frames/game1