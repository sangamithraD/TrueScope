import os
import time
import json
import torch
import langdetect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from deep_translator import GoogleTranslator

from .models import State, NewsCheck
from .external_sources import find_sources  # your external search module

# -----------------------------
# Paths
# -----------------------------
MODEL_PATH = r"C:/Users/sangamithra/True_Scope/truthlens_backend/backend/ml_model/roberta_misinfo_model"
DEFAULT_FAKE_FILE = r"C:/Users/sangamithra/True_Scope/truthlens_backend/detection/DEFAULT_FAKE_NEWS.json"

# -----------------------------
# Load Model Once
# -----------------------------
classifier = None
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()

    def classifier(text: str):
        inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        pred_id = torch.argmax(outputs.logits, dim=1).item()
        return [{
            "label": "Fake" if pred_id == 0 else "True",
            "score": torch.softmax(outputs.logits, dim=1).max().item()
        }]

    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {e}")

# -----------------------------
# Translation Helper
# -----------------------------
TRANSLATION_CACHE = {}

def translate_text_cached(text: str, target_lang: str, source_lang: str = "auto"):
    if not text:
        return text
    key = (text, source_lang, target_lang)
    if key in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[key]
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception:
        translated = text
    TRANSLATION_CACHE[key] = translated
    return translated

# -----------------------------
# State Detection
# -----------------------------
STATE_NAME_MAP = {
    "Andhra Pradesh": "Andhra Pradesh", "Arunachal Pradesh": "Arunachal Pradesh", "Assam": "Assam",
    "Bihar": "Bihar", "Chhattisgarh": "Chhattisgarh", "Goa": "Goa", "Gujarat": "Gujarat",
    "Haryana": "Haryana", "Himachal Pradesh": "Himachal Pradesh", "Jharkhand": "Jharkhand",
    "Karnataka": "Karnataka", "Kerala": "Kerala", "Madhya Pradesh": "Madhya Pradesh",
    "Maharashtra": "Maharashtra", "Manipur": "Manipur", "Meghalaya": "Meghalaya",
    "Mizoram": "Mizoram", "Nagaland": "Nagaland", "Odisha": "Odisha", "Punjab": "Punjab",
    "Rajasthan": "Rajasthan", "Sikkim": "Sikkim", "Tamil Nadu": "Tamil Nadu", "Telangana": "Telangana",
    "Tripura": "Tripura", "Uttar Pradesh": "Uttar Pradesh", "Uttarakhand": "Uttarakhand",
    "West Bengal": "West Bengal", "Delhi": "Delhi", "Puducherry": "Puducherry", "Chandigarh": "Chandigarh",
    "Dadra and Nagar Haveli": "Dadra and Nagar Haveli", "Daman and Diu": "Daman and Diu",
    "Lakshadweep": "Lakshadweep", "Jammu and Kashmir": "Jammu and Kashmir", "Ladakh": "Ladakh"
}

def detect_state(text):
    if not text:
        return "General"
    for key in STATE_NAME_MAP:
        if key.lower() in str(text).lower():
            return STATE_NAME_MAP[key]
    return "General"

