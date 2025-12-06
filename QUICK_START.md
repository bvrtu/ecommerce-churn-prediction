# 🚀 Hızlı Başlangıç Kılavuzu

## Gerçek Kaggle Dataset ile Model Eğitimi

### Adım 1: Kaggle API Kurulumu (İsteğe Bağlı)

Eğer Kaggle'dan otomatik indirmek istiyorsanız:

```bash
# Kaggle API token'ınızı ayarlayın (KAGGLE_SETUP.md'ye bakın)
pip install kaggle

# Dataset'i indirin
python download_kaggle_dataset.py
```

**VEYA** manuel olarak:
1. Kaggle'dan bir e-commerce churn dataset'i indirin
2. CSV dosyasını `data/raw/` klasörüne koyun
3. Churn kolonunun adının `churn` olduğundan emin olun

### Adım 2: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 3: Modeli Eğitin ve Test Edin

```bash
python train_and_test.py
```

Bu script:
- ✅ Dataset'i yükler (Kaggle veya sample)
- ✅ Modeli eğitir
- ✅ Test setinde değerlendirir
- ✅ Business impact analizi yapar
- ✅ Modeli kaydeder

### Adım 4: Sonuçları İnceleyin

Script çıktısında göreceksiniz:
- Model performans metrikleri (Accuracy, Precision, Recall, F1, ROC-AUC)
- Confusion matrix
- Business impact analizi
- Model kayıt konumu

### Adım 5: Uygulamayı Çalıştırın

**Streamlit Web App:**
```bash
streamlit run streamlit_app.py
```

**FastAPI:**
```bash
uvicorn app:app --reload
```

## Notebook'ları Çalıştırma

Jupyter notebook'ları detaylı analiz için:

```bash
jupyter notebook notebooks/
```

Sırayla çalıştırın:
1. `01_EDA.ipynb` - Veri analizi
2. `02_Baseline.ipynb` - Baseline model
3. `03_Feature_Engineering.ipynb` - Feature engineering
4. `04_Model_Optimization.ipynb` - Hiperparametre optimizasyonu
5. `05_Model_Evaluation.ipynb` - Model değerlendirme
6. `06_Final_Pipeline.ipynb` - Final pipeline

## Sorun Giderme

### Dataset Bulunamadı
- `data/raw/` klasöründe CSV dosyası olduğundan emin olun
- Churn kolonunun adını kontrol edin
- `src/data_loader.py` dosyasındaki column mapping'i güncelleyin

### Model Eğitimi Hatası
- Dataset'in en az 10,000 satır ve 10+ feature içerdiğinden emin olun
- Churn kolonunun binary (0/1) olduğundan emin olun
- Eksik değerleri kontrol edin

### Import Hatası
- Virtual environment'in aktif olduğundan emin olun
- `pip install -r requirements.txt` komutunu çalıştırın

## Örnek Çıktı

```
============================================================
Starting Model Training
============================================================
Features: 20
Samples: 15000
Churn rate: 25.33%

Train set: 12000 samples
Test set: 3000 samples

Training pipeline...
Evaluating on test set...

==================================================
Model Performance Metrics
==================================================
ACCURACY      : 0.8833
PRECISION     : 0.8521
RECALL        : 0.8234
F1            : 0.8375
ROC_AUC       : 0.9215
==================================================

✅ Model saved to models/final_pipeline.pkl
```

## Sonraki Adımlar

1. ✅ Model eğitildi ve test edildi
2. 📊 Notebook'ları çalıştırıp detaylı analiz yapın
3. 🚀 Uygulamayı deploy edin
4. 📝 README ve dokümantasyonu güncelleyin
5. 📤 Projeyi teslim edin!

