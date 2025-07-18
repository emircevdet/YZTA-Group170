# DriveMate

## Logo
<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/LogoDriveMate.png" width="400"/>

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
- Kişiye özel yapay zeka açıklamaları sunar   
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

Kullanıcı yolculuğu, uygulamaya kayıt olarak başlar. Kayıt işleminin ardından, ilk kullanımda sunulan yapay zeka destekli seviye belirleme testi sayesinde kullanıcının mevcut bilgi düzeyi analiz edilir.

Eğitim süreci boyunca trafik, motor ve ilk yardım gibi sınav konuları; yapay zeka tarafından sadeleştirilmiş ve anlaşılır biçimde sunulur. Her konu anlatımının ardından, gerçek sınav formatına uygun çoktan seçmeli testlerle bilgiler pekiştirilir. Dileyen kullanıcılar, doğrudan yapay zeka ile sohbet ekranına geçerek merak ettikleri konuları sorabilir, anında konu anlatımı talep edebilir.

Günlük görevlerle öğrenme süreci düzenli olarak desteklenir ve kullanıcı motivasyonunu artırmak için çeşitli ödül ve hatırlatıcı sistemler entegre edilmiştir. Sınava kalan süreyi gösteren geri sayım takvimi, süreci planlamada önemli bir rehber görevi görür.

Uygulamada yer alan “Sınav Simülasyonu” modu, süreli ve rastgele sorularla gerçek sınav atmosferini önceden yaşatarak; kullanıcıya sınav stresiyle başa çıkma ve zaman yönetimi konusunda pratik kazandırır.

Tüm bu yapı, bireyin öğrenme yolculuğunu kişiselleştiren, sürdürülebilir ve ölçülebilir hale getirerek teorik sürücü sınavına eksiksiz bir şekilde hazırlanmasını amaçlar.

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


---



# Sprint 2

## Sprint Notları

 Bu sprint, kullanıcı deneyimini zenginleştirmeye ve yapay zeka entegrasyonlarına odaklanmıştır. Sprint 2'de, yapay zeka destekli sohbet fonksiyonu, Gemini entegrasyonları ve kullanıcı arayüzü iyileştirmeleri gibi önemli özellikler geliştirilmiştir. Bu sprint'te toplam 44 puanlık iş yükü başarıyla tamamlanmıştır.

---

## Sprint Review

Sprint 2'de, projemizin yapay zeka entegrasyonları ve kullanıcı deneyimi iyileştirmeleri odaklı hedefleri başarıyla tamamlanmıştır.

- UI Tasarım Revizyonu ve Genel Stil İyileştirmeleri: Kullanıcı arayüzünde önemli tasarım revizyonları yapıldı ve genel stil tutarlılığı sağlandı. Bu sayede kullanıcı deneyimi görsel olarak zenginleştirildi.
- AI ile Sohbet Fonksiyonu: Kullanıcıların yapay zeka ile etkileşim kurabileceği sohbet özelliği geliştirildi ve temel işlevselliği test edildi.
- Seviye Belirleme Testi için Gemini Entegrasyonu: Seviye belirleme testinin daha akıllı ve dinamik hale gelmesi için Gemini yapay zeka modeli entegre edildi.
- Konu Başlıklarının Belirlenmesi ve Gemini ile Entegrasyonu: Konu başlıklarının otomatik olarak belirlenmesi ve Gemini'nin bu süreçte kullanılması sağlandı.
- Sınav Sonuç Ekranı: Kullanıcıların sınav performanslarını detaylı bir şekilde görebilecekleri sonuç ekranı geliştirildi.

Devredilen&Değiştirilen Görevler:

Yapay zeka eğitimine verilen stratejik öncelik nedeniyle, Admin Paneli ve Rozet Sistemi gibi bazı görevler kapsam dışı bırakılmıştır. Sprint 3 görevleri bu şekilde düzenlenmiştir.


---

## Sprint Retrospective

- Yapay zeka eğitimine verilen öncelik ve bu doğrultuda Admin Paneli ile Rozet Sistemi gibi bazı işlerin iptal edilmesi, ekibin stratejik hedeflere daha net odaklanmasını sağlamıştır. Bu karar, kaynakların en verimli şekilde kullanılmasına yardımcı olmuştur.

- Bu tür büyük kapsam değişikliklerinin sprint başında netleştirilmesi, ekibin motivasyonunu ve planlamasını olumlu etkilemiştir.

---
 
## Daily Scrum

Ekip üyeleri ile haftada 2 kez toplantı yapılarak ilerlemeler kontrol edildi. Her üye kendi görev ilerlemesini her gün Trello üzerinden düzenli olarak güncelledi ve WhatsApp üzerinden düzenli olarak gelişmeler konuşuldu.

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_1.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_2.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_3.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_4.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_5.png" width="300"/>

---


## Sprint Board Updates

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Trello%20ss.jpeg?raw=true" alt="Sprint Board" width="500"/>

---


## Proje Görselleri

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220653.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220720.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220747.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220829.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220902.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220916.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220928.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20220950.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20221005.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-07-18%20221035.png" width="300"/>


---


