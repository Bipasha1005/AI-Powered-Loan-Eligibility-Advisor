import joblib
import numpy as np

preprocessor = joblib.load("models/preprocessing.pkl")
model = joblib.load("models/xgb_model.pkl")

def predict_loan(user_input_df):
    X = preprocessor.transform(user_input_df)
    prob = model.predict_proba(X)[0][1]

    if prob >= 0.75:
        decision = "APPROVED"
    elif prob >= 0.50:
        decision = "REVIEW"
    else:
        decision = "REJECTED"

    return prob, decision
