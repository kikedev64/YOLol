import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests

class SummonerDownloader:
    
    def __init__(self, parent_path):
        self.USE_SELENIUM = False
        self.USE_PROXIES = False
        self.CDN_URL = "https://raw.communitydragon.org/latest/game/assets/spells/icons2d/"
        self.count = 0
        self.summoners = []
        self.parent_path = parent_path
        self.len_summs = 0
        os.makedirs(parent_path,exist_ok=True)
        
    def get_headers(self):
        ua = UserAgent()
        return {
            "User-Agent": ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

    def get_proxy(self):
        return random.choice(self.PROXIES) if self.USE_PROXIES else None
    
    def fetch_with_selenium(self, url, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # esperamos a que cargue
        time.sleep(3)
        html = driver.page_source
        driver.quit()
        return html
    
    def scrapping(self):
        # obtenemos el HTML ya sea por requests o por Selenium según USE_SELENIUM
        if self.USE_SELENIUM:
            html = self.fetch_with_selenium(self.CDN_URL)
        else:
            html = requests.get(self.CDN_URL, headers=self.get_headers(), proxies={"http": self.get_proxy(), "https": self.get_proxy()}).text

        soup = BeautifulSoup(html, "html.parser")

        # buscamos la tabla con id="list"
        table = soup.find("table", id="list")
        if not table:
            print("No se encontró la tabla #list")
            return

        # recorremos cada fila
        for tr in table.find_all("tr"):
            td_link = tr.find("td", class_="link")
            if not td_link:
                continue

            a = td_link.find("a", title=True, href=True)
            if not a:
                continue

            # texto y título
            text = a.get_text(strip=True).lower()
            title = a["title"].lower()

            # validamos si contiene “summoner” o “smite”
            if "summoner_" in text or "smite" in text or \
               "summoner_" in title or "smite" in title:
                name = text  # o bien title, según prefieras
                # construimos la URL de descarga
                href = a["href"]
                # si href es relativo, lo unimos; si ya es absoluto, lo usamos directo
                if href.startswith("http"):
                    url = href
                else:
                    url = self.CDN_URL.rstrip("/") + "/" + href.lstrip("/")
                # guardamos la tupla
                self.summoners.append((name, url))
        self.len_summs = self.summoners.__len__
        return self.summoners

    def downloader(self):
        # implementar lógica de descarga a partir de self.summoners
        print("Descargando summoners...")
        for name, url in self.summoners:
            resp = requests.get(url, headers=self.get_headers())
            if resp.status_code == 200:
                with open(os.path.join(self.parent_path,f"{name}.png"), "wb") as f:
                    f.write(resp.content)
                print(f"Summoner {name} {self.count}/{self.len_summs}")
            else:
                print(f"Error descargando {name}: {resp.status_code}")
        print("✅ Summoners descargados correctamente")

# Uso:
down = SummonerDownloader("./summoners")
resultados = down.scrapping()
down.downloader()