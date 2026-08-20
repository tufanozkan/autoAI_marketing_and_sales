# 2026-08-20: AI Chatbot "Teşekkür Ederim" Nezaket Kapanışı & Sayfa Filtresi Temizliği

**Tarih:** 2026-08-20  
**Yazar:** Antigravity AI  
**Kapsam:** AI Chatbot yanıtlarındaki "Sayfayı filtreledim" ibarelerinin ve otomatik sayfa filtre tetikleyicilerinin kaldırılması; kullanıcının "teşekkür ederim", "sağolun", "iyi günler" gibi nezaket ifadelerine karşı sohbeti baştan başlatmak yerine doğal ve kibar bir kapanış mesajı ile yanıt vermesinin sağlanması.

---

## 1. Tespit Edilen Problemler

1. **İstenmeyen "Sayfayı Filtreledim" İfadesi:**
   - Kullanıcı "1.5M TL altı araçlar" sorduğunda chatbot doğrudan araçları mesaj içinde sunmak yerine "👉 Sayfayı filtreledim." yazıyordu ve sayfa vitrinini istem dışı manipüle etmeye çalışıyordu.
   - Sayfa filtrelemesi yalnızca kullanıcının arayüzdeki butonları ve filtre çubuğunu manuel kullanmasıyla yönetilmeli; chatbot ise danışman olarak araçları mesaj penceresinde sunmalıdır.

2. **"Teşekkür Ederim" Sonrası Robotik Yeniden Başlama Hatası:**
   - Kullanıcı görüşme sonunda "teşekkür ederim" veya "sağol" yazdığında NLU intent'i boş kaldığı için bot fallback'e düşüyor ve hafızayı unutup "Merhaba Tugce Hanım! Size nasıl yardımcı olabilirim? Arkas Spoticar portföyümüzdeki araçlarımızın donanım, ekspertiz..." şeklinde baştan başlıyordu.

---

## 2. Yapılan Geliştirmeler

### A. NLU ve Intent Genişletmesi (`GRATITUDE`)
* [`backend/agent/chatbot/nlu.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/backend/agent/chatbot/nlu.py) içerisine `GRATITUDE` intent'i eklendi:
  - Tanınan kalıplar: *"teşekkür ederim"*, *"teşekkürler"*, *"çok teşekkürler"*, *"sağol"*, *"sağolun"*, *"eline sağlık"*, *"harikasın"*, *"süper"*, *"eyvallah"*, *"iyi günler"*, *"hoşça kal"*, *"görüşmek üzere"*, *"kolay gelsin"* vb.

### B. Nezaket ve Doğal Kapanış Akışı (`GRATITUDE` Handler)
* [`backend/agent/chatbot/planner.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/backend/agent/chatbot/planner.py) içerisine nezaket kapanış dalı eklendi:
  - Kullanıcı teşekkür ettiğinde bot: *"Rica ederim {İsim Hanım/Bey}! Yardımcı olabildiysem ne mutlu bana. 😊 Arkas Spoticar araçlarımız veya ekspertiz detaylarımızla ilgili aklınıza takılan bir konu olursa dilediğiniz zaman sorabilirsiniz. Keyifli ve güvenli sürüşler dilerim! 🚗✨"* diyerek doğal bir kapanış yapar.

### C. Sayfa Filtreleme İfadelerinin ve Otomatik Tetikleyicilerin Temizlenmesi
* `planner.py` içerisindeki tüm "👉 Sayfayı filtreledim.", "sayfayı yeniledim" metinleri kaldırıldı; bot kriterlere uyan araçları listeleyip doğrudan soru-cevap formatında sunacak şekilde sadeleştirildi.
* [`frontend/src/components/chat/ChatbotWidget.tsx`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/frontend/src/components/chat/ChatbotWidget.tsx) bileşeninden arama mesajlarında sayfayı zorunlu filtreleme tetikleyicisi kaldırıldı; sayfa filtreleme tamamen kullanıcının vitrindeki filtre araçlarına bırakıldı.

---

## 3. Doğrulama ve Testler
* [`tests/test_gratitude_and_chat_flow.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/tests/test_gratitude_and_chat_flow.py) yazılarak kullanıcının bildirdiği tam konuşma senaryosu (Tanışma -> Bütçe -> Donanım -> Teşekkürler) test edildi.
* 74 birim ve entegrasyon testinin tamamı başarıyla geçti (`74/74 OK`).
