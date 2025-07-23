
import os
import cv2
from tqdm import tqdm

def extract_frames_instant(video_path, interval_s: int = 30):
    """
    Extract frames from a video at specified intervals and save them as PNG files.
    Parameters:
    ----------
    video_path (str): 
        Path to the video file.
    interval_s (int): 
        Interval in seconds at which to extract frames.
    """

    parent = os.path.dirname(video_path)
    frames_root = os.path.join(parent, "frames")
    os.makedirs(frames_root, exist_ok=True)
    name, _ = os.path.splitext(os.path.basename(video_path))
    frames_dir = os.path.join(frames_root, name)
    os.makedirs(frames_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] No se pudo abrir: {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_s = total_frames / fps

    times = list(range(0, int(duration_s) + 1, interval_s))
    frame_indices = [int(t * fps) for t in times]

    print(f"📸 {name}: {len(frame_indices)} frames cada {interval_s}s")

    for idx, frame_no in tqdm(enumerate(frame_indices, 1),
                              total=len(frame_indices),
                              desc=name):
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()
        if not ret:
            continue

        out_path = os.path.join(frames_dir, f"{name}_{times[idx-1]:04d}.png")
        cv2.imwrite(out_path, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    cap.release()
    print(f"✅ Guardados en: {frames_dir}\n")

def main():
    """
    Main function to extract frames from all .mkv files in the 'video' directory.
    It processes each video file, extracting frames at specified intervals and saving them in a structured directory
    """
    
    video_folder = os.path.join(os.getcwd(), "video")
    if not os.path.isdir(video_folder):
        print("[ERROR] No hay carpeta 'video/' aquí.")
        return

    mkvs = [f for f in os.listdir(video_folder) if f.lower().endswith(".mkv")]
    if not mkvs:
        print("[INFO] No hay archivos .mkv en 'video/'.")
        return

    print(f"🎬 {len(mkvs)} .mkv en 'video/'.\n")
    for mkv in mkvs:
        extract_frames_instant(os.path.join(video_folder, mkv), interval_s=30)

    print("🏁 Hecho.")

if __name__ == "__main__":
    main()
