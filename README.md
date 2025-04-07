# Autism Spectrum Disorder (ASD) – Medical Analysis & ML Prediction System

## Project Overview

This project presents a data-driven approach to assist in the **early screening of Autism Spectrum Disorder (ASD)** in toddlers using behavioral and demographic data. Leveraging the **Autistic Spectrum Disorder Screening Data for Toddlers (July 2018)** dataset, we preprocess the data using **Apache Spark**, train machine learning models, and deploy an interactive prediction interface using **Streamlit**.

**Goal**: To build a fast, interpretable, and accessible tool that predicts potential ASD traits in toddlers based on Q-Chat-10 responses and demographic information.

---

##  Problem Statement

ASD diagnosis can be delayed due to high costs, limited clinical resources, and time-consuming procedures. Early detection is crucial for better outcomes. This project addresses these issues by:

- Utilizing machine learning for quick ASD risk classification.
- Processing data at scale with Apache Spark.
- Deploying a user-friendly interface for real-time predictions.

---

## Dataset Information

- **Name**: Autistic Spectrum Disorder Screening Data for Toddlers
- **Source**: [Autism screening data for toddlers](https://www.kaggle.com/datasets/fabdelja/autism-screening-for-toddlers?resource=download)
- **Date**: July 22, 2018
- **Type**: Behavioral, Medical, Social
- **Attributes**:
  - Q-Chat-10 behavioral responses (A1–A10)
  - Age (in months)
  - Gender, Ethnicity
  - Born with jaundice (yes/no)
  - Family history of ASD (yes/no)
  - Score and final classification

---

##  Tech Stack

| Layer        | Tools & Libraries                      |
|--------------|----------------------------------------|
| Language     | Python 3.13                            |
| Data Engine  | Apache Spark (PySpark + MLlib)         |
| ML Libraries | scikit-learn, XGBoost (local testing)  |
| Deployment   | Streamlit (for web interface)          |
| Visualization| seaborn, matplotlib, plotly            |
| Versioning   | Git, GitHub                            |

---

##  Workflow

### 1. Data Preprocessing (Apache Spark)
- Load and clean the dataset using PySpark DataFrames.
- Convert categorical and binary features to numerical.
- Feature selection and label encoding via Spark ML pipelines.

### 2. Exploratory Data Analysis
- Distribution of ASD vs. non-ASD cases.
- Feature correlation heatmaps.
- Visual trends by age, gender, etc.

### 3. Machine Learning Modeling
- Train models: Logistic Regression, Random Forest, Gradient Boosting.
- Evaluate with Accuracy, Precision, Recall, F1-score, ROC-AUC.

### 4. Deployment
- Build a **Streamlit app** that:
  - Accepts user input for all Q-Chat-10 + demographic features.
  - Displays predicted ASD risk (Yes/No) with a probability score.
  - Optionally shows feature contributions and insights.

---

## How to Run the Project

###  Prerequisites
- Python 3.13
- Apache Spark
- pip or conda
- Git

## Some important things to be noted.
## Q-CHAT-10 Scoring Guide
The Q-CHAT-10 (Quantitative Checklist for Autism in Toddlers - 10 item version) is a brief, validated screening tool designed to identify early signs of autism in toddlers aged 18 to 30 months.

# Scoring System:
- The questionnaire contains 10 Yes/No questions.
- Some items are reverse-scored.

- Each response contributes 0 or 1 point to the total score.

The total score ranges from 0 to 10.

## Interpretation:
## Total Score	Screening Outcome
-- 0 – 2	Negative screen – Low likelihood of autism
-- ≥ 3	Positive screen – Elevated likelihood of autism; further evaluation recommended
-- ⚠️ Important: The Q-CHAT-10 is a screening tool, not a diagnostic test. A score of 3 or more indicates that the child may benefit from a comprehensive diagnostic assessment by a qualified healthcare professional.

## Usage Notes:
-- Best suited for toddlers aged 18–30 months.

-- Designed for early identification of social-communication difficulties and repetitive behaviors.

-- Can be used in clinical settings, research, or community-based screening programs.

