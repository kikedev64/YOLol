import requests
import shutil
import os
import json


class ChampionDownloader:
    
    def __init__(self,parent_path):
        self.parent_path = parent_path
        self.GENERIC = "generic"
        self.GENERIC_PATH = f"./{parent_path}/default/"
        
        self.CHARACTERS = self.get_champions()
        self.CHARACTER_NUMBER = self.CHARACTERS.__len__
        self.count = 0
        
        # Generic data
        print("Descargando datos genéricos...")
        self.generic_data()
        
        # Abilitys and square
        print("Descargando campeones...")
        for character in self.CHARACTERS:
            self.download_abilities(character)
            self.download_square(character)
            print(f"{character} descargado {self.count}/{self.CHARACTER_NUMBER}.")
        print("✅ Todo descargado correctamente")
        pass

    def download_abilities(self,champion):
        self.count += 1
        route_path = f"./{self.parent_path}/{champion}"
        path_abilitys = os.path.join(route_path, "abilitys")
        
        for path in [route_path, path_abilitys]:
            os.makedirs(path, exist_ok=True)
        
        # Ability icons
        abilitys = [("q",requests.get(f"https://cdn.communitydragon.org/latest/champion/{champion}/ability-icon/q", stream=True)), 
                    ("w", requests.get(f"https://cdn.communitydragon.org/latest/champion/{champion}/ability-icon/w", stream=True)), 
                    ("e", requests.get(f"https://cdn.communitydragon.org/latest/champion/{champion}/ability-icon/e", stream=True)),
                    ("r", requests.get(f"https://cdn.communitydragon.org/latest/champion/{champion}/ability-icon/r", stream=True))
                    ]

        for ability, response in abilitys:
            print(f"Descargando habilidad {ability}...")
            if response.status_code == 200:
                file_path = os.path.join(path_abilitys, f"{ability}.png")
                with open(file_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                response.close()
            else:
                print(f"❌ No se pudo descargar {ability.upper()} para {champion} (status {response.status_code})")
        
        # Square
        self.download_square(champion)
        
    def download_square(self,champion,generic=False):
        square = requests.get(f"https://cdn.communitydragon.org/latest/champion/{champion}/square",stream=True)
        
        if square.status_code == 200:
            file_path = os.path.join(f"./{self.parent_path}/{champion if not generic else 'default'}/square_{champion}.png")
            with open(file_path,"wb") as file_output:
                shutil.copyfileobj(square.raw,file_output)
    
    
    def generic_data(self):
        os.makedirs(self.GENERIC_PATH,exist_ok=True)
        self.download_square(self.GENERIC,generic=True)
        
    def get_champions(self):
        with open('./assets/characters.json','r',encoding="utf-8") as character_json:
            data = json.load(character_json)
        
        characters = [char.lower() for char in data["data"].keys()]
        return list(characters)

# ChampionDownloader