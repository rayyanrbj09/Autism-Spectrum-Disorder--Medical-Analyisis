import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def get_user_input():
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

    answers = []
    for q in questions:
        while True:
            response = input(f"{q} (Always/Usually/Sometimes/Rarely/Never): ").strip().capitalize()
            if response in ['Always', 'Usually', 'Sometimes', 'Rarely', 'Never']:
                answers.append(response)
                break
            else:
                print("Invalid response. Please enter one of: Always, Usually, Sometimes, Rarely, Never.")

    jaundice = input("Was the child born with jaundice? (Yes/No): ").strip().lower()
    family_mem_with_asd = input("Is there any family member with ASD? (Yes/No): ").strip().lower()
    sex = input("The Gender of the toddler : ").strip().lower()
    ethnicity = str(input("Enter the child's ethnicity: ").strip())
    age_mons = int(input("Enter the child's age in months: ").strip())
    who_completed_test = input("Who completed the test? (Parent/Self/Health care professional/Other): ").strip()
    # Increment Case_No based on the dataset

    extra_info = {
        'jaundice': 'yes' if jaundice == 'yes' else 'no',
        'family_mem_with_asd': 'yes' if family_mem_with_asd == 'yes' else 'no',
        'sex': 'm' if sex == 'm' else 'f',
        'ethnicity': ethnicity,
        'age_mons': age_mons,
        'who_completed': who_completed_test
    }
    # For model input, convert to numeric:
    jaundice_val = 1 if jaundice == 'yes' else 0
    family_asd_val = 1 if family_mem_with_asd == 'yes' else 0

    return answers, extra_info, jaundice_val, family_asd_val

def convert_answers_to_binary(answers):
    binary_values = []
    for i, answer in enumerate(answers):
        answer = answer.lower()
        if i == 9:  # A10 is reverse scored
            binary_values.append(1 if answer in ['always', 'usually', 'sometimes'] else 0)
        else:
            binary_values.append(1 if answer in ['sometimes', 'rarely', 'never'] else 0)
    return binary_values

def plot_asd_inclination(score):
    plt.figure(figsize=(8, 1.5))
    colors = ['green' if i <= 3 else 'orange' if i <= 6 else 'red' for i in range(11)]
    for i in range(11):
        plt.barh(0, 1, left=i, color=colors[i])
    plt.axvline(score, color='blue', linestyle='--', linewidth=2, label=f'Score: {score}')
    plt.yticks([])
    plt.xticks(range(0, 11))
    plt.title('ASD Trait Inclination Based on Q-Chat-10')
    plt.xlabel('Score (0–10)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    try:
        # Load and clean dataset
        path = r'datasets 1/Toddler Autism dataset July 2018.csv'
        data = pd.read_csv(path)

        data.columns = [col.strip() for col in data.columns]  # Clean column names

        data['Jaundice'] = data['Jaundice'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
        data['Family_mem_with_ASD'] = data['Family_mem_with_ASD'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
        data['Class ASD Traits'] = data['Class ASD Traits'].apply(lambda x: 1 if str(x).strip().upper() == 'YES' else 0)

        feature_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10', 'Jaundice', 'Family_mem_with_ASD', 'Age_Mons']
        x = data[feature_cols]
        y = data['Class ASD Traits']

        # Train model
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # User input
        user_answers, extra_info, jaundice_val, family_asd_val = get_user_input()
        user_binary = convert_answers_to_binary(user_answers)

        user_binary.append(jaundice_val)
        user_binary.append(family_asd_val)
        user_binary.append(extra_info['age_mons'])
        # Prediction
        user_input_df = pd.DataFrame([user_binary], columns=feature_cols)
        prediction = model.predict(user_input_df)[0]
        result = 'Yes' if prediction == 1 else 'NO' # Needed to be changed 
        asd_score = sum(user_binary[:10])  # Q-chat-10 only

        print(f"\n ASD Prediction: {result}")
        print(f" Q-Chat-10 Score: {asd_score}")
        plot_asd_inclination(asd_score)

        try:
                case_no = data['Case_No'].max() + 1
        except KeyError:
            case_no = 1  # If Case_No column doesn't exist, start from 1

        # Save response
        new_entry = {
            'A1': user_binary[0], 'A2': user_binary[1], 'A3': user_binary[2],
            'A4': user_binary[3], 'A5': user_binary[4], 'A6': user_binary[5],
            'A7': user_binary[6], 'A8': user_binary[7], 'A9': user_binary[8],
            'A10': user_binary[9],'Age_Mons': extra_info['age_mons'],
            'Qchat_10_Score': asd_score,
            'Sex':extra_info['sex'], 'Ethnicity': extra_info['ethnicity'],
            'Jaundice': extra_info['jaundice'],
            'Family_mem_with_ASD': extra_info['family_mem_with_asd'],
            'Who_completed_the_test': extra_info['who_completed'],
            'Class ASD Traits': result
        }
        
        pd.DataFrame([new_entry]).to_csv(path, mode='a', header=False, index=False, encoding='utf-8-sig')
        print("User data appended successfully.")

    except Exception as e:
        print(f" Error: {e}")

if __name__ == '__main__':
    main()