import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

st.set_page_config(page_title="ASD Prediction App", layout="centered")

DATA_PATH = 'datasets 1/Toddler Autism dataset July 2018.csv'
LOG_PATH = 'user_predictions.csv'

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data.columns = [col.strip() for col in data.columns]
    data['Jaundice'] = data['Jaundice'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    data['Family_mem_with_ASD'] = data['Family_mem_with_ASD'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    data['Class ASD Traits'] = data['Class ASD Traits'].apply(lambda x: 1 if str(x).strip().upper() == 'YES' else 0)
    return data

def train_model(data):
    feature_cols = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Jaundice', 'Family_mem_with_ASD', 'Age_Mons']
    x = data[feature_cols].copy()
    y = data['Class ASD Traits'].copy()

    # Convert Q-Chat responses to binary
    for col in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A10']:
        x[col] = x[col].apply(lambda x: 1 if str(x).strip().lower() in ['sometimes', 'rarely', 'never'] else 0)
    x['A9'] = x['A9'].apply(lambda x: 1 if str(x).strip().lower() in ['always', 'usually', 'sometimes'] else 0)

    # Convert all to numeric and fill missing values
    x = x.apply(pd.to_numeric, errors='coerce').fillna(0)
    y = pd.to_numeric(y, errors='coerce').fillna(0)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x, y)

    return model, feature_cols

def convert_answers_to_binary(answers):
    binary_values = []
    for i, answer in enumerate(answers):
        answer = answer.lower()
        if i == 9:
            binary_values.append(1 if answer in ['always', 'usually', 'sometimes'] else 0)
        else:
            binary_values.append(1 if answer in ['sometimes', 'rarely', 'never'] else 0)
    return binary_values

def plot_qchat_score(score):
    fig, ax = plt.subplots(figsize=(8, 1.5))
    colors = ['green' if i <= 3 else 'orange' if i <= 6 else 'red' for i in range(11)]
    for i in range(11):
        ax.barh(0, 1, left=i, color=colors[i])
    ax.axvline(score, color='blue', linestyle='--', linewidth=2, label=f'Score: {score}')
    ax.set_yticks([])
    ax.set_xticks(range(11))
    ax.set_title('ASD Trait Inclination Based on Q-Chat-10')
    ax.set_xlabel('Score (0–10)')
    ax.legend()
    st.pyplot(fig)

# Streamlit UI
st.title("🧠 Autism Spectrum Disorder (ASD) Prediction System")
st.write("This app predicts the likelihood of Autism Spectrum Disorder (ASD) in children using the Q-Chat-10 test.")

questions = [
    "1. Does your child look at you when you call his/her name?",
    "2. How easy is it for you to get eye contact with your child?",
    "3. Does your child point to indicate that s/he wants something?",
    "4. Does your child point to share interest with you?",
    "5. Does your child pretend?",
    "6. Does your child follow where you’re looking?",
    "7. If someone is visibly upset, does your child show signs of wanting to comfort them?",
    "8. Would you describe your child’s first words as:",
    "9. Does your child use simple gestures?",
    "10. Does your child stare at nothing with no apparent purpose?"
]

options = ['Always', 'Usually', 'Sometimes', 'Rarely', 'Never']

with st.form("ASD Form"):
    answers = [st.selectbox(q, options, key=i) for i, q in enumerate(questions)]
    jaundice = st.radio("Was the child born with jaundice?", ['Yes', 'No'])
    family_asd = st.radio("Is there a family member with ASD?", ['Yes', 'No'])
    sex = st.radio("Gender of the child:", ['Male', 'Female'])
    ethnicity = st.text_input("Enter the child's ethnicity:")
    age_mons = st.slider("Age of the child (in months):", 12, 48, 24)
    who_completed = st.selectbox("Who completed the test?", ['Parent', 'Self', 'Health care professional', 'Other'])
    submitted = st.form_submit_button("Predict")

if submitted:
    data = load_data()
    model, feature_cols = train_model(data)
    binary_answers = convert_answers_to_binary(answers)
    jaundice_val = 1 if jaundice.lower() == 'yes' else 0
    family_asd_val = 1 if family_asd.lower() == 'yes' else 0

    input_vector = binary_answers + [jaundice_val, family_asd_val, age_mons]
    input_df = pd.DataFrame([input_vector], columns=feature_cols)

    prediction = model.predict(input_df)[0]
    result = "YES" if prediction < 5 else "NO"
    qchat_score = sum(binary_answers)

    st.subheader(f"ASD Prediction: **{result}**")
    st.write(f"Q-Chat-10 Score: **{qchat_score}**")
    plot_qchat_score(qchat_score)

    # Save prediction log
    if os.path.exists(LOG_PATH):
        case_no = len(pd.read_csv(LOG_PATH)) + 1
    else:
        case_no = 1

    new_entry = {
        'case_no': case_no,
        'A1': binary_answers[0], 'A2': binary_answers[1], 'A3': binary_answers[2],
        'A4': binary_answers[3], 'A5': binary_answers[4], 'A6': binary_answers[5],
        'A7': binary_answers[6], 'A8': binary_answers[7], 'A9': binary_answers[8],
        'A10': binary_answers[9], 'Jaundice': jaundice_val,
        'Family_mem_with_ASD': family_asd_val, 'Age_Mons': age_mons,
        'Qchat_10_Score': qchat_score, 'Sex': sex, 'Ethnicity': ethnicity,
        'Who_completed_the_test': who_completed, 'Class ASD Traits': 1 if result == "YES" else 0
    }

    if not os.path.exists(LOG_PATH):
        pd.DataFrame(columns=new_entry.keys()).to_csv(LOG_PATH, index=False, encoding='utf-8-sig')

    pd.DataFrame([new_entry]).to_csv(LOG_PATH, mode='a', header=False, index=False, encoding='utf-8-sig')
    
