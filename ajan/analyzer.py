import google.generativeai as genai
from config import AjanConfig
import json
import re

class AjanAnalyzer:
    def __init__(self):
        """AI Analiz Modülünü Yapılandırır"""
        if not AjanConfig.GOOGLE_API_KEY:
            print("⚠ HATA: AI için API Anahtarı eksik!")
            return
            
        genai.configure(api_key=AjanConfig.GOOGLE_API_KEY)
        # Hızlı ve etkili analiz için flash modelini kullanıyoruz
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✓ AJAN Beyni (Gemini 1.5 Flash) Aktif.")

    def _extract_json(self, text: str) -> dict:
        """AI yanıtından JSON kısmını ayıklar ve temizler"""
        try:
            # Markdown içindeki JSON bloklarını temizle
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(text)
        except Exception:
            return None

    def analyze_opportunities(self, opportunities):
        """Fırsatları tek tek AI süzgecinden geçirir"""
        analyzed_results = []
        
        if not opportunities:
            return analyzed_results

        for opp in opportunities:
            # AI için özel talimat seti (Prompt Engineering)
            prompt = f"""
            Sen profesyonel bir serbest zamanlı (freelance) iş ve mikro-ekonomi analistisin. 
            Aşağıdaki iş fırsatını piyasa koşullarına göre değerlendir. 

            İŞ BİLGİLERİ:
            - Başlık: {opp.get('title')}
            - Ödeme: {opp.get('payment')}
            - Kaynak: {opp.get('source')}
            
            GÖREVİN:
            Bu işin zorluk derecesini, ödemenin adilliğini ve harcanacak zamana değip değmeyeceğini analiz et. 
            Azerbaycan ve global piyasa dengelerini gözet.

            YANIT FORMATI (Yalnızca JSON döndür):
            {{
                "score": 1-10 arası puan,
                "analysis": "İşin avantaj ve dezavantajları hakkında samimi yorum",
                "recommended_action": "Kullanıcı bu işi almak için ne yapmalı? (Örn: Hemen yaz, pazarlık yap, pas geç)"
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                ai_data = self._extract_json(response.text)
                
                if ai_data:
                    analyzed_results.append({
                        "opportunity": opp,
                        "score": ai_data.get("score", 5),
                        "analysis": ai_data.get("analysis", "Analiz verisi oluşturulamadı."),
                        "recommended_action": ai_data.get("recommended_action", "Manuel inceleme önerilir.")
                    })
                else:
                    raise ValueError("JSON ayıklanamadı")
                    
            except Exception as e:
                print(f"AI Analiz Hatası ({opp.get('title')}): {e}")
                # Hata durumunda güvenli varsayılan değerler
                analyzed_results.append({
                    "opportunity": opp,
                    "score": 5,
                    "analysis": "Yapay zeka bu ilanı analiz ederken teknik bir sorun yaşadı.",
                    "recommended_action": "İlanı doğrudan kaynağında inceleyin."
                })
                
        return analyzed_results
