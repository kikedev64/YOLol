# Minimap Dataset Generator for League of Legends

This project aims to generate a synthetic dataset for training computer vision models on the League of Legends minimap.

## 🔍 Overview

Instead of capturing frames from real gameplay, this tool programmatically generates labeled minimap images by simulating in-game elements and conditions. This allows for fast, flexible, and automated dataset generation with precise annotations.

## 🧠 Idea

The core idea is to:
1. Start from a **clean base image** of the minimap (no fog, no icons).
2. **Overlay key static elements** like:
   - Turrets
   - Inhibitors
   - Nexus
3. **Randomly place dynamic elements**, such as:
   - Champion icons (players)
   - Pings (danger, on my way, etc.)
   - Control wards / vision markers
4. **Simulate fog of war** in random areas by darkening regions to replicate limited vision.
5. **Automatically generate YOLO annotations** (`.txt` files) with exact bounding boxes and class labels.
6. Save the dataset in a YOLO-compatible structure, ready for training.
