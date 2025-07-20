import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import os

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.scraped_data = []
    
    def scrape_quotes(self, url="http://quotes.toscrape.com"):
        """Scraper de ejemplo para quotes.toscrape.com"""
        try:
            print(f"Scrapeando: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            
            for quote in quotes:
                text = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
                
                self.scraped_data.append({
                    'text': text,
                    'author': author,
                    'tags': tags
                })
            
            print(f"Scraped {len(quotes)} quotes")
            
            # Buscar siguiente página
            next_btn = soup.find('li', class_='next')
            if next_btn:
                next_url = urljoin(url, next_btn.find('a')['href'])
                time.sleep(1)  # Ser respetuoso con el servidor
                self.scrape_quotes(next_url)
                
        except Exception as e:
            print(f"Error scrapeando {url}: {e}")
    
    def scrape_custom_site(self):
        """Scraper personalizable"""
        url = input("Ingresa la URL a scrapear: ")
        selector = input("Ingresa el selector CSS (ej: 'h2', '.title', '#content'): ")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.select(selector)
            
            for i, element in enumerate(elements):
                self.scraped_data.append({
                    'index': i + 1,
                    'text': element.get_text().strip(),
                    'html': str(element)
                })
            
            print(f"Encontrados {len(elements)} elementos")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def save_data(self, filename="scraped_data.json"):
        """Guardar datos scrapeados"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            print(f"Datos guardados en {filename}")
        except Exception as e:
            print(f"Error guardando datos: {e}")
    
    def show_data(self):
        """Mostrar datos scrapeados"""
        if not self.scraped_data:
            print("No hay datos para mostrar")
            return
        
        for i, item in enumerate(self.scraped_data[:10]):  # Mostrar solo los primeros 10
            print(f"\n--- Item {i+1} ---")
            for key, value in item.items():
                if isinstance(value, list):
                    print(f"{key}: {', '.join(value)}")
                else:
                    print(f"{key}: {value[:100]}..." if len(str(value)) > 100 else f"{key}: {value}")
        
        if len(self.scraped_data) > 10:
            print(f"\n... y {len(self.scraped_data) - 10} elementos más")

def main():
    scraper = WebScraper()
    
    while True:
        print("\n=== WEB SCRAPER ===")
        print("1. Scrapear quotes.toscrape.com (ejemplo)")
        print("2. Scrapear sitio personalizado")
        print("3. Mostrar datos scrapeados")
        print("4. Guardar datos en JSON")
        print("5. Limpiar datos")
        print("6. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            scraper.scraped_data = []  # Limpiar datos anteriores
            scraper.scrape_quotes()
        elif opcion == "2":
            scraper.scrape_custom_site()
        elif opcion == "3":
            scraper.show_data()
        elif opcion == "4":
            filename = input("Nombre del archivo (default: scraped_data.json): ") or "scraped_data.json"
            scraper.save_data(filename)
        elif opcion == "5":
            scraper.scraped_data = []
            print("Datos limpiados")
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
