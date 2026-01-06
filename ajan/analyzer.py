"""
Ajan AI Analyzer Modülü
AI kullanarak gelir fırsatlarını analiz eden modül
"""

from typing import List, Dict
import json
import re
from config import AjanConfig

try:
    if AjanConfig.AI_PROVIDER == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=AjanConfig.GOOGLE_API_KEY)
        client_initialized = True
        
        # Kullanılabilir modelleri listele (ilk çalıştırmada)
        try:
            models = genai.list_models()
            available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            print(f"✓ Kullanılabilir modeller: {available_models[:3]}...")  # İlk 3'ünü göster
        except:
            pass
    elif AjanConfig.AI_PROVIDER == "groq":
        from groq import Groq
        groq_client = Groq(api_key=AjanConfig.GROQ_API_KEY)
        client_initialized = True
    else:
        client_initialized = False
except ImportError as e:
    print(f"⚠ Ajan - AI kütüphanesi yüklenemedi: {e}")
    client_initialized = False

class AjanAnalyzer:
    """Ajan için AI kullanarak fırsatları analiz eden sınıf"""
    
    def __init__(self):
        if not client_initialized:
            raise RuntimeError("AI client başlatılamadı!")
        
        self.provider = AjanConfig.AI_PROVIDER
        
        if self.provider == "gemini":
            # Farklı model adlarını dene (yeni modeller önce)
            model_names = [
                'models/gemini-2.5-flash',      # Yeni model
                'models/gemini-2.5-pro',        # Yeni model
                'models/gemini-2.0-flash-exp',  # Yeni model
                'models/gemini-1.5-flash-latest',  # Latest versiyonu
                'models/gemini-1.5-pro-latest',
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro',
                'models/gemini-pro',     # Eski standart model
                'gemini-pro',           # Eski format
            ]
            
            self.model = None
            last_error = None
            for model_name in model_names:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    # Test için basit bir istek yap
                    test_response = self.model.generate_content("test")
                    print(f"✓ Gemini AI modeli yüklendi: {model_name}")
                    break
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if self.model is None:
                # Kullanılabilir modelleri listele
                try:
                    available_models = genai.list_models()
                    model_list = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
                    print(f"⚠ Kullanılabilir modeller: {model_list[:5]}")
                    
                    # İlk kullanılabilir modeli dene
                    if model_list:
                        try:
                            self.model = genai.GenerativeModel(model_list[0])
                            print(f"✓ İlk kullanılabilir model yüklendi: {model_list[0]}")
                        except:
                            pass
                except:
                    pass
                
                if self.model is None:
                    raise RuntimeError(f"Hiçbir Gemini modeli çalışmıyor. Son hata: {last_error}")
                    
        elif self.provider == "groq":
            self.client = groq_client
            self.model_name = "mixtral-8x7b-32768"
            print("✓ Groq AI modeli yüklendi")
    
    def analyze_opportunity(self, opportunity: Dict) -> Dict:
        """Ajan tek bir fırsatı analiz eder"""
        prompt = f"""Aşağıdaki gelir fırsatını detaylı analiz et ve değerlendir:

BAŞLIK: {opportunity.get('title', 'N/A')}
AÇIKLAMA: {opportunity.get('description', 'N/A')}
ÖDEME: {opportunity.get('payment', 'N/A')}
SÜRE: {opportunity.get('duration', 'N/A')}
ZORLUK: {opportunity.get('difficulty', 'N/A')}
KAYNAK: {opportunity.get('source', 'N/A')}

Lütfen şu kriterleri değerlendir ve JSON formatında yanıt ver:
{{
    "gerçekçilik_skoru": 1-10 arası sayı,
    "zaman_odeme_orani": 1-10 arası sayı,
    "uygunluk_skoru": 1-10 arası sayı,
    "toplam_skor": 1-10 arası sayı,
    "analiz": "Detaylı analiz metni",
    "önerilen_aksiyon": "Kullanıcıya önerilen aksiyon",
    "risk_seviyesi": "Düşük/Orta/Yüksek"
}}"""
        
        try:
            if self.provider == "gemini":
                response = self.model.generate_content(prompt)
                analysis_text = response.text
            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                analysis_text = response.choices[0].message.content
            
            # JSON'u parse et
            analysis_data = self._parse_analysis(analysis_text)
            
            return {
                'opportunity': opportunity,
                'analysis': analysis_data.get('analiz', analysis_text),
                'score': analysis_data.get('toplam_skor', self._extract_score(analysis_text)),
                'realism_score': analysis_data.get('gerçekçilik_skoru', 5),
                'time_payment_ratio': analysis_data.get('zaman_odeme_orani', 5),
                'suitability_score': analysis_data.get('uygunluk_skoru', 5),
                'recommended_action': analysis_data.get('önerilen_aksiyon', 'Değerlendirme yapılamadı'),
                'risk_level': analysis_data.get('risk_seviyesi', 'Orta')
            }
        except Exception as e:
            print(f"⚠ Ajan - Analiz hatası: {str(e)}")
            return {
                'opportunity': opportunity,
                'analysis': 'Analiz yapılamadı',
                'score': 0,
                'realism_score': 0,
                'time_payment_ratio': 0,
                'suitability_score': 0,
                'recommended_action': 'Analiz hatası',
                'risk_level': 'Bilinmiyor'
            }
    
    def _parse_analysis(self, text: str) -> Dict:
        """AI yanıtından JSON verisini parse eder"""
        try:
            # JSON bloğunu bul
            json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except:
            pass
        
        # JSON bulunamazsa, skorları manuel çıkar
        return {
            'toplam_skor': self._extract_score(text),
            'gerçekçilik_skoru': self._extract_number(text, 'gerçekçilik'),
            'zaman_odeme_orani': self._extract_number(text, 'zaman'),
            'uygunluk_skoru': self._extract_number(text, 'uygunluk'),
            'analiz': text,
            'önerilen_aksiyon': 'Manuel değerlendirme gerekli',
            'risk_seviyesi': 'Orta'
        }
    
    def _extract_number(self, text: str, keyword: str) -> float:
        """Metinden belirli bir anahtar kelimeye göre sayı çıkarır"""
        pattern = rf'{keyword}.*?(\d+(?:\.\d+)?)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except:
                pass
        return 5.0
    
    def _extract_score(self, analysis: str) -> float:
        """Analiz metninden genel skor çıkarır"""
        # "toplam_skor" veya "skor" kelimesini ara
        score = self._extract_number(analysis, 'toplam_skor')
        if score == 5.0:
            score = self._extract_number(analysis, 'skor')
        
        # Eğer hala bulunamazsa, genel bir değerlendirme yap
        if score == 5.0:
            analysis_lower = analysis.lower()
            if any(word in analysis_lower for word in ['mükemmel', 'harika', '10', 'yüksek']):
                return 9.0
            elif any(word in analysis_lower for word in ['iyi', '8', '9']):
                return 8.0
            elif any(word in analysis_lower for word in ['orta', '7']):
                return 7.0
            elif any(word in analysis_lower for word in ['düşük', 'kötü', '1', '2', '3']):
                return 3.0
        
        return min(max(score, 0.0), 10.0)  # 0-10 arası sınırla
    
    def analyze_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Ajan birden fazla fırsatı analiz eder ve sıralar"""
        analyzed = []
        total = len(opportunities)
        
        for idx, opp in enumerate(opportunities, 1):
            print(f"  [{idx}/{total}] Analiz ediliyor: {opp.get('title', 'Başlıksız')[:50]}...")
            analyzed.append(self.analyze_opportunity(opp))
        
        # Skora göre sırala
        analyzed.sort(key=lambda x: x['score'], reverse=True)
        return analyzed
    
    def chat(self, message: str, chat_history: List[Dict] = None) -> str:
        """AI ile sohbet için metod"""
        try:
            if self.provider == "gemini":
                if self.model is None:
                    return "Hata: Gemini modeli başlatılamadı. Lütfen API anahtarınızı kontrol edin."
                
                # Chat geçmişi varsa kullan
                if chat_history and len(chat_history) > 0:
                    # Gemini için chat history formatı
                    history = []
                    for msg in chat_history[-10:]:  # Son 10 mesajı al
                        if msg['role'] == 'user':
                            history.append({"role": "user", "parts": [msg['content']]})
                        elif msg['role'] == 'assistant':
                            history.append({"role": "model", "parts": [msg['content']]})
                    
                    # Chat başlat ve mesaj gönder
                    try:
                        chat = self.model.start_chat(history=history)
                        response = chat.send_message(message)
                    except Exception as e:
                        # Chat history hatası varsa, direkt generate dene
                        system_prompt = "Sen Ajan AI'sın, kullanıcılara pasif gelir fırsatları hakkında yardımcı olan bir yapay zeka asistanısın. Türkçe yanıt ver ve samimi bir ton kullan."
                        full_message = f"{system_prompt}\n\nKullanıcı: {message}\n\nAjan:"
                        response = self.model.generate_content(full_message)
                else:
                    # İlk mesaj için direkt generate
                    system_prompt = "Sen Ajan AI'sın, kullanıcılara pasif gelir fırsatları hakkında yardımcı olan bir yapay zeka asistanısın. Türkçe yanıt ver ve samimi bir ton kullan."
                    full_message = f"{system_prompt}\n\nKullanıcı: {message}\n\nAjan:"
                    response = self.model.generate_content(full_message)
                
                return response.text
                
            elif self.provider == "groq":
                messages = [
                    {"role": "system", "content": "Sen Ajan AI'sın, kullanıcılara pasif gelir fırsatları hakkında yardımcı olan bir yapay zeka asistanısın. Türkçe yanıt ver ve samimi bir ton kullan."}
                ]
                
                if chat_history:
                    messages.extend([
                        {"role": msg['role'], "content": msg['content']} 
                        for msg in chat_history[-10:]  # Son 10 mesajı al
                    ])
                
                messages.append({"role": "user", "content": message})
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7
                )
                return response.choices[0].message.content
            else:
                return "AI provider yapılandırılmamış."
                
        except Exception as e:
            return f"Üzgünüm, bir hata oluştu: {str(e)}"