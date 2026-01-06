import warnings
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")

 
"""
Ajan - Profesyonel Streamlit Web Arayüzü
Modern, kullanıcı dostu ve profesyonel tasarım
"""

import streamlit as st
from config import AjanConfig
from ajan import AjanScraper, AjanAnalyzer
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(
    page_title="Ajan AI - Mikro-Ekonomi Yapay Zeka Ajanı",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS
st.markdown("""
<style>
    /* Ana stil */
    .main {
        padding: 2rem;
    }
    
    /* Başlık stili */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Metrik kartları */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Buton stili */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander stili */
    .streamlit-expanderHeader {
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Sidebar stili */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info box */
    .stInfo {
        background-color: #e0e7ff;
        border-left: 4px solid #667eea;
    }
    
    /* Success box */
    .stSuccess {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
    }
    
    /* Error box */
    .stError {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown('<h1 class="main-title">🤖 Ajan AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Mikro-Ekonomi Yapay Zeka Ajanı | Pasif Gelir Fırsatları Bulucu</p>', unsafe_allow_html=True)

# Sidebar - Profesyonel Ayarlar Paneli
with st.sidebar:
    st.markdown("### ⚙️ Kontrol Paneli")
    st.markdown("---")
    
    # API Provider seçimi
    provider = st.selectbox(
        "🤖 AI Provider",
        ["gemini", "groq"],
        index=0,
        help="Kullanılacak AI modelini seçin"
    )
    
    # Analiz edilecek fırsat sayısı
    max_opportunities = st.slider(
        "📊 Analiz Edilecek Fırsat Sayısı",
        min_value=1,
        max_value=10,
        value=5,
        help="AI ile analiz edilecek maksimum fırsat sayısı"
    )
    
    st.markdown("---")
    
    # Platform seçimi
    st.markdown("### 🌐 Platform Filtreleri")
    freelance_enabled = st.checkbox("💼 Freelance Siteleri", value=True)
    survey_enabled = st.checkbox("📋 Anket Platformları", value=True)
    microtask_enabled = st.checkbox("🔧 Mikro Görev Siteleri", value=True)
    
    st.markdown("---")
    
    # İstatistikler
    if 'results' in st.session_state:
        st.markdown("### 📈 Son İstatistikler")
        st.metric("Bulunan Fırsat", st.session_state.get('total_found', 0))
        st.metric("Analiz Edilen", len(st.session_state.get('results', [])))
        avg_score = sum([r['score'] for r in st.session_state.get('results', [])]) / len(st.session_state.get('results', [])) if st.session_state.get('results') else 0
        st.metric("Ortalama Skor", f"{avg_score:.1f}/10")
    
    st.markdown("---")
    st.info("💡 **İpucu:** API anahtarınızı `.env` dosyasına eklemeyi unutmayın!")
    
    # Footer
    st.markdown("---")
    st.markdown("### 📧 Destek")
    st.markdown("Sorularınız için GitHub'da issue açabilirsiniz.")

# Ana içerik - Tab'lar
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Ana Sayfa", "🔍 Fırsat Ara", "📊 Dashboard", "💬 AI Chat", "ℹ️ Hakkında"])

# Tab 1: Ana Sayfa
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🌐 Otonom Tarama</h3>
            <p>İnterneti otomatik olarak tarar ve fırsatları toplar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 AI Analiz</h3>
            <p>Google Gemini ile akıllı analiz ve değerlendirme</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>⭐ Skorlama</h3>
            <p>Her fırsatı 1-10 arası profesyonel skorlama</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hızlı başlat butonu
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        st.info("👆 **Fırsat Ara** sekmesine geçerek aramaya başlayabilirsiniz!")
    
    st.markdown("---")
    
    # Son sonuçlar (eğer varsa)
    if 'results' in st.session_state and st.session_state['results']:
        st.markdown("### 📋 Son Analiz Sonuçları")
        results = st.session_state['results'][:3]  # İlk 3'ü göster
        
        for idx, result in enumerate(results, 1):
            opp = result['opportunity']
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{idx}. {opp.get('title', 'Başlıksız')}**")
                st.caption(f"📌 {opp.get('source', 'Bilinmiyor')} | 💰 {opp.get('payment', 'N/A')}")
            
            with col2:
                score_color = "🟢" if result['score'] >= 7 else "🟡" if result['score'] >= 5 else "🔴"
                st.markdown(f"### {score_color} {result['score']:.1f}/10")

# Tab 2: Fırsat Ara
with tab2:
    st.header("🔍 Gelir Fırsatlarını Ara ve Analiz Et")
    st.markdown("Ajan, belirlediğiniz platformları tarayarak en iyi gelir fırsatlarını bulur ve AI ile analiz eder.")
    st.markdown("---")
    
    # Başlat butonu
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_button = st.button("🚀 Ajan'ı Başlat", type="primary", use_container_width=True)
    
    if start_button:
        try:
            # Yapılandırmayı doğrula
            AjanConfig.validate()
            
            # Progress container
            progress_container = st.container()
            with progress_container:
                st.markdown("### ⏳ İşlem Durumu")
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_details = st.empty()
                
                # Bileşenleri başlat
                status_text.markdown("**🔧 Bileşenler başlatılıyor...**")
                status_details.text("Web scraper ve AI analyzer hazırlanıyor...")
                progress_bar.progress(10)
                
                ajan_scraper = AjanScraper()
                progress_bar.progress(30)
                
                ajan_analyzer = AjanAnalyzer()
                progress_bar.progress(50)
                
                # Fırsatları tara
                status_text.markdown("**🌐 İnternet taranıyor...**")
                status_details.text("Belirlenen platformlar taranıyor, lütfen bekleyin...")
                progress_bar.progress(60)
                
                opportunities = ajan_scraper.search_all_opportunities()
                
                # Demo veri (eğer fırsat yoksa)
                if not opportunities:
                    status_details.warning("Hiç fırsat bulunamadı, demo modunda devam ediliyor...")
                    opportunities = [
                        {
                            'title': 'Python Web Scraping Projesi',
                            'description': 'Bir web sitesinden veri çekme projesi. BeautifulSoup ve Python kullanılacak. Deneyimli geliştirici aranıyor.',
                            'payment': '$50 - $100',
                            'duration': '2-3 gün',
                            'difficulty': 'Orta',
                            'source': 'Demo - Freelancer.com',
                            'type': 'freelance'
                        },
                        {
                            'title': 'Online Anket - Ürün Değerlendirme',
                            'description': 'Yeni bir ürün hakkında 15 dakikalık anket doldurma. Basit ve hızlı.',
                            'payment': '$5',
                            'duration': '15 dakika',
                            'difficulty': 'Kolay',
                            'source': 'Demo - Swagbucks',
                            'type': 'survey'
                        },
                        {
                            'title': 'Veri Etiketleme Görevi',
                            'description': '1000 görsel için kategori etiketleme işi. Tekrarlayan görev.',
                            'payment': '$20',
                            'duration': '4-5 saat',
                            'difficulty': 'Kolay',
                            'source': 'Demo - Amazon MTurk',
                            'type': 'microtask'
                        },
                        {
                            'title': 'İçerik Yazarlığı - Blog Yazısı',
                            'description': 'Teknoloji konulu 1000 kelimelik blog yazısı yazılacak.',
                            'payment': '$30',
                            'duration': '1 gün',
                            'difficulty': 'Orta',
                            'source': 'Demo - Upwork',
                            'type': 'freelance'
                        },
                        {
                            'title': 'Çeviri İşi - İngilizce-Türkçe',
                            'description': '500 kelimelik teknik doküman çevirisi.',
                            'payment': '$25',
                            'duration': '2 saat',
                            'difficulty': 'Kolay',
                            'source': 'Demo - Fiverr',
                            'type': 'freelance'
                        }
                    ]
                
                progress_bar.progress(70)
                
                # Fırsatları analiz et
                status_text.markdown("**🤖 AI analizi yapılıyor...**")
                status_details.text(f"{min(max_opportunities, len(opportunities))} fırsat AI ile analiz ediliyor...")
                opportunities_to_analyze = opportunities[:max_opportunities]
                analyzed_opportunities = ajan_analyzer.analyze_opportunities(opportunities_to_analyze)
                
                progress_bar.progress(100)
                status_text.markdown("**✅ Tamamlandı!**")
                status_details.empty()
                
                # Sonuçları session state'e kaydet
                st.session_state['results'] = analyzed_opportunities
                st.session_state['total_found'] = len(opportunities)
                st.session_state['last_search'] = datetime.now()
                
                # Başarı mesajı
                st.success(f"🎉 **Başarılı!** {len(opportunities)} fırsat bulundu, {len(analyzed_opportunities)} tanesi analiz edildi!")
                st.balloons()
                
                # Dashboard'a yönlendir
                st.info("📊 Detaylı sonuçlar için 'Dashboard' sekmesine geçin!")
                
        except ValueError as e:
            st.error(f"❌ **Yapılandırma Hatası:** {str(e)}")
            st.info("💡 Lütfen `.env` dosyasında API anahtarınızın olduğundan emin olun.")
        except Exception as e:
            st.error(f"❌ **Hata:** {str(e)}")
            st.exception(e)

# Tab 3: Dashboard
with tab3:
    st.header("📊 Analiz Dashboard'u")
    
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        total = st.session_state.get('total_found', len(results))
        
        # Üst metrikler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Toplam Fırsat", total, delta=f"{len(results)} analiz edildi")
        
        with col2:
            avg_score = sum([r['score'] for r in results]) / len(results) if results else 0
            st.metric("⭐ Ortalama Skor", f"{avg_score:.1f}/10", delta=f"{'Yüksek' if avg_score >= 7 else 'Orta' if avg_score >= 5 else 'Düşük'}")
        
        with col3:
            high_score_count = len([r for r in results if r['score'] >= 7])
            st.metric("🎯 Yüksek Skorlu", high_score_count, delta=f"{len(results)} içinden")
        
        with col4:
            if st.session_state.get('last_search'):
                last_search = st.session_state['last_search']
                st.metric("🕒 Son Arama", last_search.strftime("%H:%M"), delta="Bugün")
        
        st.markdown("---")
        
        # Grafikler
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Skor dağılımı
            scores = [r['score'] for r in results]
            fig_scores = px.histogram(
                x=scores,
                nbins=10,
                title="Skor Dağılımı",
                labels={'x': 'Skor', 'y': 'Fırsat Sayısı'},
                color_discrete_sequence=['#667eea']
            )
            fig_scores.update_layout(showlegend=False)
            st.plotly_chart(fig_scores, use_container_width=True)
        
        with col_chart2:
            # Kategori dağılımı
            categories = {}
            for r in results:
                cat = r['opportunity'].get('type', 'diğer')
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                fig_cat = px.pie(
                    values=list(categories.values()),
                    names=list(categories.keys()),
                    title="Kategori Dağılımı",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_cat, use_container_width=True)
        
        st.markdown("---")
        
        # Detaylı sonuçlar
        st.markdown("### 📋 Detaylı Analiz Sonuçları")
        
        # Filtreleme
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            min_score = st.slider("Minimum Skor", 0.0, 10.0, 0.0, 0.5)
        with col_filter2:
            sort_by = st.selectbox("Sıralama", ["Skor (Yüksekten Düşüğe)", "Skor (Düşükten Yükseğe)", "Ödeme"])
        
        # Filtrele ve sırala
        filtered_results = [r for r in results if r['score'] >= min_score]
        
        if sort_by == "Skor (Düşükten Yükseğe)":
            filtered_results.sort(key=lambda x: x['score'])
        elif sort_by == "Ödeme":
            # Ödeme miktarını parse etmeye çalış
            def get_payment_value(opp):
                payment = opp.get('payment', '$0')
                try:
                    # $50 - $100 formatından sayı çıkar
                    numbers = [float(s.replace('$', '').strip()) for s in payment.split('-') if '$' in s]
                    return max(numbers) if numbers else 0
                except:
                    return 0
            filtered_results.sort(key=lambda x: get_payment_value(x['opportunity']), reverse=True)
        
        # Sonuçları göster
        for idx, result in enumerate(filtered_results, 1):
            opp = result['opportunity']
            
            # Skor rengi
            score = result['score']
            if score >= 7:
                score_emoji = "🟢"
                score_color = "#10b981"
            elif score >= 5:
                score_emoji = "🟡"
                score_color = "#f59e0b"
            else:
                score_emoji = "🔴"
                score_color = "#ef4444"
            
            with st.expander(
                f"{score_emoji} **#{idx} {opp.get('title', 'Başlıksız')}** - Skor: **{score:.1f}/10**",
                expanded=(idx == 1 and len(filtered_results) <= 3)
            ):
                # Üst metrikler
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💰 Ödeme", opp.get('payment', 'N/A'))
                
                with col2:
                    st.metric("⏱️ Süre", opp.get('duration', 'N/A'))
                
                with col3:
                    st.metric("📊 Zorluk", opp.get('difficulty', 'N/A'))
                
                with col4:
                    st.markdown(f'<h3 style="color: {score_color};">⭐ {score:.1f}/10</h3>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Detaylı bilgiler
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.markdown("#### 📌 Genel Bilgiler")
                    st.write(f"**Kaynak:** {opp.get('source', 'Bilinmiyor')}")
                    st.write(f"**Açıklama:** {opp.get('description', 'N/A')}")
                
                with col_info2:
                    st.markdown("#### 📊 Analiz Detayları")
                    st.write(f"**Gerçekçilik:** {result['realism_score']:.1f}/10")
                    st.write(f"**Zaman/Ödeme Oranı:** {result['time_payment_ratio']:.1f}/10")
                    st.write(f"**Uygunluk:** {result['suitability_score']:.1f}/10")
                    st.write(f"**Risk Seviyesi:** {result['risk_level']}")
                
                st.markdown("---")
                
                # Önerilen aksiyon
                st.markdown("#### 💡 Önerilen Aksiyon")
                st.success(result['recommended_action'])
                
                # Detaylı analiz
                st.markdown("#### 📝 AI Analiz Raporu")
                st.info(result['analysis'])
        
        # JSON indirme
        st.markdown("---")
        col_download1, col_download2, col_download3 = st.columns([1, 2, 1])
        with col_download2:
            results_json = json.dumps({
                'timestamp': datetime.now().isoformat(),
                'total_opportunities_found': total,
                'analyzed_count': len(results),
                'results': results
            }, ensure_ascii=False, indent=2)
            
            st.download_button(
                label="📥 Sonuçları JSON olarak indir",
                data=results_json,
                file_name=f"ajan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    else:
        st.info("👆 Önce 'Fırsat Ara' sekmesinden arama yapın!")
        st.markdown("""
        ### 📊 Dashboard Özellikleri
        
        - **İstatistikler**: Toplam fırsat, ortalama skor, yüksek skorlu fırsatlar
        - **Grafikler**: Skor dağılımı ve kategori analizi
        - **Filtreleme**: Skor ve sıralama seçenekleri
        - **Detaylı Raporlar**: Her fırsat için AI analiz raporu
        - **İndirme**: Sonuçları JSON formatında indirme
        """)

# Tab 4: AI Chat
with tab4:
    st.header("💬 AI ile Konuş")
    st.markdown("Ajan AI ile sohbet edin, sorular sorun ve tavsiyeler alın!")
    st.markdown("---")
    
    # Chat geçmişini session state'te sakla
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat geçmişini göster
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])
    
    # Kullanıcı mesajı için input
    user_input = st.chat_input("Ajan'a bir şey sorun...")
    
    if user_input:
        # Kullanıcı mesajını ekle
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # AI yanıtını al
        try:
            # AI analyzer'ı kullan
            if 'chat_analyzer' not in st.session_state:
                AjanConfig.validate()
                st.session_state.chat_analyzer = AjanAnalyzer()
            
            analyzer = st.session_state.chat_analyzer
            
            # AI'ya soru sor
            with st.spinner("🤖 Ajan düşünüyor..."):
                # Chat geçmişini hazırla (son mesaj hariç)
                chat_history = st.session_state.chat_history[:-1] if st.session_state.chat_history else []
                
                ai_response = analyzer.chat(user_input, chat_history)
            
            # AI yanıtını ekle
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': ai_response
            })
            
            # Sayfayı yenile
            st.rerun()
            
        except ValueError as e:
            st.error(f"❌ **Yapılandırma Hatası:** {str(e)}")
            st.info("💡 Lütfen `.env` dosyasında API anahtarınızın olduğundan emin olun.")
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"Yapılandırma hatası: {str(e)}"
            })
            st.rerun()
        except Exception as e:
            st.error(f"❌ **Hata:** {str(e)}")
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"Üzgünüm, bir hata oluştu: {str(e)}"
            })
            st.rerun()
    
    # Chat'i temizle butonu
    if st.session_state.chat_history:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    
    # Yardımcı bilgiler
    st.markdown("---")
    with st.expander("💡 Örnek Sorular"):
        st.markdown("""
        - Pasif gelir fırsatları nelerdir?
        - Freelance işlerde nelere dikkat etmeliyim?
        - Hangi platformlar daha güvenilir?
        - Mikro görevlerden nasıl para kazanabilirim?
        - Anket siteleri güvenilir mi?
        - En iyi pasif gelir yöntemleri nelerdir?
        """)

# Tab 5: Hakkında
with tab5:
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.header("🤖 Ajan AI Hakkında")
        st.markdown("""
        ### 🎯 Misyonumuz
        
        Ajan, sıfır sermaye ile pasif gelir fırsatlarını bulan ve analiz eden otonom bir yapay zeka ajanıdır. 
        Kullanıcılarımıza en iyi gelir fırsatlarını sunmak için AI teknolojisini kullanıyoruz.
        
        ### ✨ Özellikler
        
        - 🌐 **Otonom Web Tarama**: İnterneti otomatik olarak tarar ve fırsatları toplar
        - 🤖 **AI Destekli Analiz**: Google Gemini ile akıllı analiz ve değerlendirme
        - 📊 **Çoklu Platform**: Freelance, anket ve mikro görev sitelerini destekler
        - ⭐ **Profesyonel Skorlama**: Her fırsatı 1-10 arası detaylı skorlar
        - ⚠️ **Risk Değerlendirmesi**: Her fırsat için risk analizi yapar
        - 📈 **Dashboard**: Görsel analiz ve raporlama
        
        ### 🚀 Nasıl Çalışır?
        
        1. **Tarama**: Belirlenen platformları otomatik olarak tarar
        2. **Toplama**: Bulunan fırsatları toplar ve kategorize eder
        3. **Analiz**: AI ile her fırsatı detaylı analiz eder
        4. **Sıralama**: Skorlarına göre en iyiden en kötüye sıralar
        5. **Raporlama**: Kullanıcıya detaylı rapor ve öneriler sunar
        
        ### 🔑 API Anahtarları
        
        - **Google Gemini**: [API Anahtarı Al](https://makersuite.google.com/app/apikey)
        - **Groq**: [API Anahtarı Al](https://console.groq.com/keys)
        
        ### ⚠️ Önemli Notlar
        
        - API anahtarınızı `.env` dosyasına eklemeyi unutmayın
        - Web scraping için bazı siteler erişimi engelleyebilir (403 hatası normal)
        - Her sitenin kullanım şartlarını kontrol edin
        - Rate limiting için istekler arasında bekleme süreleri var
        
        ### 🛠️ Teknolojiler
        
        - **Python 3.8+**
        - **Streamlit** - Web arayüzü
        - **Google Gemini AI** - Yapay zeka analizi
        - **BeautifulSoup** - Web scraping
        - **Plotly** - Veri görselleştirme
        """)
    
    with col_about2:
        st.markdown("### 📊 İstatistikler")
        if 'results' in st.session_state:
            st.metric("Toplam Arama", "1" if st.session_state.get('results') else "0")
            st.metric("Bulunan Fırsat", st.session_state.get('total_found', 0))
        else:
            st.info("Henüz arama yapılmadı")
        
        st.markdown("---")
        st.markdown("### 🔗 Bağlantılar")
        st.markdown("""
        - [GitHub Repository](https://github.com)
        - [Dokümantasyon](#)
        - [Destek](#)
        """)
        
        st.markdown("---")
        st.markdown("### 📧 İletişim")
        st.markdown("Sorularınız için GitHub'da issue açabilirsiniz.")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col2:
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p>Made with ❤️ by <strong>Ajan Team</strong></p>
        <p style="font-size: 0.9rem;">© 2024 Ajan AI. Tüm hakları saklıdır.</p>
    </div>
    """, unsafe_allow_html=True)