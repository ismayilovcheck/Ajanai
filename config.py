import os
import streamlit as st # Streamlit eklendi
from dotenv import load_dotenv

load_dotenv()

class AjanConfig:
    """Ajan uygulaması yapılandırma ayarları"""
    
    # --- KRİTİK DEĞİŞİKLİK ---
    # Önce Streamlit Secrets'a bak, bulamazsan .env/Environment Variables'a bak
    if "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
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
            raise ValueError("GOOGLE_API_KEY bulunamadı! Lütfen Streamlit Secrets veya .env dosyasını kontrol edin.")
        
        # Streamlit'te print konsolda görünmez, st.write veya st.toast kullanabilirsin ama validate sessizce geçsin
        return True
