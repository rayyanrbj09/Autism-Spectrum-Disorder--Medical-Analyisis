import streamlit as st
import os
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from src.utils.report_generator import generate_pdf_report
from src.core.data_loader import load_data
from src.core.model_trainer import train_model
from src.core.predictor import make_prediction
from src.utils.visualizer import plot_qchat_score
from src.config import DATA_PATH, QCHAT_THRESHOLD, FEATURE_COLS, QUESTIONS, OPTIONS, image1, image2

# Setup logging
LOG_FILE = r'logs/asd_app.log'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set page
st.set_page_config(page_title="ASD Screening test", layout="centered")
st.markdown("""
    <style>
    .stApp {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 18px;
    }
    h1 {
        font-family: 'Trebuchet MS', Arial, sans-serif;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🧠 Autism Spectrum Disorder - Prediction system (Screening test)")
st.write("This app predicts ASD likelihood based on Q-CHAT-10 responses and provides a downloadable PDF report.")
st.markdown(f"- **Disclaimer**: This app is for educational purposes only and might be used for medical diagnosis.")
st.markdown("---")

# === Caching the data and model ===
@st.cache_resource(show_spinner="🔃 Loading and training model...")
def get_model():
    df = load_data()
    model = train_model(df)
    return model

try:
    model = get_model()
except Exception as e:
    logging.error(f"Model loading/training failed: {e}")
    st.error("Failed to load data or train model.")
    st.stop()

# === Threaded Prediction ===
def make_prediction_async(model, *args):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(make_prediction, model, *args)
        return future.result()

# === Threaded PDF Generation ===
def generate_report_async(data):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(generate_pdf_report, data)
        return future.result()

# === Form Input ===
with st.form("ASD Form"):
    answers = [st.selectbox(q, [''] + OPTIONS, key=f"q{i}", index=0) for i, q in enumerate(QUESTIONS)]
    jaundice = st.radio("Was the child born with jaundice?", ['Yes', 'No'])
    family_asd = st.radio("Is there a family member with ASD?", ['Yes', 'No'])
    age_mons = st.slider("Age of child (months):", 12, 48, 24)
    sex = st.radio('Gender of the toddler', ['M', 'F'])
    ethnicity = st.text_input('Enter the Ethnicity of the toddler')
    who_completed = st.selectbox("Who completed the test?", ['Mother', 'Parent', 'Health Care Professional', 'Family member'], index=0)
    submitted = st.form_submit_button("🔍 Predict")

# === Prediction Logic ===
if submitted:
    if '' in answers:
        st.error("Please answer all the questions before submitting.")
        logging.warning("Incomplete form submitted.")
    else:
        try:
            qchat_score, ml_result, proba, binary_answers = make_prediction_async(
                model, answers, jaundice, family_asd, age_mons, FEATURE_COLS, QCHAT_THRESHOLD
            )

            st.subheader("🔎 Results")
            st.markdown(f"- **Q-Chat-10 Score**: `{qchat_score}`")
            st.markdown(f"- **Prediction**: `{ml_result}`")
            st.markdown(f"- **Confidence**: `{proba:.2f}`")
            plot_qchat_score(qchat_score)

            # === Result Data ===
            result_data = {
                'name': 'Anonymous User',
                'email': 'anonymous@example.com',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Qchat-10 Score': qchat_score,
                'ML Prediction': ml_result,
                'Confidence': f"{proba:.2f}",
                'Age (Months)': age_mons,
                'Sex': sex,
                'Ethnicity': ethnicity,
                'Jaundice': jaundice,
                'Family with ASD': family_asd,
                'Who Completed': who_completed,
            }

            st.markdown("---")
            st.subheader("📄 Generate Your Report")

            try:
                pdf_path = generate_report_async(result_data)
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download ASD Report (PDF)",
                            data=f,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
                    st.success("✅ Report successfully generated.")
                    logging.info(f"PDF report generated: {pdf_path}")
                else:
                    st.error("❌ Failed to generate report. Check logs.")
                    logging.error("PDF path does not exist or is empty.")
            except Exception as e:
                logging.error(f"Failed to generate or offer PDF: {e}")
                st.error("Failed to generate report.")

        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            st.error("Prediction failed. Please try again.")

# === Sidebar Footer ===
st.sidebar.info("Developed with ❤️ using Streamlit by Code-Craft")
