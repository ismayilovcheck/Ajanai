import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
from config import AjanConfig

class AjanScraper:
    """Veb saytları skan edən və məlumatları çəkən sinif"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': AjanConfig.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
        self.timeout = AjanConfig.REQUEST_TIMEOUT
        print("✓ AjanScraper (Tap.az Dəstəyi ilə) başladıldı")
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            time.sleep(1.5) # Saytın bloklamaması üçün gözləmə
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            # Parser xətasının qarşısını almaq üçün
            try:
                return BeautifulSoup(response.content, 'lxml')
            except:
                return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"⚠ Xəta: {url} çəkilə bilmədi - {str(e)}")
            return None

    def scrape_tap_az(self, url: str) -> List[Dict]:
        """Tap.az-dan elanları çəkir"""
        opportunities = []
        soup = self.fetch_page(url)
        if not soup: return opportunities

        # Tap.az elan konteynerləri: 'products-i'
        items = soup.find_all('div', class_='products-i')
        
        for item in items:
            try:
                title_elem = item.find('div', class_='products-name')
                price_elem = item.find('span', class_='price-cur')
                link_elem = item.find('a', class_='products-link')
                
                if title_elem and price_elem:
                    title = title_elem.text.strip()
                    price = price_elem.parent.text.strip() # Qiymət və valyuta
                    link = "https://tap.az" + link_elem['href']
                    
                    opportunities.append({
                        'title': title,
                        'description': f"Tap.az yerli fürsət: {title}",
                        'payment': price,
                        'source': 'Tap.az',
                        'url': link,
                        'type': 'local',
                        'difficulty': 'Müəyyən edilməyib',
                        'duration': 'Danışıq asılıdır'
                    })
            except Exception as e:
                continue
        return opportunities

    def search_all_opportunities(self) -> List[Dict]:
        """Bütün platformaları tarayır"""
        all_opportunities = []
        
        # 🇦🇿 İlk olaraq yerli Tap.az elanlarını çəkirik
        print("\n🇦🇿 Tap.az taranır...")
        for site in AjanConfig.AZ_SITELERI:
            opps = self.scrape_tap_az(site)
            all_opportunities.extend(opps)
            
        # Əgər Tap.az-dan heç nə tapılmasa, demo məlumatları qaytarmamaq üçün 
        # burada boş siyahı yoxlaması edə bilərsən.
        
        return all_opportunities
