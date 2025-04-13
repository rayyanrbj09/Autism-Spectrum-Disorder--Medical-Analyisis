# main.py
import streamlit as st
import logging
import pandas as pd

logging.basicConfig(filename='asd_app.log', level=logging.DEBUG)
logging.debug("Starting Streamlit app")

try:
    from data_loader import load_data
    from model_trainer import train_model
    from predictor import make_prediction
    from visualizer import plot_qchat_score
    from config import DATA_PATH, QCHAT_THRESHOLD, FEATURE_COLS, QUESTIONS, OPTIONS
except ImportError as e:
    logging.error(f"Import error: {e}")
    st.error(f"Failed to import modules: {e}")
    st.stop()

st.set_page_config(page_title="ASD Prediction", layout="centered")

try:
    logging.debug("Rendering initial UI")
    st.title("🧠 Autism Spectrum Disorder (ASD) Prediction App")
    st.write("This app uses Q-Chat-10 screening and a machine learning model to predict ASD likelihood in toddlers.")
    st.markdown("**Disclaimer**: This tool provides an estimate based on Q-Chat-10 and machine learning. Consult a healthcare professional for a formal diagnosis.")

    logging.debug("Loading data")
    @st.cache_data
    def cached_load_data():
        return load_data()

    df = cached_load_data()
    if df is None:
        logging.error("Data loading failed")
        st.error("Failed to load dataset. Please check the file path and try again.")
        st.stop()

    logging.debug("Loading or training model")
    @st.cache_resource
    def cached_train_model(data):
        return train_model(data)

    model = cached_train_model(df)
    if model is None:
        logging.error("Model training/loading failed")
        st.error("Failed to load or train model. Check logs for details.")
        st.stop()

    logging.debug("Rendering form")
    with st.form("ASD Form"):
        answers = [st.selectbox(q, [''] + OPTIONS, key=f"q{i}", index=0) for i, q in enumerate(QUESTIONS)]
        jaundice = st.radio("Was the child born with jaundice?", ['Yes', 'No'])
        family_asd = st.radio("Is there a family member with ASD?", ['Yes', 'No'])
        age_mons = st.slider("Age of child (months):", 12, 48, 24)
        Sex = st.radio('Gender of the toddler', ['m','f'])
        Ethnicity = st.text_input('Enter the Ethnicity of the toddler')
        Who_completed_the_test = st.selectbox("Who completed the test?", ['Mother','Parent', 'Health Care Professional', 'Family member'], index=0)
        submitted = st.form_submit_button("Submit")       

    if submitted:
        logging.debug("Form submitted")
        if '' in answers:
            logging.warning("Incomplete form submission")
            st.error("Please answer all questions.")
            st.stop()

        qchat_score, ml_result, proba, binary_answers = make_prediction(
            model, answers, jaundice, family_asd, age_mons, FEATURE_COLS, QCHAT_THRESHOLD
        )

        if qchat_score is None:
            logging.error("Prediction failed")
            st.error("Prediction failed. Check logs for details.")
            st.stop()

        st.subheader("🔍 Results:")
        st.markdown(f"- **Q-Chat-10 Score**: `{qchat_score}`")
        st.markdown(f"- **ML Prediction (Random Forest)**: `{ml_result}`")
        st.markdown(f"- **Model Confidence (Prob of ASD)**: `{proba:.2f}`")

        plot_qchat_score(qchat_score)

        # Create new row with user input and prediction
        new_row = {
            'A1': binary_answers[0],
            'A2': binary_answers[1],
            'A3': binary_answers[2],
            'A4': binary_answers[3],
            'A5': binary_answers[4],
            'A6': binary_answers[5],
            'A7': binary_answers[6],
            'A8': binary_answers[7],
            'A9': binary_answers[8],
            'A10': binary_answers[9],
            'Qchat-10-Score': qchat_score,
            'Age_Mons': age_mons,
            'Sex': Sex,
            'Ethnicity' : Ethnicity,
            'Jaundice': 1 if jaundice.lower() == 'yes' else 0,
            'Family_mem_with_ASD': 1 if family_asd.lower() == 'yes' else 0,
            'Who_completed_the_test': Who_completed_the_test,
            'Class ASD Traits': 1 if ml_result == "YES" else 0
        }

        # Append new row to the dataset
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Save the updated dataset
        try:
            df.to_csv(DATA_PATH, index=False)
            st.success("Dataset updated successfully with your input!")
        except Exception as e:
            st.error(f"Failed to update dataset: {e}")

except Exception as e:
    logging.error(f"Unexpected error: {e}")
    st.error(f"An unexpected error occurred: {e}")