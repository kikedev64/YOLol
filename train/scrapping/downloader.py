import requests
import os

def download(url, path=None,name=None):
    response = requests.get(url)
    if response.status_code == 200:
        # Obtener nombre de archivo de la URL
        if name is None:
            name = url.split("/")[-1].split("?")[0]
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path,f"{name}.png"), "wb") as file:
            file.write(response.content)
        print(f"✅ Archivo guardado como: {path}")
    else:
        print(f"❌ Error al descargar: {url} (Status: {response.status_code})")

