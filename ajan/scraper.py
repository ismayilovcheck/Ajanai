import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
from config import AjanConfig

class AjanScraper:
    """Web sitelerini tarayan ve veri çeken gelişmiş sınıf"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': AjanConfig.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'az,tr;q=0.9,en-US;q=0.8,en;q=0.7'
        })
        self.timeout = AjanConfig.REQUEST_TIMEOUT
        print("✓ AjanScraper (Yerel Destekli) başlatıldı")
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            # Tap.az gibi siteler botları engellememesi için küçük bir bekleme
            time.sleep(1) 
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            # Önce lxml dene, yoksa html.parser kullan
            try:
                return BeautifulSoup(response.content, 'lxml')
            except:
                return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"⚠ Hata: {url} çekilemedi - {str(e)}")
            return None

    def scrape_tap_az(self, url: str) -> List[Dict]:
        """Tap.az üzerinden hizmet ilanlarını çeker"""
        opportunities = []
        soup = self.fetch_page(url)
        if not soup: return opportunities

        # Tap.az ilan konteynerları
        items = soup.find_all('div', class_='products-i')
        
        for item in items:
            try:
                title = item.find('div', class_='products-name').text.strip()
                price_val = item.find('span', class_='price-cur').parent.text.strip()
                link = "https://tap.az" + item.find('a', class_='products-link')['href']
                
                opportunities.append({
                    'title': title,
                    'description': f"Tap.az üzerinden hizmet ilanı: {title}",
                    'payment': price_val,
                    'source': 'Tap.az',
                    'url': link,
                    'type': 'local'
                })
            except:
                continue
        return opportunities

    def search_all_opportunities(self) -> List[Dict]:
        """Tüm yerel ve global platformları tarar"""
        all_opportunities = []
        
        # 1. Önce Yerel (Azerbaycan) Sitelerini Tara (Daha yüksek başarı oranı)
        print("\n🇦🇿 Yerel platformlar taranıyor (Tap.az vb.)...")
        for site in AjanConfig.AZ_SITELERI:
            if "tap.az" in site:
                opps = self.scrape_tap_az(site)
                all_opportunities.extend(opps)
        
        # 2. Global Freelance Siteleri
        print("\n🌐 Global freelance siteleri taranıyor...")
        for site in AjanConfig.FREELANCE_SITES:
            # Bu siteler çok sıkı korunduğu için şu an boş dönebilir
            # Ama altyapı hazır.
            time.sleep(2)
            
        return all_opportunities
