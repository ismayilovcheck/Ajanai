"""
Ajan API Client Modülü
API'lerden veri çeken yardımcı sınıf
"""

import requests
from typing import Optional, Dict
from config import AjanConfig

class AjanAPIClient:
    """Ajan için API'lerden veri çeken yardımcı sınıf"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': AjanConfig.USER_AGENT,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.timeout = AjanConfig.REQUEST_TIMEOUT
    
    def get_json(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[Dict]:
        """JSON API endpoint'inden veri çeker"""
        try:
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            response = self.session.get(
                url, 
                params=params, 
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"⚠ Ajan - API hatası ({url}): {str(e)}")
            return None
    
    def post_json(self, url: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[Dict]:
        """JSON API endpoint'ine POST isteği gönderir"""
        try:
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            response = self.session.post(
                url,
                json=data,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"⚠ Ajan - API POST hatası ({url}): {str(e)}")
            return None