# Önerilen Kaggle Dataset'leri - E-commerce Churn Prediction

## ❌ Uygun OLMAYAN Dataset
- **Recommender System Associations Rules**: Bu bir öneri sistemi dataset'i, churn prediction için uygun değil.

## ✅ ÖNERİLEN Dataset'ler

### 1. E-Commerce Customer Churn Dataset ⭐ (EN ÖNERİLEN)
**Link**: https://www.kaggle.com/datasets/aravindh1/ecommerce-customer-churn

**Özellikler**:
- ✅ Gerçek e-ticaret verileri
- ✅ Churn kolonu mevcut
- ✅ 10,000+ satır
- ✅ 15+ feature
- ✅ E-ticaret sektörüne özel

**İndirme**:
1. Link'e tıklayın
2. "Download" butonuna tıklayın
3. ZIP'i açın ve CSV'yi `data/raw/train.csv` olarak kaydedin

---

### 2. Customer Churn Prediction
**Link**: https://www.kaggle.com/datasets/carl24/ecommerce-customer-churn-prediction

**Özellikler**:
- ✅ Kapsamlı feature set
- ✅ Churn kolonu mevcut
- ✅ E-ticaret odaklı

---

### 3. Telco Customer Churn (E-commerce'e uyarlanabilir)
**Link**: https://www.kaggle.com/datasets/blastchar/telco-customer-churn

**Özellikler**:
- ✅ Çok popüler ve iyi dokümante edilmiş
- ✅ Churn kolonu mevcut
- ✅ 7,000+ satır
- ✅ Telekom sektörü ama e-commerce'e uyarlanabilir
- ⚠️ Sektör farklı ama metodoloji aynı

---

### 4. Online Retail Dataset (Churn için uyarlanabilir)
**Link**: https://www.kaggle.com/datasets/carrie1/ecommerce-data

**Özellikler**:
- ✅ Gerçek e-ticaret işlem verileri
- ✅ Churn tanımı yapılabilir (son X günde alışveriş yapmayanlar)
- ⚠️ Churn kolonu yok, siz oluşturmanız gerekir

---

## 🎯 Hangi Dataset'i Seçmeliyim?

### Eğer Hızlı Başlamak İstiyorsanız:
→ **"E-Commerce Customer Churn Dataset"** (#1) - En uygun, hazır churn kolonu var

### Eğer Daha Fazla Veri İstiyorsanız:
→ **"Telco Customer Churn"** (#3) - Çok popüler, iyi dokümante

### Eğer Kendi Churn Tanımınızı Yapmak İstiyorsanız:
→ **"Online Retail Dataset"** (#4) - İşlem verileri, churn'i siz tanımlarsınız

---

## 📋 Dataset Seçim Kriterleri

Projeniz için dataset şu kriterlere uymalı:
- ✅ **Format**: CSV, Parquet veya XLSX
- ✅ **Satır Sayısı**: En az 10,000
- ✅ **Feature Sayısı**: En az 10
- ✅ **Churn Kolonu**: Mevcut olmalı (veya oluşturulabilir olmalı)
- ✅ **Sektör**: E-ticaret (veya uyarlanabilir)

---

## 🚀 Hızlı Başlangıç

1. **Dataset'i seçin**: Yukarıdaki listeden birini seçin
2. **İndirin**: Kaggle'dan Download butonuna tıklayın
3. **Yerleştirin**: CSV'yi `data/raw/train.csv` olarak kaydedin
4. **Kontrol edin**: `python3 src/data_loader.py`
5. **Eğitin**: `python3 train_and_test.py`

---

## ⚠️ Önemli Notlar

- Dataset'te **churn kolonu** olmalı (0/1 veya Yes/No)
- Eğer churn kolonu yoksa, `src/data_loader.py` dosyasını güncelleyerek oluşturabilirsiniz
- Dataset'in en az 10,000 satır olması önerilir
- Feature sayısı en az 10 olmalı

