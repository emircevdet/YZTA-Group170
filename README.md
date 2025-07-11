# EhliyetGO

## Logo
<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Logo.png?raw=true" alt="EhliyetGO Logo" width="500"/>

## Takım

| İsim                 | Rol              |
|----------------------|------------------|
| Şevval Battal        | Scrum Master     |
| Yaren Doğan          | Product Owner    |
| Kaan Parmak          | Developer        |
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

| Katman                | Teknoloji / Kütüphane             | Açıklama                                                                 |
| --------------------- | --------------------------------- | ------------------------------------------------------------------------ |
| Arayüz (GUI)          | Tkinter                           | Masaüstü arayüz – form ekranları, butonlar ve layout düzenlemeleri      |
| Veritabanı            | SQLite                            | Kullanıcı verileri ve test kayıtlarının saklandığı yerel veritabanı      |
| Şifreleme             | hashlib                           | Kullanıcı şifrelerinin güvenli şekilde hash’lenmesi için                 |
| Kimlik Doğrulama      | JWT (Python'da `jwt` kütüphanesi) | Kullanıcının kimliğini doğrulamak için token bazlı sistem                |
| API Sunucusu          | FastAPI                           | Backend API’lerinin geliştirilmesinde kullanılan modern Python framework |
| HTTP Sunucusu         | Uvicorn                           | FastAPI uygulamasını çalıştırmak için ASGI uyumlu sunucu                 |
| Veri Formatı          | JSON                              | Kullanıcı kayıtları ve token işlemleri için hafif veri saklama formatı   |

---

# Sprint 1 

## Sprint Notları

Sprint 1 kapsamında öncelikli olarak kullanıcı kayıt/giriş işlemleri, seviye belirleme testi ve soru çözüm arayüzü gibi temel işlevler ele alındı. User Story’ler, Product Backlog’a tanımlandı ve her bir hikâye kendi içerisinde yapılacak iş task'lere bölündü. Hikaye detayları, backlog item’lara tıklanarak görüntülenebilir şekilde hazırlandı.

Toplam proje backlog’u 150 puan olarak planlandı. İlk sprint’te hedeflenen ilerleme oranı %40-50 arası belirlendi. Bu doğrultuda Sprint 1’e 66 puanlık iş yükü alındı. Backlog’daki işler puanlarına göre sıralandı ve sprint kapasitesi aşılmadan uygun hikâyeler seçildi. Hikâye bağı 66 puanı geçmemek üzere dengeli tutuldu.

---

## Daily Scrum

Ekip üyeleri ile haftada 2 kez toplantı yapılarak ilerlemeler kontrol edildi. Her üye kendi görev ilerlemesini her gün Trello üzerinden düzenli olarak güncelledi.

---

## Sprint Board Updates

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Trello%20ss.jpeg?raw=true" alt="Sprint Board" width="800"/>

---

## Sprint Review

- SQLite ile veritabanı yapısı tamamlandı.  
- Kullanıcı kayıt & giriş işlemleri çalışır durumda. Şifre hash’leme ve doğrulama mekanizması başarıyla test edildi.  
- Konu listesi ekranı ve konu bazlı test çözüm ekranı tamamlandı.  
- Seviye belirleme testi hem frontend hem backend tarafında başarılı çalışıyor. Skor veritabanına kaydediliyor.  
- Admin paneli, kullanıcı profil düzenleme ve istatistik ekranları Sprint 2’ye devredildi.

---

## Sprint Retrospective

- Görevlerin net şekilde tanımlanması ekip verimliliğini artırdı.  
- UI/UX geliştirmeleri beklenenden fazla zaman aldı. Bu durum sonraki sprint’te dikkate alınacak.  
- Task’lerin daha küçük ve ölçülebilir hale getirilmesinin faydalı olacağına karar verildi.  

---

## Proje Görselleri

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002839.png?raw=true" alt="Giriş Sayfası" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002734.png?raw=true" alt="Konu Listesi" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002724.png?raw=true" alt="Test Sayfası" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002715.png?raw=true" alt="Test Sayfası" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002705.png?raw=true" alt="Test Sayfası" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002617.png?raw=true" alt="Test Sayfası" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002528.png?raw=true" alt="Test Sayfası" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-06%20002519.png?raw=true" alt="Test Sayfası" width="300"/>

---

