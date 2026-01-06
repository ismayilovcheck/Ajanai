import google.generativeai as genai
from config import AjanConfig
import json
import re

class AjanAnalyzer:
    def __init__(self):
        """AJAN Beyni - Gemini Yapılandırması"""
        if not AjanConfig.GOOGLE_API_KEY:
            print("⚠ API Anahtarı eksik! Analiz yapılamayacak.")
            return
            
        genai.configure(api_key=AjanConfig.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✓ AJAN Beyni (Gemini) Azerbaycan yerel pazarı için optimize edildi.")

    def _clean_json_response(self, text):
        """AI yanıtındaki gereksiz metinleri temizler ve saf JSON'u bulur"""
        try:
            # Regex ile süslü parantezler arasını çek (JSON bloğunu bulur)
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except Exception as e:
            print(f"JSON Ayrıştırma Hatası: {e}")
            return None

    def analyze_opportunities(self, opportunities):
        """Fırsatları AI süzgecinden geçirir ve strateji üretir"""
        analyzed_results = []
        
        for opp in opportunities:
            # Geliştirilmiş Prompt: Yerel uzman kimliği eklendi
            prompt = f"""
            Sen Azerbaycan ve küresel iş piyasası konusunda uzman bir analistsin. 
            Aşağıdaki iş ilanını değerlendir. Ödeme Manat (AZN) ise yerel yaşam maliyetine göre, 
            Dolar (USD) ise küresel standartlara göre yorumla.

            İŞ BİLGİSİ:
            Başlık: {opp.get('title')}
            Ödeme: {opp.get('payment')}
            Kaynak: {opp.get('source')}

            GÖREV: Bu işin zaman/kazanç dengesini analiz et. 
            Yanıtı SADECE aşağıdaki JSON formatında ver:
            {{
                "score": 1-10 arası puan,
                "analysis": "İşin avantaj ve dezavantajlarını anlatan kısa, samimi bir yorum.",
                "recommended_action": "Kullanıcıya net bir tavsiye (Örn: 'Hemen ara', 'Pazarlık yap', 'Uzak dur')"
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                ai_data = self._clean_json_response(response.text)
                
                if ai_data:
                    analyzed_results.append({
                        "opportunity": opp,
                        "score": ai_data.get("score", 5),
                        "analysis": ai_data.get("analysis", "Analiz verisi alınamadı."),
                        "recommended_action": ai_data.get("recommended_action", "Aksiyon önerisi yok.")
                    })
                else:
                    raise ValueError("JSON verisi okunamadı.")

            except Exception as e:
                print(f"AI Hatası ({opp.get('title')}): {str(e)}")
                analyzed_results.append({
                    "opportunity": opp,
                    "score": 0,
                    "analysis": "Yapay zeka bu ilanı şu an analiz edemedi.",
                    "recommended_action": "İlanı manuel inceleyin."
                })
                
        return analyzed_results
