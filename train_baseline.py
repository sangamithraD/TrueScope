# backend/ml_model/train_baseline.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os

# Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "train.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "baseline_model.joblib")

print(f"📂 Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

# --- Clean & Normalize ---
# Rename to ensure consistent naming
df = df.rename(columns={"headline": "text", "label": "label"})

# Map string labels -> numeric (Fake=0, True=1)
df["label"] = df["label"].map({"Fake": 0, "True": 1})

# Drop invalid rows
df = df.dropna(subset=["text", "label"])
print(f"✅ Data cleaned. Shape: {df.shape}")

# --- Train/Test Split ---
X_train, X_val, y_train, y_val = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# --- Build Pipeline ---
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=5000)),
    ("clf", LogisticRegression(max_iter=200, class_weight="balanced", solver="liblinear"))
])

# --- Train ---
pipeline.fit(X_train, y_train)

# --- Evaluate ---
y_pred = pipeline.predict(X_val)
y_proba = pipeline.predict_proba(X_val)[:, 1]

print("🎯 Validation ROC-AUC:", roc_auc_score(y_val, y_proba))
print(classification_report(y_val, y_pred, target_names=["Fake", "True"]))

# --- Save ---
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)
print(f"💾 Model saved at: {MODEL_PATH}")
