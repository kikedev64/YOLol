import os
import random
import shutil
import yaml
import subprocess
from ultralytics import YOLO
import json

class TrainModelYOLO:
    def __init__(self,
                 source_images_dir: str,
                 source_labels_dir: str,
                 name: str = "LeagueIAModel",
                 output_dir: str = "./data",
                 train_ratio: float = 0.8,
                 val_ratio: float = 0.1,
                 test_ratio: float = 0.1,
                 project = "model_trained/runs"):
        
        self.source_images = source_images_dir
        self.source_labels = source_labels_dir
        self.output_dir = output_dir
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.name = name
        
        # Comprueba que las proporciones suman 1.0
        total = train_ratio + val_ratio + test_ratio
        if abs(total - 1.0) > 1e-6:
            raise ValueError("train_ratio + val_ratio + test_ratio must equal 1.0")
        
        # Rutas destino
        self.train_img = os.path.join(output_dir, "train", "images")
        self.train_lbl = os.path.join(output_dir, "train", "labels")
        self.val_img   = os.path.join(output_dir, "val",   "images")
        self.val_lbl   = os.path.join(output_dir, "val",   "labels")
        self.test_img  = os.path.join(output_dir, "test",  "images")
        self.test_lbl  = os.path.join(output_dir, "test",  "labels")
        self.project   = os.path.join(output_dir,"model_trained","runs")

    def shuffle(self):
        """
        Shuffles the dataset into train, validation, and test sets.
        It creates the necessary directories and copies the images and labels into their respective folders.
        The dataset is split according to the specified ratios.
        """
        
        for d in [self.train_img, self.train_lbl,
                  self.val_img,   self.val_lbl,
                  self.test_img,  self.test_lbl]:
            os.makedirs(d, exist_ok=True)

        imgs = [f for f in os.listdir(self.source_images)
                if os.path.isfile(os.path.join(self.source_images, f))
                and f.lower().endswith((".png", ".jpg", ".jpeg"))]
        random.shuffle(imgs)

        n = len(imgs)
        n_train = int(n * self.train_ratio)
        n_val   = int(n * self.val_ratio)

        n_test  = n - n_train - n_val

        splits = {
            "train": imgs[:n_train],
            "val":   imgs[n_train:n_train + n_val],
            "test":  imgs[n_train + n_val:]
        }

        for split, files in splits.items():
            for img in files:
                label = os.path.splitext(img)[0] + ".txt"
                src_img = os.path.join(self.source_images, img)
                src_lbl = os.path.join(self.source_labels, label)

                if split == "train":
                    dst_img = os.path.join(self.train_img, img)
                    dst_lbl = os.path.join(self.train_lbl, label)
                elif split == "val":
                    dst_img = os.path.join(self.val_img, img)
                    dst_lbl = os.path.join(self.val_lbl, label)
                else:
                    dst_img = os.path.join(self.test_img, img)
                    dst_lbl = os.path.join(self.test_lbl, label)

                shutil.copy2(src_img, dst_img)
                if os.path.exists(src_lbl):
                    shutil.copy2(src_lbl, dst_lbl)
                else:
                    # Etiqueta ausente: crear vacío
                    open(dst_lbl, "w").close()

        print(f"📂 Dataset split: {n_train} train, {n_val} val, {n_test} test")


    def create_yaml(self,
                    yaml_path: str,
                    names: list,
                    nc: int = None):
        """
        Creates a YAML file for YOLOv11 training configuration.
        It includes paths to the train, validation, and test images and labels,
        the number of classes, and their names.
        
        Parameters:
        ----------
        yaml_path (str): 
            Path where the YAML file will be saved.
        names (list):
            List of class names.
        nc (int, optional):
            Number of classes. If None, it will be inferred from the names list.
        """
        data = {
            'path': os.path.abspath(self.output_dir),
            'train': 'train/images',
            'val':   'val/images',
            'test':  'test/images',
            'nc':    nc or len(names),
            'names': names
        }
        os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        print(f"✅ YAML de entrenamiento creado en '{yaml_path}'")

    def train(self,
              yaml_path: str,
              model: str = "yolo11s.pt",
              epochs: int = 200,
              batch: int = 16,
              imgsz: int = 800,
              device: str = "cuda",
              patience = 20):
        """
        Trains a YOLOv11 model using the specified configuration.
        Parameters:
        ----------
        yaml_path (str):
            Path to the YAML file containing dataset configuration.
        model (str):
            Path to the pre-trained model or model architecture to use.
        epochs (int):
            Number of training epochs.
        batch (int):
            Batch size for training.
        imgsz (int):
            Image size for training.
        device (str):
            Device to use for training ('cpu' or 'cuda:0' for GPU).
        patience (int):
            Number of epochs with no improvement before early stopping.
        """
        model = YOLO(model)
        
        print("🚀 Starting YOLOv11 training")
        # Entrenamiento
        results = model.train(
            data=yaml_path,     # Ruta al archivo de configuración
            epochs=epochs,      # Número de épocas
            imgsz=imgsz,        # Tamaño de las imágenes
            batch=batch,        # Tamaño del batch
            name=self.name,     # Nombre del experimento
            project= self.project,   # Carpeta donde se guarda el experimento
            patience=patience,  # early stopping si no mejora
            device=device       # Dispositivo a usar ('cpu' o 'cuda:0' para GPU, etc.)
        )
        
        print("✅ YOLOv11 training completed")

def load_class():
    """
    Loads the class names from a local JSON file and returns them sorted.
    
    Returns:
    -------
    tuple:
        A tuple containing the sorted class names and the total number of classes.
    """
    json_path = "./characters.json"
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"❌ No se encontró el archivo: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    sorted_classes = [k for k, _ in sorted(data.items(), key=lambda item: item[1])]
    
    return sorted_classes, len(sorted_classes)

def main():
    tm = TrainModelYOLO(
        source_images_dir="E:/Repositorios/LeagueIA/train_vision/minimap_generator/train_images",
        source_labels_dir="E:/Repositorios/LeagueIA/train_vision/minimap_generator/train_images",
        output_dir="./prepared_data"
    )
    tm.shuffle()
    
    class_names, _= load_class() 
    tm.create_yaml("./prepared_data/data.yaml", names=class_names)
    
    tm.train("./prepared_data/data.yaml",model="yolo11n.pt")
    tm.train("./prepared_data/data.yaml")

if __name__ == "__main__":
    main()