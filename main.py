import streamlit as st
from config import AjanConfig
from ajan import AjanScraper, AjanAnalyzer
import json
from datetime import datetime
import plotly.express as px # Grafik için
import pandas as pd
import google.generativeai as genai

# 1. Sayfa Ayarları (En Üstte Olmalı)
st.set_page_config(page_title="AJAN AI - Mikro Ekonomi", page_icon="🤖", layout="wide")

# 2. API Bağlantısı (Secrets'tan Okuma)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Config sınıfındaki değişkeni de güncelle ki hata vermesin
    AjanConfig.GOOGLE_API_KEY = api_key 
else:
    st.error("API Anahtarı bulunamadı! Settings > Secrets kısmına ekleyin.")
    st.stop()

# 3. Görsel Stil (CSS)
st.markdown("""
    <style>
    .main-title { font-size: 3rem; font-weight: 700; color: #764ba2; text-align: center; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #667eea, #764ba2); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤖 AJAN AI</h1>', unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Otonom Pasif Gelir ve Fırsat Analiz Merkezi</p>", unsafe_allow_html=True)

# 4. Sekmeli Yapı (Profesyonel Görünüm)
tab1, tab2, tab3 = st.tabs(["🔍 Fırsat Bul", "📊 Analiz Raporu", "ℹ️ Hakkında"])

with tab1:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        start = st.button("🚀 AJAN'I ÇALIŞTIR", use_container_width=True)
    
    if start:
        with st.status("Ajan internetin derinliklerine iniyor...", expanded=True) as status:
            ajan_scraper = AjanScraper()
            ajan_analyzer = AjanAnalyzer()
            
            opps = ajan_scraper.search_all_opportunities()
            if not opps:
                st.info("Canlı veri taranamadı, analiz için demo veriler hazırlanıyor...")
                opps = [
                    {'title': 'Veri Giriş Projesi', 'payment': '$30', 'source': 'Upwork', 'type': 'freelance'},
                    {'title': 'Anket Paketi', 'payment': '$10', 'source': 'Swagbucks', 'type': 'survey'}
                ]
            
            results = ajan_analyzer.analyze_opportunities(opps[:5])
            st.session_state['son_sonuclar'] = results
            status.update(label="İşlem Tamamlandı!", state="complete")

with tab2:
    if 'son_sonuclar' in st.session_state:
        results = st.session_state['son_sonuclar']
        
        # Grafik Hazırlığı
        df = pd.DataFrame([{"Fırsat": r['opportunity']['title'], "Skor": r['score']} for r in results])
        fig = px.bar(df, x='Fırsat', y='Skor', color='Skor', title="Fırsat Skor Dağılımı")
        st.plotly_chart(fig, use_container_width=True)
        
        # Sonuç Kartları
        for res in results:
            with st.expander(f"⭐ Skor: {res['score']}/10 - {res['opportunity']['title']}"):
                st.write(res['analysis'])
                st.info(f"💡 Öneri: {res['recommended_action']}")
    else:
        st.info("Henüz bir analiz yapılmadı. Lütfen 'Fırsat Bul' sekmesine gidin.")

with tab3:
    st.write("Ajan AI, Python ve Google Gemini tabanlı bir mikro-ekonomi asistanıdır.")
