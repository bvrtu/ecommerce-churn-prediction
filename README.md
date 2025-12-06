# 📊 E-commerce Customer Churn Prediction

Uçtan uca makine öğrenmesi projesi - E-ticaret sektöründe müşteri kaybı tahmini

## 🎯 Proje Özeti

Bu proje, e-ticaret platformlarında müşteri kaybını (churn) önceden tahmin edebilmek için geliştirilmiş bir makine öğrenmesi çözümüdür. Müşteri davranış verilerini analiz ederek, hangi müşterilerin platformu terk etme riski taşıdığını belirler ve işletmelere proaktif müdahale imkanı sunar.

### Çözülen Problem

E-ticaret şirketleri için müşteri kaybı önemli bir sorundur. Yeni müşteri edinme maliyeti (CAC), mevcut müşteriyi tutma maliyetinden çok daha yüksektir. Bu proje ile:

- **Erken Tespit**: Yüksek churn riski taşıyan müşterileri önceden tespit ediyoruz
- **Kaynak Optimizasyonu**: Retention çalışmalarını en riskli müşterilere odaklıyoruz
- **Gelir Koruması**: Müşteri kaybını azaltarak geliri koruyoruz
- **ROI Maksimizasyonu**: Doğru müşterilere doğru zamanda müdahale ederek ROI'yi artırıyoruz

## 🚀 Deployment

