"""
Inference script for making predictions with the trained model.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Any, List

from src.config import MODELS_DIR
from src.pipeline import ChurnPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChurnPredictor:
    """Churn prediction inference class."""
    
    def __init__(self, model_path: Path = None):
        """Initialize the predictor with a trained model."""
        if model_path is None:
            model_path = MODELS_DIR / "final_pipeline.pkl"
        
        self.pipeline = ChurnPipeline()
        self.pipeline.load(model_path)
        logger.info(f"Model loaded from {model_path}")
    
    def predict(self, data: Dict[str, Any] | pd.DataFrame) -> Dict[str, Any]:
        """
        Make churn prediction for a single customer or batch.
        
        Args:
            data: Dictionary with customer features or DataFrame
            
        Returns:
            Dictionary with prediction results
        """
        # Convert dict to DataFrame if needed
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data.copy()
        
        # Make predictions
        predictions = self.pipeline.predict(df)
        probabilities = self.pipeline.predict_proba(df)[:, 1]
        
        # Format results
        results = []
        for i in range(len(df)):
            results.append({
                'customer_id': df.iloc[i].get('customer_id', i),
                'churn_prediction': int(predictions[i]),
                'churn_probability': float(probabilities[i]),
                'risk_level': self._get_risk_level(probabilities[i])
            })
        
        if len(results) == 1:
            return results[0]
        return results
    
    def _get_risk_level(self, probability: float) -> str:
        """Categorize churn risk based on probability."""
        if probability >= 0.7:
            return "High"
        elif probability >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    def predict_batch(self, data: List[Dict[str, Any]] | pd.DataFrame) -> List[Dict[str, Any]]:
        """Make predictions for multiple customers."""
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        return self.predict(df)


def main():
    """Example usage."""
    predictor = ChurnPredictor()
    
    # Example customer data
    sample_customer = {
        'customer_id': 12345,
        'age': 35,
        'gender': 'Male',
        'city': 'Istanbul',
        'membership_type': 'Premium',
        'total_purchases': 20,
        'total_spent': 5000,
        'days_since_last_purchase': 45,
        'days_since_signup': 365,
        'products_viewed': 100,
        'cart_abandonment_rate': 0.3,
        'customer_service_contacts': 2,
        'promo_emails_opened': 15,
        'mobile_app_usage': 1,
        'subscription_active': 1,
    }
    
    result = predictor.predict(sample_customer)
    print("\nPrediction Result:")
    print("=" * 50)
    for key, value in result.items():
        print(f"{key}: {value}")
    print("=" * 50)


if __name__ == "__main__":
    main()

