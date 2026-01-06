import os
from dotenv import load_dotenv

load_dotenv()

class AjanConfig:
    """Ajan uygulaması yapılandırma ayarları"""
    
    # AI API Ayarları
    # ÖNEMLİ: API anahtarları .env dosyasından alınır, kod içinde hardcode edilmez!
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
    
    # Scraping Ayarları
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Hedef Platformlar
    FREELANCE_SITES = [
        "https://www.freelancer.com",
        "https://www.upwork.com",
        "https://www.fiverr.com"
    ]
    
    ANKET_PLATFORMLARI = [
        "https://www.swagbucks.com",
        "https://www.toluna.com"
    ]
    
    MIKRO_GOREV_SITELERI = [
        "https://www.mturk.com",
        "https://www.clickworker.com"
    ]
    
    @classmethod
    def validate(cls):
        """API anahtarlarının varlığını kontrol et"""
        if cls.AI_PROVIDER == "gemini" and not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        elif cls.AI_PROVIDER == "groq" and not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        print(f"✓ Ajan yapılandırması doğrulandı - Provider: {cls.AI_PROVIDER}")