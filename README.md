# BLM230 - Bilgisayar Mimarisi  
## Dönem Projesi - Hamming SEC-DED Kodu Simülatörü

**Öğrenci Adı Soyadı:** Rima Farah Eleuch  
**Öğrenci Numarası:** 21360859216  

---

## 1. Projenin Amacı

Bu projenin amacı, Hamming SEC-DED (Single Error Correction, Double Error Detection) algoritmasını kullanarak, 8, 16 ve 32 bitlik veriler üzerinde hata tespit ve düzeltme işlemlerini gerçekleştiren kullanıcı dostu bir simülatör geliştirmektir. Program, hem tek bitlik hataları düzeltebilmekte hem de çift bitlik hataları tespit edebilmektedir.

---

## 2. Kullanılan Teknolojiler

- **Python 3**
- **Tkinter:** Grafiksel kullanıcı arayüzü (GUI) oluşturmak için kullanılmıştır.
- **GitHub:** Kaynak kodların barındırılması.
- **YouTube:** Demo videosunun paylaşımı için kullanılmıştır.

---

## 3. Programın Özellikleri

| Özellik                     | Açıklama |
|----------------------------|----------|
| Veri Boyutu Seçimi         | 8, 16 veya 32 bitlik veri seçilebiliyor. |
| Hamming Kod Hesaplama      | SEC-DED kurallarına uygun olarak parite bitleri hesaplanıyor. |
| Belleğe Veri Yazma/Okuma   | Kodlanmış veri belleğe kaydedilip okunabiliyor. |
| Hata Ekleme                | Kullanıcı tarafından istenilen pozisyonlarda tek ya da çift hata ekleniyor. |
| Hata Tespiti ve Düzeltme   | Sendrom analizi ile hata tespiti ve gerektiğinde otomatik düzeltme yapılabiliyor. |
| Görsel Bit Gösterimi       | Bitler renklendirilerek kullanıcıya sunuluyor. |
| Yardım Menüsü              | Kullanım kılavuzu ve program hakkında bilgi veren menüler içeriyor. |

---

## 4. Kullanım Adımları

1. **Veri Boyutunu Seçin**  
   Program başlatıldığında “Veri Boyutu” seçeneğinden 8, 16 veya 32 bit seçin.

2. **Binary Veri Girin**  
   Giriş alanına sadece 0 ve 1’lerden oluşan, seçilen boyutta bir veri girin.

3. **Hamming Kodunu Hesaplayın**  
   “Hamming Kodunu Hesapla” düğmesine tıklayarak kodlanmış veriyi üretin.

4. **Belleğe Kaydedin**  
   Kodlanmış veriyi daha sonra kullanmak üzere belleğe kaydedin.

5. **Bellekten Veri Okuyun**  
   Kaydedilen veriyi bellekten tekrar okuyabilirsiniz.

6. **Hata Ekleyin ve Sendrom Analizi Yapın**  
   - Hata tipi olarak “Tek Bit” veya “Çift Bit” seçin.  
   - Hata pozisyonlarını girin ve “Hata Ekleyin” düğmesine basın.  
   - Tek bit hatası: Program otomatik olarak sendrom hesaplayarak hatayı tespit eder ve düzeltir.  
   - Çift bit hatası: Program sendrom ve genel parite ile hatayı tespit eder ancak düzeltemez.

---

## 5. Teknik Detaylar

- **Parity Bitleri:** Pozisyonları 2ⁿ olan bitlerdir.  
- **Genel Parite:** En sona eklenir ve tüm bitlerin XOR toplamıdır.  
- **Syndrome:** Parity bitleri üzerinden hesaplanır ve hata pozisyonunu verir.  
- **Çift Hata Tespiti:** Genel parite + sendrom sayesinde tespit edilir ancak düzeltilemez.

---

## 6. Kod Yapısı

- `HammingCodeSimulator` sınıfı tüm mantığı içerir.
  - `encode_data`: Veriyi Hamming koduna çevirir.
  - `introduce_error`: Hatalı bitleri üretir.
  - `detect_and_correct_error`: Sendromla hatayı bulur ve düzeltir.
  - `visualize_bits`: Bitleri renkli görselleştirir.

---

## 7. Sonuç

Bu simülatör, Hamming SEC-DED algoritmasının çalışma prensibini hem teorik hem de pratik olarak göstermektedir. Kullanıcı dostu arayüzü ve görselleştirme özellikleri ile öğrenmeyi destekler niteliktedir.

---

## 8. Kaynaklar ve Linkler

- [**Demo Videosu (YouTube)**](https://www.youtube.com/watch?v=rsFOR4ibPbg)
