import streamlit as st
from streamlit_oauth import OAuth2Component
import requests
import logging
import os
from datetime import datetime
from report_generator import generate_pdf_report, send_email_with_report
from data_loader import load_data
from model_trainer import train_model
from predictor import make_prediction
from visualizer import plot_qchat_score
from config import DATA_PATH, QCHAT_THRESHOLD, FEATURE_COLS, QUESTIONS, OPTIONS

# --- Logging setup ---
logging.basicConfig(filename='asd_app.log', level=logging.DEBUG)

# --- OAuth2 Setup ---
redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]

google = OAuth2Component(client_id=client_id, client_secret=client_secret)

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# --- Login Flow ---
if not st.session_state.logged_in:
    result = google.authorize_button(
        name="Continue with Google",
        icon="🔐",
        redirect_uri=redirect_uri,
        scope="openid email profile",
        key="google_login",
    )

    if result:
        try:
            access_token = result.get("token", {}).get("access_token")
            if not access_token:
                st.error("Access token not found in OAuth result.")
                st.stop()

            headers = {"Authorization": f"Bearer {access_token}"}
            userinfo_response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo", headers=headers
            )

            if userinfo_response.ok:
                user_info = userinfo_response.json()
                st.session_state.logged_in = True
                st.session_state.user_info = user_info
                st.success(f"Logged in as {user_info.get('email')}")
            else:
                st.error("Failed to fetch user info from Google.")
                st.stop()

        except Exception as e:
            st.error(f"OAuth error: {e}")
            st.stop()
else:
    st.write(f"Welcome, {st.session_state.user_info.get('name', 'User')}!")

# --- Title and Introduction ---
st.title("🧠 Autism Spectrum Disorder Analysis App")
st.write("This app predicts the likelihood of ASD based on Q-CHAT-10 responses. It also generates reports if you're logged in.")
st.markdown("---")

# --- Load Data and Train Model ---
@st.cache_data
def cached_load_data():
    return load_data()

df = cached_load_data()
if df is None:
    logging.error("Data loading failed")
    st.error("Failed to load dataset.")
    st.stop()

@st.cache_resource
def cached_train_model(data):
    return train_model(data)

model = cached_train_model(df)
if model is None:
    logging.error("Model training/loading failed")
    st.error("Failed to load or train model.")
    st.stop()

# --- ASD Prediction Form ---
with st.form("ASD Form"):
    answers = [st.selectbox(q, [''] + OPTIONS, key=f"q{i}", index=0) for i, q in enumerate(QUESTIONS)]
    jaundice = st.radio("Was the child born with jaundice?", ['Yes', 'No'])
    family_asd = st.radio("Is there a family member with ASD?", ['Yes', 'No'])
    age_mons = st.slider("Age of child (months):", 12, 48, 24)
    Sex = st.radio('Gender of the toddler', ['m', 'f'])
    Ethnicity = st.text_input('Enter the Ethnicity of the toddler')
    Who_completed_the_test = st.selectbox(
        "Who completed the test?",
        ['Mother', 'Parent', 'Health Care Professional', 'Family member'],
        index=0
    )
    submitted = st.form_submit_button("Submit")

# --- On Form Submission ---
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
            'name': st.session_state.user_info['name'],
            'email': st.session_state.user_info['email'],
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
            user_reports_dir = os.path.join("user_reports", st.session_state.user_info['email'])
            os.makedirs(user_reports_dir, exist_ok=True)
            pdf_path = generate_pdf_report(result_data)
            final_pdf_path = os.path.join(user_reports_dir, os.path.basename(pdf_path))
            os.replace(pdf_path, final_pdf_path)
            send_email_with_report(st.session_state.user_info['email'], final_pdf_path)
            st.success("Report generated and sent to your email successfully.")
        except Exception as e:
            st.error(f"Error generating or sending report: {e}")
    else:
        st.warning("Please log in to save or send the report.")
