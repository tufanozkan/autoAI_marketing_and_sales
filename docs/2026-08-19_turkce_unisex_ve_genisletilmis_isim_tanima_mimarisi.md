# 2026-08-19 Türkçe Unisex ve Kapsamlı İsim Tanıma (NER) Mimarisi

## 1. Genel Bakış ve İhtiyaç
Türkçe'de `Deniz`, `Derya`, `Ege`, `Özgür`, `Utku`, `Yağmur`, `Görkem`, `İlkay`, `Işık`, `Bilge`, `Güneş`, `Devrim`, `Umut`, `Evren`, `Sefa`, `Aytaç`, `Eren`, `Toprak`, `Rüzgar` gibi yüzlerce isim **çift cinsiyetli (unisex)** olarak hem kadınlar hem de erkekler tarafından kullanılmaktadır.

Yapay zeka asistanının unisex isimlerde doğrudan tek bir cinsiyeti varsayması yerine; müşteriye kibarca hitap tercihini sorması (`Deniz Bey mi yoksa Deniz Hanım mı?`) ve gelen tercihe göre tüm sohbet boyunca bu hitabı kalıcı hafızada sürdürmesi sağlanmıştır.

## 2. Geliştirilen Katmanlar

1. **3 Seviyeli İsim Veri Tabanı:**
   * `UNISEX_NAMES`: Çift cinsiyetli isimler havuzu.
   * `FEMALE_NAMES`: 500+ saf kadın ismi.
   * `MALE_NAMES`: 700+ saf erkek ismi.
2. **Hitap Belirleme Motoru (`_get_honorific_info`):**
   * Kullanıcı ismi `UNISEX_NAMES` içinde yer alıyorsa ve henüz `"Bey"` veya `"Hanım"` tercihi yapmamışsa, sistem `is_unisex_pending = True` olarak işaretler.
   * İlk karşılama yanıtında: *"Size nasıl hitap etmemi arzu edersiniz; **Deniz Bey** mi yoksa **Deniz Hanım** mı? 😊"* sorusu iletilir.
   * Müşteri bir sonraki mesajında *"Deniz Bey"* veya *"Bey"* / *"Hanım"* dediğinde sistem bunu anında algılar, `CustomerLead` kaydını günceller ve *"Memnuniyetle Deniz Bey! Notumu aldım. ✨"* şeklinde teyit eder.
3. **Kapsamlı Stopwords & Kara Liste:**
   * `"telefon"`, `"telefonumu"`, `"numara"`, `"numaramı"`, `"vermek"`, `"istemiyorum"` gibi kelimeler isim çıkarımından tamamen izole edilmiştir.

## 3. Test ve Doğrulama

Eklenen `test_unisex_flow_deniz` birim testi ile birlikte toplam **19/19 test** başarıyla geçmiştir.
