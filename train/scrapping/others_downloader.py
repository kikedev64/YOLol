import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests

class OtherDownloader:
    """
    Class to download various game assets like summoner spells, items, minimap icons, and pings.
    It supports both direct HTTP requests and Selenium for scraping.
    """
    
    def __init__(self, parent_path,kind="summoners"):
        """
        Initializes the downloader with the specified parent path and kind of assets to download.
        Parameters:
        --------
        parent_path (str): 
            The directory where the downloaded assets will be saved.
        kind (str):
            The type of assets to download. Options are "summoners", "items", "minimap_icons", or "minimap_pings".
        """
        
        self.kind = kind
        if self.kind == "summoners" or self.kind == "items":
            format_url = "spells" if self.kind == "summoners" else "items"
            self.CDN_URL = f"https://raw.communitydragon.org/latest/game/assets/{format_url}/icons2d/"
        else:
            format_url = "icons" if self.kind == "minimap_icons" else "pings"
            self.CDN_URL = f"https://raw.communitydragon.org/latest/game/assets/ux/minimap/{format_url}/"
        self.USE_SELENIUM = False
        self.USE_PROXIES = False
        self.count = 0
        self.items_scrapped = []
        self.parent_path = parent_path
        self.len_summs = 0
        os.makedirs(parent_path,exist_ok=True)
        
    def get_headers(self):
        """
        Returns a dictionary of headers to be used in HTTP requests.
        This includes a random User-Agent and other common headers.
        
        Returns:
        --------
        dict: 
            A dictionary containing headers for the HTTP request.
        """
        ua = UserAgent()
        return {
            "User-Agent": ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

    def get_proxy(self):
        """
        Returns a random proxy from a predefined list if USE_PROXIES is True.
        
        Returns:
        --------
        str or None: 
            A random proxy address if USE_PROXIES is True, otherwise None.
        """
        return random.choice(self.PROXIES) if self.USE_PROXIES else None
    
    def fetch_with_selenium(self, url, headless=True):
        """
        Fetches the HTML content of a given URL using Selenium WebDriver.
        
        Parameters:
        --------
        url (str): 
            The URL to fetch.
        headless (bool):
            If True, runs the browser in headless mode (no GUI).
        
        Returns:
        --------
        str: 
            The HTML content of the page.
        """
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        html = driver.page_source
        driver.quit()
        return html
    
    def scrapping(self):
        """
        Scrapes the specified kind of assets from the Community Dragon CDN.
        It uses either direct HTTP requests or Selenium based on the USE_SELENIUM flag.
        """
        if self.USE_SELENIUM:
            html = self.fetch_with_selenium(self.CDN_URL)
        else:
            html = requests.get(self.CDN_URL, headers=self.get_headers(), proxies={"http": self.get_proxy(), "https": self.get_proxy()}).text

        soup = BeautifulSoup(html, "html.parser")
        time.sleep(3)
        
        table = soup.find("table", id="list")
        if not table:
            print("No se encontró la tabla #list")
            return

        for tr in table.find_all("tr"):
            td_link = tr.find("td", class_="link")
            if not td_link:
                continue

            a = td_link.find("a", title=True, href=True)
            if not a:
                continue

            text = a.get_text(strip=True).lower()
            title = a["title"].lower()
            if self.kind == "summoners":
                if "summoner_" in text or "smite" in text or \
                "summoner_" in title or "smite" in title:
                    name = text
                    href = a["href"]
                    if href.startswith("http"):
                        url = href
                    else:
                        url = self.CDN_URL.rstrip("/") + "/" + href.lstrip("/")
                    
                    print(f"Summoner EXTRA {name} scrapeado correctamente")
                    self.items_scrapped.append((name, url))
            else:
                if not text.endswith("/"):
                    name = title  
                    href = a["href"]
                    if href.startswith("http"):
                        url = href
                    else:
                        url = self.CDN_URL.rstrip("/") + "/" + href.lstrip("/")
                    print(f"Elemento {name} scrapeado correctamente")
                    self.items_scrapped.append((name, url))
                    
        self.len_summs = self.items_scrapped.__len__()

    def downloader(self):
        """
        Downloads the scraped assets to the specified parent path.
        It iterates over the scraped items and saves them to files.
        """
        
        print(f"Scrapeando {self.kind}...")
        self.scrapping()
        print(f"Descargando {self.kind}...")
        for name, url in self.items_scrapped:
            resp = requests.get(url, headers=self.get_headers())
            if resp.status_code == 200:
                with open(os.path.join(self.parent_path,name), "wb") as f:
                    f.write(resp.content)
                print(f"Elemento {name} {self.count}/{self.len_summs}")
            else:
                print(f"Error descargando {name}: {resp.status_code}")
            self.count += 1
            
        if self.kind == "summoners":
            smite_normal = requests .get("https://raw.communitydragon.org/latest/game/assets/characters/zoe/hud/icons2d/summoner_smite.png",stream=True)
            if smite_normal.status_code == 200:
                with open(os.path.join(self.parent_path,"smite_summoner.png"), "wb") as f:
                    f.write(smite_normal.content)
                print(f"Summoner smite {self.count}/{self.len_summs}")
                
        print(f"✅ {self.kind} descargados correctamente")


