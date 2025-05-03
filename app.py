import streamlit as st
import logging
import os
from datetime import datetime
from auth import login_user
from report_generator import generate_pdf_report, send_email_with_report
from data_loader import load_data
from model_trainer import train_model  # Ensure this import is correct
from predictor import make_prediction
from visualizer import plot_qchat_score
from config import DATA_PATH, QCHAT_THRESHOLD, FEATURE_COLS, QUESTIONS, OPTIONS

logging.basicConfig(filename='asd_app.log', level=logging.DEBUG)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "trigger_report" not in st.session_state:
    st.session_state.trigger_report = False

# --- UI Buttons on the Right ---
col1, col2, col3 = st.columns([6, 1, 1])

with col2:
    if not st.session_state.logged_in:
        if st.button("Login"):
            user_info = login_user()
            if user_info:
                st.session_state.logged_in = True
                st.session_state.user_info = user_info
                st.success(f"Logged in as {user_info.get('email')}")
            else:
                st.error("Login failed. Try again.")

with col3:
    if st.button("Report"):
        if not st.session_state.logged_in:
            st.warning("login for report")
            st.session_state.trigger_report = True
        else:
            st.session_state.trigger_report = True

# Extract user info safely
user_info = st.session_state.user_info if st.session_state.logged_in else {}
user_email = user_info.get("email", "")
user_name = user_info.get("name", "User")

# --- Main App Content ---
st.title("🧠 Autism Spectrum Disorder Analysis App")
st.write("This app predicts the likelihood of ASD based on Q-CHAT-10 responses. It also generates reports if you're logged in.")
st.markdown("---")

# Load data and model
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

# Only show previous reports if logged in
if st.session_state.logged_in:
    user_reports_dir = os.path.join("user_reports", user_email)
    os.makedirs(user_reports_dir, exist_ok=True)
    existing_reports = [f for f in os.listdir(user_reports_dir) if f.endswith(".pdf")]

    if existing_reports:
        st.subheader("📄 Your Past Reports")
        for rep in existing_reports:
            with open(os.path.join(user_reports_dir, rep), "rb") as f:
                st.download_button(label=f"Download {rep}", data=f, file_name=rep)
    else:
        st.info("No previous reports found.")

# --- Form for ASD Prediction ---
with st.form("ASD Form"):
    answers = [st.selectbox(q, [''] + OPTIONS, key=f"q{i}", index=0) for i, q in enumerate(QUESTIONS)]
    jaundice = st.radio("Was the child born with jaundice?", ['Yes', 'No'])
    family_asd = st.radio("Is there a family member with ASD?", ['Yes', 'No'])
    age_mons = st.slider("Age of child (months):", 12, 48, 24)
    Sex = st.radio('Gender of the toddler', ['m', 'f'])
    Ethnicity = st.text_input('Enter the Ethnicity of the toddler')
    Who_completed_the_test = st.selectbox("Who completed the test?", ['Mother', 'Parent', 'Health Care Professional', 'Family member'], index=0)
    submitted = st.form_submit_button("Submit")

if submitted:
    if '' in answers:
        st.error("Please answer all questions.")
        st.stop()

    qchat_score, ml_result, proba, binary_answers = make_prediction(
        model, answers, jaundice, family_asd, age_mons, FEATURE_COLS, QCHAT_THRESHOLD
    )

    st.subheader("🔍 Results")
    st.markdown(f"- **Q-Chat-10 Score**: {qchat_score}")
    st.markdown(f"- **Prediction**: {ml_result}")
    plot_qchat_score(qchat_score)

    if st.session_state.logged_in:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_data = {
            'name': user_name,
            'email': user_email,
            'timestamp': timestamp,
            'Qchat-10 Score': qchat_score,
            'ML Prediction': ml_result,
            'Confidence': f"{proba:.2f}",
            'Age (Months)': age_mons,
            'Sex': Sex,
            'Ethnicity': Ethnicity,
            'Jaundice': jaundice,
            'Family with ASD': family_asd,
            'Who Completed': Who_completed_the_test,
        }

        try:
            user_reports_dir = os.path.join("user_reports", user_email)
            os.makedirs(user_reports_dir, exist_ok=True)
            pdf_path = generate_pdf_report(result_data)
            final_pdf_path = os.path.join(user_reports_dir, os.path.basename(pdf_path))
            os.replace(pdf_path, final_pdf_path)
            send_email_with_report(user_email, final_pdf_path)
            st.success("Report generated and sent to your email successfully.")
        except Exception as e:
            st.error(f"Error generating or sending report: {e}")
    else:
        st.warning("Please login to save or send the report.")
