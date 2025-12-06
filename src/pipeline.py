"""
Final ML Pipeline for E-commerce Churn Prediction.
This script contains the complete preprocessing and training pipeline.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import logging
from typing import Tuple, Dict, Any

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectKBest, f_classif

import xgboost as xgb
import lightgbm as lgb
# import catboost as cb  # Optional - not used in current pipeline

from src.config import *
from src.utils import save_model, save_processed_data, calculate_metrics, print_metrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChurnPipeline:
    """Complete pipeline for churn prediction."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.label_encoders = {}
        self.feature_selector = None
        self.model = None
        self.feature_names = None
        
    def preprocess(self, df: pd.DataFrame, is_training: bool = True) -> pd.DataFrame:
        """Preprocess the data."""
        df = df.copy()
        
        # Handle TotalCharges if it's a string (Telco dataset)
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            df['TotalCharges'] = df['TotalCharges'].fillna(0)
        
        # Remove non-feature columns
        cols_to_remove = ['customer_id', 'customerID', 'signup_date'] if 'customer_id' in df.columns or 'customerID' in df.columns else []
        if 'signup_date' in df.columns:
            cols_to_remove.append('signup_date')
        df = df.drop(columns=[col for col in cols_to_remove if col in df.columns])
        
        # Handle missing values
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if TARGET_COLUMN in numerical_cols:
            numerical_cols.remove(TARGET_COLUMN)
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Impute numerical missing values
        if len(numerical_cols) > 0:
            if is_training:
                df[numerical_cols] = self.imputer.fit_transform(df[numerical_cols])
            else:
                df[numerical_cols] = self.imputer.transform(df[numerical_cols])
        
        # Encode categorical variables
        for col in categorical_cols:
            if is_training:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str).fillna('Unknown'))
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    # Handle unseen categories
                    df[col] = df[col].astype(str).fillna('Unknown')
                    unseen_mask = ~df[col].isin(self.label_encoders[col].classes_)
                    if unseen_mask.any():
                        df.loc[unseen_mask, col] = self.label_encoders[col].classes_[0]
                    df[col] = self.label_encoders[col].transform(df[col])
                else:
                    df[col] = 0
        
        # Feature engineering
        if 'days_since_signup' in df.columns and 'total_purchases' in df.columns:
            df['purchases_per_day'] = df['total_purchases'] / (df['days_since_signup'] + 1)
        
        if 'total_spent' in df.columns and 'total_purchases' in df.columns:
            df['avg_order_value'] = df['total_spent'] / (df['total_purchases'] + 1)
        
        if 'days_since_last_purchase' in df.columns and 'days_since_signup' in df.columns:
            df['activity_ratio'] = 1 - (df['days_since_last_purchase'] / (df['days_since_signup'] + 1))
        
        return df
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Train the pipeline."""
        logger.info("Starting pipeline training...")
        
        # Preprocess
        X_processed = self.preprocess(X, is_training=True)
        
        # Convert to numpy if needed
        if isinstance(X_processed, pd.DataFrame):
            X_processed = X_processed.values
        
        # Handle class imbalance
        if FEATURE_CONFIG['handle_imbalance']:
            try:
                # Convert y to numpy array if it's a pandas Series
                y_array = y.values if hasattr(y, 'values') else y
                smote = SMOTE(random_state=MODEL_CONFIG['random_state'])
                X_processed, y_array = smote.fit_resample(X_processed, y_array)
                y = pd.Series(y_array) if isinstance(y, pd.Series) else y_array
                logger.info(f"After SMOTE - X shape: {X_processed.shape}, y distribution: {pd.Series(y).value_counts().to_dict()}")
            except Exception as e:
                logger.warning(f"SMOTE failed: {e}. Continuing without SMOTE.")
                y_array = y.values if hasattr(y, 'values') else y
        
        # Feature selection
        if FEATURE_CONFIG['feature_selection']:
            try:
                self.feature_selector = SelectKBest(
                    score_func=f_classif, 
                    k=min(FEATURE_CONFIG['top_n_features'], X_processed.shape[1])
                )
                X_processed = self.feature_selector.fit_transform(X_processed, y)
                self.feature_names = self.feature_selector.get_support()
                logger.info(f"Selected {X_processed.shape[1]} features")
            except Exception as e:
                logger.warning(f"Feature selection failed: {e}. Using all features.")
                self.feature_selector = None
        
        # Scale features
        if FEATURE_CONFIG['numerical_scaling']:
            X_processed = self.scaler.fit_transform(X_processed)
        
        # Train model
        self.model = xgb.XGBClassifier(**XGBOOST_PARAMS)
        self.model.fit(X_processed, y)
        logger.info("Pipeline training completed!")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        X_processed = self.preprocess(X, is_training=False)
        
        # Convert to numpy if needed
        if isinstance(X_processed, pd.DataFrame):
            X_processed = X_processed.values
        
        if self.feature_selector:
            X_processed = self.feature_selector.transform(X_processed)
        
        if FEATURE_CONFIG['numerical_scaling']:
            X_processed = self.scaler.transform(X_processed)
        
        return self.model.predict(X_processed)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Get prediction probabilities."""
        X_processed = self.preprocess(X, is_training=False)
        
        # Convert to numpy if needed
        if isinstance(X_processed, pd.DataFrame):
            X_processed = X_processed.values
        
        if self.feature_selector:
            X_processed = self.feature_selector.transform(X_processed)
        
        if FEATURE_CONFIG['numerical_scaling']:
            X_processed = self.scaler.transform(X_processed)
        
        return self.model.predict_proba(X_processed)
    
    def save(self, filepath: Path) -> None:
        """Save the pipeline."""
        pipeline_dict = {
            'scaler': self.scaler,
            'imputer': self.imputer,
            'label_encoders': self.label_encoders,
            'feature_selector': self.feature_selector,
            'model': self.model,
            'feature_names': self.feature_names,
        }
        joblib.dump(pipeline_dict, filepath)
        logger.info(f"Pipeline saved to {filepath}")
    
    def load(self, filepath: Path) -> None:
        """Load the pipeline."""
        pipeline_dict = joblib.load(filepath)
        self.scaler = pipeline_dict['scaler']
        self.imputer = pipeline_dict['imputer']
        self.label_encoders = pipeline_dict['label_encoders']
        self.feature_selector = pipeline_dict['feature_selector']
        self.model = pipeline_dict['model']
        self.feature_names = pipeline_dict['feature_names']
        logger.info(f"Pipeline loaded from {filepath}")


def main():
    """Main training function."""
    # Load data
    logger.info("Loading data...")
    df = pd.read_csv(TRAIN_FILE)
    logger.info(f"Data loaded. Shape: {df.shape}")
    
    # Prepare features and target
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=MODEL_CONFIG['test_size'],
        random_state=MODEL_CONFIG['random_state'],
        stratify=y
    )
    
    logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
    
    # Train pipeline
    pipeline = ChurnPipeline()
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    metrics = calculate_metrics(y_test, y_pred, y_pred_proba)
    print_metrics(metrics)
    
    # Save pipeline
    pipeline_path = MODELS_DIR / "final_pipeline.pkl"
    pipeline.save(pipeline_path)
    
    logger.info("Training completed successfully!")


if __name__ == "__main__":
    main()

