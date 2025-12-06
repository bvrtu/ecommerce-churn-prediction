"""
Script to download Kaggle dataset for E-commerce Churn Prediction.

Popular datasets:
1. 'aravindh1/ecommerce-customer-churn' - E-commerce customer churn dataset
2. 'blastchar/telco-customer-churn' - Telco customer churn (can be adapted)
3. 'carl24/ecommerce-customer-churn-prediction' - E-commerce churn prediction

Usage:
    python download_kaggle_dataset.py
"""

import sys
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).parent))
from src.config import RAW_DATA_DIR
from src.data_loader import download_kaggle_dataset, load_kaggle_ecommerce_churn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Popular e-commerce churn datasets
DATASETS = {
    'ecommerce-churn-1': {
        'name': 'aravindh1/ecommerce-customer-churn',
        'description': 'E-commerce Customer Churn Dataset'
    },
    'ecommerce-churn-2': {
        'name': 'carl24/ecommerce-customer-churn-prediction',
        'description': 'E-commerce Customer Churn Prediction'
    },
    'telco-churn': {
        'name': 'blastchar/telco-customer-churn',
        'description': 'Telco Customer Churn (can be adapted for e-commerce)'
    }
}


def main():
    """Download Kaggle dataset."""
    print("=" * 60)
    print("Kaggle Dataset Downloader for E-commerce Churn Prediction")
    print("=" * 60)
    print("\nAvailable datasets:")
    for key, info in DATASETS.items():
        print(f"  {key}: {info['name']} - {info['description']}")
    
    print("\n" + "=" * 60)
    print("NOTE: You need Kaggle API credentials to download datasets.")
    print("1. Go to https://www.kaggle.com/settings")
    print("2. Scroll to 'API' section")
    print("3. Click 'Create New Token' to download kaggle.json")
    print("4. Place kaggle.json in ~/.kaggle/ directory")
    print("5. Install kaggle: pip install kaggle")
    print("=" * 60)
    
    # Use the first dataset by default
    dataset_key = 'ecommerce-churn-1'
    dataset_name = DATASETS[dataset_key]['name']
    
    print(f"\nDownloading dataset: {dataset_name}")
    print("If this fails, you can manually download from Kaggle and place in data/raw/")
    
    try:
        download_kaggle_dataset(dataset_name, RAW_DATA_DIR)
        print("\n✅ Dataset downloaded successfully!")
        print(f"Location: {RAW_DATA_DIR}")
        
        # Try to load and preview
        try:
            df = load_kaggle_ecommerce_churn(RAW_DATA_DIR)
            print(f"\nDataset preview:")
            print(f"Shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"\nFirst few rows:")
            print(df.head())
        except Exception as e:
            logger.warning(f"Could not preview dataset: {e}")
            print("\nPlease check the downloaded files and adjust column names if needed.")
    
    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print("\nAlternative: Manual download")
        print("1. Go to https://www.kaggle.com/datasets")
        print("2. Search for 'ecommerce customer churn'")
        print("3. Download the dataset")
        print("4. Extract and place CSV files in data/raw/ directory")
        print("5. Make sure the churn column is named 'churn' or update data_loader.py")


if __name__ == "__main__":
    main()

