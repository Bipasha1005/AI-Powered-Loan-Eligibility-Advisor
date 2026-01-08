import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def load_data(path):
    df = pd.read_csv(path)

    # 🔥 FIX 1: Clean column names
    df.columns = df.columns.str.strip()

    # 🔥 FIX 2: Clean string values
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df

def preprocess_and_save(df):
    target_col = "loan_status"

    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")

    # 🔥 FIX 3: Encode target labels
    label_encoder = LabelEncoder()
    df[target_col] = label_encoder.fit_transform(df[target_col])
    # Approved → 1, Rejected → 0 (or vice versa)

    joblib.dump(label_encoder, "models/label_encoder.pkl")

    X = df.drop(columns=["loan_id", target_col])
    y = df[target_col]

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ])

    X_processed = preprocessor.fit_transform(X)

    joblib.dump(preprocessor, "models/preprocessing.pkl")

    return X_processed, y

if __name__ == "__main__":
    df = load_data("data/loan_approval_dataset.csv")
    X, y = preprocess_and_save(df)
    print("✅ Preprocessing completed | Labels encoded correctly")
