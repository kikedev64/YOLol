# 🧠 LolNet: Real-Time Strategy Prediction from League of Legends

**LolNet** is a project that leverages computer vision and deep learning to analyze the current state of a League of Legends match and predict the best possible moves in real time.

The project consists of the following main components:

---

## 🎞️ 1. Frame Extractor (`extract_frames.py`)

Extracts image frames from `.mkv` match recordings at fixed intervals. These frames serve as the raw visual input for training the AI model.

### Input Directory:
```
LolNet/
├── video/
│   ├── game1.mkv
│   ├── game2.mkv
```

### Output:
```
LolNet/
└── frames/
    ├── game1/
    ├── game2/
```

### How to Use:
```bash
python extract_frames.py
```

---

## 🗺️ 2. Minimap Dataset Generator

Programmatically generates synthetic minimap images with labeled annotations, simulating game elements like turrets, inhibitors, champions, pings, and fog of war. Each minimap is saved with a 16-character UUID to ensure uniqueness and is exported in a YOLO-compatible format for object detection models.

---

## 🧠 3. Neural Network Inference Engine *(WIP)*

Uses the extracted visual data to feed a neural network capable of:
- Understanding the current map state.
- Predicting optimal team decisions and player actions.
- Providing real-time strategy suggestions during gameplay or replay analysis.

---

## 🚀 Goal

The ultimate aim of **LolNet** is to build an intelligent system that observes a game of League of Legends and acts as a strategic assistant — learning from past matches and making tactical predictions as the game unfolds.

## 🛠️ Dependencies
```bash
pip install opencv-python tqdm
```

> More modules like PyTorch, Ultralytics (YOLO), and others will be required as the model and inference components are integrated.

---

## 📌 Status
- ✅ Dataset generation complete
- ✅ Frame extraction complete
- 🔄 Real-time strategy prediction (in progress)

---

## 👤 Author
Developed by a League of Legends enthusiast with a passion for AI, vision systems, and real-time game analytics.

Feel free to contribute or use this project as a foundation for your own League-related AI research.

---

## 📂 Project Structure
```
LolNet/
├── video/               # Source .mkv match videos
├── frames/              # Extracted frames from match videos
├── train_images/        # Synthetic minimap dataset (YOLO format)
├── extract_frames.py    # Frame extractor script
├── minimap_generator.py # Minimap dataset generator
└── README.md            # This file
```

---

## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit to the author.
- **NonCommercial** — You may not use the material for commercial purposes.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license.

For full license text, visit: [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/)
