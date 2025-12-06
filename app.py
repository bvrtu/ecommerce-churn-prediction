"""
FastAPI application for E-commerce Churn Prediction.
Provides REST API endpoints for model inference.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import logging

from src.inference import ChurnPredictor
from src.config import MODELS_DIR, API_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Churn Prediction API",
    description="API for predicting customer churn in e-commerce",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
try:
    predictor = ChurnPredictor()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    predictor = None


# Request/Response models
class CustomerFeatures(BaseModel):
    """Customer features for prediction."""
    customer_id: Optional[int] = None
    age: int = Field(..., ge=18, le=100, description="Customer age")
    gender: str = Field(..., description="Customer gender")
    city: str = Field(..., description="Customer city")
    membership_type: str = Field(..., description="Membership type")
    total_purchases: int = Field(..., ge=0, description="Total number of purchases")
    total_spent: float = Field(..., ge=0, description="Total amount spent")
    days_since_last_purchase: int = Field(..., ge=0, description="Days since last purchase")
    days_since_signup: int = Field(..., ge=0, description="Days since signup")
    products_viewed: int = Field(..., ge=0, description="Number of products viewed")
    cart_abandonment_rate: float = Field(..., ge=0, le=1, description="Cart abandonment rate")
    customer_service_contacts: int = Field(..., ge=0, description="Number of customer service contacts")
    promo_emails_opened: int = Field(..., ge=0, description="Number of promo emails opened")
    mobile_app_usage: int = Field(..., ge=0, le=1, description="Mobile app usage (0 or 1)")
    subscription_active: int = Field(..., ge=0, le=1, description="Subscription active (0 or 1)")


class PredictionResponse(BaseModel):
    """Prediction response model."""
    customer_id: Optional[int]
    churn_prediction: int
    churn_probability: float
    risk_level: str


class BatchPredictionRequest(BaseModel):
    """Batch prediction request model."""
    customers: List[CustomerFeatures]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "E-commerce Churn Prediction API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": predictor is not None
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(customer: CustomerFeatures):
    """
    Predict churn for a single customer.
    
    Args:
        customer: Customer features
        
    Returns:
        Prediction result with churn probability and risk level
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        result = predictor.predict(customer.dict())
        return PredictionResponse(**result)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_churn_batch(request: BatchPredictionRequest):
    """
    Predict churn for multiple customers.
    
    Args:
        request: List of customer features
        
    Returns:
        List of prediction results
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        customers_data = [customer.dict() for customer in request.customers]
        results = predictor.predict_batch(customers_data)
        return [PredictionResponse(**result) for result in results]
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["reload"]
    )

