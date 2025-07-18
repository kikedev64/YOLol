# 🗺️ Minimap Dataset Generator for League of Legends

This tool generates synthetic minimap images for training computer vision models on League of Legends.

## 🎯 Purpose

Instead of capturing frames from real games, this generator creates artificial minimap screenshots with realistic in-game configurations and precise annotations, automating large-scale dataset creation for machine learning models.

## ⚙️ Functionality

The generator simulates the minimap using the following pipeline:

1. **Base Image Initialization**
   - Start from a clean minimap base (no fog, icons, or overlays).

2. **Static Element Placement** (fixed positions):
   - **Turrets**: Spawned in predefined positions based on turret type and lane.
   - **Inhibitors**: Added with variant appearances and fixed positions.
   - **Nexus**: Spawned in default base locations.
   - **Jungle Elements**: Static camps and structures (e.g., buffs, dragon, Baron) are placed once and do not vary.

3. **Dynamic Element Placement** (random positions):
   - **Champions**: Randomly selected and placed at plausible positions.
   - **Pings**: Random ping icons (e.g., danger, assist, missing) scattered over the map.
   - **Wards & Vision Markers**: Added to mimic real match clutter and detection difficulty.

4. **Fog of War Simulation**
   - Randomly darkened circular regions emulate player-limited vision.

5. **Resolution Downsampling**
   - Once composed, the minimap image is resized to simulate actual input size for vision models, reducing high-res artifacts.

6. **UUID Assignment & Annotation**
   - Each minimap is saved with a random 16-character UUID (64-bit entropy) to avoid name collisions.
   - Corresponding YOLO annotation `.txt` files are generated with exact bounding boxes and class IDs.

7. **Export**
   - The dataset is stored in a YOLO-compatible folder structure, ready to be used for training with tools like YOLOv8.

---

This process ensures each generated image is unique, reproducible, and labeled with pixel-perfect precision, facilitating supervised training at scale.
