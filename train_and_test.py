"""
Complete training and testing script for E-commerce Churn Prediction.
This script handles the full ML pipeline from data loading to model evaluation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix, classification_report
)

sys.path.append(str(Path(__file__).parent))
from src.config import *
from src.data_loader import load_kaggle_ecommerce_churn, create_sample_dataset
from src.pipeline import ChurnPipeline
from src.utils import save_model, calculate_metrics, print_metrics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_data():
    """Load dataset - tries Kaggle dataset first, then creates sample."""
    logger.info("Loading dataset...")
    
    try:
        # Try to load real Kaggle dataset
        df = load_kaggle_ecommerce_churn(RAW_DATA_DIR)
        
        # Handle TotalCharges if it's a string (Telco dataset)
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            df['TotalCharges'] = df['TotalCharges'].fillna(0)
            logger.info("TotalCharges converted to numeric")
        
        logger.info("✅ Kaggle dataset loaded successfully!")
        return df
    except Exception as e:
        logger.warning(f"Could not load Kaggle dataset: {e}")
        logger.info("Creating sample dataset instead...")
        
        if not TRAIN_FILE.exists():
            df = create_sample_dataset(n_samples=15000, save_path=TRAIN_FILE)
        else:
            df = pd.read_csv(TRAIN_FILE)
        
        logger.info("✅ Sample dataset loaded!")
        return df


def train_model(df: pd.DataFrame):
    """Train the churn prediction model."""
    logger.info("=" * 60)
    logger.info("Starting Model Training")
    logger.info("=" * 60)
    
    # Prepare features and target
    if 'customer_id' in df.columns:
        X = df.drop(columns=[TARGET_COLUMN, 'customer_id'])
    else:
        X = df.drop(columns=[TARGET_COLUMN])
    
    y = df[TARGET_COLUMN]
    
    logger.info(f"Features: {X.shape[1]}")
    logger.info(f"Samples: {X.shape[0]}")
    logger.info(f"Churn rate: {y.mean():.2%}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=MODEL_CONFIG['test_size'],
        random_state=MODEL_CONFIG['random_state'],
        stratify=y
    )
    
    logger.info(f"Train set: {X_train.shape[0]} samples")
    logger.info(f"Test set: {X_test.shape[0]} samples")
    
    # Train pipeline
    logger.info("\nTraining pipeline...")
    pipeline = ChurnPipeline()
    pipeline.fit(X_train, y_train)
    
    # Evaluate on test set
    logger.info("\nEvaluating on test set...")
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = calculate_metrics(y_test, y_pred, y_pred_proba)
    print_metrics(metrics)
    
    # Detailed classification report
    logger.info("\nClassification Report:")
    logger.info("\n" + classification_report(y_test, y_pred))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    logger.info("\nConfusion Matrix:")
    logger.info(f"\n{cm}")
    logger.info(f"\nTrue Negatives: {cm[0,0]}, False Positives: {cm[0,1]}")
    logger.info(f"False Negatives: {cm[1,0]}, True Positives: {cm[1,1]}")
    
    # Save model
    model_path = MODELS_DIR / "final_pipeline.pkl"
    pipeline.save(model_path)
    logger.info(f"\n✅ Model saved to {model_path}")
    
    return pipeline, metrics, X_test, y_test, y_pred, y_pred_proba


def evaluate_business_impact(y_test, y_pred, y_pred_proba):
    """Evaluate business impact of the model."""
    logger.info("\n" + "=" * 60)
    logger.info("Business Impact Analysis")
    logger.info("=" * 60)
    
    # Calculate potential savings
    retention_cost = BUSINESS_RULES['retention_cost']
    acquisition_cost = BUSINESS_RULES['acquisition_cost']
    
    # True positives: Correctly identified churners
    tp = ((y_test == 1) & (y_pred == 1)).sum()
    
    # False negatives: Missed churners (will churn but not identified)
    fn = ((y_test == 1) & (y_pred == 0)).sum()
    
    # Potential savings from retention campaigns
    potential_savings = tp * (acquisition_cost - retention_cost)
    
    # Lost opportunity cost (missed churners)
    lost_opportunity = fn * acquisition_cost
    
    logger.info(f"\nRetention Campaigns Needed: {tp}")
    logger.info(f"Retention Cost: ${tp * retention_cost:,}")
    logger.info(f"Potential Savings (vs Acquisition): ${potential_savings:,}")
    logger.info(f"\nMissed Churners: {fn}")
    logger.info(f"Lost Opportunity Cost: ${lost_opportunity:,}")
    logger.info(f"\nNet Benefit: ${potential_savings - lost_opportunity:,}")


def main():
    """Main training and testing function."""
    try:
        # Load data
        df = load_data()
        
        # Train model
        pipeline, metrics, X_test, y_test, y_pred, y_pred_proba = train_model(df)
        
        # Business impact
        evaluate_business_impact(y_test, y_pred, y_pred_proba)
        
        # Final summary
        logger.info("\n" + "=" * 60)
        logger.info("Training Complete!")
        logger.info("=" * 60)
        logger.info(f"\nModel Performance:")
        logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall: {metrics['recall']:.4f}")
        logger.info(f"  F1-Score: {metrics['f1']:.4f}")
        logger.info(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
        
        logger.info(f"\n✅ Model is ready for deployment!")
        logger.info(f"   Model location: {MODELS_DIR / 'final_pipeline.pkl'}")
        logger.info(f"\nNext steps:")
        logger.info(f"   1. Test the API: python app.py")
        logger.info(f"   2. Run Streamlit app: streamlit run streamlit_app.py")
        logger.info(f"   3. Review notebooks for detailed analysis")
        
    except Exception as e:
        logger.error(f"Error during training: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

