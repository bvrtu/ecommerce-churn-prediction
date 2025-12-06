# ✅ Deployment Checklist

## ÖNCE YAPILMASI GEREKENLER

### 1. Model Dosyası Kontrolü
```bash
ls -lh models/final_pipeline.pkl
# Dosya var mı ve boyutu nedir?
```

### 2. Requirements.txt Kontrolü
```bash
cat requirements.txt
# Tüm bağımlılıklar listelenmiş mi?
```

### 3. Streamlit App Test
```bash
streamlit run streamlit_app.py
# Local'de çalışıyor mu?
```

### 4. Git Repository Hazırlığı
```bash
git status
# Tüm dosyalar commit edildi mi?
```

---

## STREAMLIT CLOUD DEPLOYMENT

### Adım 1: GitHub Repository
- [ ] GitHub'da repository oluşturuldu
- [ ] Tüm dosyalar push edildi
- [ ] Model dosyası (final_pipeline.pkl) repository'de var

### Adım 2: Streamlit Cloud
- [ ] https://streamlit.io/cloud adresine gidildi
- [ ] GitHub ile giriş yapıldı
- [ ] "New app" oluşturuldu
- [ ] Repository seçildi
- [ ] Main file: `streamlit_app.py` ayarlandı
- [ ] Deploy butonuna tıklandı

### Adım 3: Deployment Sonrası
- [ ] App başarıyla deploy oldu
- [ ] Link alındı
- [ ] App test edildi (çalışıyor mu?)
- [ ] README.md'ye link eklendi

---

## HIZLI DEPLOYMENT KOMUTLARI

```bash
# 1. Git repository hazırla
cd /Users/bartu/Desktop/ecommerce-churn-prediction
git init
git add .
git commit -m "Complete project ready for deployment"

# 2. GitHub'a push
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-churn-prediction.git
git branch -M main
git push -u origin main

# 3. Streamlit Cloud'da deploy et
# Manuel olarak: https://streamlit.io/cloud
```

---

## SORUN GİDERME

### Problem: Model dosyası çok büyük (>100MB)
**Çözüm**: Git LFS kullan
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes models/final_pipeline.pkl
git commit -m "Add model with Git LFS"
git push
```

### Problem: Deployment'ta model bulunamıyor
**Çözüm**: Model dosyasının repository'de olduğundan emin olun
```bash
git ls-files | grep final_pipeline.pkl
# Dosya listede olmalı
```

### Problem: Requirements.txt'teki paketler yüklenemiyor
**Çözüm**: Versiyonları kontrol edin, Python 3.14 uyumlu olmalı

---

## TESLİM FORMU İÇİN GEREKLİ BİLGİLER

1. **GitHub Repository Link**: 
   ```
   https://github.com/YOUR_USERNAME/ecommerce-churn-prediction
   ```

2. **Deployment Link**: 
   ```
   https://YOUR_USERNAME-streamlit-app-xxx.streamlit.app
   ```

3. **Model Performans Metrikleri**:
   - Accuracy: 0.7949
   - Precision: 0.6204
   - Recall: 0.5856
   - F1-Score: 0.6025
   - ROC-AUC: 0.8387

4. **Dataset**: Telco Customer Churn (7,043 samples)

5. **Sektör**: Telekom (E-commerce'e uyarlanabilir)

---

## SON KONTROL

- [ ] Tüm dosyalar commit edildi
- [ ] GitHub'a push edildi
- [ ] Deployment yapıldı
- [ ] Deployment linki çalışıyor
- [ ] README.md güncel
- [ ] Ekran görüntüleri eklendi
- [ ] Proje teslim formu dolduruldu

**Hazırsınız! 🚀**

