# DriveMate

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
- Geri sayım sistemi ve motivasyon mesajları  

---

## Kullanıcı Hikayesi

Kullanıcı, uygulamaya kayıt olarak başlar. Kayıt işleminin ardından, ilk olarak;  yapay zeka destekli seviye belirleme testi sayesinde kullanıcının mevcut bilgi düzeyi analiz edilir.

Eğitim süreci boyunca trafik, motor ve ilk yardım gibi sınav konuları; yapay zeka tarafından sadeleştirilmiş ve anlaşılır biçimde sunulur. Her konu anlatımının ardından, gerçek sınav formatına uygun çoktan seçmeli testlerle bilgiler pekiştirilir. Dileyen kullanıcılar, doğrudan yapay zeka ile sohbet ekranına geçerek merak ettikleri konuları sorabilir, anında konu anlatımı talep edebilir.

Kullanıcı motivasyonunu artırmak için çeşitli  hatırlatıcı pop-up'lar sisteme entegre edilmiştir. Sınava kalan süreyi gösteren geri sayım takvimi, süreci planlamada önemli bir rehber görevi görür.

Uygulamada yer alan yapay zeka desteği sayesinde, süreli ve rastgele sorularla gerçek sınav soruları hazırlanır. Bu sayede, Kullanıcı sınav atmosferini önceden deneyimler; kullanıcıya sınav stresiyle başa çıkma ve zaman yönetimi konusunda pratik kazandırır.

Uygulama; kullanıcının öğrenme yolculuğunu kişiselleştiren, yapay zeka destekli ve ölçülebilir hale getirerek teorik sürücü sınavına eksiksiz bir şekilde hazırlanmasını amaçlar.


---

## Kullanılan Teknolojiler

Elbette, verdiğiniz görseldeki tabloyu README.md dosyasına doğrudan ekleyebileceğiniz Markdown formatında hazırladım. Bu format, GitHub gibi platformlarda otomatik olarak tablo olarak görüntülenecektir.


## Kullanılan Teknolojiler

| Katman             | Teknoloji / Kütüphane                                 | Açıklama                                                                                               |
| :----------------- | :---------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| Kullanıcı Arayüzü  | `tkinter`, `ttk`, `messagebox`, `scrolledtext`, `tkfont` | Python'un yerleşik GUI kütüphanesi. Masaüstü arayüz bileşenleri için kullanılır.                       |
| Veri Katmanı       | `sqlite3`                                             | Hafif, dosya tabanlı veritabanı. Kullanıcı verileri ve uygulama içeriği saklanır.                      |
| İş Mantığı         | `datetime`, `random`, `json`                          | Tarih/zaman işlemleri, rastgelelik ve veri yönetimi için yardımcı modüller.                           |
| Güvenlik           | `hashlib`, `dotenv`, `os`                             | Şifreleme, gizli anahtar yönetimi ve sistemle etkileşim için kullanılır.                               |
| Yapay Zeka         | `google.generativeai`                                 | Google Gemini API entegrasyonu. AI destekli yanıtlar ve öneriler üretir.                               |
| Çoklu İş Parçacığı | `threading`                                           | Arka planda işlem yürütme. GUI donmadan AI yanıtları alınabilir.                                       |
| Web Servisleri     | `fastapi`, `pydantic`                                 | RESTful API endpoint'leri ve veri doğrulama. Uygulama dış sistemlerle entegre olabilir. (Not: Mevcut kodda kullanılmamaktadır, ancak gelecekteki entegrasyonlar için belirtilmiştir.) |




Önemli Not: "Web Servisleri" katmanına, mevcut kodunuzda fastapi ve pydantic kullanılmadığına dair bir not ekledim. Eğer bu teknolojileri projenizin gelecekteki bir aşamasında kullanmayı planlıyorsanız bu şekilde bırakabilirsiniz. Ancak, şu anki kodunuz sadece bir masaüstü uygulaması olduğu için bu katman aslında aktif olarak kullanılmıyor. Bu notu eklemek, projenizin mevcut durumu hakkında daha şeffaf bir bilgi sağlayacaktır. İsterseniz bu satırı tamamen kaldırabilirsiniz.

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


# Sprint 3

## Sprint Notları

Sprint 3, projenin son aşaması olup, temel olarak yapay zeka entegrasyonlarının ince ayarları, kullanıcı arayüzünün son rötuşları ve uygulamanın genel test ve dağıtım süreçlerine odaklanmıştır. Bu sprint, DriveMate'in kullanıma hazır hale getirilmesi için kritik adımları içermektedir.

Toplam proje backlog’u 150 puan olarak planlanmıştı. İlk sprint’te hedeflenen ilerleme oranı %40-50 arası belirlendi. Bu doğrultuda Sprint 1’e 66 puanlık iş yükü alındı. Sprint 2'de 42 puanlık iş yükü tamamlandı. Sprint 3'te ise kalan 42 puanlık iş yükünün tamamlanması hedeflendi. Bu noktada bazı iş yükleri beklenenden daha yüksek puanlı olarak güncellendi ve iş yükleri eşdeğer bazı geliştirmelerden vazgeçildi.
---

