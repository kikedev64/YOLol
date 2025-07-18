import cv2
import numpy as np
import mss
from ultralytics import YOLO

def main():
    # Carga tu modelo entrenado
    model = YOLO("C:/Users/fxkik/Documents/LeagueIA/train/train_model/prepared_data/model_trained/runs/LeagueIAModel/weights/best.pt")

    # Crear ventana redimensionable con tamaño inicial 1280x720 (16:9)
    win_name = "Detección Minimap LoL"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_name, 1280, 720)
    cv2.setWindowProperty(win_name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)

    # Inicializa captura de pantalla con mss
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Monitor principal
        print("🔍 Iniciando detección en tiempo real. Pulsa 'q' para salir.")

        while True:
            # Captura la pantalla
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Realiza predicción
            results = model(frame)[0]

            # Dibuja cajas y etiquetas
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = f"{model.names[cls]} {conf:.2f}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Obtener tamaño actual de la ventana
            try:
                _, _, w, h = cv2.getWindowImageRect(win_name)
            except AttributeError:
                w, h = 1280, 720  # fallback si no está disponible

            # Redimensiona el frame según la ventana
            resized_frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)

            # Muestra el frame en la ventana
            cv2.imshow(win_name, resized_frame)

            # Salir con 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
