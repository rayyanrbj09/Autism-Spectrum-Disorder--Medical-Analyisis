# model_trainer.py
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from src.config import FEATURE_COLS

MODEL_PATH = r'models/asd_model.joblib'

def train_model(data):
    """
    Train a Random Forest model or load it if it exists.
    Returns: Trained or loaded model.
    """
    try:
        # Check if the model file exists
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model

        # If no model exists, train a new one
        x = data[FEATURE_COLS].copy()
        y = data['Class ASD Traits'].copy()

        # Convert Q-Chat answers to binary
        for col in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']:
            x[col] = x[col].astype(str).str.strip().str.lower().map(
                lambda val: 1 if val in ['sometimes', 'rarely', 'never'] else 0
            ).fillna(0)
        x['A10'] = x['A10'].astype(str).str.strip().str.lower().map(
            lambda val: 1 if val in ['always', 'usually', 'sometimes'] else 0
        ).fillna(0)

        x = x.apply(pd.to_numeric, errors='coerce').fillna(0)
        valid_idx = y.notna()
        x = x[valid_idx]
        y = y[valid_idx].astype(int)

        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', max_depth=5)
        model.fit(x, y)

        # Save the trained model
        joblib.dump(model, MODEL_PATH)
        st.write("Trained and saved new model.")

        return model
    except Exception as e:
        st.error(f"Error training or loading model: {e}")
        return None