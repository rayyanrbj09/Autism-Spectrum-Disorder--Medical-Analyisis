# predictor.py
import streamlit as st
import pandas as pd

def convert_answers(answers):
    """
    Convert Q-Chat answers to binary values.
    Returns: List of binary values.
    """
    binary = []
    valid_options = ['always', 'usually', 'sometimes', 'rarely', 'never']
    for i, ans in enumerate(answers):
        ans = ans.strip().lower()
        if ans not in valid_options:
            st.warning(f"Invalid answer for question {i+1}: {ans}. Defaulting to 'Never'.")
            ans = 'never'
        if i == 9:  # A10 has reversed scoring
            binary.append(1 if ans in ['always', 'usually', 'sometimes'] else 0)
        else:
            binary.append(1 if ans in ['sometimes', 'rarely', 'never'] else 0)
    return binary

def make_prediction(model, answers, jaundice, family_asd, age_mons, feature_cols, threshold):
    """
    Generate ML-based prediction based on Q-Chat score threshold.
    Returns: Q-Chat score, ML result, ML probability, and binary answers.
    """
    try:
        binary_answers = convert_answers(answers)
        jaundice_val = 1 if jaundice.lower() == 'yes' else 0
        family_val = 1 if family_asd.lower() == 'yes' else 0
        input_vec = binary_answers + [jaundice_val, family_val, age_mons]

        if len(input_vec) != len(feature_cols):
            st.error("Input vector length mismatch with expected features.")
            return None, None, None, None

        input_df = pd.DataFrame([input_vec], columns=feature_cols)
        qchat_score = sum(binary_answers)
        
        ml_result = "YES" if qchat_score > threshold else "NO"
        proba = model.predict_proba(input_df)[0][1]

        return qchat_score, ml_result, proba, binary_answers
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None, None, None, None