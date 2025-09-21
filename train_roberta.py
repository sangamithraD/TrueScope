import pandas as pd
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from datasets import Dataset

# -----------------------------
# Load multiple Excel datasets
# -----------------------------
files = [
    r"/content/Liar_Dataset.xlsx",
    r"/content/True.xlsx",
    r"/content/FA-KES-Dataset.xlsx",
    r"/content/Fake_final.xlsx",
    r"/content/fake_news_dataset.xlsx",
    r"/content/train.csv"
]

# -----------------------------
# Normalize datasets
# -----------------------------
standard_headline_names = ["headline", "headlines", "heading", "title", "text", "content", "news"]
standard_label_names = ["label", "labels", "category", "target", "class"]

dfs = []
for file in files:
    try:
        if file.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            df = pd.read_csv(file)

        # Find headline column
        headline_col = None
        for col in df.columns:
            if col.lower().strip() in standard_headline_names:
                headline_col = col
                break

        # Find label column
        label_col = None
        for col in df.columns:
            if col.lower().strip() in standard_label_names:
                label_col = col
                break

        if headline_col and label_col:
            df = df[[headline_col, label_col]].rename(
                columns={headline_col: "headline", label_col: "label"}
            )
            dfs.append(df)
            print(f"✅ Loaded & normalized: {file} ({len(df)} rows)")
        else:
            print(f"⚠️ Skipped {file}, missing headline/label columns")

    except Exception as e:
        print(f"❌ Failed to load {file}: {e}")

# Merge all normalized datasets
data = pd.concat(dfs, ignore_index=True)
print("✅ Raw dataset size after normalization:", len(data))

# Ensure consistent column naming
if "headlines" in data.columns:
    data.rename(columns={"headlines": "headline"}, inplace=True)
elif "heading" in data.columns:
    data.rename(columns={"heading": "headline"}, inplace=True)

# Drop NaNs if any
data = data.dropna(subset=["headline", "label"])
data = data[["headline", "label"]]

print("✅ Raw dataset size:", len(data))
print(data.head())

# -----------------------------
# Encode labels
# -----------------------------
data["label"] = data["label"].astype(str).str.strip().str.lower()

label2id = {"fake": 0, "false": 0, "true": 1, "real": 1}
id2label = {0: "Fake", 1: "True"}

# Map and drop unknowns
before = len(data)
data["label"] = data["label"].map(label2id)
data = data.dropna(subset=["label"])
after = len(data)
print(f"⚠️ Dropped {before - after} rows due to unknown labels")

data["label"] = data["label"].astype(int)

print("✅ Cleaned dataset size:", len(data))
print(data["label"].value_counts())

# -----------------------------
# Train/Test Split
# -----------------------------
train_texts, val_texts, train_labels, val_labels = train_test_split(
    data["headline"], data["label"], test_size=0.2, random_state=42
)

# -----------------------------
# Tokenizer
# -----------------------------
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

def tokenize(batch):
    return tokenizer(batch["headline"], padding="max_length", truncation=True, max_length=128)

train_dataset = Dataset.from_dict({"headline": train_texts.tolist(), "label": train_labels.tolist()})
val_dataset = Dataset.from_dict({"headline": val_texts.tolist(), "label": val_labels.tolist()})

train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)

# -----------------------------
# Model
# -----------------------------
model = RobertaForSequenceClassification.from_pretrained(
    "roberta-base",
    num_labels=2,
    id2label=id2label,
    label2id=label2id
)

# -----------------------------
# Training
# -----------------------------
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",   # ✅ corrected
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    load_best_model_at_end=True
)

def compute_metrics(eval_pred):
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary")
    acc = accuracy_score(labels, predictions)
    return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

# -----------------------------
# Save final model & tokenizer
# -----------------------------         finally what to include to save the trained model in roberta_misinfo_model
# -----------------------------
# Save final model & tokenizer
# -----------------------------
save_dir = "roberta_misinfo_model"

model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)

print(f"✅ Model and tokenizer saved to {save_dir}")


