import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load artifacts
model = joblib.load("models/xgb_model.pkl")
preprocessor = joblib.load("models/preprocessing.pkl")

def generate_shap_summary(df_sample):
    # Preprocess data
    X_processed = preprocessor.transform(df_sample)

    # Background data (small subset)
    background = shap.sample(X_processed, 50)

    # 🔥 FUNCTION-BASED EXPLAINER (BUG-FREE)
    explainer = shap.Explainer(
        model.predict_proba,
        background
    )

    shap_values = explainer(X_processed)

    # Use class 1 (Approved)
    shap.summary_plot(
        shap_values[..., 1],
        X_processed,
        show=False
    )

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv("data/loan_approval_dataset.csv")
    df.columns = df.columns.str.strip()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    df = df.drop(columns=["loan_id", "loan_status"])

    sample = df.sample(100, random_state=42)

    generate_shap_summary(sample)