# -----------------------------
# Load Default Fake News
# -----------------------------
def load_fake_news():
    if not os.path.exists(DEFAULT_FAKE_FILE):
        print("❌ DEFAULT_FAKE_NEWS.json not found!")
        return {}
    try:
        with open(DEFAULT_FAKE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load default fake news: {e}")
        return {}

DEFAULT_FAKE_NEWS = load_fake_news()

# -----------------------------
# Education Tips
# -----------------------------
def get_education_tips():
    return [
        "Cross-check news across multiple trusted sources.",
        "Verify the date & context of the claim.",
        "Be careful of emotionally charged clickbait.",
        "Use fact-checking portals like AltNews or PolitiFact."
    ]

# -----------------------------
# Authoritative Sources
# -----------------------------
AUTHORITATIVE_DOMAINS = [
    "gov.in", "nic.in", "niti.gov.in", "prsindia.org", "meity.gov.in", "mha.gov.in",
    "mhrd.gov.in", "indianrailways.gov.in", "pmindia.gov.in", "rajyasabha.nic.in", "loksabha.nic.in",
    "ap.gov.in", "assam.gov.in", "bihar.gov.in", "goa.gov.in", "gujarat.gov.in", "kerala.gov.in",
    "ka.gov.in", "tn.gov.in", "mh.gov.in", "wb.gov.in", "delhi.gov.in", "telangana.gov.in",
    "who.int", "cdc.gov", "nasa.gov", "noaa.gov", "unesco.org", "un.org", "nature.com",
    "sciencedirect.com", "springer.com", "plos.org", "nih.gov", "esa.int", "sciencemag.org",
    "factcheck.org", "snopes.com", "politifact.com", "altnews.in", "boomlive.in", "fullfact.org"
]

MYTH_KEYWORDS = ["myth", "hoax", "false", "rumor", "fake", "untrue", "debunked"]

def filter_authoritative_sources(sources):
    filtered = []
    for s in sources:
        url = s.get("url", "")
        snippet = s.get("snippet", "").lower()
        if any(domain in url for domain in AUTHORITATIVE_DOMAINS):
            if any(k in snippet for k in MYTH_KEYWORDS):
                s["context_flag"] = "myth"
            else:
                s["context_flag"] = "confirmed"
            filtered.append(s)
    return filtered

# -----------------------------
# Check News API
# -----------------------------
@api_view(["POST"])
def check_news(request):
    start_time = time.time()
    text = request.data.get("text", "").strip()
    if not text:
        return Response({"error": "No text provided"}, status=400)
    if classifier is None:
        return Response({"error": "Model not loaded"}, status=500)

    # Language detection & translation
    try:
        detected_lang = langdetect.detect(text)
    except Exception:
        detected_lang = "en"
    english_text = text if detected_lang == "en" else translate_text_cached(text, "en", source_lang=detected_lang)

    # State detection on English text
    state_name = detect_state(english_text)

    # ML prediction
    pred = classifier(english_text)[0]
    score = float(pred.get("score", 0.0))

    # External sources
    sources = find_sources(english_text, lang=detected_lang)
    authoritative_sources = filter_authoritative_sources(sources)

    confirmed_sources = [s for s in authoritative_sources if s.get("context_flag") == "confirmed"]

    # Strict True / Fake
    if confirmed_sources:
        final_label = "True / Confirmed"
        final_confidence = min(1.0, score + 0.3)
        explanation = "Authoritative sources confirm this claim."
    else:
        final_label = "False / Refuted"
        final_confidence = max(0.0, 1 - score)
        explanation = "No authoritative evidence found. The claim is likely false."

        # Save fake news in state
        if state_name not in DEFAULT_FAKE_NEWS:
            DEFAULT_FAKE_NEWS[state_name] = []
        DEFAULT_FAKE_NEWS[state_name].append(text)

    # Back-translate everything
    if detected_lang != "en":
        final_label = translate_text_cached(final_label, detected_lang, "en")
        explanation = translate_text_cached(explanation, detected_lang, "en")
        for s in authoritative_sources:
            if "snippet" in s and s["snippet"]:
                s["snippet"] = translate_text_cached(s["snippet"], detected_lang, "en")
        education_tips = [translate_text_cached(tip, detected_lang, "en") for tip in get_education_tips()]
    else:
        education_tips = get_education_tips()

    # Save in DB
    try:
        state_obj, _ = State.objects.get_or_create(name=state_name)
        NewsCheck.objects.get_or_create(
            state=state_obj,
            text=text,
            text_en=english_text,
            prediction_label=final_label,
            confidence=final_confidence,
        )
    except Exception:
        pass

    response_data = {
        "input": {"original": text},
        "prediction": {"label": final_label, "confidence": round(final_confidence, 3)},
        "sources": authoritative_sources,
        "state": state_name,
        "explanation": explanation,
        "education": education_tips,
        "meta": {"latency_seconds": round(time.time() - start_time, 3), "language_detected": detected_lang}
    }

    return Response(response_data)

# -----------------------------
# State API
# -----------------------------
@api_view(["GET"])
def state_news(request, state_name):
    state_name = STATE_NAME_MAP.get(state_name, state_name)
    news_list = DEFAULT_FAKE_NEWS.get(state_name, []).copy()
    return Response({"state": state_name, "fake_news": news_list})

# -----------------------------
# Map Data API
# -----------------------------
@api_view(["GET"])
def map_data(request):
    result = {}
    total_fake = 0
    for state in STATE_NAME_MAP.values():
        fake_count = len(DEFAULT_FAKE_NEWS.get(state, []))
        total_fake += fake_count
        status = "low"
        if fake_count > 10:
            status = "high"
        elif fake_count > 5:
            status = "moderate"
        result[state] = {"fake": fake_count, "total": fake_count, "status": status}
    general_fake = len(DEFAULT_FAKE_NEWS.get("General", []))
    result["General"] = {"fake": general_fake, "total": general_fake, "status": "low"}
    result["India"] = {"fake": total_fake + general_fake, "total": total_fake + general_fake, "status": "low"}
    return Response(result)

# -----------------------------
# Health Check
# -----------------------------
@api_view(["GET"])
def health_check(request):
    return Response({"status": "OK"})
