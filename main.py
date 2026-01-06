#!/usr/bin/env python3
"""
Ajan - Mikro-Ekonomi Yapay Zeka Ajanı
Sıfır sermaye ile pasif gelir fırsatlarını bulan ve analiz eden otonom AI ajanı
"""

from config import AjanConfig
from ajan import AjanScraper, AjanAnalyzer
import json
from datetime import datetime

def print_header():
    """Başlık yazdır"""
    print("\n" + "=" * 70)
    print(" " * 20 + "AJAN")
    print(" " * 10 + "Mikro-Ekonomi Yapay Zeka Ajanı")
    print("=" * 70)

def print_separator():
    """Ayırıcı çizgi yazdır"""
    print("-" * 70)

def main():
    """Ajan ana program akışı"""
    print_header()
    
    # Yapılandırmayı doğrula
    try:
        AjanConfig.validate()
    except ValueError as e:
        print(f"\n✗ HATA: {e}")
        print("\nLütfen .env dosyasını kontrol edin ve API anahtarınızı ekleyin.")
        return
    
    print_separator()
    
    # Bileşenleri başlat
    print("\n🔧 Bileşenler başlatılıyor...")
    try:
        ajan_scraper = AjanScraper()
        ajan_analyzer = AjanAnalyzer()
    except Exception as e:
        print(f"\n✗ HATA: Bileşenler başlatılamadı - {str(e)}")
        return
    
    print_separator()
    
    # Fırsatları tara
    print("\n🌐 Ajan interneti tarıyor...")
    print("   (Bu işlem birkaç dakika sürebilir)\n")
    
    opportunities = ajan_scraper.search_all_opportunities()
    
    # Eğer fırsat bulunamazsa demo veri kullan
    if not opportunities:
        print("\n⚠ Ajan hiç fırsat bulamadı.")
        print("   Demo modunda devam ediliyor...\n")
        opportunities = [
            {
                'title': 'Python Web Scraping Projesi',
                'description': 'Bir web sitesinden veri çekme projesi. BeautifulSoup kullanılacak.',
                'payment': '$50 - $100',
                'duration': '2-3 gün',
                'difficulty': 'Orta',
                'source': 'Demo - Freelancer.com',
                'type': 'freelance'
            },
            {
                'title': 'Online Anket - Ürün Değerlendirme',
                'description': 'Yeni bir ürün hakkında 15 dakikalık anket doldurma.',
                'payment': '$5',
                'duration': '15 dakika',
                'difficulty': 'Kolay',
                'source': 'Demo - Swagbucks',
                'type': 'survey'
            },
            {
                'title': 'Veri Etiketleme Görevi',
                'description': '1000 görsel için kategori etiketleme işi.',
                'payment': '$20',
                'duration': '4-5 saat',
                'difficulty': 'Kolay',
                'source': 'Demo - Amazon MTurk',
                'type': 'microtask'
            }
        ]
    
    print(f"\n✓ Ajan {len(opportunities)} fırsat buldu")
    print_separator()
    
    # Fırsatları analiz et
    print("\n🤖 Ajan fırsatları AI ile analiz ediyor...")
    print("   (AI analizi yapılıyor, lütfen bekleyin...)\n")
    
    # İlk 5 fırsatı analiz et (API limitlerini korumak için)
    opportunities_to_analyze = opportunities[:5]
    analyzed_opportunities = ajan_analyzer.analyze_opportunities(opportunities_to_analyze)
    
    print_separator()
    
    # Sonuçları göster
    print("\n" + "=" * 70)
    print(" " * 25 + "AJAN ANALİZ SONUÇLARI")
    print("=" * 70)
    
    for i, result in enumerate(analyzed_opportunities, 1):
        opp = result['opportunity']
        print(f"\n{'='*70}")
        print(f"[{i}] {opp.get('title', 'Başlıksız')}")
        print(f"{'='*70}")
        print(f"📌 Kaynak: {opp.get('source', 'Bilinmiyor')}")
        print(f"💰 Ödeme: {opp.get('payment', 'N/A')}")
        print(f"⏱️  Süre: {opp.get('duration', 'N/A')}")
        print(f"📊 Zorluk: {opp.get('difficulty', 'N/A')}")
        print(f"\n⭐ Toplam Skor: {result['score']:.1f}/10")
        print(f"   • Gerçekçilik: {result['realism_score']:.1f}/10")
        print(f"   • Zaman/Ödeme Oranı: {result['time_payment_ratio']:.1f}/10")
        print(f"   • Uygunluk: {result['suitability_score']:.1f}/10")
        print(f"   • Risk Seviyesi: {result['risk_level']}")
        print(f"\n💡 Önerilen Aksiyon:")
        print(f"   {result['recommended_action']}")
        print(f"\n📝 Detaylı Analiz:")
        analysis_text = result['analysis']
        if len(analysis_text) > 300:
            analysis_text = analysis_text[:300] + "..."
        print(f"   {analysis_text}")
    
    print("\n" + "=" * 70)
    
    # Sonuçları kaydet
    results_data = {
        'timestamp': datetime.now().isoformat(),
        'total_opportunities_found': len(opportunities),
        'analyzed_count': len(analyzed_opportunities),
        'results': analyzed_opportunities
    }
    
    output_file = 'ajan_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Ajan sonuçları '{output_file}' dosyasına kaydetti")
    print(f"✓ Toplam {len(opportunities)} fırsat bulundu, {len(analyzed_opportunities)} tanesi analiz edildi")
    print("\n🎉 Ajan görevini tamamladı!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n✗ Beklenmeyen hata: {str(e)}")