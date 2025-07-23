import requests
import os

def download(url, path=None,name=None):
    """
    Downloads a file from a given URL and saves it to the specified path.

    Parameters:
    ----------
    url (str): 
        The URL of the file to download.
    path (str, optional):
        The directory where the file should be saved. If None, the current directory is used.
    name (str, optional):
        The name to save the file as. If None, the name is derived from the URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        if name is None:
            name = url.split("/")[-1].split("?")[0]
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path,f"{name}.png"), "wb") as file:
            file.write(response.content)
        print(f"✅ Archivo guardado como: {path}")
    else:
        print(f"❌ Error al descargar: {url} (Status: {response.status_code})")

