import streamlit as st
import requests
import logging
import os
from datetime import datetime
from streamlit_oauth import OAuth2Component
from report_generator import generate_pdf_report, send_email_with_report
from data_loader import load_data
from model_trainer import train_model
from predictor import make_prediction
from visualizer import plot_qchat_score
from config import DATA_PATH, QCHAT_THRESHOLD, FEATURE_COLS, QUESTIONS, OPTIONS

# Initialize logging
logging.basicConfig(filename='asd_app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# OAuth credentials from Streamlit secrets
redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]

# Initialize the OAuth component
google = OAuth2Component(
    client_id=client_id,
    client_secret=client_secret,
)

# --- Helper Functions ---
def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

def load_and_train_model():
    try:
        # Load Data
        df = load_data()
        if df is None:
            logging.error("Failed to load dataset.")
            st.error("Failed to load dataset.")
            return None

        # Train Model
        model = train_model(df)
        if model is None:
            logging.error("Model training/loading failed.")
            st.error("Failed to load or train model.")
            return None

        return model
    except Exception as e:
        logging.error(f"Error in loading data or training model: {e}")
        st.error("Error in loading data or training model.")
        return None

def handle_oauth_flow():
    try:
        result = google.authorize_button(
            name="Login",
            redirect_uri=redirect_uri,
            scope="openid email profile",
            key="google_login",
        )

        if result:
            access_token = result.get("token", {}).get("access_token")
            if not access_token:
                logging.error("Access token not found in OAuth result.")
                st.error("Access token not found in OAuth result.")
                return None

            headers = {"Authorization": f"Bearer {access_token}"}
            userinfo_response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)

            if userinfo_response.ok:
                user_info = userinfo_response.json()
                st.session_state.logged_in = True
                st.session_state.user_info = user_info
                st.success(f"Logged in as {user_info.get('email')}")
                logging.info(f"User {user_info.get('email')} logged in successfully.")
                return user_info
            else:
                logging.error("Failed to fetch user info.")
                st.error("Failed to fetch user info.")
                return None
        else:
            return None
    except Exception as e:
        logging.error(f"OAuth login error: {e}")
        st.error(f"OAuth login error: {e}")
        return None

def generate_and_send_report(qchat_score, ml_result, proba, result_data):
    try:
        user_reports_dir = os.path.join("user_reports", st.session_state.user_info['email'])
        os.makedirs(user_reports_dir, exist_ok=True)
        pdf_path = generate_pdf_report(result_data)
        final_pdf_path = os.path.join(user_reports_dir, os.path.basename(pdf_path))
        os.replace(pdf_path, final_pdf_path)
        send_email_with_report(st.session_state.user_info['email'], final_pdf_path)
        st.success("✅ Report generated and sent to your email successfully.")
        logging.info("Report generated and sent successfully.")
    except Exception as e:
        logging.error(f"Error generating or sending report: {e}")
        st.error(f"Error generating or sending report: {e}")

# --- Main Flow ---
def main():
    # Initialize session state
    initialize_session_state()

    # --- Login Flow ---
    if not st.session_state.logged_in:
        user_info = handle_oauth_flow()
        if not user_info:
            return
    else:
        st.write(f"Welcome, {st.session_state.user_info.get('name', 'User')}!")

    # --- App Title ---
    st.title("🧠 Autism Spectrum Disorder Analysis App")
    st.write("This app predicts the likelihood of ASD based on Q-CHAT-10 responses and provides a downloadable PDF report.")
    st.markdown("---")

    # --- Load and Train ---
    model = load_and_train_model()
    if model is None:
        return

    # --- Prediction Form ---
    with st.form("ASD Form"):
        answers = [st.selectbox(q, [''] + OPTIONS, key=f"q{i}", index=0) for i, q in enumerate(QUESTIONS)]
        jaundice = st.radio("Was the child born with jaundice?", ['Yes', 'No'])
        family_asd = st.radio("Is there a family member with ASD?", ['Yes', 'No'])
        age_mons = st.slider("Age of child (months):", 12, 48, 24)
        Sex = st.radio('Gender of the toddler', ['m', 'f'])
        Ethnicity = st.text_input('Enter the Ethnicity of the toddler')
        Who_completed_the_test = st.selectbox("Who completed the test?", ['Mother', 'Parent', 'Health Care Professional', 'Family member'], index=0)
        submitted = st.form_submit_button("Submit")

    # --- Submission Logic ---
    if submitted:
        if '' in answers:
            st.error("Please answer all questions.")
            logging.warning("Some questions were left unanswered.")
            return

        qchat_score, ml_result, proba, binary_answers = make_prediction(
            model, answers, jaundice, family_asd, age_mons, FEATURE_COLS, QCHAT_THRESHOLD
        )

        st.subheader("🔍 Results")
        st.markdown(f"- **Q-Chat-10 Score**: {qchat_score}")
        st.markdown(f"- **Prediction**: {ml_result}")
        plot_qchat_score(qchat_score)

        # --- Report Generation ---
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

            # Generate and send report
            generate_and_send_report(qchat_score, ml_result, proba, result_data)
        else:
            st.warning("Please log in to save or send the report.")
            logging.warning("User not logged in, unable to generate report.")

# Run the app
if __name__ == "__main__":
    main()
