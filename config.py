import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class AjanConfig:
    """Ajan uygulaması yapılandırma ayarları"""
    
    # API Ayarları
    if "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
    REQUEST_TIMEOUT = 30
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    
    # --- YEREL PLATFORMLAR (AZERBAYCAN) ---
    AZ_SITELERI = [
        "https://tap.az/elanlar/xidmetler/it-internet-proqramlasdirma",
        "https://tap.az/elanlar/xidmetler/tercume",
        "https://lalafo.az/azerbaijan/vakansiyalar"
    ]
    
    # Global Platformlar
    FREELANCE_SITES = ["https://www.freelancer.com", "https://www.upwork.com"]
    ANKET_PLATFORMLARI = ["https://www.swagbucks.com"]
    MIKRO_GOREV_SITELERI = ["https://www.clickworker.com"]
    
    @classmethod
    def validate(cls):
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY bulunamadı!")
        return True
