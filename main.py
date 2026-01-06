import google.generativeai as genai
from config import AjanConfig
import json

class AjanAnalyzer:
    def __init__(self):
        # Gemini API yapılandırması
        genai.configure(api_key=AjanConfig.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✓ AJAN Beyni (Gemini) başarıyla bağlandı.")

    def analyze_opportunities(self, opportunities):
        """Fırsatları AI süzgecinden geçirir"""
        analyzed_results = []
        
        for opp in opportunities:
            # AI'ya verilen talimat (Prompt)
            prompt = f"""
            Sen profesyonel bir finans ve iş analistisin. 
            Aşağıdaki iş fırsatını analiz et. Ödeme miktarı AZN (Manat) veya USD olabilir.
            
            İŞ DETAYLARI:
            Başlık: {opp.get('title')}
            Ödeme: {opp.get('payment')}
            Kaynak: {opp.get('source')}
            
            Lütfen yanıtını şu JSON formatında ver:
            {{
                "score": 1-10 arası sayı,
                "analysis": "İşin avantaj ve dezavantajlarını anlatan 1-2 cümlelik yorum.",
                "recommended_action": "Kullanıcı bu fırsatla ilgili tam olarak ne yapmalı?"
            }}
            """
            
            try:
                # AI yanıt üretiyor
                response = self.model.generate_content(prompt)
                # JSON metnini temizle (AI bazen Markdown ekler)
                clean_json = response.text.replace('```json', '').replace('```', '').strip()
                ai_data = json.loads(clean_json)
                
                analyzed_results.append({
                    "opportunity": opp,
                    "score": ai_data.get("score", 5),
                    "analysis": ai_data.get("analysis", "Analiz verisi alınamadı."),
                    "recommended_action": ai_data.get("recommended_action", "Aksiyon önerisi yok.")
                })
            except Exception as e:
                print(f"AI Hatası: {str(e)}")
                # Hata durumunda boş dönmemesi için varsayılan değer
                analyzed_results.append({
                    "opportunity": opp,
                    "score": 0,
                    "analysis": "Yapay zeka bu fırsatı şu an yorumlayamadı.",
                    "recommended_action": "İlanı manuel kontrol edin."
                })
                
        return analyzed_results
