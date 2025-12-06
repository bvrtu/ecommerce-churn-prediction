"""
Data loading and preprocessing utilities.
This script helps download and prepare the dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import RAW_DATA_DIR, TRAIN_FILE, TEST_FILE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_kaggle_dataset(dataset_name: str, save_path: Path, files: list = None) -> None:
    """
    Download dataset from Kaggle.
    Requires kaggle API credentials in ~/.kaggle/kaggle.json
    
    Args:
        dataset_name: Kaggle dataset name (e.g., 'aravindh1/ecommerce-customer-churn')
        save_path: Directory to save the dataset
        files: Optional list of specific files to download
    """
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        logger.info(f"Downloading dataset: {dataset_name}")
        save_path.mkdir(parents=True, exist_ok=True)
        
        if files:
            for file in files:
                api.dataset_download_file(dataset_name, file, path=str(save_path))
        else:
            api.dataset_download_files(dataset_name, path=str(save_path), unzip=True)
        
        logger.info(f"Dataset downloaded successfully to {save_path}")
        
    except ImportError:
        logger.error("Kaggle API not installed. Install with: pip install kaggle")
        logger.info("Alternatively, you can manually download the dataset from Kaggle")
        raise
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        logger.info("Make sure you have:")
        logger.info("1. Kaggle API credentials in ~/.kaggle/kaggle.json")
        logger.info("2. kaggle package installed: pip install kaggle")
        raise


def load_kaggle_ecommerce_churn(dataset_path: Path = None) -> pd.DataFrame:
    """
    Load and preprocess a real Kaggle e-commerce churn dataset.
    This function handles common e-commerce churn dataset formats.
    """
    if dataset_path is None:
        dataset_path = RAW_DATA_DIR
    
    # Try to find the dataset file
    possible_files = ['train.csv', 'data.csv', 'ecommerce_churn.csv', 'customer_churn.csv', 'churn.csv']
    train_file = None
    
    for file in possible_files:
        file_path = dataset_path / file
        if file_path.exists():
            train_file = file_path
            break
    
    if train_file is None:
        # List available files
        available_files = list(dataset_path.glob('*.csv'))
        if available_files:
            train_file = available_files[0]
            logger.info(f"Using file: {train_file.name}")
        else:
            raise FileNotFoundError(f"No CSV file found in {dataset_path}")
    
    logger.info(f"Loading dataset from {train_file}")
    df = pd.read_csv(train_file)
    
    # Common column name mappings for churn datasets
    column_mappings = {
        'Churn': 'churn',
        'churn': 'churn',
        'Exited': 'churn',
        'is_churn': 'churn',
        'CustomerID': 'customer_id',
        'customer_id': 'customer_id',
        'Customer ID': 'customer_id',
    }
    
    # Rename columns if needed
    df = df.rename(columns=column_mappings)
    
    # Ensure churn column exists and is binary
    if 'churn' not in df.columns:
        # Try to find churn column with different names
        churn_cols = [col for col in df.columns if 'churn' in col.lower() or 'exited' in col.lower()]
        if churn_cols:
            df['churn'] = df[churn_cols[0]]
        else:
            raise ValueError("Churn column not found in dataset")
    
    # Convert churn to binary if needed
    if df['churn'].dtype == 'object':
        df['churn'] = df['churn'].map({'Yes': 1, 'No': 0, 'True': 1, 'False': 0, True: 1, False: 0})
    df['churn'] = df['churn'].astype(int)
    
    logger.info(f"Dataset loaded. Shape: {df.shape}")
    logger.info(f"Churn rate: {df['churn'].mean():.2%}")
    logger.info(f"Columns: {df.columns.tolist()}")
    
    return df


def create_sample_dataset(n_samples: int = 15000, save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Create a sample e-commerce churn dataset for demonstration.
    This is a synthetic dataset that mimics real e-commerce customer data.
    """
    np.random.seed(42)
    
    n_samples = n_samples
    
    # Generate customer features
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.normal(35, 12, n_samples).astype(int),
        'gender': np.random.choice(['Male', 'Female', 'Other'], n_samples),
        'city': np.random.choice(['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya'], n_samples),
        'membership_type': np.random.choice(['Basic', 'Premium', 'Gold'], n_samples, p=[0.5, 0.3, 0.2]),
        'signup_date': pd.date_range('2020-01-01', periods=n_samples, freq='D')[:n_samples],
        'total_purchases': np.random.poisson(15, n_samples),
        'total_spent': np.random.lognormal(5, 1, n_samples),
        'avg_order_value': np.random.lognormal(4, 0.8, n_samples),
        'days_since_last_purchase': np.random.exponential(30, n_samples).astype(int),
        'days_since_signup': np.random.exponential(365, n_samples).astype(int),
        'products_viewed': np.random.poisson(50, n_samples),
        'cart_abandonment_rate': np.random.beta(2, 5, n_samples),
        'customer_service_contacts': np.random.poisson(2, n_samples),
        'promo_emails_opened': np.random.poisson(10, n_samples),
        'mobile_app_usage': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'subscription_active': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
    }
    
    df = pd.DataFrame(data)
    
    # Create churn target based on features (realistic churn logic)
    churn_prob = (
        (df['days_since_last_purchase'] > 60) * 0.4 +
        (df['total_purchases'] < 5) * 0.3 +
        (df['customer_service_contacts'] > 5) * 0.2 +
        (df['cart_abandonment_rate'] > 0.7) * 0.1 +
        (df['subscription_active'] == 0) * 0.2 +
        np.random.random(n_samples) * 0.1
    )
    
    df['churn'] = (churn_prob > 0.5).astype(int)
    
    # Add some missing values
    missing_cols = ['customer_service_contacts', 'promo_emails_opened']
    for col in missing_cols:
        missing_idx = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
        df.loc[missing_idx, col] = np.nan
    
    # Ensure age is reasonable
    df['age'] = df['age'].clip(18, 80)
    
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path, index=False)
        logger.info(f"Sample dataset saved to {save_path}")
    
    return df


if __name__ == "__main__":
    # Create sample dataset if train file doesn't exist
    if not TRAIN_FILE.exists():
        logger.info("Creating sample dataset...")
        df = create_sample_dataset(n_samples=15000, save_path=TRAIN_FILE)
        logger.info(f"Dataset created with shape: {df.shape}")
        logger.info(f"Churn rate: {df['churn'].mean():.2%}")
    else:
        logger.info(f"Dataset already exists at {TRAIN_FILE}")

