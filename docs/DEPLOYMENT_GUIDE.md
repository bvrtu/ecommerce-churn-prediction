# Deployment Guide

## Local Deployment

### 1. Streamlit App

```bash
streamlit run streamlit_app.py
```

App will be available at: `http://localhost:8501`

### 2. FastAPI

```bash
uvicorn app:app --reload
```

API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## Cloud Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy!

### HuggingFace Spaces

1. Create a new Space on HuggingFace
2. Select Streamlit as SDK
3. Upload your files
4. Deploy!

### Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run streamlit_app.py`
5. Deploy!

### Heroku

1. Create `Procfile`:
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
docker build -t churn-prediction .
docker run -p 8501:8501 churn-prediction
```

