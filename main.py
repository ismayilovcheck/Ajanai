import streamlit as st
from config import AjanConfig
from ajan import AjanScraper, AjanAnalyzer
import json
from datetime import datetime
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="AJAN - Mikro Ekonomi", page_icon="🤖")

# --- API ANAHTARI BAĞLANTISI ---
# Streamlit Secrets'tan anahtarı alıyoruz
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("HATA: API Anahtarı bulunamadı. Lütfen Streamlit Secrets ayarlarını yapın.")
# ------------------------------

st.title("🤖 AJAN AI")
st.subheader("Mikro-Ekonomi Yapay Zeka Ajanı")
st.write("Sıfır sermaye ile pasif gelir fırsatlarını analiz eden otonom ajan.")

# Başlatma Butonu
if st.button("Fırsatları Aramaya Başla"):
    with st.status("🔧 Bileşenler başlatılıyor ve internet taranıyor...", expanded=True) as status:
        try:
            ajan_scraper = AjanScraper()
            ajan_analyzer = AjanAnalyzer()
            
            st.write("🌐 İnternet taranıyor (Freelance siteleri, anketler)...")
            opportunities = ajan_scraper.search_all_opportunities()
            
            # Eğer fırsat yoksa demo veriler
            if not opportunities:
                st.warning("Gerçek zamanlı fırsat bulunamadı, demo veriler yükleniyor...")
                opportunities = [
                    {'title': 'Python Web Scraping Projesi', 'payment': '$50 - $100', 'source': 'Freelancer', 'duration': '2 gün', 'difficulty': 'Orta'},
                    {'title': 'Veri Etiketleme Görevi', 'payment': '$20', 'source': 'Amazon MTurk', 'duration': '4 saat', 'difficulty': 'Kolay'}
                ]
            
            st.write(f"✅ {len(opportunities)} fırsat bulundu. Analiz ediliyor...")
            analyzed_opportunities = ajan_analyzer.analyze_opportunities(opportunities[:5])
            status.update(label="Analiz Tamamlandı!", state="complete", expanded=False)

        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")
            st.stop()

    # Sonuçları Ekrana Yazdır
    st.divider()
    st.header("🎯 Analiz Sonuçları")

    for i, result in enumerate(analyzed_opportunities, 1):
        opp = result['opportunity']
        with st.expander(f"{i}. {opp.get('title')}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"💰 **Ödeme:** {opp.get('payment')}")
                st.write(f"📌 **Kaynak:** {opp.get('source')}")
            with col2:
                st.write(f"📊 **Zorluk:** {opp.get('difficulty')}")
                st.write(f"⭐ **Skor:** {result['score']}/10")
            
            st.info(f"💡 **Önerilen Aksiyon:** {result['recommended_action']}")
            st.write(f"📝 **Detaylı Analiz:** {result['analysis']}")

    st.success("🎉 Ajan görevini başarıyla tamamladı!")
