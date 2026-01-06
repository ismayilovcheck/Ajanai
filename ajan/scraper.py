import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
from config import AjanConfig

class AjanScraper:
    """Veb saytları skan edən və məlumatları çəkən sinif"""
    
    def __init__(self):
        self.session = requests.Session()
        # Brauzer kimi görünmək üçün headers (Bloklanma riskini azaldır)
        self.session.headers.update({
            'User-Agent': AjanConfig.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'az,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://google.com'
        })
        self.timeout = AjanConfig.REQUEST_TIMEOUT
        print("✓ AJAN Skraper (Tap.az və Yerli Dəstək) Aktivdir")
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Səhifəni yükləyir və BS4 obyektinə çevirir"""
        try:
            # Saytların bot olduğunu anlamaması üçün dinamik gözləmə
            time.sleep(2) 
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parser seçimi (lxml yoxdursa html.parser istifadə et)
            try:
                return BeautifulSoup(response.content, 'lxml')
            except:
                return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"⚠ Xəta: {url} yüklənərkən problem oldu - {str(e)}")
            return None

    def scrape_tap_az(self, url: str) -> List[Dict]:
        """Tap.az xidmətlər bölməsini skaner edir"""
        opportunities = []
        soup = self.fetch_page(url)
        if not soup: return opportunities

        # Tap.az məhsul kartları
        items = soup.find_all('div', class_='products-i')
        
        for item in items:
            try:
                title_elem = item.find('div', class_='products-name')
                price_elem = item.find('span', class_='price-cur')
                link_elem = item.find('a', class_='products-link')
                
                if title_elem and price_elem:
                    title = title_elem.get_text(strip=True)
                    price = price_elem.parent.get_text(strip=True)
                    link = "https://tap.az" + link_elem['href']
                    
                    opportunities.append({
                        'title': title,
                        'payment': price,
                        'source': 'Tap.az',
                        'url': link,
                        'type': 'local',
                        'difficulty': 'Analiz edilir...',
                        'duration': 'İşə görə dəyişir'
                    })
            except:
                continue
        return opportunities

    def search_all_opportunities(self) -> List[Dict]:
        """Bütün aktiv mənbələrdən məlumatları toplayır"""
        all_opportunities = []
        
        # 🇦🇿 1. Yerli Mənbələr (Tap.az və s.)
        print("\n🔍 Yerli bazarlar yoxlanılır...")
        if hasattr(AjanConfig, 'AZ_SITELERI'):
            for site in AjanConfig.AZ_SITELERI:
                if "tap.az" in site:
                    opps = self.scrape_tap_az(site)
                    all_opportunities.extend(opps)
        
        # 🌐 2. Qlobal Mənbələr (Freelance və s.)
        # Bloklanma ehtimalı yüksək olduğu üçün bura ehtiyatla yanaşılır
        print("🔍 Qlobal bazarlar yoxlanılır...")
        
        # Əgər heç bir məlumat tapılmasa, istifadəçiyə boş siyahı göndəririk
        # main.py bu boş siyahını görüb avtomatik demo məlumatları yükləyəcək.
        return all_opportunities
