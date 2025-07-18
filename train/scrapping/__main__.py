from champion_downloader import ChampionDownloader
from others_downloader import OtherDownloader
from downloader import download
import os
import argparse

def main(parent_path):
    """
    Main function to initiate the downloading of various game assets.
    It sets up the necessary directories and calls the download methods for different asset types.
    
    Parameters:
    ----------
    parent_path (str):
        The directory where the downloaded assets will be saved.
    """
    
    os.makedirs(parent_path,exist_ok=True)
    print("Iniciando descargas...")
    print("\nSummoners\n")
    
    # Downloading summoners
    OtherDownloader(f"{parent_path}/summoners").downloader()

    print("\nItems\n")
    # Downloading items
    OtherDownloader(f"{parent_path}/items",kind="items").downloader()
    
    print("\nItems\n")
    # Downloading minimap icons
    OtherDownloader(f"{parent_path}/minimap/icons",kind="minimap_icons").downloader()

    print("\nPings\n")
    # Downloading minimap icons
    OtherDownloader(f"{parent_path}/minimap/pings",kind="minimap_pings").downloader()

    print("\nCampeones\n")
    ChampionDownloader(f"{parent_path}/characters")
     
    print("\nUtils\n")
    print("Descargando minimapa...")
    download("https://static.wikia.nocookie.net/leagueoflegends/images/0/04/Summoner%27s_Rift_Minimap.png/revision/latest?cb=20240527145536",f"{parent_path}/utils","minimap.png")

if __name__ == "__main__":
    """
    Entry point for the script. It parses command line arguments and calls the main function.
    """
    parser = argparse.ArgumentParser(description="Scraper Lol")
    parser.add_argument("--path", type=str, default="./data_train", help="Ruta donde guardar los datos.")
    args = parser.parse_args()
    main(args.path)