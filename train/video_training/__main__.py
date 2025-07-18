#!/usr/bin/env python3
import os
import cv2
from tqdm import tqdm

def extract_frames_instant(video_path, interval_s: int = 30):
    """
    Extrae un frame cada `interval_s` segundos de video_path (.mkv)
    de forma instantánea (sin reproducir) y los guarda en:
      video/frames/<nombre_del_video>/*.png
    con máxima calidad (PNG, sin compresión).
    """
    # Preparar carpeta de salida
    parent = os.path.dirname(video_path)
    frames_root = os.path.join(parent, "frames")
    os.makedirs(frames_root, exist_ok=True)
    name, _ = os.path.splitext(os.path.basename(video_path))
    frames_dir = os.path.join(frames_root, name)
    os.makedirs(frames_dir, exist_ok=True)

    # Abrir vídeo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] No se pudo abrir: {video_path}")
        return

    # Parámetros vídeo
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_s = total_frames / fps

    # Calcular índices de frame a extraer
    times = list(range(0, int(duration_s) + 1, interval_s))
    frame_indices = [int(t * fps) for t in times]

    print(f"📸 {name}: {len(frame_indices)} frames cada {interval_s}s")

    for idx, frame_no in tqdm(enumerate(frame_indices, 1),
                              total=len(frame_indices),
                              desc=name):
        # Ir directo al frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()
        if not ret:
            continue
        # Guardar PNG sin compresión
        out_path = os.path.join(frames_dir, f"{name}_{times[idx-1]:04d}.png")
        cv2.imwrite(out_path, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    cap.release()
    print(f"✅ Guardados en: {frames_dir}\n")

def main():
    video_folder = os.path.join(os.getcwd(), "video")
    if not os.path.isdir(video_folder):
        print("[ERROR] No hay carpeta 'video/' aquí.")
        return

    # Solo .mkv
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
