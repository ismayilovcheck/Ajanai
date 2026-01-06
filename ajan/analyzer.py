import google.generativeai as genai
from config import AjanConfig
import json

class AjanAnalyzer:
    def __init__(self):
        # Config'den API anahtarını alıp Gemini'yi başlatıyoruz
        genai.configure(api_key=AjanConfig.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✓ AI Analiz Modülü (Gemini) Hazır.")

    def analyze_opportunities(self, opportunities):
        analyzed_results = []
        
        for opp in opportunities:
            # AI'ya gönderilecek talimat (Prompt)
            prompt = f"""
            Sen uzman bir mikro-ekonomi ve iş analisti yapay zekasın. 
            Aşağıdaki iş fırsatını analiz et ve 10 üzerinden bir skor ver.
            
            İŞ DETAYI:
            Başlık: {opp['title']}
            Ödeme: {opp['payment']}
            Kaynak: {opp['source']}
            
            Lütfen şu formatta yanıt ver (Sadece JSON):
            {{
                "score": 0-10 arası sayı,
                "analysis": "İşin zorluğu ve kazanç oranı hakkında kısa yorum",
                "recommended_action": "Kullanıcı bu işi almak için ne yapmalı?"
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                # AI'dan gelen metni JSON olarak temizle ve işle
                analysis_text = response.text.replace('```json', '').replace('```', '').strip()
                ai_data = json.loads(analysis_text)
                
                analyzed_results.append({
                    "opportunity": opp,
                    "score": ai_data.get("score", 5),
                    "analysis": ai_data.get("analysis", "Analiz yapılamadı"),
                    "recommended_action": ai_data.get("recommended_action", "Harekete geçilmedi")
                })
            except Exception as e:
                print(f"AI Analiz Hatası: {e}")
                # Hata durumunda varsayılan değerler
                analyzed_results.append({
                    "opportunity": opp,
                    "score": 5,
                    "analysis": "Yapay zeka bu ilanı şu an yorumlayamadı.",
                    "recommended_action": "İlanı manuel inceleyin."
                })
                
        return analyzed_results
