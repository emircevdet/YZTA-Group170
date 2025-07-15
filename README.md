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

Ehliyet teorik sınavına hazırlanan bireylerin öğrenme sürecini daha kolay, daha etkili ve daha kişisel hale getirmektir.

- Klasik ezber yöntemlerini modernleştirir  
- Kişiye özel çalışma planı ve yapay zeka açıklamaları sunar  
- Kullanıcının eksik konularını analiz ederek hedefli tekrar sağlar  
- Sınav stresine karşı gerçek sınav formatında denemeler yapar  

---

## Hedef Kitle

- İlk kez ehliyet alacak bireyler (18+)
- Yoğun çalışan yetişkinler
- Sürücü kursları (B2B modeli için)

---

## Özellikler

- Gemini destekli konu anlatımı ve soru çözüm açıklamaları  
- Seviye tespit testi ve akıllı çalışma planı  
- Gerçek sınav formatında deneme sınavları  
- Günlük görevler ve geri sayım sistemi  

---

## Kullanıcı Hikayesi

kullanıcının kayıt olmasıyla başlar. Kayıt işleminin ardından, ilk kullanımda seviye belirleme testi sunularak bireyin mevcut bilgi düzeyi tespit edilir. Bu sayede kullanıcı, seviyesine uygun içeriklerle yönlendirilir.

Süreç boyunca trafik, motor ve ilk yardım gibi sınav konuları, yapay zeka destekli anlatımlarla sadeleştirilmiş bir biçimde sunulur. Konu anlatımlarının ardından, gerçek sınav formatına uygun çoktan seçmeli testlerle pekiştirme yapılır. Her soru sonrası, doğru ve yanlış seçenekler yapay zeka tarafından detaylı şekilde açıklanır. Bu açıklamalar, kullanıcının eksik bilgilerini tespit edip daha odaklı çalışmasını mümkün kılar. Kullanıcı dilerse direkt AI ile sohbet alanına geçip, sorularını sohbet üzerine sorabilir, konu anlatımı talep edebilir.

Kullanıcının sistem üzerindeki tüm etkileşimleri kayıt altına alınır ve analiz edilir. Bu veriler doğrultusunda, kişiselleştirilmiş çalışma planları, tekrar önerileri ve zayıf konu başlıkları otomatik olarak oluşturulur. Günlük görevler ve başarı rozetleri ile öğrenme süreci takip edilirken aynı zamanda motivasyon unsurları da entegre edilir.

Geri sayım takvimi, kullanıcıya sınava ne kadar süre kaldığını hatırlatır. Uygulama içerisinde yer alan sınav simülasyonu modülü, süreli ve rastgele sorularla gerçek sınav deneyimini önceden yaşatır. Bu modül, sınav stresi ve zaman yönetimi konularında deneyim kazanmayı destekler.

Tüm sistem, bireyin öğrenme yolculuğunu ölçülebilir, kişiye özel ve sürdürülebilir bir yapıya dönüştürerek teorik sınava eksiksiz şekilde hazırlanmasını hedefler.

---

## Kullanılan Teknolojiler

| Katman                | Teknoloji / Kütüphane             | Açıklama                                                                 |
| --------------------- | --------------------------------- | ------------------------------------------------------------------------ |
| Arayüz (GUI)          | Tkinter                           | Masaüstü arayüz – form ekranları, butonlar ve layout düzenlemeleri      |
| Veritabanı            | SQLite                            | Kullanıcı verileri ve test kayıtlarının saklandığı yerel veritabanı      |
| Şifreleme             | hashlib                           | Kullanıcı şifrelerinin güvenli şekilde hash’lenmesi için                 |
| Kimlik Doğrulama      | JWT (Python'da `jwt` kütüphanesi) | Kullanıcının kimliğini doğrulamak için token bazlı sistem                |
| API Sunucusu          | FastAPI                           | Backend API’lerinin geliştirilmesinde kullanılan modern Python framework |
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
# Sprint 2

## Sprint Notları

