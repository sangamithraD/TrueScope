import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from backend.ml_model.fact_check_service import fact_check_search


MODEL_PATH = "detection/services/fake_news_model.pkl"

# Load model if exists, otherwise create a dummy one
if os.path.exists(MODEL_PATH):
    vectorizer, model = joblib.load(MODEL_PATH)
else:
    # Minimal demo training (can expand later with real dataset)
    fake_texts = ["Neem juice cures dengue instantly", "Earth is flat", "Drinking bleach kills coronavirus"]
    real_texts = ["NASA confirms water on the moon", "WHO recommends vaccination", "Stock markets rise today"]

    texts = fake_texts + real_texts
    labels = ["fake"] * len(fake_texts) + ["real"] * len(real_texts)

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    model = PassiveAggressiveClassifier(max_iter=1000)
    model.fit(X, labels)

    joblib.dump((vectorizer, model), MODEL_PATH)

def analyze_text(text: str) -> str:
    """Analyze text and return prediction"""
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    return "Likely Fake" if prediction == "fake" else "Likely Real"
