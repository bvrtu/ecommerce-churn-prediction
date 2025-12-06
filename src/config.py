"""
Configuration file for the E-commerce Churn Prediction project.
Contains paths, business rules, and model settings.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Model paths
MODELS_DIR = PROJECT_ROOT / "models"

# Output paths
OUTPUT_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset configuration
DATASET_NAME = "ecommerce_customer_churn"
TRAIN_FILE = RAW_DATA_DIR / "train.csv"
TEST_FILE = RAW_DATA_DIR / "test.csv"

# Target variable
TARGET_COLUMN = "churn"

# Business rules
BUSINESS_RULES = {
    "churn_definition": "Customer who has not made a purchase in the last 30 days",
    "high_value_threshold": 1000,  # High value customer threshold in currency
    "retention_cost": 50,  # Cost to retain a customer
    "acquisition_cost": 200,  # Cost to acquire a new customer
    "min_precision": 0.70,  # Minimum precision for production model
    "min_recall": 0.65,  # Minimum recall for production model
}

# Model configuration
MODEL_CONFIG = {
    "random_state": 42,
    "test_size": 0.2,
    "validation_size": 0.2,
    "cv_folds": 5,
    "scoring_metric": "roc_auc",
}

# Feature engineering
FEATURE_CONFIG = {
    "categorical_encoding": "target",  # target, onehot, label
    "numerical_scaling": True,
    "handle_imbalance": True,  # Use SMOTE or class weights
    "feature_selection": True,
    "top_n_features": 30,
}

# Model hyperparameters (will be optimized)
XGBOOST_PARAMS = {
    "n_estimators": 100,
    "max_depth": 6,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": MODEL_CONFIG["random_state"],
}

LIGHTGBM_PARAMS = {
    "n_estimators": 100,
    "max_depth": 6,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": MODEL_CONFIG["random_state"],
}

CATBOOST_PARAMS = {
    "iterations": 100,
    "depth": 6,
    "learning_rate": 0.1,
    "random_state": MODEL_CONFIG["random_state"],
    "verbose": False,
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
}

# Monitoring
MONITORING_CONFIG = {
    "log_predictions": True,
    "log_interval": 100,  # Log every N predictions
    "performance_threshold": 0.70,  # Alert if model performance drops below this
}

