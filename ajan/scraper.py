"""
Ajan Web Scraper Modülü
Web sitelerini tarayan ve gelir fırsatlarını toplayan modül
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
from config import AjanConfig

class AjanScraper:
    """Ajan için web sitelerini tarayan ve veri çeken sınıf"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': AjanConfig.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
        })
        self.timeout = AjanConfig.REQUEST_TIMEOUT
        print("✓ AjanScraper başlatıldı")
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Bir web sayfasını çeker ve BeautifulSoup nesnesi döndürür"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"⚠ Ajan - Hata: {url} çekilemedi - {str(e)}")
            return None
    
    def scrape_freelance_opportunities(self, site_url: str) -> List[Dict]:
        """Freelance sitelerinden fırsatları çeker"""
        opportunities = []
        print(f"  → {site_url} taranıyor...")
        
        soup = self.fetch_page(site_url)
        if not soup:
            return opportunities
        
        # TODO: Siteye özel scraping mantığı buraya eklenecek
        # Örnek yapı:
        # projects = soup.find_all('div', class_='project-item')
        # for project in projects:
        #     opportunities.append({
        #         'title': project.find('h3').text.strip(),
        #         'description': project.find('p').text.strip(),
        #         'payment': project.find('span', class_='amount').text.strip(),
        #         'source': site_url
        #     })
        
        return opportunities
    
    def scrape_survey_opportunities(self, site_url: str) -> List[Dict]:
        """Anket platformlarından fırsatları çeker"""
        opportunities = []
        print(f"  → {site_url} taranıyor...")
        
        soup = self.fetch_page(site_url)
        if not soup:
            return opportunities
        
        # TODO: Siteye özel scraping mantığı buraya eklenecek
        
        return opportunities
    
    def scrape_microtask_opportunities(self, site_url: str) -> List[Dict]:
        """Mikro görev sitelerinden fırsatları çeker"""
        opportunities = []
        print(f"  → {site_url} taranıyor...")
        
        soup = self.fetch_page(site_url)
        if not soup:
            return opportunities
        
        # TODO: Siteye özel scraping mantığı buraya eklenecek
        
        return opportunities
    
    def search_all_opportunities(self) -> List[Dict]:
        """Ajan tüm platformları tarar ve fırsatları toplar"""
        all_opportunities = []
        
        print("\n📊 Freelance siteleri taranıyor...")
        for site in AjanConfig.FREELANCE_SITES:
            opps = self.scrape_freelance_opportunities(site)
            all_opportunities.extend(opps)
            time.sleep(2)  # Rate limiting
        
        print("\n📋 Anket platformları taranıyor...")
        for site in AjanConfig.ANKET_PLATFORMLARI:
            opps = self.scrape_survey_opportunities(site)
            all_opportunities.extend(opps)
            time.sleep(2)
        
        print("\n🔧 Mikro görev siteleri taranıyor...")
        for site in AjanConfig.MIKRO_GOREV_SITELERI:
            opps = self.scrape_microtask_opportunities(site)
            all_opportunities.extend(opps)
            time.sleep(2)
        
        return all_opportunities