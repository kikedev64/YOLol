#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import random
import json
import os
import shutil
import uuid
import yaml
import numpy as np
from tqdm import tqdm

class Minimap:
    """
    Class to generate a minimap for training a computer vision model.
    It includes methods to load icons, create a minimap with various game elements,
    and save the minimap with YOLO format labels.
    
    Attributes:
    ----------
    minimap (Image): 
        The base minimap image.
    shadow_map (Image):
        The shadow map image used for war zones.
    position_json_map_file (str):
        Path to the JSON file containing positions of items on the map.
    icons_dir (str):
        Directory containing icons for various game elements.
    source_square (str):
        Directory containing champion icons.
    destination_square (str):
        Directory where champion icons will be saved.
    extract_s (bool):
        If True, extracts champion icons from the source directory.
    yolo_output (str):
        Path to save YOLO format labels.
    yolo_labels (list):
        List to store YOLO labels.
    character_dir (dict):
        Dictionary mapping champion names to their IDs.
    elements_in_map (list):
        List of elements already placed on the minimap.
    objects_in_image (list):
        List of objects placed on the minimap with their properties.
    position_item_dict (dict):
        Dictionary mapping item names to their positions and sizes on the minimap.
    """
    def __init__(self,
                 minimap='./utils/minimap.png',
                 shadow_map="./utils/shadow_map.png",
                 position_json_map_file="./utils/locations_item_map.json",
                 icons_dir="./utils/icons",
                 source_square="C:/Users/fxkik/Documents/LeagueIA/train/scrapping/data_train/characters",
                 destination_square="./utils/character_items",
                 extract_s=False,
                 yolo_output="./utils/map_labels.txt"):
        """
        Initializes the Minimap class with the given parameters.

        Parameters:
        ----------
        minimap (str): 
            Path to the base minimap image.
        shadow_map (str):
            Path to the shadow map image used for war zones.
        position_json_map_file (str):
            Path to the JSON file containing positions of items on the map.
        icons_dir (str):
            Directory containing icons for various game elements.
        source_square (str):
            Directory containing champion icons.
        destination_square (str):
            Directory where champion icons will be saved.
        extract_s (bool):
            If True, extracts champion icons from the source directory.
        yolo_output (str):
            Path to save YOLO format labels.
        """
        
        self.minimap = Image.open(minimap)
        self.elements_in_map = []
        self.shadow_map = Image.open(shadow_map)
        self.position_json_map_file = position_json_map_file
        self.icons_dir = icons_dir
        self.source_dir = source_square
        self.dest_dir = destination_square
        self.yolo_output = yolo_output
        self.yolo_labels = []
        self.character_dir = {}
        
        
        # if extract_s is True, it will extract the champion icons from the source directory.
        if extract_s:
            self.extract_squares()
        
        """
        Initial flow, load the position_item_dict from the JSON file,
        load the character directory, and create the items map.
        """
        self.load_character_dir()
        self.load_pos_item_map()
        self.create_items_map()
        self.war_zones()
        self.downgrade_resolution()
        
        

    def war_zones(self, count=5):
        """
        Applies a shadow effect to random areas of the minimap to simulate war zones.
        
        Parameters:
        ----------
        count (int):
            Number of war zones to apply.
        """
        W, H = self.minimap.size

        fog_color = (0, 0, 0, 204)
        fog = Image.new("RGBA", (W, H), fog_color)

        visibility_mask = Image.new("L", (W, H), 0)
        draw = ImageDraw.Draw(visibility_mask)

        for item_map in self.objects_in_image:
            cx = item_map["x"] + item_map["width"] // 2
            cy = item_map["y"] + item_map["height"] // 2

            vision_radius = int(max(item_map["width"], item_map["height"]) * 0.8)

            draw.ellipse(
                (cx - vision_radius, cy - vision_radius, cx + vision_radius, cy + vision_radius),
                fill=255
            )

        visibility_mask = visibility_mask.filter(ImageFilter.GaussianBlur(radius=15))

        inverted_mask = ImageChops.invert(visibility_mask)
        
        inverted_mask = inverted_mask.point(lambda p: int(p * 0.9))

        fog.putalpha(inverted_mask)

        self.minimap = Image.alpha_composite(self.minimap.convert("RGBA"), fog)



    def load_pos_item_map(self):
        """
        Loads the position of items on the map from a JSON file.
        """

        with open(self.position_json_map_file, "r") as f:
            self.position_item_dict = json.load(f)
    
    def insert_element(self,x,y,width,height,iconmap,name,resize=False):
        """
        Inserts an icon into the minimap at the specified position.

        Parameters:
        ----------
        x (int):
            X-coordinate where the icon will be placed.
        y (int):
            Y-coordinate where the icon will be placed.
        width (int):
            Width of the icon.
        height (int):
            Height of the icon.
        iconmap (Image):
            The icon image to be placed on the minimap.
        name (str):
            Name of the icon, used for labeling in YOLO format.
        resize (bool):
            If True, resizes the icon to fit the specified width and height.
        """
        if resize:
            iconmap = iconmap.resize((width,height), Image.LANCZOS)
        result = self.minimap.copy()
        result.paste(iconmap,(x,y),iconmap)
        self.minimap = result
        if name:
            if not hasattr(self, "objects_in_image"):
                self.objects_in_image = []
            self.objects_in_image.append({
                "name": name,
                "x": x,
                "y": y,
                "width": width,
                "height": height
            })
    
    def dicc_icon_to_image(self,kind,can_repeat=False):
        """
        Returns a random icon from the dictionary of icons based on the specified kind.

        Parameters:
        ----------
        kind (str):
            The category of icons to select from (e.g., "nex_", "tower_", "inhib_").
        can_repeat (bool):
            If True, allows the same icon to be selected multiple times; otherwise, it will not
            select an icon that has already been placed on the minimap.
        
        Returns:
        -------
        Image:
            The selected icon as a PIL Image.
        """
        if not hasattr(self,"dict_icons"):
            self.dicc_icons = {
                "nex_":{
                    "nex_alive_blue": "./utils/icons/nexus/nexus_blue.png",
                    "nex_alive_red": "./utils/icons/nexus/nexus_red.png",
                    "nex_died": "./utils/icons/nexus/nexus_died.png"
                },
                "tower_": {
                    "tower_died": "./utils/icons/towers/tower_died.png",
                    "tower_died_low": "./utils/icons/towers/tower_died_low.png",
                    "tower_died_medium": "./utils/icons/towers/tower_died_medium.png",
                    "tower_blue_bounty": "./utils/icons/towers/tower_blue_bounty.png",
                    "tower_blue_low_bounty": "./utils/icons/towers/tower_blue_low_bounty.png",
                    "tower_blue_low_bounty_wiuouth": "./utils/icons/towers/tower_blue_low_bounty_wiouth.png",
                    "tower_blue_medium_bounty": "./utils/icons/towers/tower_blue_medium_bounty.png",
                    "tower_blue_medium_bounty_wiuouth": "./utils/icons/towers/tower_blue_medium_bounty_wiouth.png",
                    "tower_red_bounty": "./utils/icons/towers/tower_red_bounty.png",
                    "tower_red_bounty_wiouth": "./utils/icons/towers/tower_red_bounty_wiouth.png",
                    "tower_red_low_bounty": "./utils/icons/towers/tower_red_low_bounty.png",
                    "tower_red_low_bounty_wiouth": "./utils/icons/towers/tower_red_low_bounty_wiouth.png",
                    "tower_red_medium_bounty": "./utils/icons/towers/tower_red_medium_bounty.png",
                    "tower_red_medium_bounty_wiouth": "./utils/icons/towers/tower_red_medium_bounty_wiouth.png",
                    "turret_1plate": "./utils/icons/towers/turret_1plate.png",
                    "turret_2plate": "./utils/icons/towers/turret_2plate.png",
                    "turret_3plate": "./utils/icons/towers/turret_3plate.png",
                    "turret_4plate": "./utils/icons/towers/turret_4plate.png",
                    "turret_5plate": "./utils/icons/towers/turret_5plate.png",
                    "turret_red_1plate": "./utils/icons/towers/turret_red_1plate.png",
                    "turret_red_2plate": "./utils/icons/towers/turret_red_2plate.png",
                    "turret_red_3plate": "./utils/icons/towers/turret_red_3plate.png",
                    "turret_red_4plate": "./utils/icons/towers/turret_red_4plate.png",
                    "turret_red_5plate": "./utils/icons/towers/turret_red_5plate.png",
                    "turret_blue_1plate": "./utils/icons/towers/turret_blue_1plate.png",
                    "turret_blue_2plate": "./utils/icons/towers/turret_blue_2plate.png",
                    "turret_blue_3plate": "./utils/icons/towers/turret_blue_3plate.png",
                    "turret_blue_4plate": "./utils/icons/towers/turret_blue_4plate.png",
                    "turret_blue_5plate": "./utils/icons/towers/turret_blue_5plate.png"
                },
                "inhib_":
                    {
                        "inhib_died":"./utils/icons/inhib/inhibitor_died.png",
                        "inhib_blue":"./utils/icons/inhib/inhibitor_blue.png",
                        "inhib_red":"./utils/icons/inhib/inhibitor_red.png"
                    }
            }
        
        if kind not in self.dicc_icons:
            raise ValueError(f"Categoría '{kind}' no encontrada en dicc_icons")
        
        if not can_repeat:
            available_icons = [k for k in self.dicc_icons[kind] if k not in self.elements_in_map]
        else:
            available_icons = list(self.dicc_icons[kind])
        if not available_icons:
            raise ValueError(f"No quedan iconos disponibles para '{kind}'")
    
        selected_icon = random.choice(available_icons)
        self.elements_in_map.append(selected_icon)
        
        path = self.dicc_icons[kind][selected_icon]
        return Image.open(path).convert("RGBA")
    
    def create_items_map(self):
        """
        Creates the minimap by placing various game elements such as nexus, towers, inhibitors, jungle items, and champions.
        It randomly selects icons for each element and places them on the minimap at specified positions.
        """

        # Nexus
        nexus = [nexo for nexo in self.position_item_dict if nexo["name"].startswith("nex_")]
        for nexo in nexus:
            random_nexo = self.dicc_icon_to_image("nex_")
            self.insert_element(
                x=nexo["x"],y=nexo["y"],
                height=nexo["height"],width=nexo["width"],
                iconmap=random_nexo,
                resize=True,
                name="nexo"
        )
        
        # Towers
        towers = [tower for tower in self.position_item_dict if tower["name"].startswith("tower_")]
        
        for tower in towers:
            random_tower = self.dicc_icon_to_image("tower_")
            self.insert_element(
                x=tower["x"],y=tower["y"],
                height=tower["height"],width=tower["width"],
                iconmap=random_tower,
                resize=True,
                name="tower"
            )
        
        # Inhibitors
        inhibs = [inhib for inhib in self.position_item_dict if inhib["name"].startswith("inhib_")]
        
        for inhib in inhibs:
            random_inhib = self.dicc_icon_to_image("inhib_",can_repeat=True)
            self.insert_element(
                x=inhib["x"],y=inhib["y"],
                height=inhib["height"],width=inhib["width"],
                iconmap=random_inhib,
                resize=True,
                name="inhibitor")
    
        # Jungle items
        jungle_dir = './utils/icons/jungle'
        jungle_items = [f for f in os.listdir(jungle_dir) if not f == "blue_red.png"] 
        np.random.shuffle(jungle_items)
        for jungle_place in self.position_item_dict:
            if jungle_place["name"].startswith("jungle_"):
                item = jungle_items.pop()
                self.insert_element(
                    x=jungle_place["x"],y=jungle_place["y"],
                    height=jungle_place["height"],width=jungle_place["width"],
                    name="jungle",
                    iconmap=Image.open(os.path.join(jungle_dir,item)).convert("RGBA"),
                    resize=True
                    )
            if jungle_place["name"].startswith("redblue_"):
                self.insert_element(
                    x=jungle_place["x"],y=jungle_place["y"],
                    height=jungle_place["height"],width=jungle_place["width"],
                    name="jungle",
                    iconmap=Image.open(os.path.join(jungle_dir,"blue_red.png")).convert("RGBA"),
                    resize=True
                    )

        # Characters
        champ_names = list(self.character_dir.keys())
        selected = random.sample(champ_names, min(15, len(champ_names)))
        red_recall = Image.open("./utils/recall/red_recall.png").convert("RGBA")
        blue_recall = Image.open("./utils/recall/blue_recall.png").convert("RGBA")
        W, H = self.minimap.size

        for champ in selected:
            path = os.path.join(self.dest_dir, f"square_{champ}.png")
            icon = Image.open(path).convert("RGBA")
            icon = icon.resize((45, 45), Image.LANCZOS)
            w, h = icon.size

            mask = Image.new("L", (w, h), 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.ellipse((0, 0, w, h), fill=255)
            icon.putalpha(mask)

            x = random.randint(0, W - w)
            y = random.randint(0, H - h)

            self.insert_element(
                x=x, y=y,
                width=w, height=h,
                iconmap=icon, resize=False,
                name=champ
            )

            draw = ImageDraw.Draw(self.minimap)
            cx, cy = x + w / 2, y + h / 2
            r = w / 2
            
            style = random.choice(["red","blue","recall_red","recall_blue"])
            
            if style == 'red':
                draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(213, 32, 22), width=2)
            elif style == 'blue':
                draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(10, 121, 186), width=2)
            elif style == 'recall_red':
                self.minimap.paste(red_recall.resize((w + 10, h + 10), Image.LANCZOS), (x - 5, y - 5), red_recall.resize((w + 10, h + 10), Image.LANCZOS))
            elif style == 'recall_blue':
                self.minimap.paste(blue_recall.resize((w + 10, h + 10), Image.LANCZOS), (x - 5, y - 5), blue_recall.resize((w + 10, h + 10), Image.LANCZOS))
                    
            
        # Pings
        ping_dir = "./utils/pings"
        ping_files = [f for f in os.listdir(ping_dir) if f.lower().endswith(".png")]
        selected_pings = random.sample(ping_files, k=20) 

        for ping_file in selected_pings:
            ping_icon = Image.open(os.path.join(ping_dir, ping_file)).convert("RGBA")
            ping_icon = ping_icon.resize((30, 30), Image.LANCZOS)
            w, h = ping_icon.size

            x = random.randint(0, W - w)
            y = random.randint(0, H - h)

            self.insert_element(
                x=x, y=y,
                width=w, height=h,
                iconmap=ping_icon,
                resize=False,
                name="ping"
            )

    
    def load_character_dir(self):
        """
        Loads the character directory from the destination square directory.
        It creates a dictionary mapping champion names to their IDs based on the filenames in the directory.
        """
        self.character_dir = {}
        for fn in os.listdir(self.dest_dir):
            if fn.startswith("square_") and fn.lower().endswith(".png"):
                champ = fn.removeprefix("square_").removesuffix(".png")
                self.character_dir[champ] = len(self.character_dir)


    def extract_squares(self):
        """
        Extracts champion icons from the source directory and saves them to the destination directory.
        It copies files that start with "square_" and do not contain "generic" in their names.
        """
        os.makedirs(self.dest_dir, exist_ok=True)
        count = 0
        for root, _, files in os.walk(self.source_dir):
            for fn in files:
                if fn.startswith("square_") and fn.lower().endswith(".png") and fn.lower().find("generic") == -1:
                    self.character_dir[(fn.removeprefix("square_").removesuffix(".png"))] = self.character_dir.keys().__len__()
                    src = os.path.join(root, fn)
                    dst = os.path.join(self.dest_dir, fn)
                    try:
                        shutil.copy2(src, dst)
                        count += 1
                    except Exception as e:
                        print(f"⚠️ Error copiando {src}: {e}")
        print(f"✅ Copiados {count} archivos a '{self.dest_dir}'")
    
    def save_yolo_labels(self, output_folder, image=True,ignore_labels = ["nexus","inhibitor","nexo"]):
        """
        Saves the minimap image and its corresponding YOLO format labels to the specified output folder.
        
        Parameters:
        ----------
        output_folder (str):
            The directory where the minimap image and labels will be saved.
        image (bool):
            If True, saves the minimap image; otherwise, only saves the labels.
        ignore_labels (list):
            List of labels to ignore when saving YOLO labels.
        """
        """ 
        Careful with this, less than 16 can generate colision with 30k minimaps
        Colision probability is 1/2^64, so it's very low.
        """
        image_id = str(uuid.uuid4())[:16]
        width, height = self.minimap.size

        if image:
            img_path = os.path.join(output_folder, f"{image_id}.png")
            self.minimap.save(img_path)

        label_path = os.path.join(output_folder, f"{image_id}.txt")
        with open(label_path, "w") as f:
            for obj in self.objects_in_image:
                name = obj["name"]
                if any(name == ign or name.startswith(ign) for ign in ignore_labels):
                    continue
                if name in getattr(self, "character_dir", {}):
                    cls = self.character_dir[name]
                else:
                    continue
                x = obj["x"]; y = obj["y"]
                w = obj["width"]; h = obj["height"]
                x_center = (x + w / 2) / width
                y_center = (y + h / 2) / height
                w_norm = w / width
                h_norm = h / height

                f.write(f"{cls} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
    
    def downgrade_resolution(self, scale_factor=0.4):
        """
        Downgrades the resolution of the minimap by scaling it down and then back up.
        This simulates a lower resolution while maintaining the overall structure of the minimap.
        """

        original_size = self.minimap.size
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        downgraded = self.minimap.resize(new_size, Image.BILINEAR)
        self.minimap = downgraded.resize(original_size, Image.BILINEAR)

    
    def save_character_json(self):
        """
        Saves the character directory to a JSON file.
        This file contains the mapping of champion names to their IDs.
        """

        if not self.character_dir:
            raise RuntimeError("self.character_dir está vacío; asegúrate de haber llamado a load_character_dir() o extract_squares().")

        with open("./characters.json", "w", encoding="utf-8") as f:
            json.dump(self.character_dir, f, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    """
    Main function to generate minimaps for training.
    It creates a specified number of minimaps, saves them in a directory, and prints the completion message.
    """
    
    print("\n🧠 Generación de minimapas para entrenamiento")
    print("────────────────────────────────────────────\n")
    
    output_folder = os.path.join(os.getcwd(), "train_images")
    os.makedirs(output_folder, exist_ok=True)

    NUM_MAPS = 5000

    for i in tqdm(range(NUM_MAPS), desc="🗺️ Generando minimapas", ncols=100):
        minimap = Minimap(extract_s=i==0)
        minimap.save_yolo_labels(output_folder, image=True) 

    print("\n✅ Generación finalizada: {} minimapas guardados en '{}'".format(NUM_MAPS, output_folder)) 


   
