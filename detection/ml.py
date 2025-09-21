import os
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# -----------------------------
# Model path
# -----------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "roberta_misinfo_model")

# -----------------------------
# Load model + tokenizer (once)
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = RobertaTokenizer.from_pretrained(MODEL_PATH)
model = RobertaForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

id2label = {0: "Fake", 1: "True"}

# -----------------------------
# Predict function
# -----------------------------
def predict_text(english_text: str):
    """
    Input: text (English string)
    Output: (label, confidence)
    """
    try:
        # Encode text
        inputs = tokenizer(
            english_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        ).to(device)

        # Run model
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]

        # Get predicted class
        pred_id = int(probs.argmax())
        label = id2label[pred_id]
        confidence = float(probs[pred_id])

        return label, confidence

    except Exception as e:
        return "Error", 0.0