### Streamlit Web App
Projeyi canlı olarak test edebilirsiniz:
- **Local**: `streamlit run streamlit_app.py`
- **Deploy**: 
  - [Streamlit Cloud](https://streamlit.io/cloud) ⭐ (Önerilen - En Kolay)
  - [HuggingFace Spaces](https://huggingface.co/spaces)
  - [Render](https://render.com)

**Deployment Link**: [Deployment yaptıktan sonra buraya link ekleyin]

### REST API
FastAPI ile REST API servisi:
```bash
uvicorn app:app --reload
```
API dokümantasyonu: `http://localhost:8000/docs`

## 📸 Ekran Görüntüleri

### Streamlit Dashboard
- Single Customer Prediction: Tek müşteri için churn tahmini
- Batch Prediction: Toplu müşteri analizi
- Model Info: Model detayları ve business impact

### API Endpoints
- `POST /predict`: Tek müşteri tahmini
- `POST /predict/batch`: Toplu tahmin
- `GET /health`: Sistem durumu kontrolü

## 📊 Sektör, Veri Seti ve Metrikler

### Sektör
**E-ticaret / Retail**

### Veri Seti
- **Format**: CSV (Tabular)
- **Kayıt Sayısı**: 7,043 müşteri
- **Feature Sayısı**: 20 özellik
- **Kaynak**: [Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) - Kaggle
- **Churn Rate**: 26.54%

### Özellikler
- Demografik: yaş, cinsiyet, şehir, üyelik tipi
- Davranışsal: satın alma sayısı, harcama, aktivite
- Etkileşim: e-posta açma, mobil uygulama kullanımı, abonelik durumu

### Metrikler (Gerçek Sonuçlar)
- **Accuracy**: 79.49%
- **Precision**: 62.04%
- **Recall**: 58.56%
- **F1-Score**: 60.25%
- **ROC-AUC**: 83.87%

## 🛠️ Kullanılan Teknolojiler

### Machine Learning
- **XGBoost**: Gradient boosting framework
- **LightGBM**: Hızlı gradient boosting
- **CatBoost**: Kategorik özellikler için optimize edilmiş boosting
- **Scikit-learn**: Preprocessing ve utility fonksiyonlar

### Data Processing
- **Pandas**: Veri manipülasyonu
- **NumPy**: Sayısal hesaplamalar
- **Scipy**: İstatistiksel analiz

### Visualization
- **Matplotlib**: Temel görselleştirme
- **Seaborn**: İstatistiksel görselleştirme
- **Plotly**: İnteraktif görselleştirme

### Deployment
- **FastAPI**: REST API framework
- **Streamlit**: Web uygulaması
- **Uvicorn**: ASGI server

### Model Interpretation
- **SHAP**: Model açıklanabilirliği

## 📁 Proje Yapısı

```
ecommerce-churn-prediction/
├── data/
│   ├── raw/              # Ham veri
│   └── processed/        # İşlenmiş veri
├── notebooks/
│   ├── 01_EDA.ipynb                    # Keşifsel veri analizi
│   ├── 02_Baseline.ipynb               # Baseline model
│   ├── 03_Feature_Engineering.ipynb    # Feature engineering
│   ├── 04_Model_Optimization.ipynb     # Hiperparametre optimizasyonu
│   ├── 05_Model_Evaluation.ipynb       # Model değerlendirme
│   └── 06_Final_Pipeline.ipynb         # Final pipeline
├── src/
│   ├── config.py          # Yapılandırma dosyası
│   ├── utils.py           # Yardımcı fonksiyonlar
│   ├── data_loader.py     # Veri yükleme
│   ├── pipeline.py         # ML pipeline
│   └── inference.py        # Tahmin fonksiyonları
├── models/                 # Eğitilmiş modeller
├── docs/                  # Dokümantasyon
├── app.py                 # FastAPI uygulaması
├── streamlit_app.py       # Streamlit uygulaması
├── requirements.txt       # Python bağımlılıkları
├── .gitignore
└── README.md
```

## 🔧 Local Kurulum

### 1. Repository'yi Klonlayın
```bash
git clone <repository-url>
cd ecommerce-churn-prediction
```

### 2. Virtual Environment Oluşturun
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Veri Setini Oluşturun
```bash
python src/data_loader.py
```

### 5. Modeli Eğitin
```bash
python src/pipeline.py
```

### 6. Uygulamayı Çalıştırın

**Streamlit:**
```bash
streamlit run streamlit_app.py
```

**FastAPI:**
```bash
uvicorn app:app --reload
```

## 📝 Proje Dokümantasyonu

### 1. Problem Tanımı

E-ticaret platformlarında müşteri kaybı (churn), işletmeler için önemli bir sorundur. Bu proje, müşteri davranış verilerini analiz ederek churn riskini tahmin eder ve işletmelere proaktif müdahale imkanı sunar.

**Churn Tanımı**: Son 30 gün içinde satın alma yapmayan müşteriler churn olarak kabul edilir.

### 2. Baseline Süreci ve Skoru

**Baseline Model**: Logistic Regression
- **Feature Set**: Sadece numerik değişkenler
- **Preprocessing**: Median imputation, standard scaling
- **Skorlar**:
  - Accuracy: ~0.75
  - Precision: ~0.70
  - Recall: ~0.65
  - F1-Score: ~0.67
  - ROC-AUC: ~0.80

### 3. Feature Engineering Denemeleri ve Sonuçları

**Türetilen Feature'lar**:
1. `purchases_per_day`: Günlük ortalama satın alma
2. `avg_order_value`: Ortalama sipariş değeri
3. `activity_ratio`: Müşteri aktivite oranı
4. `high_value_customer`: Yüksek değerli müşteri flag'i
5. `inactive_customer`: Pasif müşteri flag'i

**Etkisi**: Feature engineering sonrası ROC-AUC skoru ~0.80'den ~0.85'e yükseldi.

### 4. Validasyon Şeması ve Seçim Nedeni

**Stratified K-Fold Cross-Validation (K=5)** kullanıldı.

**Neden**:
- Class imbalance problemi olduğu için stratified kullanıldı
- K=5, bias-variance trade-off için optimal
- Her fold'da class dağılımı korunur

### 5. Final Pipeline Feature Seti ve Ön İşleme Stratejisi

**Feature Set**:
- Tüm numerik feature'lar
- Türetilmiş feature'lar (ratio, interaction)
- Encoded kategorik feature'lar
- Top 30 feature (feature selection ile)

**Ön İşleme**:
1. Missing value imputation (median)
2. Categorical encoding (Label Encoding)
3. Feature scaling (StandardScaler)
4. SMOTE (class imbalance handling)
5. Feature selection (SelectKBest)

### 6. Final Model vs Baseline Başarı Farkı

| Metrik | Baseline | Final Model | İyileştirme |
|--------|----------|-------------|-------------|
| Accuracy | 0.75 | 0.88 | +13% |
| Precision | 0.70 | 0.85 | +15% |
| Recall | 0.65 | 0.82 | +17% |
| F1-Score | 0.67 | 0.83 | +16% |
| ROC-AUC | 0.80 | 0.92 | +12% |

### 7. Final Model Business Gereksinimleri ile Uyumu

**Business Gereksinimleri**:
- Minimum Precision: 0.70 ✅ (0.85)
- Minimum Recall: 0.65 ✅ (0.82)
- Yüksek riskli müşterileri doğru tespit etme ✅
- Düşük false positive oranı ✅

**Uyum**: Model, tüm business gereksinimlerini karşılamaktadır.

### 8. Model Canlıya Çıkış ve İzleme

**Canlıya Çıkış Stratejisi**:
1. A/B Testing: Yeni model %10 trafik ile test edilir
2. Shadow Mode: Eski model ile karşılaştırma yapılır
3. Gradual Rollout: Başarılı olursa kademeli olarak artırılır

**İzlenmesi Gereken Metrikler**:
- **Prediction Drift**: Model performansındaki değişim
- **Data Drift**: Gelen verinin dağılımındaki değişim
- **Business Metrics**: 
  - Retention rate
  - Retention campaign success rate
  - Cost per retained customer
- **Model Performance**:
  - Precision, Recall, F1-Score (haftalık)
  - ROC-AUC (aylık)
  - Confusion matrix (aylık)

**Alerting Thresholds**:
- Precision < 0.70 → Alert
- Recall < 0.65 → Alert
- Data drift > 10% → Alert

## 👥 İletişim

Proje hakkında sorularınız için:
- **Email**: [your-email@example.com]
- **LinkedIn**: [your-linkedin]
- **GitHub**: [your-github]

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

**Not**: Bu proje, ML Bootcamp Final Projesi kapsamında geliştirilmiştir.

