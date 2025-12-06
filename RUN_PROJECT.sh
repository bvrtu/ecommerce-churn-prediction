#!/bin/bash

# E-commerce Churn Prediction - Proje Çalıştırma Scripti

echo "=========================================="
echo "E-commerce Churn Prediction - Setup"
echo "=========================================="

# 1. Virtual environment kontrolü
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment oluşturuluyor..."
    python3 -m venv venv
fi

# 2. Virtual environment'ı aktif et
echo "🔧 Virtual environment aktif ediliyor..."
source venv/bin/activate

# 3. Bağımlılıkları yükle
echo "📥 Bağımlılıklar yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Dataset oluştur (eğer yoksa)
echo "📊 Dataset kontrol ediliyor..."
python3 src/data_loader.py

# 5. Modeli eğit ve test et
echo "🚀 Model eğitimi başlatılıyor..."
python3 train_and_test.py

echo ""
echo "=========================================="
echo "✅ Proje hazır!"
echo "=========================================="
echo ""
echo "Sonraki adımlar:"
echo "1. Streamlit uygulaması: streamlit run streamlit_app.py"
echo "2. FastAPI: uvicorn app:app --reload"
echo "3. Notebook'lar: jupyter notebook notebooks/"