## Sprint Hedefleri

- Sınav Geri Sayım Modülü'nün geliştirilmesi ve entegrasyonu.
- Konular bölümündeki Gemini entegrasyonunun eğitimi ve test edilmesi.
- Seviye Belirleme Testi bölümü için Gemini'ın daha iyi sorular hazırlaması için eğitimi ve test edilmesi.
- Daha iyi bir kullanıcı deneyimi için "DriveMate'e sor" butonunun Gemini ile eğitilmesi ve test edilmesi.
- Kullanıcı arayüzünde son rötuşların yapılması.
- Uygulamanın kapsamlı son testlerinin yapılması ve hazır hale getirilmesi.

---

## Sprint Backlog (Tahmini Efor Puanları)

| Görev Başlığı                                                                        | Efor |
|--------------------------------------------------------------------------------------|------|
| Sınav Geri Sayım Modülü                                                              | 3    |
| Konular bölümündeki Gemini'ın eğitilmesi ve test edilmesi                            | 10   |
| Seviye Belirleme Testi bölümü için Gemini'ın daha iyi sorular hazırlaması için eğitilmesi ve test edilmesi | 8    |
| Daha iyi bir kullanıcı deneyimi için DriveMate'e sor butonun Gemini ile eğitilmesi ve test edilmesi | 8    |
| UI Son Rötuşlar                                                                      | 3    |
| Final Test & Deploy                                                                  | 10   |
| **Toplam Sprint 3 Eforu**                                                            | **42** |

---

## Daily Scrum

Ekip üyeleri ile haftada 1-2 kez toplantı yapılarak ilerlemeler kontrol edildi. Her üye kendi görev ilerlemesini her gün Trello üzerinden düzenli olarak güncelledi ve WhatsApp üzerinden düzenli olarak gelişmeler konuşuldu.

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_Sprint-3.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_Sprint-3-2.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_Sprint-3-3.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_Sprint-3-4.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/DailyScrum_Sprint-3-5.png" width="300"/>

---

## Sprint Board Updates

https://trello.com/b/Lzt9ovYD/bootcamp-ai-170-drivemate

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Trello_ss_3.Sprint.png" width="500"/>


---

## Sprint Review

Sprint 3, DriveMate projesinin son sprint'i olarak başarıyla tamamlanmıştır. Bu sprint'te belirlenen hedefler süreç içerisinde güncellenerek, beklenen kalitede ve zamanında yerine getirilmiştir.

- **Sınav Geri Sayım Modülü:** Geliştirildi ve ana ekrana entegre edildi. Kullanıcıların sınava kalan süreyi net bir şekilde takip etmesi sağlandı.
- **Gemini Entegrasyonları (Konular, Seviye Belirleme, DriveMate'e Sor):** Tüm Gemini entegrasyonları (konu anlatımı iyileştirmeleri, seviye belirleme testi soru kalitesi artırımı ve "DriveMate'e Sor" butonu) başarıyla eğitildi ve test edildi. Yapay zeka yanıtlarının doğruluğu ve kullanışlılığı önemli ölçüde arttırıldı.
- **UI Son Rötuşlar:** Kullanıcı arayüzünde yapılan son iyileştirmelerle genel estetik ve kullanılabilirlik artırıldı. Fontlar, renk paletleri ve ikonlar tutarlı hale getirildi.
- **Final Test & Deploy:** Uygulamanın kapsamlı son testleri (fonksiyonel, performans, güvenlik) tamamlandı. Tespit edilen tüm kritik hatalar giderildi. Uygulama, son kullanıcıya dağıtıma hazır hale getirildi ve başarılı bir şekilde deploy edildi.

---

## Sprint Retrospective

**Neler İyi Gitti?**

- **Net Hedefler ve Odaklanma:** Sprint 3'ün son sprint olması ve hedeflerin net bir şekilde belirlenmesi, ekibin motivasyonunu ve odaklanmasını artırdı.
- **Yapay Zeka Entegrasyonlarının Başarısı:** Gemini entegrasyonlarının beklenenden daha iyi performans göstermesi ve kullanıcı deneyimine önemli katkı sağlaması büyük bir başarıydı.
- **Etkili İletişim:** Daily Scrum toplantıları ve WhatsApp üzerinden sürekli iletişim, olası sorunların hızlıca tespit edilip çözülmesine yardımcı oldu.
- **Kapsamlı Test Süreci:** Final test ve deploy aşamasında uygulanan detaylı testler, uygulamanın yüksek kalitede sunulmasını sağladı.

**Neler Daha İyi Yapılabilirdi?**

- **Dokümantasyon Detayı:** Özellikle yapay zeka eğitim süreçleri ve kullanılan prompt mühendisliği teknikleri hakkında daha detaylı iç dokümantasyon, gelecekteki geliştirmeler için faydalı olabilirdi.





---

## Proje Görselleri

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-1.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-2.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-3.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-4.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-5.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-6.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-7.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-8.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-9.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-10.png" width="300"/>

<img src="https://github.com/emircevdet/YZTA-Group170/blob/main/Final-11.png" width="300"/>



