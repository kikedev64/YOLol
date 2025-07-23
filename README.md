# 🧠 YOLol: Minimap Computer Vision for League of Legends

**YOLol** is a project that uses **computer vision** to automatically analyze the **minimap** in League of Legends (14.20) matches, extracting valuable information about the location of champions.

This system is designed for training AI models or performing visual match analysis through minimap frames.

![Minimap](assets/minimap.gif)

It has been trained on over **30,000 automatically generated images** to recognize the following champions:

- Aatrox
- Ahri
- Akali
- Akshan
- Alistar
- Amumu
- Anivia
- Annie
- Aphelios
- Ashe
- AurelionSol
- Azir
- Bard
- Belveth
- Blitzcrank
- Brand
- Braum
- Caitlyn
- Camille
- Cassiopeia
- Chogath
- Corki
- Darius
- Diana
- Draven
- DrMundo
- Ekko
- Elise
- Evelynn
- Ezreal
- Fiddlesticks
- Fiora
- Fizz
- Galio
- Gangplank
- Garen
- Gnar
- Gragas
- Graves
- Gwen
- Hecarim
- Heimerdinger
- Illaoi
- Irelia
- Ivern
- Janna
- JarvanIV
- Jax
- Jayce
- Jhin
- Jinx
- KaiSa
- Kalista
- Karma
- Karthus
- Kassadin
- Katarina
- Kayle
- Kayn
- Kennen
- Khazix
- Kindred
- Kled
- KogMaw
- Ksante
- LeBlanc
- LeeSin
- Leona
- Lillia
- Lissandra
- Lucian
- Lulu
- Lux
- Malphite
- Malzahar
- Maokai
- MasterYi
- MissFortune
- MonkeyKing
- Mordekaiser
- Morgana
- Nami
- Nasus
- Nautilus
- Neeko
- Nidalee
- Nilah
- Nocturne
- Nunu
- Olaf
- Orianna
- Ornn
- Pantheon
- Poppy
- Pyke
- Qiyana
- Quinn
- Rakan
- Rammus
- RekSai
- Rell
- Renata
- Renekton
- Rengar
- Riven
- Rumble
- Ryze
- Samira
- Sejuani
- Senna
- Seraphine
- Sett
- Shaco
- Shen
- Shyvana
- Singed
- Sion
- Sivir
- Skarner
- Sona
- Soraka
- Swain
- Sylas
- Syndra
- TahmKench
- Taliyah
- Talon
- Taric
- Teemo
- Thresh
- Tristana
- Trundle
- Tryndamere
- TwistedFate
- Twitch
- Udyr
- Urgot
- Varus
- Vayne
- Veigar
- VelKoz
- Vex
- Vi
- Viego
- Viktor
- Vladimir
- Volibear
- Warwick
- Xayah
- Xerath
- XinZhao
- Yasuo
- Yone
- Yorick
- Yuumi
- Zac
- Zed
- Zeri
- Ziggs
- Zilean
- Zoe
- Zyra
---

## 🎞️ 1. Frame Extractor (`extract_frames.py`)

Extracts frames from `.mkv` video files containing full matches. These frames are used to detect and analyze champion positions on the minimap.

### Expected Structure:
```
YOLol/
└── video_training/
    ├── video/
    │   ├── game1.mkv
    │   ├── game2.mkv
    ├── extract_frames.py
```

### Output:
```
YOLol/
└── video_training/
    ├── video/
    │   ├── game1.mkv
    │   ├── game2.mkv
    ├── extract_frames.py
    └── frames/
            ├── game1/
            └── game2/
```

### Usage:
```bash
python extract_frames.py
```

---

## 🗺️ 2. Minimap Dataset Generator (`minimap_generator.py`)

This component generates a synthetic dataset simulating the minimap with YOLO annotations representing:
- Champion positions (allies and enemies)
- Towers and inhibitors
- Other visual elements like fog of war, pings, or structures

Each image is saved with a unique 16-character UUID and an accompanying `.txt` file in YOLO format.YOLol
---

## 🚀 Objective

The goal of **YOLol** is to build an automated computer vision system capable of accurately identifying **champions on the minimap** of League of Legends matches, for later use in analytics, movement prediction, or automated learning.

---

## 🛠️ Dependencies
```bash
pip install -r ./requirements.txt
```
> Integration with PyTorch, YOLO (Ultralytics), and other training/detection tools is planned.

---

## 📌 Project Status
- ✅ Frame extraction completed
- ✅ Synthetic minimap dataset generation completed
- ✅ Object detection model training (in progress)

---

## 📂 Project Structure
```
YOLol/
├── assets/               # Visual assets like the README GIF
├── minimap_generator/    # Full automation pipeline for minimap generation
├── results/              # Latest trained YOLO model (ready to use)
├── scrapping/            # Scripts to download assets from Riot's CDN and Dragon raw
├── train_model/          # Codebase for training the YOLO model
├── video_training/       # Script to auto-extract frames from video at set intervals
└── README.md             # This file

```

---

## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit.
- **NonCommercial** — You may not use the material for commercial purposes.
- **ShareAlike** — You must distribute your contributions under the same license.

Full license: [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/)
