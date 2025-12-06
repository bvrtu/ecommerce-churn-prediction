"""
Utility functions for the E-commerce Churn Prediction project.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging

from src.config import MODELS_DIR, PROCESSED_DATA_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(file_path: Path) -> pd.DataFrame:
    """Load data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def save_model(model: Any, filename: str) -> None:
    """Save trained model to disk."""
    filepath = MODELS_DIR / filename
    joblib.dump(model, filepath)
    logger.info(f"Model saved to {filepath}")


def load_model(filename: str) -> Any:
    """Load trained model from disk."""
    filepath = MODELS_DIR / filename
    model = joblib.load(filepath)
    logger.info(f"Model loaded from {filepath}")
    return model


def save_processed_data(df: pd.DataFrame, filename: str) -> None:
    """Save processed data to disk."""
    filepath = PROCESSED_DATA_DIR / filename
    df.to_csv(filepath, index=False)
    logger.info(f"Processed data saved to {filepath}")


def load_processed_data(filename: str) -> pd.DataFrame:
    """Load processed data from disk."""
    filepath = PROCESSED_DATA_DIR / filename
    df = pd.read_csv(filepath)
    logger.info(f"Processed data loaded from {filepath}")
    return df


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_pred_proba: np.ndarray = None) -> Dict[str, float]:
    """Calculate classification metrics."""
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, 
        f1_score, roc_auc_score, confusion_matrix
    )
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1': f1_score(y_true, y_pred, zero_division=0),
    }
    
    if y_pred_proba is not None:
        metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
    
    return metrics


def print_metrics(metrics: Dict[str, float]) -> None:
    """Print metrics in a formatted way."""
    print("\n" + "=" * 50)
    print("Model Performance Metrics")
    print("=" * 50)
    for metric, value in metrics.items():
        print(f"{metric.upper():15s}: {value:.4f}")
    print("=" * 50 + "\n")

