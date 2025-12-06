# Kaggle Dataset Setup Guide

## 1. Kaggle API Kurulumu

### Adım 1: Kaggle API Token'ı Alın

1. https://www.kaggle.com/ adresine gidin ve giriş yapın
2. Profil ayarlarına gidin: https://www.kaggle.com/settings
3. "API" bölümüne scroll edin
4. "Create New Token" butonuna tıklayın
5. `kaggle.json` dosyası indirilecek

### Adım 2: Token'ı Yerleştirin

**Mac/Linux:**
```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

**Windows:**
```bash
mkdir %USERPROFILE%\.kaggle
move %USERPROFILE%\Downloads\kaggle.json %USERPROFILE%\.kaggle\
```

### Adım 3: Kaggle API'yi Yükleyin

```bash
pip install kaggle
```

## 2. Dataset İndirme

### Otomatik İndirme (Önerilen)

```bash
python download_kaggle_dataset.py
```

### Manuel İndirme

Eğer API çalışmazsa:

1. https://www.kaggle.com/datasets adresine gidin
2. "ecommerce customer churn" araması yapın
3. Uygun bir dataset seçin (örnekler):
   - "E-Commerce Customer Churn"
   - "Customer Churn Prediction"
   - "Online Retail Dataset"
4. Dataset'i indirin
5. CSV dosyalarını `data/raw/` klasörüne kopyalayın

## 3. Popüler E-commerce Churn Dataset'leri

### Önerilen Dataset'ler:

1. **E-Commerce Customer Churn**
   - Kaggle: `aravindh1/ecommerce-customer-churn`
   - Özellikler: Gerçek e-ticaret verileri

2. **Customer Churn Prediction**
   - Kaggle: `carl24/ecommerce-customer-churn-prediction`
   - Özellikler: Kapsamlı feature set

3. **Online Retail Dataset**
   - Kaggle: `carrie1/ecommerce-data`
   - Özellikler: Churn için uyarlanabilir

## 4. Dataset Formatı

Dataset'iniz şu formatta olmalı:

- **Format**: CSV
- **Churn Column**: `churn` veya `Churn` (binary: 0/1 veya Yes/No)
- **Minimum Rows**: 10,000+
- **Minimum Features**: 10+

### Gerekli Kolonlar (örnek):

- `customer_id`: Müşteri ID
- `churn`: Hedef değişken (0/1)
- Demografik: age, gender, city, etc.
- Davranışsal: purchases, spending, activity, etc.

## 5. Dataset Kontrolü

Dataset'i yükledikten sonra kontrol edin:

```python
import pandas as pd
from pathlib import Path

df = pd.read_csv('data/raw/your_dataset.csv')
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Churn column: {df['churn'].value_counts() if 'churn' in df.columns else 'NOT FOUND'}")
```

## 6. Sorun Giderme

### Problem: "Kaggle API authentication failed"
**Çözüm**: `kaggle.json` dosyasının doğru yerde olduğundan ve izinlerinin doğru olduğundan emin olun.

### Problem: "Dataset not found"
**Çözüm**: Dataset adını kontrol edin. Format: `username/dataset-name`

### Problem: "Churn column not found"
**Çözüm**: `src/data_loader.py` dosyasındaki `load_kaggle_ecommerce_churn` fonksiyonunu güncelleyin veya dataset'inizdeki churn kolonunu `churn` olarak yeniden adlandırın.

## 7. Alternatif: Örnek Dataset Kullanımı

Eğer Kaggle dataset'i bulamazsanız, proje otomatik olarak örnek dataset oluşturacaktır:

```bash
python src/data_loader.py
```

Bu, gerçekçi bir e-ticaret churn dataset'i oluşturur ve model eğitimi için kullanılabilir.

