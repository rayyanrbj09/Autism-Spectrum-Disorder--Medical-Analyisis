import pandas as pd
import numpy as np
from train_model import RandomForestClassifier, train_test_split, pd

def test_model_prediction():
    # Sample input  # 13 features
    sample_input = [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 24]  # Another sample input
    # Feature columns must match training
    feature_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10', 'Jaundice', 'Family_mem_with_ASD', 'Age_Mons']
    input_df = pd.DataFrame([sample_input], columns=feature_cols)

    # Train dummy model for test
    data = pd.read_csv(r"D:\Autism-Spectrum-Disorder--Medical-Analyisis\datasets 1\Toddler Autism dataset July 2018.csv")
    data['Jaundice'] = data['Jaundice'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    data['Family_mem_with_ASD'] = data['Family_mem_with_ASD'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    data['Class ASD Traits'] = data['Class ASD Traits'].apply(lambda x: 1 if str(x).strip().upper() == 'YES' else 0)
    X = data[feature_cols]
    y = data['Class ASD Traits']

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    prediction = model.predict(input_df)[0]
    assert prediction in [0, 1]
