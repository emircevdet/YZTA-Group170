# EhliyetGO
## Logo
<img width="680" alt="image" src="https://github.com/user-attachments/assets/16d835f5-debd-4885-bef0-10a3759ca36f" />

## Takım

| İsim                 | Rol              |
|----------------------|------------------|
| Şevval Battal        | Scrum Master     |
| Yaren Doğan          | Developer        |
| Kaan Parmak          | Product Owner    |
| Emir Cevdet Ünsal    | Developer        |
| Barış Ozan           | Developer        |


---

Yapay zeka destekli bu masaüstü uygulaması, ehliyet teorik sınavına hazırlanan bireyler için kişiselleştirilmiş, verimli ve etkileşimli bir öğrenme deneyimi sunar.  
Konu anlatımı, test çözümü, sınav simülasyonu ve yapay zeka destekli geri bildirimlerle kullanıcıyı sınava eksiksiz şekilde hazırlar.

---

## Amaç

Bu projenin amacı, ehliyet teorik sınavına hazırlanan bireylerin öğrenme sürecini daha kolay, daha etkili ve daha kişisel hale getirmektir.

- Klasik ezber yöntemlerini modernleştirir  
- Kişiye özel çalışma planı ve yapay zeka açıklamaları sunar  
- Kullanıcının eksik konularını analiz ederek hedefli tekrar sağlar  
- Sınav stresine karşı gerçek sınav formatında denemeler yapar  

---

## Hedef Kitle

- İlk kez ehliyet alacak bireyler (18+)
- Yoğun çalışan yetişkinler
- Mobil öğrenmeye alışık kullanıcılar
- Sürücü kursları (B2B modeli için)

---

## Özellikler

- Gemini destekli konu anlatımı ve soru çözüm açıklamaları  
- Seviye tespit testi ve akıllı çalışma planı  
- Gerçek sınav formatında deneme sınavları  
- Günlük görevler, rozetler ve geri sayım sistemi  
- Zayıf konulara özel tekrar önerileri  
- Admin paneliyle içerik yönetimi  

---

## User Stories

EhliyetGO kullanıcıları, uygulamaya kayıt olarak kişisel ilerlemelerini takip etmek ve ilk kullanımda sunulan seviye belirleme testiyle kendi öğrenme yolculuklarını başlatmak ister. Yapay zeka destekli konu anlatımı sayesinde trafik, motor, ilk yardım gibi sınav konularını anlaşılır biçimde dinleyip, gerektiğinde tekrar edebilmek onlar için kritik önemdedir. Kullanıcılar sınav formatında testler çözerek bilgilerini ölçmek, her soru için yapay zekadan açıklayıcı geri bildirim alarak eksik konularını hızlıca fark etmek isterler. Sistem, geçmiş yanıtları analiz ederek kişiye özel çalışma planı ve tekrar önerileri sunmalı, günlük görevler ve başarı rozetleriyle kullanıcıyı düzenli çalışmaya teşvik etmelidir. Zaman yönetimi açısından kullanıcılar için sınav geri sayım takvimi ve gerçek sınav simülasyonları ile performanslarını ölçebilecekleri bir yapı önemlidir. Uygulamanın temel amacı; her kullanıcının öğrenme sürecini kişiselleştirilmiş, etkileşimli ve sürdürülebilir hale getirmektir.

---

## Kullanılan Teknolojiler

| Katman             | Teknoloji / Kütüphane                          | Açıklama                                                    |
|--------------------|------------------------------------------------|-------------------------------------------------------------|
| Arayüz (GUI)       | Tkinter/PyQt5                                  | Masaüstü kullanıcı arayüzü – butonlar, formlar, test ekranı |
| AI Entegrasyonu    | Google Gemini API                              | Konu anlatımı ve soru açıklamaları için yapay zeka servisi  |
| Veritabanı         | SQLite/TinyDB                                  | Kullanıcı verisi, sorular, puanlar vs. için lokal veritabanı|
| HTTP İstekleri     | requests/httpx                                 | Yapay zeka API'lerine bağlanmak için                        |
| Veri Formatı       | JSON                                           | Soru havuzu ve kullanıcı ayarları için hafif veri yapısı    |
| Paketleme          | PyInstaller/cx_Freeze                          | Uygulamayı .exe/.app gibi çalıştırılabilir hale getirme     |
| Görseller          | .png / .ico / .jpg                             | Uygulama ikonları ve UI görselleri                          |
| Test / Debugging   | unittest/logging                               | Birim testleri ve hata loglama işlemleri                    |

