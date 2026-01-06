import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class AjanConfig:
    """Ajan tətbiqi konfiqurasiya tənzimləmələri"""
    
    # API Tənzimləmələri
    if "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
    REQUEST_TIMEOUT = 30
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # --- YERLİ PLATFORMALAR (AZƏRBAYCAN) ---
    AZ_SITELERI = [
        "https://tap.az/elanlar/xidmetler/it-internet-proqramlasdirma",
        "https://tap.az/elanlar/xidmetler/tercume",
        "https://tap.az/elanlar/xidmetler/dizayn-ve-reklam"
    ]
    
    # Global Platformlar (Ehtiyat üçün)
    FREELANCE_SITES = ["https://www.freelancer.com"]
    ANKET_PLATFORMLARI = ["https://www.swagbucks.com"]
    MIKRO_GOREV_SITELERI = ["https://www.clickworker.com"]
    
    @classmethod
    def validate(cls):
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY tapılmadı! Lütfen Streamlit Secrets-i yoxlayın.")
        return True
