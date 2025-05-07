# data_loader.py
import streamlit as st
import pandas as pd
import logging
from config import DATA_PATH

logging.basicConfig(filename='asd_app.log', level=logging.DEBUG)

def load_data():
    """
    Load and preprocess the dataset.
    Returns: Preprocessed DataFrame or None if loading fails.
    """
    logging.debug(f"Attempting to load dataset from: {DATA_PATH}")
    try:
        df = pd.read_csv(DATA_PATH)
        logging.debug("Dataset loaded successfully")
        df.columns = [col.strip() for col in df.columns]
        
        # Validate required columns
        required_cols = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 
                        'Jaundice', 'Family_mem_with_ASD', 'Age_Mons', 'Class ASD Traits']
        if not all(col in df.columns for col in required_cols):
            missing_cols = set(required_cols) - set(df.columns)
            logging.error(f"Missing columns in dataset: {missing_cols}")
            st.error(f"Dataset missing required columns: {missing_cols}")
            return None
        
        # Preprocess Jaundice
        if df['Jaundice'].dtype == object:  # Likely strings
            df['Jaundice'] = df['Jaundice'].astype(str).str.strip().str.lower().map({'yes': 1, 'no': 0, 'nan': 0}).fillna(0)
        else:  # Already numeric
            df['Jaundice'] = pd.to_numeric(df['Jaundice'], errors='coerce').fillna(0).astype(int)

        # Preprocess Family_mem_with_ASD
        if df['Family_mem_with_ASD'].dtype == object:
            df['Family_mem_with_ASD'] = df['Family_mem_with_ASD'].astype(str).str.strip().str.lower().map({'yes': 1, 'no': 0, 'nan': 0}).fillna(0)
        else:
            df['Family_mem_with_ASD'] = pd.to_numeric(df['Family_mem_with_ASD'], errors='coerce').fillna(0).astype(int)

        # Preprocess Class ASD Traits
        if df['Class ASD Traits'].dtype == object:
            df['Class ASD Traits'] = df['Class ASD Traits'].astype(str).str.strip().str.upper().map({'YES': 1, 'NO': 0, 'nan': 0}).fillna(0)
        else:
            df['Class ASD Traits'] = pd.to_numeric(df['Class ASD Traits'], errors='coerce').fillna(0).astype(int)

        logging.debug("Dataset preprocessed successfully")
        return df
    except FileNotFoundError:
        logging.error(f"Dataset not found at {DATA_PATH}")
        
        return None
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        st.error(f"Error loading dataset: {e}")
        return None